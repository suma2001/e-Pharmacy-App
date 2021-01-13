from .models import Item, Cart
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib import messages
from googlevoice import Voice
import requests
from math import radians, sin, asin, sqrt, cos
import urllib.parse
from django.http.response import JsonResponse
from django.views.generic.base import View, TemplateView
from django.views.decorators.csrf import csrf_exempt
# from PIL import Image, ImageFilter
# from tesserocr import PyTessBaseAPI
from user.models import Shop
# from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
# from django.core.urlresolvers import reverse
import geocoder
from .models import Document
from .forms import DocumentForm
import json

try:
        import Image
except ImportError:
        from PIL import Image
import pytesseract


# class OcrFormView(TemplateView):
#     template_name = 'cart/ocr_form.html'
# ocr_form_view = OcrFormView.as_view()


# class OcrView(View):
#     def post(self, request, *args, **kwargs):
#         with PyTessBaseAPI() as api:
#             with Image.open(request.FILES['image']) as image:
#                 sharpened_image = image.filter(ImageFilter.SHARPEN)
#                 api.SetImage(sharpened_image)
#                 utf8_text = api.GetUTF8Text()

#         return JsonResponse({'utf8_text': utf8_text})
# ocr_view = csrf_exempt(OcrView.as_view())

from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from .models import Document
from .forms import DocumentForm

# global i
# i=0
def home1(request):
    documents = Document.objects.all()
    return render(request, 'cart/home.html', { 'documents': documents })


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'cart/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'cart/simple_upload.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cart:home1')
    else:
        form = DocumentForm()
    return render(request, 'cart/model_form_upload.html', {
        'form': form
    })


def ocr(request):
    global i
    if request.method=="POST":
        i=4
        docs = Document.objects.all()
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            i += 1 
            print(i)
            # import ipdb;ipdb.set_trace()
            d = Document.objects.get(id=i)
            
            #print d.docfile
            k=pytesseract.image_to_string(Image.open(d.docfile))
            print(k)
            listofwords=k.split(' ')
            total_list = []
            for item in Item.objects.all():
                total_list.append(item.name.lower())

            flag=0
            for word in listofwords:
                if word in total_list:
                    flag=1
                    print("Add item to cart")

            if flag==0:
                print("Oops!! No such item exists")

            handle = open('data.txt', 'a+')
            handle.write(k)
            handle.close()

            txt_file = r"data.txt"

            # Redirect to the document list after POST
            return redirect('cart:ocr')
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    return render(request, 'cart/list.html',{'documents': documents, 'form': form})


def home(request):
    all_items = Item.objects.all()
    if not request.user.is_authenticated:
        print('No one inside the app')
        num_items_in_cart = 0
        return render(request, 'cart/index.html', {'all_items': all_items , 'num_items_in_cart': num_items_in_cart})
    else:
        user = request.user
        num_items_in_cart = user.profile.cart_items.all().count()
        return render(request, 'cart/index.html', {'all_items': all_items , 'num_items_in_cart': num_items_in_cart})

def itemlist(request):
    all_items = Item.objects.all()
    user = request.user
    if not user.is_authenticated:
        num_items_in_cart=0
        return render(request, 'cart/itemlist.html', {'all_items': all_items , 'num_items_in_cart': num_items_in_cart})
    num_items_in_cart=user.profile.cart_items.all().count()
    return render(request, 'cart/itemlist.html', {'all_items': all_items , 'num_items_in_cart': num_items_in_cart})

def shoppingcart(request):
    user = request.user
    print("Hey Dude")
    if not user.is_authenticated:
        num_items_in_cart=0
        return render(request, 'cart/shopping-cart.html', {'num_items_in_cart': num_items_in_cart})
    all_user_items = user.profile.cart_items.all()
    print(all_user_items)
    tot_cost = 0
    for i in all_user_items:
        print(i.quantity)
        tot_cost += i.itemtotal
    print(tot_cost)
    num_items_in_cart=user.profile.cart_items.all().count()
    return render(request, 'cart/shopping-cart.html', {'num_items_in_cart': num_items_in_cart, 'all_user_items': all_user_items, 'tot_cost': tot_cost})



