from flask import Flask, send_from_directory, request, jsonify
import numpy as np
import timeit
import time
import matplotlib.pyplot as plt
import threading

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/static/js/<path:path>')
def serve_js(path):
    return send_from_directory('static/static/js', path)

@app.route('/static/css/<path:path>')
def serve_css(path):
    return send_from_directory('static/static/css', path)

@app.route('/static/media/<path:path>')
def serve_media(path):
    return send_from_directory('static/static/media', path)

def run_flask_app():
    app.run(host='0.0.0.0', port=50)

def run_calcul_server():
    # Code pour exécuter votre serveur de calcul
    @app.route("/test", methods=['POST','GET'])
    def members():
        json_data = request.get_json()  # Récupère le JSON envoyé
        # Effectuez le traitement souhaité sur le JSON ici
        print(json_data)

        #data = json.loads(json_data)

        # Accéder à la valeur de "size"
        size_min = int(json_data['minSize'])
        size_max = int(json_data['maxSize'])
        step_size = int(json_data['number'])

        
        temps_moy=[]
        taille=[]
        



        # Afficher la valeur de "size"
        print(size_min, size_max)

        for size in range(size_min, size_max, step_size):
            temps=[]
            for i in range(1000):
                real_part = np.random.rand(size, size)
                imag_part = np.random.rand(size, size)
                complex_matrix = real_part + 1j * imag_part


                #start_time = timeit.default_timer()
                start_time = time.time()
                inverse = np.linalg.inv(complex_matrix)
                #end_time = timeit.default_timer()
                end_time = time.time()
                temps.append(end_time - start_time)

            taille.append(size)
            temps_moy.append(np.mean(temps)*10**3)

        print(temps_moy)
        result = {"taille": taille,
                "res": temps_moy}

        return jsonify(result)

    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    # Créez les threads pour les deux serveurs
    flask_thread = threading.Thread(target=run_flask_app)
    calcul_thread = threading.Thread(target=run_calcul_server)

    # Lancez les threads
    flask_thread.start()
    calcul_thread.start()

    # Attendez que les threads
