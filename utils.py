from curl_cffi import requests as cureq
from bs4 import BeautifulSoup

class BuscadorLocalizaciones:
    def __init__(self, query):
        self.query = query
        self.url = f"https://www.accuweather.com/es/search-locations?query={query}"
        self.contenido = None
        
    def obtener_respuesta(self):
        try:
            respuesta = cureq.get(self.url, impersonate="chrome")
            if respuesta.status_code == 200:  
                self.contenido = respuesta.content  
                return True
            return False
        except Exception as e:
            print(f"Error en la solicitud: {e}")
            return False
        
    def obtener_datos(self):
        if not self.contenido:
            if not self.obtener_respuesta():
                return None  # Si no hay contenido y no se puede obtener respuesta
        
        sopa = BeautifulSoup(self.contenido, "html.parser")
        resultados = []
        
        # Buscar TODOS los resultados, no solo uno
        contenedor = sopa.find_all("div",{"class":"locations-list content-module"})
        
        
        # Extraer nombre largo y URL
        nombres = [elemento.find_all("p", {"class":"location-long-name"}) for elemento in contenedor]
        enlaces = [elemento.find_all("a",{"class":""}) for elemento in contenedor]
        
        if nombres and enlaces:
            for nombre,enlace in zip(nombres[0],enlaces[0]):
                # Extraer location key de la URL
                url_completa = enlace["href"]
                
                resultados.append({
                    "nombre": nombre.get_text(strip=True),
                    "url": f"https://www.accuweather.com{url_completa}",
                })
        
        return resultados

