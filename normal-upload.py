import requests
import os
from datetime import datetime, timezone

# Detalles de tu cuenta y archivo
account_name = "<azure-account-name>"
container_name = "<container-name>"
sas_token = "<azure-blob-container-sasToken>"  # Generado desde Azure
file_path = "<file-path>"  # Ejemplo: "C:/Users/archivo.txt"
blob_name = os.path.basename(file_path)  # Nombre del blob (archivo en el contenedor)

# URL para subir el archivo
url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}?{sas_token}"

# Leer el contenido del archivo para proveer el content length
with open(file_path, "rb") as file:
    file_content = file.read()

# Encabezados requeridos para el funcionamiento de la API
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
