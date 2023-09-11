# context processors are simple functions defined to populate templates with a context
from account.models import Cart


def cart_count(request):
    count=Cart.objects.filter(user=request.user.id,status="cart").count()
    return{'count': count}