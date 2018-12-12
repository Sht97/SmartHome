//SENSOR MOVIMIENTO

#include <ESP8266WiFi.h>
#include <PubSubClient.h> //This library provides a client for doing simple publish/subscribe messaging with a server that supports MQTT
//https://pubsubclient.knolleary.net/api.html --> documentation


#define BUILTIN_LED 2
#define PIR_MOTION_SENSOR D5

// Update these with values suitable for your network.
const char* ssid = "Nett1"; //"DontKillTux";
const char* password ="zvwq1218"; //"mariaisabel";
const char* mqtt_server = "192.168.43.225";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;

// Variable state represents home state-> 0 normal  - 1 lookout
char state = 0;

void setup() {
  pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  pinMode(PIR_MOTION_SENSOR, INPUT);
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}
//If the client is used to subscribe to topics, a callback function must be provided in the constructor. This function is called when new messages arrive at the client.

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  //Change sensor state
  if ((char)payload[5]=='1')
    state = 1;
  else
    state = 0;   

}//end void callback

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("casa/pir", "Enviando el primer mensaje");
      // ... and resubscribe
      client.subscribe("casa/pir_conf");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  long now = millis(); //devuelve el número de milisegundos desde que Arduino se ha reseteado
  if (now - lastMsg > 500) {
    lastMsg = now;
    Serial.print(state);
    if (state){
      if(digitalRead(PIR_MOTION_SENSOR)){//if it detects the moving people?
        //Serial.println("Hi,people is coming");
        snprintf (msg, 50, "alarm");
        Serial.print("Publish message: ");
        Serial.println(msg);
        // sending alarm to gateway!!!
        client.publish("casa/pir", msg);
      } else{
        snprintf (msg, 50, "0");
        Serial.print("Publish message: ");
        Serial.println(msg);
        //client.publish("casa/pir", msg);
        //Serial.println("Watching");
      }
    }
  }
}
