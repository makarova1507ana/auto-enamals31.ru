from carts.models import Cart


def get_user_carts(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).order_by("created_timestamp")

    if not request.session.session_key:
        request.session.create()
    return Cart.objects.filter(session_key=request.session.session_key).order_by("created_timestamp")


def get_user_carts_order(request):
    if request.user.is_authenticated:
        return Cart.objects.filter(user=request.user).filter(is_buy=True).order_by("created_timestamp")
    if not request.session.session_key:
        request.session.create()
    return Cart.objects.filter(session_key=request.session.session_key).filter(is_buy=True).order_by("created_timestamp")
