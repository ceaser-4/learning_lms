import datetime

def use_coupon(coupon_expir_date):
    """判断优惠券是否过期"""
    now = datetime.datetime.now()
    if now > coupon_expir_date:
        return "优惠券已过期，无法使用"
    return "优惠券使用成功"