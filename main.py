from fastapi import FastAPI
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity



#iniciamos FastAPI y el dataframe
app = FastAPI()

game = pd.read_parquet(r"DATA_LIMPIA/gameclean.parquet")
df_PlayTimeGenre=pd.read_parquet(r"FUNCIONES/df_PlayTimeGenre.parquet")
df_UserForGenre = pd.read_parquet(r"FUNCIONES/df_UserForGenre.parquet")
df_UserRecommend = pd.read_parquet(r"FUNCIONES/df_UserRecommend.parquet")
df_UsersNotRecommend = pd.read_parquet(r"FUNCIONES/df_UsersNotRecommend.parquet")
df_Sentiment_Analysis = pd.read_parquet(r"FUNCIONES/df_Sentiment_Analysis.parquet")


#PRIMERA FUNCIÓN
@app.get('/PlayTimeGenre/{genero}')
def PlayTimeGenre(genero : str):
    # Filtrar el DataFrame para obtener solo las filas que contienen el género específico
    filtro_genero = df_PlayTimeGenre['genres'].str.contains(genero, case=False, na=False)
    df_filtrado = df_PlayTimeGenre[filtro_genero]
    df_agrupado = df_filtrado.groupby('year')['playtime_forever'].sum().reset_index()
    # Encontrar el año con la mayor suma de 'playtime_forever'
    df_agrupado['year'] = df_agrupado['year'].astype(int)
    anio_mayor_suma = df_agrupado.loc[df_agrupado['playtime_forever'].idxmax(), 'year']
    respuesta = {f"Año de lanzamiento con más horas jugadas para Género el {genero}": anio_mayor_suma}
    return str(respuesta)     




#SEGUNDA FUNCIÓN
@app.get('/userforgenre/{genero}')
def userforgenre(genero: str):
    # Filtrar el DataFrame para el género especificado
    filtro_genero = df_UserForGenre['genres'].str.contains(genero, case=False, na=False)
    df_filtrado = df_UserForGenre[filtro_genero]

    # Agrupar por 'user_id' y 'year', sumar las horas jugadas
    df_agrupado = df_filtrado.groupby(['user_id', 'year'])['playtime_forever'].sum().reset_index()

    # Encontrar el usuario con la máxima suma de horas jugadas
    idx_max_playtime = df_agrupado['playtime_forever'].idxmax()
    usuario_max_playtime = df_agrupado.loc[idx_max_playtime, 'user_id']

    # Filtrar el DataFrame para el usuario con máxima suma de horas jugadas
    df_usuario = df_agrupado[df_agrupado['user_id'] == usuario_max_playtime]

    # Crear el formato "Horas jugadas"
    resultado_final = [{'Año': int(row['year']), 'Horas': int(row['playtime_forever'])} for _, row in df_usuario.iterrows()]
    
    final = {"Usuario con más horas jugadas para Género {}:".format(genero): usuario_max_playtime, "Horas jugadas": resultado_final}

    return str(final)





#TERCERA FUNCIÓN
@app.get('/UsersRecommend/{year}')
def UsersRecommend(year: int):
    
    df = df_UserRecommend[df_UserRecommend['year'] == str(year)]

    # Contar el número de recomendaciones para cada juego
    top_juegos = df[['sentiment_analysis', 'app_name']].groupby('app_name').sum().sort_values(by='sentiment_analysis', ascending=False).head(3)

    # Crear el formato de salida
    resultado_final = [{"Puesto {}".format(i+1): juego} for i, (juego, _) in enumerate(top_juegos.reset_index().values)]

    return str(resultado_final)





#CUARTA FUNCIÓN
@app.get('/UsersNotRecommend/{year}')
def UsersNotRecommend(year: int):
    
    df = df_UsersNotRecommend[df_UsersNotRecommend['year'] == str(year)]

    # Contar el número de recomendaciones para cada juego
    top_juegos = df['app_name'].value_counts().head(3)

    # Crear el formato de salida
    resultado_final = [{"Puesto {}".format(i+1): juego} for i, (juego, _) in enumerate(top_juegos.reset_index().values)]

    return str(resultado_final)




#QUINTA FUNCIÓN
@app.get('/Sentiment_analysis/{year}')
def Sentiment_analysis(year: int):
    # Filtra el DataFrame para obtener la fila correspondiente al año de lanzamiento
    
    year_fila = df_Sentiment_Analysis[df_Sentiment_Analysis['year'] == str(year)]

    # Extrae los valores de las columnas Negativo, Neutro y Positivo
    negativo = year_fila['Negativo'].values[0]
    neutro = year_fila['Neutro'].values[0]
    positivo = year_fila['Positivo'].values[0]

    # Crea un diccionario con la información en el formato solicitado
    resultado = {
        year: {
            'Negative ': negativo,
            'Neutral': neutro,
            'Positive': positivo
        }
    }

    return str(resultado)





#FUNCIÓN DE RECOMENDACIÓN
@app.get('/recomendacion_juego/{product_id}')
def recomendacion_juego(product_id: int):
    try:
        # Obtener el ID del juego
        target_game = game[game['item_id'] == str(product_id)]

        if target_game.empty:
            return {"message": "No se encontró el juego de referencia."}

        # Combina las etiquetas (tags) y géneros en una sola cadena de texto para el juego de referencia
        target_game_tags_and_genres = ' '.join(target_game['tags'].fillna('').astype(str) + ' ' + target_game['genres'].fillna('').astype(str))

        

        # Combina las etiquetas (tags) y géneros de todos los juegos en una sola cadena de texto
        game['tags_and_genres'] = game['tags'].fillna('').astype(str) + ' ' + game['genres'].fillna('').astype(str)

        # Crea un vectorizador TF-IDF
        tfidf_vectorizer = TfidfVectorizer()

        # Transforma todas las etiquetas y géneros en una matriz TF-IDF
        tfidf_matrix = tfidf_vectorizer.fit_transform(game['tags_and_genres'])

        # Transforma las etiquetas y géneros del juego de referencia en una matriz TF-IDF
        target_tfidf_matrix = tfidf_vectorizer.transform([target_game_tags_and_genres])

        # Calcula la similitud del coseno entre el juego de referencia y todos los juegos
        similarity_scores = cosine_similarity(target_tfidf_matrix, tfidf_matrix)

        # Ordena los juegos por similitud y obtén los índices de los juegos más similares
        similar_games_indices = similarity_scores.argsort()[0][::-1]

        # Recomienda los juegos más similares (puedes ajustar el número de recomendaciones)
        num_recommendations = 5
        recommended_games = game.iloc[similar_games_indices[1:num_recommendations + 1]]

        # Devuelve la lista de juegos recomendados
        return recommended_games['app_name'].tolist()

    except Exception as e:
        return {"message": f"Error: {str(e)}"}
    

