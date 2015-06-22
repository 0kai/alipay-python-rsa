# -*- coding: utf-8 -*-
import rsa
import base64
import os
from urllib import quote

from django.conf import settings

_private_rsa_key = None
_public_rsa_key_ali = None

#def module_init():
path = os.path.dirname(__file__)
priv_path = os.path.abspath(os.path.join(path, "rsa_private_key.pem"))
pub_path_ali = os.path.abspath(os.path.join(path, "rsa_public_key_ali.pem"))

pem = open(priv_path, "r").read()
_private_rsa_key = rsa.PrivateKey.load_pkcs1(pem)

pem = open(pub_path_ali, "r").read()
_public_rsa_key_ali = rsa.PublicKey.load_pkcs1_openssl_pem(pem)

#init when run
#module_init()

class Alipay(object):
    ## default value
    service = "mobile.securitypay.pay"# api name, default value
    _input_charset = "utf-8"
    sign_type = "RSA"# only support RSA
    payment_type = 1

    # get value from settings.py
    # partner id, len=16 (2088...)
    partner = getattr(settings, "ALIPAY_PARTNER", None)
    notify_url = getattr(settings, "ALIPAY_NOTIFY_URL", None)
    # the account id of seller (email or phone or partner id)
    seller_id = getattr(settings, "ALIPAY_SELLER_ID", None)

    print partner, notify_url, seller_id

    def __init__(self, out_trade_no, subject, body, total_fee):
        # unique value, max=64
        self.out_trade_no = out_trade_no
        # order title/ trade keys, max=128
        self.subject = subject
        # the detail info of order, max=512
        self.body = body
        # the total pay fee
        self.total_fee = total_fee

    def init_optional_value(self, it_b_pay):
        # order timeout, m:minute, h:hour, d:day ("30m")
        self.it_b_pay = it_b_pay

    def _build_sign_url(self):
        url = ""
        # static value
        url = url + 'service="%s"' % self.service
        url = url + '&_input_charset="%s"' % self._input_charset
        url = url + '&payment_type="%d"' % self.payment_type
        url = url + '&partner="%s"' % self.partner
        url = url + '&notify_url="%s"' % self.notify_url
        url = url + '&seller_id="%s"' % self.seller_id
        # init value
        url = url + '&out_trade_no="%s"' % self.out_trade_no
        url = url + '&subject="%s"' % self.subject
        url = url + '&body="%s"' % self.body
        url = url + '&total_fee="%0.2f"' % self.total_fee
        # optional value
        if hasattr(self, "it_b_pay"):
            url = url + '&it_b_pay="%s"' % self.it_b_pay

        return url

    def _create_sign(self, content):
        content = content.encode(self._input_charset)
        sign = rsa.sign(content, _private_rsa_key, "SHA-1")
        sign = base64.encodestring(sign).replace("\n", "")
        return 'sign="%s"&sign_type="%s"' % (quote(sign), self.sign_type)

    def create_pay_url(self):
        content = self._build_sign_url()
        sign_url = self._create_sign(content)
        return "%s&%s" % (content, sign_url)

def notify_sign_value(request, content, key):
    if key in request.POST:
        value = request.POST[key]
        print "key: ", key, "value: ", value
        return "&%s=%s"%(key, value)
    else:
        return ""

def check_notify_sign(request):
    """
    按照字母顺序排序，然后使用阿里云的公匙验证。
    """
    content = ""
    post_list = sorted(request.POST.iteritems(), key=lambda d:d[0], reverse=False)
    for key_value in post_list:
        if key_value[0] not in ["sign", "sign_type"]:
            content = "%s&%s=%s"%(content, key_value[0], key_value[1])

    #remove the first &
    content = content[1:]
    content = content.encode("utf-8")
    try:
        sign = request.POST["sign"]
        sign = base64.decodestring(sign)
        rsa.verify(content, sign, _public_rsa_key_ali)
        return True
    except Exception,e:
        print "check_notify_sign error", e
        return False
