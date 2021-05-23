import unittest
import paho.mqtt.client as mqtt


if __name__ == '__main__':
    unittest.main()

class MyTestCase(unittest.TestCase):
    def setUp(self):
        super().__init__()
        self.client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        client.subscribe("$SYS/#")

    def on_message(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

    def test_connect(self):
        self.client.connect("127.0.0.1", 1883, 60)

    def test_subscribe(self):
        pass
        # self.test_connect()
