from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns=[
    # url(r'^home1', views.home1, name='home1'),
    # url(r'^uploads/simple/', views.simple_upload, name='simple_upload'),
    # url(r'^uploads/form/', views.model_form_upload, name='model_form_upload'),
    url(r'^ocr/$', views.ocr, name='ocr'),
    url(r'^maps', views.maps, name='maps'),
    url(r'^home/', views.home, name='home'),
    url(r'^add_item/', views.add_item, name='add_item'),
    url(r'^itemlist/', views.itemlist, name='itemlist'),
    url(r'^shoppingcart/', views.shoppingcart, name='shoppingcart'),
    url(r'^search/', views.searchpage , name='searchpage'),
    url(r'^searchnearbyshops/', views.searchnearbyshops , name='searchnearbyshops'),
    url(r'^searchitem/', views.search , name='search'),
    url(r'^sort_alphabet/', views.sort_alphabet , name='sort_alphabet'),
    url(r'^sort_desc_alphabet/', views.sort_desc_alphabet , name='sort_desc_alphabet'),
    url(r'^sort_price/', views.sort_price , name='sort_price'),
    url(r'^sort_desc_price/', views.sort_desc_price , name='sort_desc_price'),
    # url(r'^ocr/', ocr_view, name='ocr_view'),
    # url(r'^ocrform/', ocr_form_view, name='ocr_form_view'),
    url(r'^checkout/', views.checkout , name='checkout'),
    url(r'^productpage/(?P<Id>[0-9]+)', views.product_page, name='product_page'),
    url(r'^add_to_cart/(?P<Item_id>[0-9]+)',views.add_to_cart, name='add_to_cart'),
    url(r'^remove_from_cart/(?P<Item_id>[0-9]+)',views.remove_from_cart, name='remove_from_cart'),
    url(r'^remove_single_item_from_cart/(?P<Item_id>[0-9]+)',views.remove_single_item_from_cart, name='remove_single_item_from_cart'),
    url(r'^add_single_item_into_cart/(?P<Item_id>[0-9]+)',views.add_single_item_into_cart, name='add_single_item_into_cart')

]

