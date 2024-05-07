# Machine Learning Operations con datasets de Steam

Este trabajo es un Proyecto de Machine Learning Operations para el Proyecto Individidual n°1 de la carrera de Data Sciencia de Henry.
El mismo consta de 4 partes:

**ETL**  	 

**Feature Engeaniering**  

**EDA**  

**Desarrollo de funciones a deployar via Render**

El objetivo final es producir un **MVP** de una API que responda a 6 consultas distintas a partir de la data provista.

## ETL: 

En este paso (presente en el notebook **etl.ipynb**), se toman los 3 archivos comprimidos en formato json que están presentes en la carpeta **archivos_zip**. 
Para realizar el proceso de extracción se utiliza la librería **gzip** para abri el archivo y luego se lee cada línea como un archivo json. 
Luego se realizan distintos procesos de transformación de datos desde eliminar datos nulos o duplicados, transformar el tipo de dato de algunas columnas, etc. Se eliminan columnas con información repetida o muy parecida y columnas con información que no es necesaria para el análisis posterior. 
También se realiza una reducción del dataset para facilitar el análisis, entiendo el caracter de MVP del proyecto. El dataset **items** se reduce de 5 millones de filas a 300 mil. Para esto utilizamos como criterio utilizar a los 1000 jugadores que más juegos jugaron y que han realizado reviews.
Finalmente se exportan en formato csv a la carpeta **archivos_csv** para poder ser utilizados por el main.py que generará los endpoints de la API.

## Feature Engeeniering

Este proceso se encuentra en el notebook **feature_eng.ipynb** y utiliza archivo **reviews_final.csv**. En el mismo con el módulo **SentimentIntensityAnalyzer** de la librería **nltk** analiza las reviews del dataset y les asigna un puntaje en 'negative', 'neutral' y 'possitive'. Luego se selecciona el puntaje de más peso para etiquetar en 0, 1, o 2 (según el analisis arroje sentimiento negativo, neutral o positivo). Finalmente se exporta a la carpeta **archivos_csv** como **reviews_sentiment_analysis.csv**.

## EDA 

Este exploratory data analysis complementa el ya realizado durante el proceso de extracción. Este EDA se realiza pensando en cómo implementar el sistema de recomendación basada en la similitud de coseno. Para buscar similitud entre juegos, vamos a utilizar etiqueras o géneros, así como las horas jugadas y la recomendación promedio y cantidad de recomendación. Se estudia como se vinculan estas variables en búsqueda de outliers o correlaciones significativas. En función de todo el análisis se generar un dataset final **data_para_ML** que va a parar a la carpeta **archivos_csv**.

**Desarrollo de funciones a deployar via Render**

Para este proceso se utiliza  el framework de **fastapi**. Cada función definida se convierte en un endpoint de la API gracias al uso del decorador @app.get. 
Las funciones son:

**RecommendationSystem**: Recibe el id de un juego y devuelve el nombre de los 5 juegos más parecidos según el modelo.

**UserForGenre**: Recibe un género y devuelve el jugador que más horas juegos de ese género, junto con los 3 años que más jugó y las horas para esos años.

**PlayTimeGenre**: Recibe un género y devuelve el año donde se lanzaron los juegos de ese género que más horas se jugaron.

**UsersRecommend** Recibe un año y devuelve los 3 juegos que más recomendaron los usuarios ese año.

**UsersNotRecommend** Recibe un año y devuelve los 3 juegos que menos recomendaron los usuarios ese año.

**SentimentAnalysis** Recibe un año y devuelve la cantidad de reseñas negativas, neutras y positivas que obtuvieron los juegos lanzados ese año. 

## Proximos pasos

Para un desarrollo más integrado que genere un producto final, reconozco tres próximos pasos.

El primero tiene que ver con trabajar con el total de la información, y no con un recorte. También se podría estudiar de qué forma trabajar con valores nulos.

Además, se puede mejorar notablemente el análisis de sentimiento. En esta primer instancia se trabajo con un modelo empaquetado dentro de la librería nltk pero se podría investigar otro o incluso entrenar un modelo con parte de la data que permite etiquetarla luego. 

Finalmente el sistema de recomendación puede modificarse en función de la data nueva. El dataset completo tiene 20 veces más data de la que utilizamos para el MVP. La cantidad de información para cada juego va a variar mucho con lo cual habría que hacer un nuevo EDA para examinar las variables más prominentes.
