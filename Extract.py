import requests
from re import sub
from bs4 import BeautifulSoup

def Steam(link):
    response = BeautifulSoup(requests.get(link).content, 'html.parser')
        
    titulo = response.find('title').text

    descripcion = sub('\t|\r', '',response.find(id='game_area_description').text)[1:]

    fecha = response.find('div', class_ = 'date')
    fecha = fecha.text if fecha else 'Proximamente'

    precio = response.find('div', class_ = 'discount_final_price')
    if precio:
        precio = precio.text
    else:
        try: 
            precio = sub('\n|\t|\r', '', response.find('div', class_ = 'game_purchase_price price').string)
        except: 
            precio = None
        precio = precio if precio else 'Proximamente'

    for i in response.find_all('div',class_ = 'dev_row'):
        if 'Developer' in i.text:
            desarrollador = i.text[12:].split('\n')[0]
        elif 'Publisher' in i.text:
            distribuidor = i.text[12:].split('\n')[0]       
    
    img = requests.get(response.find('img', class_ = 'game_header_image_full')['src'])
    with open("image.png", "wb") as Archivo:
        Archivo.write(img.content)    
    
    return titulo.replace('\n',''), ' '.join(descripcion.split(' ')[:60])+'...', fecha, precio, desarrollador, distribuidor

def Insta(link):
    response = BeautifulSoup(requests.get(link).content, 'html.parser')
    
    titulo = response.find('div', class_ = 'name').text
    
    descripcion = response.find('div', class_ = 'text readable').text[1:].replace('[Product Contents]','')

    fecha = response.find('div', itemprop = 'datePublished').text.replace('\n','')

    precio = response.find_all('div', class_ = 'total')[1].text

    des_dis = response.find_all('a', class_ = 'limiter')
    desarrollador = des_dis[0].text.replace('\n','')
    distribuidor = des_dis[1].text.replace('\n','')

    img = requests.get(response.find('img')['data-src'])
    with open("image.png", "wb") as Archivo:
        Archivo.write(img.content)

    return titulo.replace('\n',''), ' '.join(descripcion.split(' ')[:60])+'...', fecha, precio, desarrollador, distribuidor

def extract(posicion_genero=None,posicion_url=None):
    from random import randrange, choice
    
    Urls = {0:'store.steampowered.com/tag/es/',1:'www.instant-gaming.com/es/busquedas/?q='}
    Genero = [['action/','acción'],['adventure/','aventura'],['fps/','fps'],['arcade/','arcade'],['indie/','indie'],
              ['un_jugador/','un+jugador'],['rpg/','rpg'],['strategy/','estrategia']]

    if not posicion_url:
        posicion_url = randrange(2)
    if not posicion_genero:
        posicion_genero = randrange(8)

    url=requests.get('https://'+Urls[posicion_url]+Genero[posicion_genero][posicion_url])
    response = BeautifulSoup(url.content,'html.parser')

    if posicion_url==0:
        link = choice([i.get('href') for i in response.find_all('a', class_ = 'tab_item')])
        titulo, descripcion, fecha, precio, desarrollador, distribuidor = Steam(link)
    elif posicion_url==1:
        link = choice([i.get('href') for i in response.find_all('a',class_ = 'cover')])
        titulo, descripcion, fecha, precio, desarrollador, distribuidor = Insta(link)

    return titulo, descripcion, fecha, precio, desarrollador, distribuidor, link, posicion_url