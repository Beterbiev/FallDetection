from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/datos', methods=['GET', 'POST'])
def recibir_datos():
    if request.method == 'POST':
        # Realizar operaciones con los datos recibidos
        accel_x = request.form['accel_x']
        accel_y = request.form['accel_y']
        accel_z = request.form['accel_z']
        gyro_x = request.form['gyro_x']
        gyro_y = request.form['gyro_y']
        gyro_z = request.form['gyro_z']
        
        # Realizar las operaciones que deseas con los datos recibidos
        
        print("Aceleracion: ", accel_x, ", ", accel_y, ", ", accel_z)
        print("Giroscopio: ", gyro_x, ", ", gyro_y, ", ", gyro_z)
        
        # Retornar una respuesta al cliente
        data = {
            'accel_x': accel_x,
            'accel_y': accel_y,
            'accel_z': accel_z,
            'gyro_x': gyro_x,
            'gyro_y': gyro_y,
            'gyro_z': gyro_z
        }
        
        return jsonify(data), 200
    
    else:
         return "Solicitud GET recibida correctamente", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)