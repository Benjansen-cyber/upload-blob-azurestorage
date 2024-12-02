import requests
import os
from datetime import datetime, timezone

# URL de tu Function App (asegúrate de incluir la URL completa de la función HTTP Trigger)
url = "https://<function-app>.azurewebsites.net"

# Parámetros que vas a enviar en la solicitud de token SAS a function app
def Sas_Token():
    body_request = {
        "":"",
        "":""
    }
    headers = {
        #autenticacions
        "x-functions-key": "<function-key-acces>"
    }
    try:
        # Realizar una solicitud GET
        response = requests.get(url, json=body_request,headers=headers)
        if response.status_code == 200:
            print("Respuesta de la función:")
            print(response.text)
            return response.text
        else:
            print(f"Error: Código de estado {response.status_code}")
            print("Mensaje:", response.text)
    except Exception as e:
        print("Ocurrió un error al intentar consumir la función:", str(e))

#-------------------------
# subida de archivo 

# Detalles de tu cuenta y archivo
account_name = "<storage-name>"
container_name = "<container-name>"
sas_token = Sas_Token()  # Generado desde Azure
file_path = "path file"  # Ejemplo: "C:/Users/archivo.txt"
blob_name = os.path.basename(file_path)  # Nombre del blob (archivo en el contenedor)

# URL para subir el archivo
url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"

# Leer el contenido del archivo
with open(file_path, "rb") as file:
    file_content = file.read()

# Encabezados requeridos
headers = {
    "x-ms-version": "2020-02-10",
    "x-ms-date": datetime.now(tz=timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT"),
    "x-ms-blob-type": "BlockBlob",  # Tipo de blob
    "Content-Length": str(len(file_content)),  # Tamaño del archivo
    "Content-Type": "application/octet-stream",  # Tipo de contenido
}

# Hacer la solicitud PUT
response = requests.put(url, headers=headers, data=file_content)

# Verificar el resultado
if response.status_code == 201:
    print("Archivo subido exitosamente.")
else:
    print(f"Error al subir el archivo. Código: {response.status_code}")
    print(response.text)
