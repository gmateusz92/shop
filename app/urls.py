from django.urls import path
from .views import HomeView, ItemDetailView, add_to_cart, remove_from_cart

app_name = 'app'

urlpatterns = [

    path('', HomeView.as_view(), name='home-page'),
    path('product/<slug>', ItemDetailView.as_view(), name='product-page'), #do detail view dajemy slug
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart')
    # path('<int:id>/', views.detail, name='detail'),
    # path('checkout/', views.checkout, name='checkout'),

]