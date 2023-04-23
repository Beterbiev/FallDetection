#include <Wire.h>
#include <WiFi.h>
#include <WiFiManager.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <HTTPClient.h>

Adafruit_MPU6050 mpu;

const char* ssid = "FallDetection";
const char* password = "oscar123";

const char* SERVER_IP = "192.168.0.33";
const int SERVER_PORT = 5000;
const char* SERVER_PATH = "/datos";

void setup() {
  Serial.begin(115200);
  esp_netif_init();
  initWiFi();
  Wire.begin();
  mpu.begin();

  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }

  mpu.setAccelerometerRange(MPU6050_RANGE_8_G);
  mpu.setGyroRange(MPU6050_RANGE_500_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  postData(a, g);

  printData(a, g);

  delay(1000);
}

void postData(sensors_event_t a, sensors_event_t g) {
  HTTPClient http;
  String serverAddress = "http://" + String(SERVER_IP) + ":" + String(SERVER_PORT) + String(SERVER_PATH);
  String data = "accel_x=" + String(a.acceleration.x) + "&accel_y=" + String(a.acceleration.y) + "&accel_z=" + String(a.acceleration.z) + "&gyro_x=" + String(g.gyro.x) + "&gyro_y=" + String(g.gyro.y) + "&gyro_z=" + String(g.gyro.z);
  http.begin(serverAddress);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");

  int httpResponseCode = http.POST(data);
  if (httpResponseCode > 0) {
    Serial.print("Envío de datos exitoso, código de respuesta HTTP: ");
    Serial.println(httpResponseCode);
  } else {
    Serial.print("Error en el envío de datos, código de respuesta HTTP: ");
    Serial.println(httpResponseCode);
  }
  http.end();
}

void printData(sensors_event_t a, sensors_event_t g) {
  float accelX = a.acceleration.x;
  float accelY = a.acceleration.y;
  float accelZ = a.acceleration.z;
  
  float gyroX = g.gyro.x;
  float gyroY = g.gyro.y;
  float gyroZ = g.gyro.z;

  Serial.print("Aceleracion: ");
  Serial.print(accelX);
  Serial.print(", ");
  Serial.print(accelY);
  Serial.print(", ");
  Serial.println(accelZ);

  Serial.print("Giroscopio: ");
  Serial.print(gyroX);
  Serial.print(", ");
  Serial.print(gyroY);
  Serial.print(", ");
  Serial.println(gyroZ);
}

void initWiFi() {
  WiFi.mode(WIFI_STA);

  WiFiManager wm;

  bool res = wm.autoConnect(ssid, password);

  if (!res) {
    Serial.println("Failed to connect");
  }

  Serial.println("");
  Serial.print("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(1000);
  }
  Serial.println("");
  Serial.println(WiFi.localIP());
}
