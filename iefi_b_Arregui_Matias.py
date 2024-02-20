# <----------------------------------------------------------------->
import os
import requests as rq
from bs4 import BeautifulSoup
import csv

def limpiador(objeto, lista)->None:
    """limpiador: funcion que limpia etiquetas HTML y demas, dejando solo lo importante.

    Args:
        objeto (Object): donde se alojan los datos web.
        lista (str): donde se guardaran los datos.
    """
    for x in objeto:
        titulo =str(x.text).replace("\n","")
        titulo=titulo.strip("  ")
        lista.append(titulo)

def unificadorDatosListas(*args)->list:
    """unificadorDatosLista: unifica las listas con datos, ordenando de manera que, se ordenen segun pertenencia.

    Returns:
        list: lista ordenada con los valores adecuados.
    """
    lista_datos=[]
    largo=0
    for x in args:
        largo = len(x)
        break
    for i in range(largo):
        lista_unificada=[x[i] for x in args]
        lista_datos.append(lista_unificada)
    return lista_datos

# Tiene que funcionar en todo equipo que utilice o no OneDrive y en los idiomas español e inglés.
# OBTENER ENTORNO DE USUARIO / PERMITE ACCEDER A DEMAS DIRECTORIOS
usuario=str(os.environ.get("USERPROFILE"))
# BUSCAMOS LA RUTA ABSOLUTA DEL DOCUMENTOS ------------------------------------------------>
if os.path.exists(usuario+"OneDrive\\Documents"):
    ruta_documentos=f"{usuario}OneDrive\\Documents"
    print(f"Ruta Absoluta a documentos: {ruta_documentos}")
elif os.path.exists(usuario+"OneDrive\\Documentos"):
    ruta_documentos=f"{usuario}OneDrive\\Documentos"
    print(f"Ruta Absoluta a documentos: {ruta_documentos}")
elif os.path.exists(usuario+"\\Documentos"):
    ruta_documentos=f"{usuario}\\Documentos"
    print(f"Ruta Absoluta a documentos: {ruta_documentos}")
else:
    ruta_documentos=f"{usuario}\\Documents"
    print(f"Ruta Absoluta a documentos: {ruta_documentos}")

#CREAMOS LA RUTA ABSOLUTA A CARPETA
ruta_carpeta=ruta_documentos + "\\iefi_b"

# Crear una carpeta iefi_b en Documentos:
#SE CREA LA CARPETA EN CASO QUE NO EXISTA
if not os.path.exists(ruta_carpeta):
    os.mkdir(ruta_carpeta)

try:
    # Obtener la página https://www.imdb.com/movies-coming-soon/ 
    # A CAUSA DE NO PODER OBTENER DATOS POR ASUNTOS DE SEGURIDAD DE LA PAGINA, UTILIZAMOS EL SITIO WEB DEL CARENA
    # Recomendado request.get()
    link = rq.get("https://iscarena-cba.infd.edu.ar/sitio/")
    # Guardar el archivo el archivo html como imdb.com.html, utilizar with open con file=response.content y mode=’wb’.
    with open(ruta_carpeta+"\\imdb.com.html", mode="wb") as file:
        file.write(link.content)
        file.close()


    # Encontrar todos los artículos de noticias:
    soup = BeautifulSoup(link.text, "html.parser")

    #GUARDAMOS EL CONTENEDOR DE INFORMACION, DONDE SE ENCUENTRAN LAS NOTICIAS
    contenedor = soup.find_all("section", {"class": "noticias_redinfod"})

    #INICIALIZAMOS LAS LISTAS DONDE SE ALOJARAN LOS DIFERENTES DATOS
    lista_titulos = []
    lista_fecha = []
    lista_texto = []
    titulos, fechas, texto_contenido = "", "", ""

    #OBTENEMOS TITULO, FECHA Y CONTENIDO PREVIO DE LA NOTICIA
    for section in contenedor:
        #OBTENEMOS TITULO
        titulos = section.find_all("a")
        #OBTENEMOS FECHAS DE PUBLICACION
        fechas = section.find_all("div", {"class":"fecha"})
        #OBTENEMOS CONTENIDO PREVIO DE LA NOTICIA
        texto_contenido = section.find_all("p")

    #lIMPIAMOS DATOS INNECESARIO DE LOS DATOS OBTENIDOS, MEDIANTE LA FUNCION "limpiador"
    limpiador(titulos, lista_titulos)
    limpiador(fechas, lista_fecha)
    limpiador(texto_contenido, lista_texto)

    # Inicializar la lista data 
    #UTILIZAMOS LA FUNCION QUE NOS PERMITE UNIFICAR DATOS DE MANERA CORRECTA.
    data = unificadorDatosListas(lista_titulos, lista_fecha,lista_texto)
    #GUARDAMOS LOS DATOS EN UN ARCHIVO CSV
    with open(ruta_carpeta+"\\imdb.csv", 'w', newline='') as archivo:
        writer = csv.writer(archivo)
        long=len(data)
        cont=0
        for lista in data: 
            for elemento in lista:
                writer.writerow(["Titulo"])
                writer.writerow(lista[0:1])
                writer.writerow(["Fecha"])
                writer.writerow(lista[1:2])
                writer.writerow(["Texto"])
                writer.writerow(lista[2:])
                writer.writerow([" "])
                break
                #UTILIZAMOS BREAK, PARA QUE SOLAMENTE SE CARGEN LOS DATOS DE UNA SOLA VEZ A LA TABLA Y NO SE REPITAN DATOS.
except:
    print("ERROR DE CONEXION")



