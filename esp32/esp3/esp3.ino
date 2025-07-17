#include <WiFi.h>
#include <PubSubClient.h>

#define ESP_NAME "esp3"

WiFiClient espClient;
PubSubClient mqttClient(espClient);

const int trigger_ultrasonic = 5;
const int echo_ultrasonic = 18;

const char* ssid = "FRITZ!Box 6490 FR4";
const char* password = "EG28kc56pu18vz";

const char* mqtt_server = "192.168.178.69";
const int mqtt_port = 1883;
const char* mqtt_user = "";
const char* mqtt_password = "";
const char* topic_distance = ESP_NAME "/sensor/distance";


void setup() {
  Serial.begin(115200);
  setup_wifi();
  mqttClient.setServer(mqtt_server, mqtt_port);
  pinMode(trigger_ultrasonic, OUTPUT);
  pinMode(echo_ultrasonic, INPUT);
  delay(100);
}


void setup_wifi() {
  delay(10);
  Serial.print("Connect with WLAN ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WLAN connected, IP: ");
  Serial.println(WiFi.localIP());
}


void reconnect_mqtt() {
  while (!mqttClient.connected()) {
    Serial.print("Connect MQTT…");
    if (mqttClient.connect("ESP32Client", mqtt_user, mqtt_password)) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" – new attempt in 5 s");
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
  delay(200);

  if (!mqttClient.connected()) {
    reconnect_mqtt();
  }
  mqttClient.loop();

  char payload_dist[64];
  snprintf(payload_dist, sizeof(payload_dist),
           "{\"distance\":%u}",
           distance);

  mqttClient.publish(topic_distance, payload_dist);
  Serial.print("Publish: ");
  Serial.println(payload_dist);

  delay(5000);
}