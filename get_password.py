import base64
import hmac


def get_password(productId, deviceId, deviceSecret):
    """获取加密后的token值"""
    msg = deviceId + "&" + productId
    # key = base64.b64decode(deviceSecret)
    key = deviceSecret
    sign_b = hmac.new(key=key.encode(), msg=msg.encode(), digestmod='sha1')
    password = base64.b64encode(sign_b.digest()).decode()
    return password


# if __name__ == '__main__':
#     productId = '102019'
#     deviceId = '10013675'
#     deviceSecret = 'MDk0MjAxOWYwNjNiZmFmNWE0OWY='
#
#     # print(token(id,access_key))
#     a = get_password(productId, deviceId, deviceSecret)
#     print(a)


