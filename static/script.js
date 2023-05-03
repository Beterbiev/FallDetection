const gyroX = document.getElementById('gyroX');
const gyroY = document.getElementById('gyroY');
const gyroZ = document.getElementById('gyroZ');
const accX = document.getElementById('accX');
const accY = document.getElementById('accY');
const accZ = document.getElementById('accZ');

let data = {
  gyro_x: NaN,
  gyro_y: NaN,
  gyro_z: NaN,
  accel_x: NaN,
  accel_y: NaN,
  accel_z: NaN
};

let gyroscope = [];  // Arreglo para almacenar el giroscopio
let acceleration = [];  // Arreglo para almacenar la aceleración
let time = [];  // Arreglo para almacenar el tiempo


// Realizar una solicitud AJAX para obtener los datos del servidor Flask
function getData() {
  const xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        const data = JSON.parse(xhr.responseText);
        console.log(xhr.responseText);
        console.log(data);
        gyroX.innerHTML = parseFloat(data.gyro_x).toFixed(2);
        gyroY.innerHTML = parseFloat(data.gyro_y).toFixed(2);
        gyroZ.innerHTML = parseFloat(data.gyro_z).toFixed(2);
        accX.innerHTML = parseFloat(data.accel_x).toFixed(2);
        accY.innerHTML = parseFloat(data.accel_y).toFixed(2);
        accZ.innerHTML = parseFloat(data.accel_z).toFixed(2);

        // Agregar la aceleración y el tiempo al arreglo correspondiente
        acceleration.push(parseFloat(data.accel_x));
        time.push(new Date().getTime());

        gyroscope.push(parseFloat(data.gyro_x));
        time.push(new Date().getTime());


        // Graficar la aceleración con el tiempo
        Plotly.newPlot('plot', [{
          x: time,
          y: acceleration,
          type: 'scatter',
          mode: 'lines',
          name: 'Aceleración'
        }, {
          x: time,
          y: gyroscope,
          type: 'scatter',
          mode: 'lines',
          name:'Giroscopio'
        }]);

      } else {
        console.log('Error: ' + xhr.status);
      }
    }
  };
  xhr.open('GET', '/datos');
  xhr.send();
}



// Actualizar los datos cada 500 milisegundos
setInterval(getData, 500);