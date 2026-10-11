# Steam Game Recommendation System

Proyecto de **ingeniería de datos, análisis exploratorio y recomendación de videojuegos** con Python y FastAPI. Procesa información de juegos, usuarios y reseñas para habilitar consultas analíticas y recomendaciones basadas en contenido.

**Tecnologías identificadas:** Python · pandas · scikit-learn · FastAPI · Parquet · TF-IDF.

> **Estado:** proyecto existente documentado a partir de su código y su README original. El servicio desplegado y las métricas del recomendador no se han verificado durante esta revisión.

## Visión general

~~~mermaid
flowchart LR
    A["Datos de juegos,<br/>usuarios y reseñas"] --> B["ETL"]
    B --> C["Análisis exploratorio"]
    C --> D["Tablas preparadas<br/>Parquet"]
    D --> E["Consultas FastAPI"]
    D --> F["TF-IDF + similitud coseno"]
    F --> E
~~~

| Etapa | Recursos |
| --- | --- |
| Transformación y limpieza | [ETL](ETL) |
| Análisis exploratorio | [EDA](EDA) |
| Datos preparados | [DATA_LIMPIA](DATA_LIMPIA) |
| Tablas para consultas | [FUNCIONES](FUNCIONES) |
| API | [main.py](main.py) |
| Dependencias | [requirements.txt](requirements.txt) |

## Funcionalidades implementadas en el código

| Ruta | Propósito |
| --- | --- |
| /PlayTimeGenre/{genero} | Consultar el año de mayor tiempo de juego por género. |
| /userforgenre/{genero} | Resumir actividad y horas de juego de usuarios por género. |
| /UsersRecommend/{year} | Consultar juegos recomendados por año. |
| /UsersNotRecommend/{year} | Consultar juegos no recomendados por año. |
| /Sentiment_analysis/{year} | Consultar conteos de sentimiento por año. |
| /recomendacion_juego/{product_id} | Proponer juegos similares según géneros y etiquetas. |

La función de recomendación de **main.py** crea representaciones TF-IDF a partir de géneros y etiquetas y calcula similitud coseno entre el juego consultado y otros juegos.

## Datos y método

El proyecto parte de archivos de datos de Steam, prepara tablas con ETL y EDA, y consulta conjuntos Parquet desde FastAPI. El README original incluye una [carpeta externa con datos](https://drive.google.com/drive/folders/1HqBG2-sUkz_R3h1dZU5F2uAzpRn7BSpj); revisa su procedencia y permisos antes de reutilizarla.

**Nota técnica:** las rutas de la API dependen de los archivos Parquet esperados en **DATA_LIMPIA** y **FUNCIONES**. La existencia de estos directorios no garantiza que todas las consultas puedan ejecutarse sin preparación adicional.

## Instalación de referencia

En una instalación de Python, desde la raíz del repositorio:

~~~bash
python -m venv .venv
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
~~~

Estos son comandos de referencia basados en la estructura existente: **no se han ejecutado ni validado** en esta actualización. En un entorno real, activa primero el entorno virtual y verifica que estén presentes los datos Parquet que espera **main.py**.

El README original apuntaba a https://sistema-de-recomendacion-steam.onrender.com como despliegue; **no se ha verificado que continúe disponible**.

## Alcance y tareas pendientes

- Documentar origen, licencias y volumen de datos.
- Mostrar consultas con respuestas reales y verificables.
- Definir una evaluación cuantitativa de las recomendaciones.
- Revisar archivos generados como **__pycache__** que están incluidos en el repositorio.
- Mejorar pruebas y reproducibilidad, sin dar por confirmados resultados no medidos.

---

**Enfoque:** data engineering, análisis exploratorio y recomendaciones basadas en contenido.
