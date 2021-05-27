import paho.mqtt.client as mqtt
import time


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Client:(" + str(client._client_id,
                           encoding="utf-8") + ") connected broker with result: " + mqtt.connack_string(rc))
    # client.subscribe("mytopic")


def on_publish(client, userdata, mid):
    print("Client:(" + str(client._client_id, encoding="utf-8") + ") published topic with message id(" + str(
        mid) + ")")



def on_subscribe(client, userdata, mid, granted_qos):
    print("Client:(" + str(client._client_id, encoding="utf-8") + ") subscribe message: mid(" + str(
        mid) + ") with Qos " + str(granted_qos[0]) + " successfully ")


def on_unsubscribe(client, userdata, mid):
    print("Client:(" + str(client._client_id, encoding="utf-8") + ") unsubscribe message: mid(" + str(
        mid) + ") unsubscribed successfully")


def on_message(client, userdata, msg):
    print("Client:(" + str(client._client_id, encoding="utf-8") + ") received message: '" + str(
        msg.payload) + "' from topic '" + msg.topic)


def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnection.")
    print("Client:(" + str(client._client_id, encoding="utf-8") + ") disconnect successfully")

def test_init():
    client_pub = mqtt.Client(client_id="client_pub", clean_session=True, userdata="HI", protocol=mqtt.MQTTv311,
                             transport=123)

def set_up_client():
    client_pub = mqtt.Client(client_id="client_pub", clean_session=True, userdata="HI", protocol=mqtt.MQTTv311,
                             transport="tcp")
    client_sub = mqtt.Client(client_id="client_sub", clean_session=True, userdata=None, protocol=mqtt.MQTTv311,
                             transport="tcp")

    client_pub.on_connect = on_connect
    client_pub.on_message = on_message
    client_pub.on_publish = on_publish
    client_pub.on_subscribe = on_subscribe
    client_pub.on_unsubscribe = on_unsubscribe
    client_pub.on_disconnect = on_disconnect

    client_sub.on_connect = on_connect
    client_sub.on_message = on_message
    client_sub.on_publish = on_publish
    client_sub.on_subscribe = on_subscribe
    client_sub.on_unsubscribe = on_unsubscribe
    client_sub.on_disconnect = on_disconnect

    # connection
    client_pub.connect("127.0.0.1", 1883, 60)
    client_sub.connect("127.0.0.1", 1883, 60)

    time.sleep(1)

    # publish
    client_pub.publish(topic="mytopic1", payload="hello, there", qos=0, retain=True)  # retain topic
    # client_pub.publish(topic="mytopic11", payload="This is topic11", qos=1, retain=True)
    # client_pub.publish(topic="mytopic12", payload="This is topic12", qos=2, retain=True)
    # client_pub.publish(topic="mytopic13", payload="This is topic13", qos=3, retain=True)   # qos错误示例

    client_sub.publish(topic="mytopic2", payload="This is topic2", qos=0, retain=False)  # not retain topic

    # subscribe
    # client_pub.subscribe("mytopic1", 0)  # 自我订阅
    client_sub.subscribe("Hello", 0)  # 其他订阅者客户端订阅
    # client_sub.subscribe("mytopic1", 1)  # Qos level wrong
    #client_sub.subscribe([("mytopic1", 0), ("mytopic2", 0)])    # 一箭多星

    # unsubscribe
    client_pub.unsubscribe("mytopic1")
    client_sub.unsubscribe("mytopic1")

    # loop
    client_pub.loop_start()
    client_sub.loop_forever()
    # disconnetct
    # client_pub.disconnect()
    # client_sub.disconnect()

if __name__ == '__main__':
    # set_up_client()
    test_init()
