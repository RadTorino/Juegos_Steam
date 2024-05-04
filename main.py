import pandas as pd
from fastapi import FastAPI

app = FastAPI()

# importación de tablas

juegos = pd.read_csv('archivos_csv/games_final.csv')
items = pd.read_csv('archivos_csv/items_final_pulido.csv')
reviews = pd.read_csv('archivos_csv/reviews_final.csv')


#armo df acorde a las necesidades de la función

reviews_fecha = reviews.drop(columns=['funny', 'helpful', 'recommend', 'sentiment_analysis']) #elimino las columnas que no me sirven
juegos_años = pd.merge(items, reviews_fecha, on= ['user_id', 'item_id'], how='inner') #concateno para tener items y fecha de review en un mismo df


@app.get("/")
async def ruta_prueba():
    return "Hola"


@app.get("/UserForGenre")
async def UserForGenre(genero):
    #obtengo liste de ids de juegos que se corresponden con ese género
    juegos_id = juegos[juegos.tags.apply(lambda x:(genero.capitalize() in x) )]['id']
    #creo diccionario con jugadores y horas jugadas
    jugadores = juegos_años.user_id.unique()
    horas_jugadas = { jugador:0 for jugador in jugadores}
   #filtro el df con los ids de los juegos que responden al género 
    juegos_filtrados = juegos_años[juegos_años['item_id'].isin(juegos_id)]
    # itero para sumar horas jugadas para cada jugador
    for indice, fila in juegos_filtrados.iterrows():
        horas_jugadas[fila['user_id']] += fila['playtime_forever']
    #jugador con más horas jugadas
    max_user = max(horas_jugadas, key=horas_jugadas.get)
    # diccionario para calcular años con más horas jugadas.
    horas_por_año = {año:0 for año in juegos_años.posted.unique()}

    juegos_filtrados_por_usuario = juegos_años[(juegos_años['item_id'].isin(juegos_id)) & (juegos_años['user_id'] == max_user)]

    for indice, fila in juegos_filtrados_por_usuario.iterrows():
        horas_por_año[fila['posted']] += fila['playtime_forever']

    
    horas_por_año_ordenado = sorted(horas_por_año.items(), key=lambda x: x[1], reverse=True)
    
    horas_jugadas_top = [{"Año": año, "Horas": horas} for año, horas in horas_por_año_ordenado[:3] if horas > 0]
    
    return {
  f"Usuario con más horas jugadas para Género {genero.capitalize()}": {max_user},
  "Horas jugadas": str(horas_jugadas_top)
}


@app.get("/PlayTimeGenre")
def PlayTimeGenre(genero):
    #obtengo lista de ids de juegos que se corresponden con ese género
    juegos_id = juegos[juegos.tags.apply(lambda x:(genero.capitalize() in x) )]['id']
    #filtro el df con los ids de los juegos que responden al género 
    juegos_filtrados = juegos_años[juegos_años['item_id'].isin(juegos_id)]
    # itero para sumar horas jugadas para cada jugador
    horas_por_release_year = {year:0 for year in juegos.release_date.unique()}
    for indice, fila in juegos_filtrados.iterrows():
        filtro = juegos['id'] == fila['item_id']
        if isinstance(juegos.loc[filtro, 'release_date'], int): ## este filtro es para eliminar los juegos con release_date nulo
            año_lanzamiento = int(juegos.loc[filtro, 'release_date'])
            horas_por_release_year[año_lanzamiento]+= fila['playtime_forever']
    
    año = max(horas_por_release_year, key=horas_por_release_year.get)

    return {f"Año de lanzamiento con más horas jugadas para Género {genero.capitalize()} : {año}"}

@app.get("/UsersRecommend")
def UsersRecommend(año):
    if año not in reviews.posted.unique():
        return f"No hay recomendaciones para ese año. Pruebe con uno de estos años: {reviews.posted.unique()}"
    
    df = reviews[(reviews.posted == año)&(reviews['item_id'].isin(juegos.id))][['posted', 'item_id', 'recommend', 'sentiment_analysis']]

    juegos_recomendados = {item :0 for item in df.item_id.unique()}
    
    for indice, fila in df.iterrows():
        if fila.recommend is True:
            juegos_recomendados[fila['item_id']] +=1
        juegos_recomendados[fila['item_id']] += fila.sentiment_analysis
    
    juegos_recomendados = sorted(juegos_recomendados.items(), key=lambda x: x[1], reverse=True)
    
    juego1 = str(juegos[juegos['id'] == juegos_recomendados[0][0]]['app_name'].iloc[0])
    juego2 = str(juegos[juegos['id'] == juegos_recomendados[1][0]]['app_name'].iloc[0])
    juego3 = str(juegos[juegos['id'] == juegos_recomendados[2][0]]['app_name'].iloc[0])

    return {
    "Puesto 1": juego1,
    "Puesto 2": juego2,
    "Puesto 3": juego3
}
    
@app.get("/UsersNotRecommend")
def UsersNotRecommend(año):
    if año not in reviews.posted.unique():
        return f"No hay recomendaciones para ese año. Pruebe con uno de estos años: {reviews.posted.unique()}"
    
    df = reviews[(reviews.posted == año)&(reviews['item_id'].isin(juegos.id))][['posted', 'item_id', 'recommend', 'sentiment_analysis']]

    juegos_recomendados = {item :0 for item in df.item_id.unique()}
    
    for indice, fila in df.iterrows():
        if fila.recommend is False:
            juegos_recomendados[fila['item_id']] +=1
        if fila.sentiment_analysis == 0:
            juegos_recomendados[fila['item_id']] +=1
    
    juegos_recomendados = sorted(juegos_recomendados.items(), key=lambda x: x[1], reverse=True)
    
    juego1 = str(juegos[juegos['id'] == juegos_recomendados[0][0]]['app_name'].iloc[0])
    juego2 = str(juegos[juegos['id'] == juegos_recomendados[1][0]]['app_name'].iloc[0])
    juego3 = str(juegos[juegos['id'] == juegos_recomendados[2][0]]['app_name'].iloc[0])

    return {
    "Puesto 1": juego1,
    "Puesto 2": juego2,
    "Puesto 3": juego3
}

@app.get("/SentimentAnalysis")
def SentimentAnalysis(año):
    juegos_de_ese_año = list(juegos[juegos['release_date']== año].id)
    reseñas = list(reviews[reviews['item_id'].isin(juegos_de_ese_año)]['sentiment_analysis'])
    if len(reseñas) == 0:
        return "No hay reseñas para juegos lanzados ese año"
    else:
        return f"Negative = {reseñas.count(0)}, Neutral = {reseñas.count(1)}, Positive = {reseñas.count(2)}"