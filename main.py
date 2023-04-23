from flask import Flask, request

app = Flask(__name__)

@app.route('/datos', methods=['POST'])
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
        
        # Retornar una respuesta al cliente
        return "Datos recibidos correctamente", 200
    else:
        # Retornar una respuesta al cliente si la solicitud no es POST
        return "Método no permitido", 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)