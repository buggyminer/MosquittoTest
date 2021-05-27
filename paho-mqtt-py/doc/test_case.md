# 初始化

## value

### clean_session

[True,False,123,'123']

### protocols

[mqtt.MQTTv31,mqtt.MQTTv311,mqtt.mqtt.MQTTv5,123,'123']

### transport

['tcp','websocket',123,'123']

| 用例 | clean_session | protocol      | transport | 结果    |
| ---- | ------------- | ------------- | --------- | ------- |
| 000  | True          | mqtt.MQTTv311 | tcp       | success |
| 001  | True          | mqtt.MQTTv311 | websocket | success |
| 002  | True          | mqtt.MQTTv311 | 123       | fail    |
| 003  | True          | mqtt.MQTTv311 | '123'     | fail    |

