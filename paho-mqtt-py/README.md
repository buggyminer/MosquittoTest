## paho-mqtt 安装

### 创建虚拟环境(可选)

```shell
virtualenv paho-mqtt
source paho-mqtt/bin/activate
```

### 安装paho-mqtt

```shell
pip install paho-mqtt
```

或

```shell
git clone https://github.com/eclipse/paho.mqtt.python
cd paho.mqtt.python
python setup.py install
```

### 测试(可选)

如果需要所有的测试，请在paho.mqtt.python文件夹中添加paho.mqtt.testing库
```shell
git clone https://github.com/eclipse/paho.mqtt.testing.git
```