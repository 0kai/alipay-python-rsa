Alipay-python-rsa
===========
*注：本项目使用是在Django上开发，其他框架可做参考*

## **使用方法** ##

<br>
settings.py配置
```python
ALIPAY_PARTNER = "2088...."
ALIPAY_NOTIFY_URL = "http://your.web.com/j_AlipayNotify/"
ALIPAY_SELLER_ID = ALIPAY_PARTNER
```

替换rsa密匙key，使用openssl生成
```python
rsa_private_key.pem #私匙
rsa_public_key.pem #公匙
rsa_publick_key_ali.pem #阿里云的公匙
```

获取签名
```python
alipay = Alipay(order.trade_no, subject, body, total_fee)
data["alipay_token"] = alipay.create_pay_url()
```

验证签名
```python
#参考view.py与check_notify_sign()
```

## **备注** ##
支付宝只提供php示例，python代码只能自己写。移动支付仅能使用RSA加密。
<br>
本代码使用的解决方案是，签名与在服务端实现,客户端调用api。
<br>
网上也有很多其他示例，仅供参考!
<br>
代码解释，可参照我的博客：http://0kai.net/blog/?id=39