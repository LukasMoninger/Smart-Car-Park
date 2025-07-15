#include <WiFi.h>
#include <Wire.h>
#include <PubSubClient.h>
#include <Adafruit_AHTX0.h>
#include <SparkFun_ENS160.h>


#define ESP_NAME "esp1"

Adafruit_AHTX0 aht;
SparkFun_ENS160 ens;
WiFiClient espClient;
PubSubClient mqttClient(espClient);

const int ventilation = 2;
const int trigger_ultrasonic = 5;
const int echo_ultrasonic = 18;

const char* ssid = "FRITZ!Box 6490 FR4";
const char* password = "EG28kc56pu18vz";

const char* mqtt_server = "192.168.178.69";
const int mqtt_port = 1883;
const char* mqtt_user = "";
const char* mqtt_password = "";
const char* topic_distance = ESP_NAME "/sensor/distance";
const char* topic_co2 = ESP_NAME "/sensor/co2";


void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);
  setup_wifi();
  mqttClient.setServer(mqtt_server, mqtt_port);

  pinMode(ventilation, OUTPUT);
  digitalWrite(ventilation, LOW);
  pinMode(trigger_ultrasonic, OUTPUT);
  pinMode(echo_ultrasonic, INPUT);

  if (!aht.begin()) {
    Serial.println("AHT21 nicht gefunden!");
    while (1) delay(10);
  }
  Serial.println("AHT21 bereit.");

  if (!ens.begin()) {
    Serial.println("Could not communicate with the ENS160, check wiring.");
    while (1) delay(10);
  }

  if (ens.setOperatingMode(SFE_ENS160_RESET))
    Serial.println("Ready.");

  delay(100);
  ens.setOperatingMode(SFE_ENS160_STANDARD);

  int ensStatus = ens.getFlags();
  Serial.print("Gas Sensor Status Flag (0 - Standard, 1 - Warm up, 2 - Initial Start Up): ");
  Serial.println(ensStatus);
}


void setup_wifi() {
  delay(10);
  Serial.print("Verbinde mit WLAN ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WLAN verbunden, IP: ");
  Serial.println(WiFi.localIP());
}


void reconnect_mqtt() {
  while (!mqttClient.connected()) {
    Serial.print("Verbinde MQTT…");
    if (mqttClient.connect("ESP32Client", mqtt_user, mqtt_password)) {
      Serial.println("verbunden");
    } else {
      Serial.print("fehlgeschlagen, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" – neuer Versuch in 5 s");
      delay(5000);
    }
  }
}


void loop() {
  digitalWrite(trigger_ultrasonic, LOW);
  delayMicroseconds(2);
  digitalWrite(trigger_ultrasonic, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigger_ultrasonic, LOW);

  long duration = pulseIn(echo_ultrasonic, HIGH);
  long distance = duration / 58.2;
  String disp = String(distance);

  Serial.print("Distance: ");
  Serial.print(disp);
  Serial.println(" cm");
  
  int air_quality_index = 0;
  int volatile_organic_compounds = 0;
  int co2 = 0;
  int gas_status = 0;
  if(ens.checkDataStatus()){
    air_quality_index = ens.getAQI();
		Serial.print("Air Quality Index (1-5) : ");
		Serial.println(air_quality_index);

    volatile_organic_compounds = ens.getTVOC();
		Serial.print("Total Volatile Organic Compounds: ");
		Serial.print(volatile_organic_compounds);
		Serial.println("ppb");

    co2 = ens.getECO2();
		Serial.print("CO2 concentration: ");
		Serial.print(co2);
		Serial.println("ppm");

    gas_status = ens.getFlags();
	  Serial.print("Gas Sensor Status Flag (0 - Standard, 1 - Warm up, 2 - Initial Start Up): ");
    Serial.println(gas_status);
		Serial.println();
	}
	delay(200);
  
  
  if (!mqttClient.connected()) {
    reconnect_mqtt();
  }
  mqttClient.loop();

  char payload_co2[64];
  snprintf(payload_co2, sizeof(payload_co2),
           "{\"eCO2\":%u}",
           co2);

  mqttClient.publish(topic_co2,  payload_co2);
  Serial.print("Publish: ");
  Serial.println(payload_co2);

  char payload_dist[64];
  snprintf(payload_dist, sizeof(payload_dist),
           "{\"distance\":%u}",
           distance);

  mqttClient.publish(topic_distance,  payload_dist);
  Serial.print("Publish: ");
  Serial.println(payload_dist);

  if(co2 > 850){
    activate_ventilation();
  }else{
    deactivate_ventilation();
  }

  delay(5000);
}

void activate_ventilation(){
  digitalWrite(ventilation, HIGH);
}

void deactivate_ventilation(){
  digitalWrite(ventilation, LOW);
}

void test_temp_humidity() {
  if (!aht.begin()) {
    Serial.println("AHT21 nicht gefunden!");
    while (1) delay(10);
  }
  Serial.println("AHT21 bereit.");

  while (true) {
    sensors_event_t humidity, temp;
    aht.getEvent(&humidity, &temp);
    Serial.print("Temp: ");
    Serial.print(temp.temperature);
    Serial.print(" °C, ");
    Serial.print("Luftfeuchte: ");
    Serial.print(humidity.relative_humidity);
    Serial.println(" %");
    delay(2000);
  }
}

void test_i2c() {
  delay(1000);
  Serial.println("I2C Scanner startet...");

  byte error, address;
  int nDevices = 0;

  for (address = 1; address < 127; address++) {
    Wire.beginTransmission(address);
    error = Wire.endTransmission();

    if (error == 0) {
      Serial.print("I2C Gerät gefunden bei Adresse 0x");
      Serial.println(address, HEX);
      nDevices++;
    }
  }

  if (nDevices == 0) Serial.println("Keine I2C-Geräte gefunden.");
  else Serial.println("Scan abgeschlossen.");
}
