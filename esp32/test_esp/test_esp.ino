#include <WiFi.h>
#include <Wire.h>
#include <PubSubClient.h>
#include <Adafruit_AHTX0.h>
#include <SparkFun_ENS160.h>

Adafruit_AHTX0 aht;
SparkFun_ENS160 myENS;

const int trigPin = 5;
const int echoPin = 18;

const char* ssid     = "FRITZ!Box 6490 FR4";
const char* password = "EG28kc56pu18vz";

const char* mqtt_server = "192.168.178.69";
const int   mqtt_port   = 1883;
const char* mqtt_user   = "";  // "" falls nicht benötigt
const char* mqtt_pass   = "";  // "" falls nicht benötigt

const char* topic_co2  = "sensor/raum/co2";
const char* topic_tvoc = "sensor/raum/tvoc";

WiFiClient espClient;
PubSubClient mqttClient(espClient);


void setup() {
  Wire.begin();

	Serial.begin(115200);

  // WLAN & MQTT
  setup_wifi();
  mqttClient.setServer(mqtt_server, mqtt_port);

	if( !myENS.begin() )
	{
		Serial.println("Could not communicate with the ENS160, check wiring.");
		while(1);
	}

  Serial.println("Example 1 Basic Example.");

	if( myENS.setOperatingMode(SFE_ENS160_RESET) )
		Serial.println("Ready.");

	delay(100);
	myENS.setOperatingMode(SFE_ENS160_STANDARD);

	int ensStatus = myENS.getFlags();
	Serial.print("Gas Sensor Status Flag (0 - Standard, 1 - Warm up, 2 - Initial Start Up): ");
	Serial.println(ensStatus);
	
  /*
  Serial.begin(9600);
  Wire.begin(21, 22);

  pinMode(2, OUTPUT);
  digitalWrite(2, LOW);

  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);

  if (!aht.begin()) {
    Serial.println("AHT21 nicht gefunden!");
    while (1) delay(10);
  }
  Serial.println("AHT21 bereit.");

  // ENS160 initialisieren
  if (!ens160.begin(ENS160_I2CADDR_1)) {
    Serial.println("ENS160 nicht gefunden!");
    while (1) delay(10);
  }
  ens160.setMode(ENS160_OPMODE_STD);
  Serial.println("ENS160 bereit.");
  */
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
  // Solange nicht verbunden, alle 5 Sekunden neu versuchen
  while (!mqttClient.connected()) {
    Serial.print("Verbinde MQTT…");
    if (mqttClient.connect("ESP32Client", mqtt_user, mqtt_pass)) {
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
  /*
  if( myENS.checkDataStatus() )
	{
		Serial.print("Air Quality Index (1-5) : ");
		Serial.println(myENS.getAQI());

		Serial.print("Total Volatile Organic Compounds: ");
		Serial.print(myENS.getTVOC());
		Serial.println("ppb");

		Serial.print("CO2 concentration: ");
    
		Serial.print(myENS.getECO2());
		Serial.println("ppm");

	  Serial.print("Gas Sensor Status Flag (0 - Standard, 1 - Warm up, 2 - Initial Start Up): ");
    Serial.println(myENS.getFlags());

		Serial.println();
	}

	delay(200);
  */

  if (!mqttClient.connected()) {
    reconnect_mqtt();
  }
  mqttClient.loop();
  
  int eco2 = myENS.getECO2();
  Serial.print("CO2: " + eco2);

  char payload[64];
  snprintf(payload, sizeof(payload),
           "{\"eCO2\":%u}",
           eco2);
  Serial.println(payload);

  // Publish
  mqttClient.publish(esp1/sensor/co2,  payload);  // hier sende ich beides im gleichen Topic

  Serial.print("Publish: ");
  Serial.println(payload);

  delay(5000);

  /*
  // Temperatur und Luftfeuchtigkeit lesen (für ENS160-Kompensation nützlich!)
  sensors_event_t humidity, temp;
  aht.getEvent(&humidity, &temp);

  Serial.print("Temp: "); Serial.print(temp.temperature); Serial.print(" °C, ");
  Serial.print("Luftfeuchte: "); Serial.print(humidity.relative_humidity); Serial.println(" %");

  // ENS160-Daten aktualisieren
  //ens160.setEnv(temp.temperature, humidity.relative_humidity);

  // ENS160-Werte auslesen
  //Serial.print("eCO2: "); Serial.print(ens160.geteCO2()); Serial.print(" ppm, ");
  //Serial.print("TVOC: "); Serial.print(ens160.getTVOC()); Serial.println(" ppb");

  delay(2000); // 2 Sekunden warten
  */
  
}

void test_ventilation(){
  delay(4000);
  digitalWrite(2, HIGH);
  delay(4000);
  digitalWrite(2, LOW);
}

void test_ultrasonic(){
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  
  long duration = pulseIn(echoPin, HIGH);
  long distance = duration / 58.2;
  String disp = String(distance);

  Serial.print("Distance: ");
  Serial.print(disp);
  Serial.println(" cm");
  delay(1000);
}

void test_temp_humidity(){
  if (!aht.begin()) {
    Serial.println("AHT21 nicht gefunden!");
    while (1) delay(10);
  }
  Serial.println("AHT21 bereit.");

  while(true){
    sensors_event_t humidity, temp;
    aht.getEvent(&humidity, &temp);
    Serial.print("Temp: "); Serial.print(temp.temperature); Serial.print(" °C, ");
    Serial.print("Luftfeuchte: "); Serial.print(humidity.relative_humidity); Serial.println(" %");
    delay(2000);
  }
}

void test_i2c(){
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

void test_mqtt(){

}
