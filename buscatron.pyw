# -------------------Autor y Funcionalidad----------------
"""
Autor: Raúl Seara Barroso
Funcionalidad: 
    Aplicación de búsqueda en la web utilizando diferentes técnicas de Scraping y Crawling
"""
# ----------------------Librerías-------------------------------------------------------------
# ----Interfaz gráfica
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox

# -----Búsqueda en Google con Web Driver
# Importamos los paquetes necesarios: el driver y el timer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import requests
import urllib.request

# -------Búsqueda con la API de Google
from google_images_search import GoogleImagesSearch

# Clave de la API
key = 'AIzaSyCwyYnQEC6bmXq5DuTiPPIBQ0RTVOi363c'
# ID del Buscador o CX:
idBuscador = 'd9e4271b079afcc62'


# --------------------------------Creación de la Interfaz-----------------------------------
raiz = Tk()
raiz.title("BuscaTRÓN")

busquedaTk = StringVar()
numBusquedas = IntVar()
buscadorSeleccionado = StringVar()

bienvenidaLabel = Label(raiz, text="¡Bienvenido al BuscaTRÓN!")
bienvenidaLabel.pack()

# Ventanas emergentes del menú
def infoGoogleDriver():
    messagebox.showinfo(
        message='Esta búsqueda funciona mediante un navegador de Google Chrome autónomo.\nBuscará imágenes como si fuese una persona, mostrando en tiempo real como se mueve por la página y como las descarga.\nLos resultados aparecerán en la carpeta "GoogleDriver"', title='Google Driver')

def infoAPIGoogle():
    messagebox.showinfo(
        message='Esta búsqueda funciona mediante la API de Google.\nInternamente esta aplicación guarda un buscador propio con su clave para poder buscar en Google.\nNo muestra gráficamente los resultados.\nAlmacena las fotos en la carpeta "GoogleAPI"', title='API de Google')

def infoOpcionesGenerales():
    messagebox.showinfo(
        message='"Introduce lo que quieras buscar:" aquí tenemos que poner el parámetro de búsqueda que va a determinar los resultados.\n\n"Introduce el número de imágenes a descargar:" en este caso, lo que seleccionamos es cuantas imágenes vamos a descargar.', title='Opciones generales')

def infoAcercaDe():
    messagebox.showinfo(
        message='El BuscaTRÓN es una aplicación de búsqueda automática de imágenes\nDesarrollada por Raúl Seara Barroso - 2021', title='Acerca de')


# Elementos del menú
barraMenu = Menu(raiz)
raiz.config(menu=barraMenu)
# Con tearoff quitamos las barritas por defecto
ayudaMenu=Menu(barraMenu, tearoff=0)
ayudaMenu.add_command(label="Google Driver", command=infoGoogleDriver)
ayudaMenu.add_command(label="API de Google", command=infoAPIGoogle)
ayudaMenu.add_command(label="Opciones generales", command=infoOpcionesGenerales)
ayudaMenu.add_separator()
ayudaMenu.add_command(label="Acerca de...", command=infoAcercaDe)

barraMenu.add_cascade(label="Ayuda", menu=ayudaMenu)


seleccionBuscadorLabel = Label(
    raiz, text="Por favor, selecciona un buscador entre los disponibles:")
seleccionBuscadorLabel.pack()

opcionesBusqueda = ['Google Driver', 'API de Google']
comboBox = Combobox(raiz, width=50, values=opcionesBusqueda, state='readonly')
comboBox.current(0)
comboBox.pack()

miFrame = Frame(raiz, width=250, height=200)
miFrame.pack()

cuadroBusqueda = Entry(miFrame, textvariable=busquedaTk)
cuadroBusqueda.grid(row=1, column=1, padx=5, pady=5)

cuadroNumBusquedas = Spinbox(miFrame, from_=1, to=10000, textvariable=numBusquedas)
cuadroNumBusquedas.grid(row=2, column=1, padx=5, pady=5)

busquedaLabel = Label(miFrame, text="Introduce lo que quieres buscar: ")
busquedaLabel.grid(row=1, column=0, sticky="e", padx=5, pady=5)

numBusquedasLabel = Label(miFrame, text="Introduce el número de imágenes a descargar: ")
numBusquedasLabel.grid(row=2, column=0, sticky="e", padx=5, pady=5)

# ---------------------------Funciones de búsqueda------------------------

# ----1 - Google con Web Driver
# Creamos una función que recibe el parámetro de búsqueda, abre Chrome, va hasta Google y realiza la búsqueda

