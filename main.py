from flask import Flask, request, render_template, jsonify
import joblib
import numpy as np
from scipy.stats import skew, kurtosis
import entropy as ent

app = Flask(__name__)

datos_recibidos = {}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/datos', methods=['POST'])
def recibir_datos():
    global datos_recibidos
    if request.method == 'POST':
        datos_recibidos['accel_x'] = np.array(list(map(float, request.form['accel_x'].split(','))))
        datos_recibidos['accel_y'] = np.array(list(map(float, request.form['accel_y'].split(','))))
        datos_recibidos['accel_z'] = np.array(list(map(float, request.form['accel_z'].split(','))))
        datos_recibidos['gyro_x'] = np.array(list(map(float, request.form['gyro_x'].split(','))))
        datos_recibidos['gyro_y'] = np.array(list(map(float, request.form['gyro_y'].split(','))))
        datos_recibidos['gyro_z'] = np.array(list(map(float, request.form['gyro_z'].split(','))))
        
        print("Aceleracion: ", datos_recibidos['accel_x'], ", ", datos_recibidos['accel_y'], ", ", datos_recibidos['accel_z'])
        print("Giroscopio: ", datos_recibidos['gyro_x'], ", ", datos_recibidos['gyro_y'], ", ", datos_recibidos['gyro_z'])
    
    return '', 204

def calcular_caracteristicas(accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z):
    features = []
    
    accmagnitude = np.sqrt(accel_x**2 + accel_y**2 + accel_z**2)
    gccmagnitude = np.sqrt(gyro_x**2 + gyro_y**2 + gyro_z**2)
    
    for data in [accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z]:
        mean = np.mean(data)
        std = np.std(data)
        var = np.var(data)
        minimum = np.min(data)
        maximum = np.max(data)
        skewness = skew(data)
        kurtosis_val = kurtosis(data)
        spectral_entropy = ent.spectral_entropy(data, 200, method='fft')
        
        features.extend([mean, std, var, minimum, maximum, skewness, kurtosis_val, spectral_entropy])
    
    #spectral_entropy_acc = ent.spectral_entropy(accmagnitude, 200, method='fft')
    #spectral_entropy_gcc = ent.spectral_entropy(gccmagnitude, 200, method='fft')
    #features.extend([spectral_entropy_acc, spectral_entropy_gcc])
    
    return features

def clasificar(datos):
    # Cargar el modelo SVM
    modelo_svm = joblib.load('SVM.pkl')

    # Extraer las características de los datos recibidos
    features = calcular_caracteristicas(datos['accel_x'], datos['accel_y'], datos['accel_z'], datos['gyro_x'], datos['gyro_y'], datos['gyro_z'])

    # Realizar la predicción con el modelo SVM utilizando las características
    prediccion = modelo_svm.predict([features])

    return prediccion.tolist()

@app.route('/predict', methods=['GET'])
def predecir():
    # Verificar si hay datos almacenados en la variable datos_recibidos
    if not datos_recibidos:
        return jsonify({'error': 'No hay datos disponibles'}), 404

    # Realizar la clasificación de los datos
    prediccion = clasificar(datos_recibidos)

    # Vaciar los datos recibidos
    datos_recibidos = {}

    # Devolver la predicción en la respuesta
    return jsonify({'prediccion': prediccion}), 200

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