@csrf_exempt
def searchnearbyshops(request):
    print("HELO RE")
     
    print(request.method)
    all_shops = (Shop.objects.order_by('distance'))
    shops = all_shops
    num_shops = all_shops.count()
    ans=[]
    for shop in all_shops:
        dic={}
        dic['name'] = shop.shop_name
        dic['lat'] = shop.latitude
        dic['lng'] = shop.longitude
        ans.append(dic)
    list = ans
    json_list = json.dumps(list)
    lat1=0.0
    lon1=0.0
    if 1==1:
        lat1 = 11.5450
        lon1 = 79.5212
        # print(request.POST['lat'],request.POST['lon'])
        lati = float(lat1)
        loni = float(lon1)
        print(lati, loni)

        for shop in Shop.objects.all():
            lat2 = shop.latitude
            lon2 = shop.longitude
            lon1, lat1, lon2, lat2 = map(radians, [loni, lati, lon2, lat2])
            # haversine formula 
            dlon = lon2 - lon1 
            dlat = lat2 - lat1 
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * asin(sqrt(a)) 
            r = 6371 # Radius of earth in kilometers. Use 3956 for miles
            ans = c*r
            print(ans)
            shop.distance = ans
            shop.save()

        all_shops =  (Shop.objects.order_by('distance'))
        ans=[]
        for shop in all_shops:
            dic={}
            dic['name'] = shop.shop_name
            dic['lat'] = shop.latitude
            dic['lng'] = shop.longitude
            ans.append(dic)
        print("SHops are: ")
        print(all_shops)

        # json_list = simplejson.dumps(list)
        
        list = ans
        json_list = json.dumps(list)
        # render_to_response(template_name, {'json_list': json_list})
        print(lati, loni)
        return render(request, 'cart/shop_locator.html', {'all_shops': json_list, 'shops': shops, 'num_shops': num_shops, 'lati': lati, 'loni': loni, 'shop_active': 'active'})
    # return redirect("user:profile")
    return render(request, 'cart/shop_locator.html', {'all_shops': json_list, 'shops': shops, 'num_shops': num_shops, 'lati': lat1, 'loni': lon1, 'shop_active':'active'})

def maps(request):
    return render(request, 'cart/map.html')

def search(request):
    print(request.method)
    if request.method == 'POST':
        itemname = request.POST.get('inp')
        print(itemname)
        item_obj = Item.objects.filter(name=itemname)
        num_items_in_cart = item_obj.count()
        if num_items_in_cart==0:
            messages.warning(request, "No such item!!")
            return redirect('cart:searchpage')
        context = {'all_items': item_obj , 'num_items_in_cart': num_items_in_cart}
        return render(request, 'cart/product_card.html', context)


def searchpage(request):
    all_items = Item.objects.all()
    user = request.user
    paginator = Paginator(all_items, 6)
    page = request.GET.get('page')
    all_items = paginator.get_page(page)
    # paginate_by = 2
    if not user.is_authenticated:
        num_items_in_cart=0
    else:
        num_items_in_cart = user.profile.cart_items.all().count()
    context = {'all_items': all_items , 'num_items_in_cart': num_items_in_cart, 'order_active': 'active'}
    return render(request, 'cart/product_card.html', context)

def sort_alphabet(request):
    lis = Item.objects.order_by('name')
    print(lis)
    user = request.user
    paginator = Paginator(lis, 3)
    page = request.GET.get('page')
    lis = paginator.get_page(page)
    # paginate_by = 2
    if not user.is_authenticated:
        num_items_in_cart=0
    else:
        num_items_in_cart = user.profile.cart_items.all().count()
    context = {'all_items': lis , 'num_items_in_cart': num_items_in_cart, 'order_active': 'active', }
    return render(request, 'cart/product_card.html', context)

def sort_price(request):
    lis = Item.objects.order_by('price')
    print(lis)
    user = request.user
    paginator = Paginator(lis, 3)
    page = request.GET.get('page')
    lis = paginator.get_page(page)
    # paginate_by = 2
    if not user.is_authenticated:
        num_items_in_cart=0
    else:
        num_items_in_cart = user.profile.cart_items.all().count()
    context = {'all_items': lis , 'num_items_in_cart': num_items_in_cart, 'order_active': 'active', }
    return render(request, 'cart/product_card.html', context)

def sort_desc_price(request):
    lis = Item.objects.order_by('-price')
    print(lis)
    user = request.user
    paginator = Paginator(lis, 3)
    page = request.GET.get('page')
    lis = paginator.get_page(page)
    # paginate_by = 2
    if not user.is_authenticated:
        num_items_in_cart=0
    else:
        num_items_in_cart = user.profile.cart_items.all().count()
    context = {'all_items': lis , 'num_items_in_cart': num_items_in_cart, 'order_active': 'active', }
    return render(request, 'cart/product_card.html', context)


