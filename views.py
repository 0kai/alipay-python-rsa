# -*- coding: utf-8 -*-

@require_POST
@csrf_exempt
def j_AlipayNotify(request):
    while True:
        verify_status = check_notify_sign(request)
        if verify_status:
            trade_no = request.POST["out_trade_no"]
            trade_status = request.POST["trade_status"]
            #TRADE_FINISHED can't refund
            if trade_status in ["TRADE_SUCCESS", "TRADE_FINISHED"]:
                pass
            return HttpResponse("success")
        break

    print "verify_status False"
    return HttpResponse("success")


