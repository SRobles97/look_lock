import paho.mqtt.client as mqtt
from config import Config

mqtt_client = mqtt.Client()


# Configurar el cliente MQTT
def configure_mqtt(app):
    mqtt_client.username_pw_set(Config.MQTT_TOKEN)
    mqtt_client.connect(Config.MQTT_SERVER, Config.MQTT_PORT, 60)


def publish_to_mqtt(topic, message):
    mqtt_client.publish(topic, message)
