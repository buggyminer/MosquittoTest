from logging import NOTSET
from time import sleep, time
from typing import Protocol
import unittest
from unittest.case import expectedFailure
import paho.mqtt.client as mqtt
import os


def write_file(data):
    with open('log', 'w', encoding='utf-8')as f:
        f.write(data)


def read_file():
    with open('log', 'r')as f:
        data = f.read()
    return data


def initClient():
    return mqtt.Client(client_id="client_sub", clean_session=None, userdata=None, protocol=mqtt.MQTTv311,
                       transport="tcp")


# The callback for when the client receives a CONNACK response from the server.


def on_connect(client, userdata, flags, rc):
    data = "Client:(" + str(client._client_id, encoding="utf-8") + \
           ") connected broker with result: " + mqtt.connack_string(rc)


def on_subscribe(client, userdata, mid, granted_qos):
    data = "Client:(" + str(client._client_id, encoding="utf-8") + \
           ") with Qos " + str(granted_qos[0]) + " successfully"
    write_file(data)


def get_subscribe_str(client_id, qos):
    return "Client:(" + client_id + ") with Qos " + str(qos) + " successfully"


def on_unsubscribe(client, userdata, mid):
    data = "Client:(" + str(client._client_id, encoding="utf-8") + \
           ") unsubscribed successfully"
    write_file(data)


def get_unsubscribe_str(client_id):
    return "Client:(" + client_id + ") unsubscribed successfully"


def on_message(client, userdata, msg):
    data = "Client:(" + str(client._client_id, encoding="utf-8") + \
           ") received message: " + str(msg.payload) + " from topic " + msg.topic
    write_file(data)


def get_message(client_id, msg, topic):
    return "Client:(" + client_id + ") received message: b'" + str(msg) + "' from topic " + topic


def on_disconnect(client, userdata, rc):
    if rc != 0:
        data = "Unexpected disconnection."
    data = "Client:(" + str(client._client_id,
                            encoding="utf-8") + ") disconnect successfully"


def client_init(name_str, url, port):
    client = mqtt.Client(client_id=name_str, clean_session=True,
                         userdata=None, protocol=mqtt.MQTTv311, transport="tcp")
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.on_unsubscribe = on_unsubscribe
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.connect(url, port)
    return client


def loop(client=None, topic=""):
    if client is None:
        os.system('mosquitto_pub -t ' + topic + ' -h localhost -m "' + topic + '"')
        return
    client.loop_start()
    if topic != "":
        os.system('mosquitto_pub -t ' + topic + ' -h localhost -m "' + topic + '"')
    sleep(1)
    client.loop_stop()


