from logging import NOTSET
from typing import Protocol
import unittest
from unittest.case import expectedFailure
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Client:(" + str(client._client_id,
                           encoding="utf-8") + ") connected broker with result: " + mqtt.connack_string(rc))

def on_subscribe(client, userdata, mid, granted_qos):
    print("Client:(" + str(client._client_id, encoding="utf-8") + ") subscribe message: mid(" + str(
        mid) + ") with Qos " + str(granted_qos[0]) + " successfully ")


def on_unsubscribe(client, userdata, mid):
    print("Client:(" + str(client._client_id, encoding="utf-8") + ") unsubscribe message: mid(" + str(
        mid) + ") unsubscribed successfully")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")
    print("Client:(" + str(client._client_id, encoding="utf-8") + ") disconnect successfully")

def on_message(client, userdata, msg):
    print("Client:(" + str(client._client_id, encoding="utf-8") + ") received message: '" + str(
        msg.payload) + "' from topic '" + msg.topic)

transports=['tcp','websockets','123']

def test_client_init(transport):
    try:
        client=mqtt.Client(client_id="client_sub",clean_session=None,  userdata=None, protocol=mqtt.MQTTv311,transport=transport)
        return client
    except Exception as e:
        raise e


class TestConnectUnit(unittest.TestCase):
    def test_connect_normal(self):
        client=mqtt.Client(client_id="client_sub", clean_session=True, userdata=None, protocol=mqtt.MQTTv311,transport="tcp")
        client.on_connect=on_connect
        client.on_disconnect=on_disconnect
        res=1
        try:
            res=client.connect("127.0.0.1", 1883, 60)
        except Exception as e:
            self.assertFalse(e)
        self.assertEqual(res,0)
        res=1

        client.loop_start()
        client.loop_stop()
        
        try:
            res=client.disconnect()
        except Exception as e:
            self.assertFalse(e)
        self.assertEqual(res,0)

    def test_connect_host_eclipse_org(self):
        client=mqtt.Client(client_id="client_sub", clean_session=True, userdata=None, protocol=mqtt.MQTTv311,transport="tcp")
        client.on_connect=on_connect
        client.on_disconnect=on_disconnect
        res=1
        try:
            res=client.connect("eclipse.org", 1883, 60)
        except Exception as e:
            self.assertFalse(e)
        self.assertEqual(res,0)

        client.loop_start()
        client.loop_stop()

        client.disconnect()

    def test_connect_port_1885(self):
        client=mqtt.Client(client_id="client_sub", clean_session=True, userdata=None, protocol=mqtt.MQTTv311,transport="tcp")
        client.on_connect=on_connect
        client.on_disconnect=on_disconnect
        res=1
        try:
            res=client.connect("127.0.0.1", 1885, 60)
        except Exception as e:
            self.assertEqual(str(e),"[WinError 10061] 由于目标计算机积极拒绝，无法连接。")

        client.loop_start()
        client.loop_stop()

        self.assertEqual(res,0)
        client.disconnect()
    
    def test_connect_host_str_123(self):
        client=mqtt.Client(client_id="client_sub", clean_session=True, userdata=None, protocol=mqtt.MQTTv311,transport="tcp")
        client.on_connect=on_connect
        client.on_disconnect=on_disconnect
        res=0
        try:
            res=client.connect("123", 1885, 60)
        except Exception as e:
            self.assertEqual(str(e),"[Errno 11001] getaddrinfo failed")
        self.assertEqual(res,0)
        client.disconnect()


    def test_init_normal(self):
        try:
            client=mqtt.Client(client_id="client_sub",clean_session=None,  userdata=None, protocol=mqtt.MQTTv311,transport='tcp')
        except Exception as e:
            self.assertFalse(e)
        
    def test_init_transport_websockets(self):
        try:
            client=mqtt.Client(client_id="client_sub",clean_session=None,  userdata=None, protocol=mqtt.MQTTv311,transport='websockets')
        except Exception as e:
            self.assertFalse(e)

    def test_init_protocol_mqttv5(self):
        try:
            client=mqtt.Client(client_id="client_sub",clean_session=None,  userdata=None, protocol=mqtt.MQTTv5,transport='tcp')
        except Exception as e:
            self.assertFalse(e)
    

if __name__=="__main__":
    unittest.main()