from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from twilio.rest import Client
from datetime import datetime
from user.models import History
from cart.models import Cart
# from sendsms import api

@csrf_exempt
def payment_done(request):
    num_items_in_cart = 0
    context = {'num_items_in_cart': num_items_in_cart}
    return render(request, 'payment/done.html', context)


@csrf_exempt
def payment_cancelled(request):
    return render(request, 'payment/cancelled.html')


def send(phone_no):
    
    # api.send_sms(body='Hellooo', from_phone='+916382677337', to=['+918124956344'])

    print(phone_no)
    phone_no = "6382677337"
    account_sid = "ACf62e531f2099e445acf3cce250fbdc6a"
    auth_token  = "86e2d4b6723e59a265aafbafa24d7bdb"
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body="Thank you for Shopping with us...",
        to="+91" + phone_no,
        from_="+12512500974",
        )
    print (message.sid)

def payment_process(request):
    # What you want the button to do.
    user = request.user
    if request.method == 'POST':
        # hist=History()
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        phone_no = request.POST.get('phone_no')
        print(address, pincode)
        user.profile.address = address + " " + pincode
        user.profile.phone_no = phone_no
        user.save()
        print(user.profile.cart_items.all())

        # hist=History()
        # hist.ordered_items.set(user.profile.cart_items.all())
        # hist.save()

        cart_names = []
        amount = 0
        for obj in user.profile.cart_items.all():
            cart_names.append(obj.item.name)
            amount = amount + (obj.item.price * obj.quantity)

        paypal_dict = {
            "business": settings.PAYPAL_RECEIVER_EMAIL,
            "amount": amount,
            "item_name": cart_names,
            "invoice": cart_names,
            "currency_code": 'INR',
            "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
            "return": request.build_absolute_uri(reverse('payment:done')),
            "cancel_return": request.build_absolute_uri(reverse('payment:cancelled')),
            "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
        }

        # send(user.profile.phone_no)
        # Create the instance.
        form = PayPalPaymentsForm(initial=paypal_dict)
        num_items_in_cart = user.profile.cart_items.all().count()
        context = {"form": form, 'num_items_in_cart':num_items_in_cart}
        return render(request, "payment/payment.html", context)

    # context = {"form": form, 'num_items_in_cart':num_items_in_cart}
    return render(request, "payment/payment.html")