class TestSubUnit(unittest.TestCase):
    url = "127.0.0.1"
    port = 1883
    new_topic = "c"
    exist_topic = "test"
    common_topic = "hello"
    qos0 = 0
    qos1 = 1
    qos2 = 2
    qos_error = 3

    def test_server_no_topic(self):
        client_id = "test_server_no_topic"
        qos = self.qos0
        client = client_init(client_id, self.url, self.port)
        client.subscribe(self.new_topic, qos=qos)

        loop(client)
        self.assertEqual(read_file(), get_subscribe_str(client_id, qos))

        client.unsubscribe(self.new_topic)

        loop(client)
        self.assertEqual(read_file(), get_unsubscribe_str(client_id))

        client.disconnect()

    def test_server_exist_topic(self):
        client_id = "test_server_exist_topic"
        qos = self.qos0
        client = client_init(client_id, self.url, self.port)
        client.subscribe(self.exist_topic, qos=qos)

        loop(client)
        self.assertEqual(read_file(), get_subscribe_str(client_id, qos))

        client.unsubscribe(self.exist_topic)
        client.disconnect()

    def test_multiple_topic(self):
        client_id = "test_multiple_topic"
        qos = self.qos0
        client = client_init(client_id, self.url, self.port)
        client.subscribe([(self.exist_topic, qos), (self.common_topic, qos)])

        loop(client)
        self.assertEqual(read_file(), get_subscribe_str(client_id, qos))

        loop(client, self.exist_topic)
        self.assertEqual(read_file(), get_message(client_id, self.exist_topic, self.exist_topic))

        loop(client, self.common_topic)
        self.assertEqual(read_file(), get_message(client_id, self.common_topic, self.common_topic))

        client.unsubscribe(self.exist_topic)

        loop(client)
        self.assertEqual(read_file(), get_unsubscribe_str(client_id))

        client.unsubscribe(self.common_topic)

        loop(client)
        self.assertEqual(read_file(), get_unsubscribe_str(client_id))

        client.disconnect()

    def test_publish_without_subscribe(self):
        loop(topic=self.exist_topic)

        client_id = "test_publish_without_subscribe"
        qos = self.qos0

        client = client_init(
            "test_publish_without_subscribe", self.url, self.port)
        client.subscribe(self.exist_topic, qos=self.qos0)

        loop(client)
        self.assertEqual(read_file(), get_subscribe_str(client_id, qos))

        client.unsubscribe(self.exist_topic)
        client.disconnect()

    def test_recv_message_once(self):
        client_id = "test_recv_message_once"
        qos = self.qos0

        client = client_init(client_id, self.url, self.port)
        client.subscribe(self.common_topic, qos=qos)

        loop(client, self.common_topic)
        self.assertEqual(read_file(), get_message(
            client_id, self.common_topic, self.common_topic))

        client.unsubscribe(self.common_topic)
        client.disconnect()

    def test_recv_message_multiple(self):
        client_id = "test_recv_message_multiple"
        qos = self.qos0
        client = client_init(client_id, self.url, self.port)
        client.subscribe([(self.exist_topic, qos), (self.common_topic, qos)])

        loop(client, self.exist_topic)
        self.assertEqual(read_file(), get_message(
            client_id, self.exist_topic, self.exist_topic))

        loop(client, self.common_topic)
        self.assertEqual(read_file(), get_message(
            client_id, self.common_topic, self.common_topic))

        client.unsubscribe(self.exist_topic)
        client.unsubscribe(self.common_topic)
        client.disconnect()

    def test_recv_message_main_topic(self):
        client_id_a = "test_recv_message_main_topic_a"
        client_id_b = "test_recv_message_main_topic_b"
        qos = self.qos0
        client_a = client_init(client_id_a, self.url, self.port)
        client_b = client_init(client_id_b, self.url, self.port)

        client_a.subscribe(self.common_topic + '/a', qos)
        client_b.subscribe(self.common_topic + '/b', qos)

        client_a.loop_start()
        client_b.loop_start()

        os.system('mosquitto_pub -t ' + self.common_topic+'/a' + ' -h localhost -m "' + self.common_topic+'/a' + '"')

        sleep(1)

        self.assertEqual(read_file(), get_message(
            client_id_a, self.common_topic + '/a', self.common_topic + '/a'))

        os.system(
            'mosquitto_pub -t ' + self.common_topic + '/b' + ' -h localhost -m "' + self.common_topic + '/b' + '"')

        sleep(1)

        self.assertEqual(read_file(), get_message(
            client_id_b, self.common_topic + '/b', self.common_topic + '/b'))

        client_a.loop_stop()
        client_b.loop_stop()

        client_a.unsubscribe(self.common_topic + '/a')
        client_b.unsubscribe(self.common_topic + '/b')
        client_a.disconnect()
        client_b.disconnect()

    def test_recv_message_sub_topic(self):
        client_id = "test_recv_message_sub_topic"
        qos = self.qos0
        client = client_init(client_id, self.url, self.port)
        client.subscribe(self.common_topic, qos=qos)

        loop(client, self.common_topic)
        self.assertEqual(read_file(), get_message(
            client_id, self.common_topic, self.common_topic))

        client.unsubscribe(self.common_topic)
        client.disconnect()


if __name__ == "__main__":
    unittest.main()
