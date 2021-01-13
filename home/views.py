from django.shortcuts import render
from cart.models import Item, Cart

# Create your views here.
def landing(request):
    all_items = Item.objects.all()
    if not request.user.is_authenticated:
        print('No one inside the app')
        num_items_in_cart = 0
        context = {'all_items': all_items , 'num_items_in_cart': num_items_in_cart, 'home_active':'active'}
        return render(request, 'home/landingpage1.html', context)
    else:
        user = request.user
        num_items_in_cart = user.profile.cart_items.all().count()
        context = {'all_items': all_items , 'num_items_in_cart': num_items_in_cart, 'home_active':'active'}
        return render(request, 'home/landingpage1.html', context)


def about(request):
    return render(request, 'home/about.html', {'about_active':'active'})

def contact(request):
    return render(request, 'home/contact.html', {'contact_active':'active'})
