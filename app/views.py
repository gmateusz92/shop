from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, OrderItem, Order
from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.contrib import messages

def item_list(request):
    items = Item.objects.all()
    return render(request, 'home-page.html', {'items': items})

def checkout(request):
    return render(request, 'checkout.html')


class HomeView(ListView):
    model = Item
    template_name = 'home-page.html'


class ItemDetailView(DetailView): #dla detail dajemy object w templates
    model = Item
    template_name = 'product-page.html'

def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create( #created bo zwraca tuple
        item=item,
        user=request.user,
        ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)# jezeli uzytkownik ma juz zamowienia ale nie ukonczone
    if order_qs.exists(): #jezeli query set istnieje
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "this item quantity was updated")
        else:
            messages.info(request, "this item was added to your card")
            order.items.add(order_item)
            return redirect('app:product-page', slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item) #skad items
        messages.info(request, "this item was added to your card")
    return redirect('app:product-page', slug=slug)

def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False)
    if order_qs.exists(): #jezeli query set istnieje
        order = order_qs[0]
        #check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "this item was removed from  your card")
            return redirect('app:product-page', slug=slug)
        else:
            #add a message saying the user doesnt have an order
            messages.info(request, "this item was not in your card")
    else:
        messages.info(request, "ypu do not have an active order")
        return redirect('app:product-page', slug=slug)
    return redirect('app:product-page', slug=slug)