def googleDriver(busqueda, num_busquedas):
    # Primero localizamos el driver en nuestro equipo
    driver = webdriver.Chrome('C:/chromedriver.exe')

    # Arrays para guardar la url, el texto y las dimensiones (se podrían combinar en una matriz)
    # Sin uso actual (guarda en cada vuelta del for)
    #images_url = []
    #images_text = []
    #images_dimen = []

    # Opción 1: Buscar metiendo la búsqueda en el cuadro de texto:
    # driver.get('https://www.google.es/imghp?hl=en&tab=ri&authuser=0&ogbl')
    # box = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
    # box.send_keys(busqueda)
    # box.send_keys(Keys.ENTER)

    # Opción 2: Meter la búsqueda en la ruta de Google (tiene añadida la opción de "grande" para coger imágenes buenas)
    driver.get(
        f"https://www.google.com/search?q={busqueda}&tbm=isch&hl=es&tbs=isz:l")
    # f"https://www.google.com/search?q={busqueda}&tbm=isch")

    # Una vez hecha la búsqueda, hacemos scroll hasta el final de la página y pulsamos el botón "Mostrar más resultados"
    last_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0,document.body.scrollHeight)')
        time.sleep(2)
        new_height = driver.execute_script('return document.body.scrollHeight')
        try:
            driver.find_element_by_xpath(
                '//*[@id="islmp"]/div/div/div/div/div[3]/div[2]/input').click()
                # '//*[@id="islmp"]/div/div/div/div/div[4]/div[2]/input
            # '//*[@id="islmp"]/div/div/div/div/div[5]/input'
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

            # Agregamos la ruta de la imagen a la lista de imagenes, el texto que la acompaña y sus dimensiones
            # images_url.append(imagen.get_attribute("src"))
            # images_text.append(imagenText)
            # images_dimen.append(imagenDim)

            # Con esto descargamos las imágenes y las guardamos con el nombre de la búsqueda
            urllib.request.urlretrieve(imagen.get_attribute(
                "src"), f"./GoogleDriver/{busqueda}"+str(i)+".jpg")

            print(f"Guardando imagen {i}")
            with open(f"./GoogleDriver/{busqueda}.txt", 'a', encoding='utf-8') as f:
                f.write("Url: " + imagen.get_attribute("src")+"\n")
                f.write("Tamaño en píxeles: "+imagenDim+"\n")
                f.write("Texto que la acompaña: "+imagenText+"\n")
                f.write(""+"\n")

        except:
            print("Ha fallado al guardar la imagen")
            pass
    # Quit cierra todas las sesiones, close solo la pestaña actual
    driver.quit()
    messagebox.showinfo(
        message='La búsqueda ha concluido, puedes buscar de nuevo', title='Búsqueda finalizada con éxito')

# ------2 Búsqueda con la API de Google (busca en toda la web)-----------------------------------

def googleAPI(busqueda, num_busquedas):
    # Asignamos las variables de la clave y el id del buscador
    gis = GoogleImagesSearch(key, idBuscador)

    # Parámetros de Búsqueda seleccionables
    """
    _search_params = {
        'q': 'busqueda',
        'num': numerodebusquedas,
        'safe': 'high',
        'fileType': 'jpg',
        'imgType': 'clipart|face|lineart|news|photo',
        'imgSize': 'huge|icon|large|medium|small|xlarge|xxlarge',
        'imgDominantColor': 'black|blue|brown|gray|green|pink|purple|teal|white|yellow',
        'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived'
    }
    """

    # Funciona bien pero está un poco desfasado, los resultados son antiguos
    gis.search(search_params={'q': busqueda, 'num': num_busquedas}, path_to_dir='./GoogleAPI',
               custom_image_name=busqueda)
    
    messagebox.showinfo(
        message='La búsqueda ha concluido, puedes buscar de nuevo', title='Búsqueda finalizada con éxito')


# -------------------------Botón de búsqueda----------------------------------------------


def buscar(busq, numB):
    if busq != "" and numB > 0:
        #print(f"Opción del buscador: {comboBox.get()}")
        # OJO: Current obtiene el índice del elemento y get() el valor
        if comboBox.get() == 'Google Driver':
            # Ventana de éxito que muestra que la búsqueda está en curso
            messagebox.showinfo(
                message=f'Has decidido buscar {busq} {numB} veces, usando Google Driver.\nPor favor, espera a que acabe para buscar de nuevo', title='Búsqueda en curso')
            #print(f"Has decidido buscar: {busq} el siguiente número de veces: {numB} usando Google Driver")
            googleDriver(busq, numB)

        else:
            # Ventana de éxito que muestra que la búsqueda está en curso
            messagebox.showinfo(
                message=f'Has decidido buscar {busq} {numB} veces, usando la API de Google.\nPor favor, espera a que acabe para buscar de nuevo.', title='Búsqueda en curso')
            #print(f"Has decidido buscar: {busq} el siguiente número de veces: {numB} usando la API de Google")
            googleAPI(busq, numB)

    else:
        # Ventana de fallo que indica que no se puede producir la búsqueda al no existir
        messagebox.showerror(
            message='Por favor, introduce los valores que faltan', title='No se puede hacer la búsqueda')
        #print("No ha seleccionado opciones correctas")


# Si no ponemos lambda, el botón llama directamente a la función, sin esperar
botonBusqueda = Button(raiz, text="Realizar búsqueda",
                       command=lambda: buscar(busquedaTk.get(), numBusquedas.get()))
#botonBusqueda.grid(row=0, column=2, sticky="e", padx=10, pady=10)
botonBusqueda.pack()

# Al final del todo, para mantener la ventana de búsqueda abierta
raiz.mainloop()