def sort_desc_alphabet(request):
    lis = Item.objects.order_by('-name')
    print(lis)
    user = request.user
    paginator = Paginator(lis, 3)
    page = request.GET.get('page')
    lis = paginator.get_page(page)
    # paginate_by = 2
    if not user.is_authenticated:
        num_items_in_cart=0
    else:
        num_items_in_cart = user.profile.cart_items.all().count()
    context = {'all_items': lis , 'num_items_in_cart': num_items_in_cart, 'order_active': 'active', }
    return render(request, 'cart/product_card.html', context)

def product_page(request, Id):
    item = get_object_or_404(Item, id=Id)
    user = request.user
    num_items_in_cart = user.profile.cart_items.all().count()
    return render(request, 'cart/product_page.html', {'num_items_in_cart':num_items_in_cart, 'item':item})

def add_to_cart(request, Item_id):
    item = get_object_or_404(Item, id=Item_id)
    check=0
    user = request.user
    if not user.is_authenticated:
        return redirect('user:register')
    for obj in user.profile.cart_items.all():
        if obj.item.id == item.id:
            obj.quantity=obj.quantity+1
            obj.itemtotal=(item.price)*float(obj.quantity)
            obj.save()
            check=1
    if check==0:
        temp=Cart()
        temp.item=item
        temp.quantity=1
        temp.itemtotal=(item.price)*float(temp.quantity)
        temp.save()
        user.save()
        user.profile.cart_items.add(temp)
        user.save()
        print(user.profile.cart_items.all())
    all_user_items = user.profile.cart_items.all()
    all_items = Item.objects.all()
    num_items_in_cart = user.profile.cart_items.all().count()
    tot_cost=0
    for i in all_user_items:
        print(i.quantity)
        tot_cost += i.itemtotal
    print(tot_cost)
    # return render(request, 'cart/product_card.html', {'all_items': all_items , 'num_items_in_cart': num_items_in_cart})
    return render(request, 'cart/shopping-cart.html', {'all_user_items': all_user_items ,'user':user,'num_items_in_cart':num_items_in_cart, 'tot_cost': tot_cost})

def add_single_item_into_cart(request, Item_id):
    item = get_object_or_404(Item, id=Item_id)
    user = request.user
    for obj in user.profile.cart_items.all():
        if obj.item.id == item.id:
            obj.quantity+=1
            obj.itemtotal=(item.price)*float(obj.quantity)
            obj.save()
    return redirect('cart:shoppingcart')

def add_item(request):
    print("hello")
    
    if request.method=='POST':
        # print(request.GET['countrySelect'])
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image = request.POST.get('image')
        user = request.user 
        print(user)
        shop = get_object_or_404(Shop, username=user)
        print(shop, shop.id)
        item = Item()
        item.name = name
        all_items = Item.objects.all()
        flag=0
        for it in Item.objects.all():
            if it.name==item.name:
                print("Already in list")
                messages.warning(request, "Already in list")
                flag=1

        if flag==0:
            item.price = price
            item.description = description
            item.image = image
            item.save()
            item.shop_having.add(shop)
            item.save()
            all_items = Item.objects.all()
            return render(request, 'cart/itemlist.html', {'all_items': all_items})
        return render(request, 'cart/itemlist.html', {'all_items': all_items})
    return render(request, 'cart/additemtolist.html')

def remove_from_cart(request, Item_id):
    item = get_object_or_404(Item, id=Item_id)
    user = request.user
    for obj in user.profile.cart_items.all():
        if obj.item.id == item.id:
            user.profile.cart_items.filter(id=obj.id ).delete()
    return redirect('cart:shoppingcart')


def remove_single_item_from_cart(request, Item_id):
    item = get_object_or_404(Item, id=Item_id)
    user = request.user
    for obj in user.profile.cart_items.all():
        if obj.item.id == item.id:
            if obj.quantity>1:
                obj.quantity-=1
                obj.itemtotal=(item.price)*float(obj.quantity)
                obj.save()
            else:
                user.profile.cart_items.filter(id=obj.id).delete()
    return redirect('cart:shoppingcart')


def checkout(request):
    user = request.user
    if not user.is_authenticated:
        num_items_in_cart=0
        return render(request, 'cart/payment.html', {'num_items_in_cart': num_items_in_cart})
    all_items = user.profile.cart_items.all()
    num_items_in_cart = all_items.count()
    tot_cost=0
    for i in all_items:
        print(i.quantity)
        tot_cost += i.itemtotal
    # print(tot_cost)
    context = {'num_items_in_cart': num_items_in_cart, 'all_items':all_items, 'tot_cost':tot_cost}
    return render(request, 'cart/payment.html', context)

