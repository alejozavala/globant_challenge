from flask import Flask, request, jsonify
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import csv
import pymysql
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Configuración de credenciales OAuth 2.0
CLIENT_SECRETS_FILE = 'credenciales.json' 
SCOPES = ['https://www.googleapis.com/auth/drive'] 

#Conexion a MySQL
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'rootroot'
DB_NAME = 'globant_challenge'

# Función para autenticar y acceder a Google Drive
def get_drive_files():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    folder_id = '1J4Ccf7XHZ4967dHpGZ5cKBYFkT4UC9Mu'
    files = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()

    return files

def get_google_drive_credentials():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES, redirect_uri='http://localhost:5000/login/callback')
    credentials = flow.run_local_server(port=0)
    return credentials

credentials = get_google_drive_credentials()
files = get_drive_files(credentials)

# Función para cargar los datos desde un archivo CSV a la base de datos MySQL
def load_data_to_mysql(file_id, table_name):
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    file = drive.CreateFile({'id': file_id})
    file.GetContentFile('temp.csv')

    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = conn.cursor()

    with open('temp.csv', 'r') as csvfile:
        csv_data = csv.reader(csvfile)
        next(csv_data) 
        for row in csv_data:
            cursor.execute(f"INSERT INTO {table_name} VALUES ({', '.join('%s' for _ in row)})", row)

    conn.commit()
    conn.close()


@app.route('/load-data', methods=['GET', 'POST'])
def load_data():
"""
Esta función maneja las solicitudes para cargar datos desde un archivo CSV en la base de datos MySQL
Si la solicitud es un método POST, se espera que contenga un JSON con el ID del archivo y el nombre de la tabla.
Si la solicitud es un método GET, se espera que contenga el ID del archivo como un parámetro de consulta.
En ambos casos, la función responde con una vista previa de los datos del archivo CSV o maneja la carga de datos según corresponda
"""
    if request.method == 'POST':
        # Manejar la carga de datos desde el archivo CSV
        request_data = request.get_json()
        file_id = request_data.get('file_id')
        table_name = request_data.get('table_name')

        if not file_id or not table_name:
            return jsonify({'error': 'File ID and table name are required'}), 400

        try:
            load_data_to_mysql(file_id, table_name)
            return jsonify({'success': True}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    elif request.method == 'GET':
         # Obtener una vista previa de los datos del archivo CSV
        file_id = request.args.get('file_id')
        #table_name = request.args.get('table_name')

        if not file_id:
            return jsonify({'error': 'file_id required'}), 400

        try:
            preview_data = get_preview_data_from_csv(file_id)
            return jsonify(preview_data), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
def get_preview_data_from_csv(file_id):
    # Verificar la existencia del archivo en Google Drive
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    folder_id = '1J4Ccf7XHZ4967dHpGZ5cKBYFkT4UC9Mu' 
    files = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
    file_found = False

    for file in files:
        if file['id'] == file_id:
            file_found = True
            break

    if not file_found:
        raise Exception('File not found in Google Drive')

    preview_data = []
    return preview_data[:10]  # Devolver los primeros 10 registros como vista previa

 
def index():
    return 'Landing Page Test'

if __name__ == '__main__':
    app.run(debug=True)
