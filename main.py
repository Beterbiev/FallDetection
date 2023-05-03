from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

datos_recibidos = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/datos', methods=['POST'])
def recibir_datos():
    global datos_recibidos
    if request.method == 'POST':
        # Obtener los datos recibidos en la solicitud POST y almacenarlos en la variable datos_recibidos
        datos_recibidos['accel_x'] = request.form['accel_x']
        datos_recibidos['accel_y'] = request.form['accel_y']
        datos_recibidos['accel_z'] = request.form['accel_z']
        datos_recibidos['gyro_x'] = request.form['gyro_x']
        datos_recibidos['gyro_y'] = request.form['gyro_y']
        datos_recibidos['gyro_z'] = request.form['gyro_z']
        
        print("Aceleracion: ", datos_recibidos['accel_x'], ", ", datos_recibidos['accel_y'], ", ", datos_recibidos['accel_z'])
        print("Giroscopio: ", datos_recibidos['gyro_x'], ", ", datos_recibidos['gyro_y'], ", ", datos_recibidos['gyro_z'])
    
    return '', 204

@app.route('/datos', methods=['GET'])
def enviar_datos():
    global datos_recibidos
    # Comprobar si hay datos almacenados en la variable datos_recibidos
    if not datos_recibidos:
        return jsonify({'error': 'No hay datos disponibles'}), 404
    
    # Devolver los datos almacenados en la variable datos_recibidos
    return jsonify(datos_recibidos), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
