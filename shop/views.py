from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from datetime import date
from django.contrib.auth import login
from .models import Product, Purchase
from .forms import RegistrationForm


def index(request):
    products = Product.objects.all()
    discount_today = False

    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        bday = request.user.profile.birthday
        if bday and bday.day == date.today().day and bday.month == date.today().month:
            discount_today = True

    for p in products:
        p.discounted_price = round(p.price * Decimal("0.9"), 2) if discount_today else None

    context = {
        "products": products,
        "discount_today": discount_today
    }

    return render(request, "shop/index.html", context)


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = RegistrationForm()
    return render(request, "shop/register.html", {"form": form})


def buy_product(request, product_id):
    if not request.user.is_authenticated:
        return redirect('register')

    product = get_object_or_404(Product, pk=product_id)
    discount = False

    # проверка дня рождения
    profile = getattr(request.user, 'profile', None)
    if profile and profile.birthday:
        today = date.today()
        if profile.birthday.day == today.day and profile.birthday.month == today.month:
            discount = True

    price_to_pay = product.price
    if discount:
        price_to_pay = round(product.price * Decimal("0.9"), 2)

    if request.method == "POST":
        address = request.POST.get("address")
        if address:
            Purchase.objects.create(
                product=product,
                person=request.user,
                price=price_to_pay,
                address=address
            )
            return redirect('index')

    return render(request, "shop/buy.html", {
        "product": product,
        "discounted_price": price_to_pay if discount else None
    })
