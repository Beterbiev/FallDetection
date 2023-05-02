// Obtener los elementos HTML necesarios
const gyroX = document.getElementById('gyroX');
const gyroY = document.getElementById('gyroY');
const gyroZ = document.getElementById('gyroZ');
const accX = document.getElementById('accX');
const accY = document.getElementById('accY');
const accZ = document.getElementById('accZ');

// Realizar una solicitud AJAX para obtener los datos del servidor Flask
function getData() {
  const xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        // Actualizar los valores HTML con los datos recibidos
        const data = JSON.parse(xhr.responseText);
        console.log('Datos recibidos:', data);
        gyroX.innerHTML = data.gyro_x.toFixed(2);
        gyroY.innerHTML = data.gyro_y.toFixed(2);
        gyroZ.innerHTML = data.gyro_z.toFixed(2);
        accX.innerHTML = data.accel_x.toFixed(2);
        accY.innerHTML = data.accel_y.toFixed(2);
        accZ.innerHTML = data.accel_z.toFixed(2);

        // Enviar los datos de vuelta al servidor Flask
        const accelXValue = data.accel_x.toFixed(2);
        const accelYValue = data.accel_y.toFixed(2);
        const accelZValue = data.accel_z.toFixed(2);
        const gyroXValue = data.gyro_x.toFixed(2);
        const gyroYValue = data.gyro_y.toFixed(2);
        const gyroZValue = data.gyro_z.toFixed(2);
        xhr.open('POST', '/datos');
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.send('accel_x=' + accelXValue + '&accel_y=' + accelYValue + '&accel_z=' + accelZValue + '&gyro_x=' + gyroXValue + '&gyro_y=' + gyroYValue + '&gyro_z=' + gyroZValue);
      } else {
        // Manejar errores
        console.log('Error: ' + xhr.status);
      }
    }
  };
}

// Actualizar los datos cada 500 milisegundos
setInterval(getData, 500);
