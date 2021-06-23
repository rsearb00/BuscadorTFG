# Importamos los paquetes necesarios: el driver y el timer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
import urllib.request

# Arrays para guardar la url, el texto y las dimensiones (se podrían combinar en una matriz)
images_url = []
images_text = []
images_dimen = []

# Creamos una función que recibe el parámetro de búsqueda, abre Chrome, va hasta Google y realiza la búsqueda
def buscar_imagen(busqueda, num_busquedas):
    # Primero localizamos el driver en nuestro equipo
    driver = webdriver.Chrome('C:/chromedriver.exe')

    # Opción 1: Buscar metiendo la búsqueda en el cuadro de texto:
    # driver.get('https://www.google.es/imghp?hl=en&tab=ri&authuser=0&ogbl')
    # box = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
    # box.send_keys(busqueda)
    # box.send_keys(Keys.ENTER)

    # Opción 2: Meter la búsqueda en la ruta de Google (tiene añadida la opción de "grande" para coger imágenes buenas)
    driver.get(
        f"https://www.google.com/search?q={busqueda}&tbm=isch&hl=es&tbs=isz:l")
    # f"https://www.google.com/search?q={busqueda}&tbm=isch")

    # Una vez hecha la búsqueda, hacemos scroll hasta el final de la página
    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(2)
        new_height = driver.execute_script('return document.body.scrollHeight')
        try:
            driver.find_element_by_xpath(
                '//*[@id="islmp"]/div/div/div/div/div[5]/input').click()
            time.sleep(2)
        except:
            pass
        if new_height == last_height:
            break
        last_height = new_height

    # Una vez tenemos la página completa, creamos un bucle que recorre las imágenes una a una
    # Se puede poner un número máximo o que recorra todas las que hay
    # Range: primer número, empieza, último, no lo coge. Se puede poner otro argumento más para indicar los saltos.
    for i in range(1, num_busquedas+1):
        try:
            # Pulsamos sobre la imagen y obtenemos la imagen individual al hacer click (modo de selección de Google)
            driver.find_element_by_xpath(
                '//*[@id="islrg"]/div[1]/div['+str(i)+']/a[1]/div[1]/img').click()

            # Ponemos un sleep para que dé tiempo a que cargue la imagen (si no lo ponemos, obtiene la miniatura sin cargar la completa)
            time.sleep(4)

            # Con la imagen abierta, copiamos el Xpath (mejor esto que directamente coger la ruta) para sacar el texto y la ruta
            imagen = driver.find_element_by_xpath(
                '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div/div[2]/a/img')

            # Buscamos ahora el span donde se guarda el tamaño en píxeles de la imagen
            imagenDim = driver.find_element_by_class_name(
                "VSIspc").get_attribute("innerHTML")

            # Buscamos el texto que acompaña a la imagen
            imagenText = driver.find_element_by_xpath(
                '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[3]/div[2]/a').get_attribute("title")

            # Agregamos la ruta de la imagen a la lista de imagenes, el texto que la acompaña
            images_url.append(imagen.get_attribute("src"))
            images_text.append(imagenText)
            images_dimen.append(imagenDim)
            # Con esto descargamos las imágenes y las guardamos con el nombre de la búsqueda
            urllib.request.urlretrieve(imagen.get_attribute(
                "src"), f"C:/Users/Raul/Desktop/Uni 2020-2021/Segundo Cuatrimestre/TFG/Pruebas/FotosGoogle//{busqueda}"+str(i)+".jpg")
        except:
            pass

    # Espera 10 segundos y cierra el Chrome
    time.sleep(10)


busqueda = input("Introduce lo que quieres buscar: ")
num_busquedas = input("Introduce el número de búsquedas: ")
print(
    f"Has decidido buscar {busqueda} el siguiente número de veces {num_busquedas}")
buscar_imagen(busqueda, int(num_busquedas))

# El número + 1 porque range no incluye el extremo superior
for i in range(1, int(num_busquedas)+1):
    # Escribimos por pantalla
    print(f"Imagen {i}:")
    print(images_url[i-1])
    print(images_dimen[i-1])
    print(images_text[i-1]+"\n")

    # Escribimos en el fichero de texto
    # (si no ponemos el encoding, con algunos caracteres falla)
    with open(f"C:/Users/Raul/Desktop/Uni 2020-2021/Segundo Cuatrimestre/TFG/Pruebas/FotosGoogle//{busqueda}.txt", 'a', encoding='utf-8') as f:
        f.write("Url: " + images_url[i-1]+"\n")
        f.write("Tamaño en píxeles: "+images_dimen[i-1]+"\n")
        f.write("Texto que la acompaña: "+images_text[i-1]+"\n")
        f.write(""+"\n")
