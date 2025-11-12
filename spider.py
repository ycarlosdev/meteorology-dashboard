from curl_cffi import requests as cureq
from selectolax.parser import HTMLParser
from utiles import BuscadorLocalizaciones
import re


def obtener_html_localizacion(nombre_ciudad: str) -> str:
    """
    Busca la ciudad con BuscadorLocalizaciones y devuelve el HTML de su página.
    """
    buscador = BuscadorLocalizaciones(nombre_ciudad)

    if not buscador.obtener_respuesta():
        raise ValueError(f"No se pudo obtener datos para la ciudad: {nombre_ciudad}")

    resultados = buscador.obtener_datos()
    url = resultados[0]["url"]

    respuesta = cureq.get(url, impersonate="chrome")
    return respuesta.text


def extraer_datos(html: str) -> dict:
    """
    A partir del HTML extrae los datos meteorológicos principales.
    """
    tree = HTMLParser(html)
    
    # Clima
    try:
        clima = tree.css_first("span.phrase").text().strip()
    except Exception as e:
        print(f"No se pudo obtener el clima : {e}")

    # Temperatura principal
    try:
        temperatura = tree.css_first("div.temp").text().strip()
    except Exception as e:
        print(f"No se pudo obtener la temperatura : {e}")
        
    # Sensación térmica
    try:
        sensacion_termica_extraida = tree.css_first("div.real-feel").text().strip()
        sensacion_termica_modificada = re.search(r"\d{2}",sensacion_termica_extraida).group(0)
        sensacion_termica = sensacion_termica_modificada + "°C"
    except Exception as e:
        print(f"Error al obtener la sensación térmica : {e}")

    # Otros valores (sensación real, viento, ráfagas...)
    valores = []
    contenedores = tree.css(
        "div.cur-con-weather-card__panel.details-container div.spaced-content.detail"
    )

    for nodo in contenedores:
        valor = nodo.css_first(".value").text().strip()
        valores.append(valor)

    # Función auxiliar para obtener valor de forma segura
    def obtener_valor_seguro(lista, indice, default="N/A"):
        try:
            return lista[indice] if len(lista) > indice else default
        except IndexError:
            return default
        
    if len(valores) == 4:
        return {
            "clima": clima if 'clima' in locals() else "N/A",
            "temperatura": temperatura if 'temperatura' in locals() else "N/A",
            "sensacion_termica": sensacion_termica if "sensacion_termica" in locals() else "N/A",
            "viento": obtener_valor_seguro(valores, 1),
            "rafagas": obtener_valor_seguro(valores, 2),
            "calidad_viento": obtener_valor_seguro(valores, 3)
        }
    else:
        return {
            "clima": clima if 'clima' in locals() else "N/A",
            "temperatura": temperatura if 'temperatura' in locals() else "N/A",
            "sensacion_termica": sensacion_termica if "sensacion_termica" in locals() else "N/A",
            "viento": obtener_valor_seguro(valores, 0),
            "rafagas": obtener_valor_seguro(valores, 1),
            "calidad_viento": obtener_valor_seguro(valores, 2)
        }

        


if __name__ == "__main__":
    html = obtener_html_localizacion("miami")
    datos = extraer_datos(html)
    
    print("Clima:",datos["clima"])
    print("Temperatura:", datos["temperatura"])
    print("Sensación Térmica:", datos["sensacion_termica"])
    print("Viento:", datos["viento"])
    print("Ráfagas:", datos["rafagas"])
    print("Calidad del viento:", datos["calidad_viento"])
