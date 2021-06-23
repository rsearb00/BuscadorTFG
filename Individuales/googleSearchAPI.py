from google_images_search import GoogleImagesSearch

# Clave de la API
API_KEY='AIzaSyCwyYnQEC6bmXq5DuTiPPIBQ0RTVOi363c'
key=API_KEY
# ID del Buscador o CX:
idBuscador='d9e4271b079afcc62'


# you can provide API key and CX using arguments,
# or you can set environment variables: GCS_DEVELOPER_KEY, GCS_CX
gis = GoogleImagesSearch(key, idBuscador)

# Parámetros de Búsqueda
_search_params = {
    'q': 'Marca.com',
    'num': 5,
    'safe': 'high',
    'fileType': 'jpg',
    #'imgType': 'clipart|face|lineart|news|photo',
    #'imgSize': 'huge|icon|large|medium|small|xlarge|xxlarge',
    #'imgDominantColor': 'black|blue|brown|gray|green|pink|purple|teal|white|yellow',
    #'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived'
}


# Funciona bien pero está un poco desfasado, los resultados son antiguos
gis.search(search_params={'q': 'Marca.com','num':5}, path_to_dir='./SearchEngine', 
           custom_image_name='Marca')
