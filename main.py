import pandas as pd
from fastapi import FastAPI

app = FastAPI()

# importación de tablas

juegos = pd.read_csv('archivos_csv/games_final.csv')
items = pd.read_csv('archivos_csv/items_final_pulido.csv')
reviews = pd.read_csv('archivos_csv/reviews_final.csv')

juegos = juegos.dropna(subset=['genres']) #elimino los juegos que no tienen género ya que no me sirven

#armo df acorde a las necesidades de la función

reviews.posted = pd.to_datetime(reviews.posted).dt.year #paso a formato fecha y me quedo solo con el año
reviews_fecha = reviews.drop(columns=['funny', 'helpful', 'recommend', 'review']) #elimino las columnas que no me sirven
juegos_años = pd.merge(items, reviews_fecha, on= ['user_id', 'item_id'], how='inner') #concateno para tener items y fecha de review en un mismo df
#la columna playtime_forever está en minutos, la paso a años.
juegos_años.playtime_forever = juegos_años.playtime_forever/60

@app.get("/")
async def ruta_prueba():
    return "Hola"

@app.get("/UserForGenre")
async def UserForGenre(genero):
    #obtengo liste de ids de juegos que se corresponden con ese género
    juegos_id = juegos[juegos.genres.apply(lambda x:(genero.capitalize() in x) )]['id']
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
