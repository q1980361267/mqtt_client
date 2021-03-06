import paho.mqtt.client as mqtt
import get_password
import json
import time
import struct


# 获得参数
with open('test-config.json', 'r') as f:
    f_json = json.load(f)
    productId = f_json.get('productId')
    deviceId = f_json.get('deviceId')
    deviceSecret = f_json.get('deviceSecret')
    address = f_json.get('url')
    port = f_json.get('port')

# 连接成功后就回调此方法
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


    # client.subscribe("$SYS/#")
    # client.subscribe("standard/cmd/pid/101530/devkey/10114695")
    # _send = {
    #     'someDouble': 12.1234,
    #     'someString': 'abcd'
    # }
    # _send_all = b'\03' + struct.pack()
    # client.publish(topic='standard/data/pid/102052/devkey/10013705', payload=json.dumps(_send))


# 收到服务端的publish消息时回调此方法
def on_message(client, userdata, msg):
    # print(msg.topic + " " + str(msg.payload))

    print('收到报文：% r ' % (msg.payload))
    _recv = msg.payload.decode()
    _recv_dict = json.loads(_recv)
    _functionType = _recv_dict['functionType']
    # print(_functionType)
    _uuid = _recv_dict['uuid']
    _identifier = _recv_dict['identifier']
    _identifierValue = _recv_dict['identifierValue']
    if _functionType == 'propertySet':
        _send = json.dumps({'uuid': _uuid, 'code': 0, 'msg': '', 'identifier': _identifier, 'value': 'null'})
        client.publish(topic='standard/resp/pid/{}/devkey/{}'.format(productId, deviceId), payload=_send.encode())
        print('回应报文：', _send)
    elif _functionType == 'propertyGet':
        if _identifier == 'someDouble':
            _send = json.dumps({'identifier': _identifier, 'value': 12.123, 'code': 0, 'msg': 'success', 'uuid': _uuid})
            client.publish(topic='standard/resp/pid/{}/devkey/{}'.format(productId, deviceId), payload=_send.encode())
            print('回应报文：', _send)
        elif _identifier == 'someInteger':
            _send = json.dumps({'identifier': _identifier, 'value': 999, 'code': 0, 'msg': 'success', 'uuid': _uuid})
            client.publish(topic='standard/resp/pid/{}/devkey/{}'.format(productId, deviceId), payload=_send.encode())
            print('回应报文：', _send)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
# client.loop_forever()


if __name__ == '__main__':
    my_password = get_password.get_password(productId, deviceId, deviceSecret)
    print('my_paaword: ', my_password)
    client = mqtt.Client(client_id=deviceId)  # 创建client实例
    client.username_pw_set(username=productId, password=my_password)  # 设置client的接入信息-用户名，密码

    client.on_connect = on_connect  # 回调信息
    client.on_message = on_message  # 回调收到的message

    client.connect(address, port)  # 客户端连接报文
    # client.subscribe(topic='standard/cmd/pid/102052/devkey/10013705')
    client.loop_start()
    time.sleep(5)
    while True:
        # _json = json.dumps({'someDouble': 999.999})
        # _json = json.dumps({'someDouble': 42.32})
        # _len = len(_json)
        # _upload = b'\x03' + struct.pack('!H', _len) + _json.encode()
        # # print(_upload)
        # client.publish(topic="standard/data/pid/{}/devkey/{}".format(productId, deviceId), payload=_upload)
        # time.sleep(10)
        # _json = json.dumps({'someString': 'abcd'})
        # _len = len(_json)
        # _upload = b'\x03' + struct.pack('!H', _len) + _json.encode()
        # # print(_upload)
        # client.publish(topic="standard/data/pid/{}/devkey/{}".format(productId, deviceId), payload=_upload)
        # print('上报信息： someDouble : %r' % (_upload))
        #         # _json = json.dumps({'someDouble': 82.32})
        #         # _len = len(_json)
        #         # _upload = b'\x03' + struct.pack('!H', _len) + _json.encode()
        #         # # print(_upload)
        #         # client.publish(topic="standard/data/pid/{}/devkey/{}".format(productId, deviceId), payload=_upload)
        #         # time.sleep(10)
        # print('上报信息： someDouble : %r' % (_upload))
        _json = json.dumps({'someInteger': 55, 'someString': 'abcd'})
        _len = len(_json)
        _upload = b'\x03' + struct.pack('!H', _len) + _json.encode()
        # print(_upload)
        client.publish(topic="standard/data/pid/{}/devkey/{}".format(productId, deviceId), payload=_upload)
        # time.sleep(10)
        print('上报信息： value : %r' % (_upload))
        # _json = json.dumps({'someString': 'abcd'})
        # _len = len(_json)
        # _upload = b'\x03' + struct.pack('!H', _len) + _json.encode()
        # # print(_upload)
        # client.publish(topic="standard/data/pid/{}/devkey/{}".format(productId, deviceId), payload=_upload)
        time.sleep(10)
        # print('上报信息： someString : %r' % (_upload))