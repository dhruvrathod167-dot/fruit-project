from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Order   # if you have Order model
from .models import *
from django.db.models import Q

# Create your views here.


def register(request):
    if request.method == 'POST':
        try:
    
            name=request.POST.get('name') 
            contact =request.POST.get('contact')
            email=request.POST.get('email')
            password=request.POST.get('password')
            
            Register.objects.create(
                name=name,
                contact=contact,
                email=email,
                password=password
                
            ) 
            messages.success(request,"Register successfully")
            return redirect('login')
        
        except Exception as e:
            messages.error(request,f"Error occurred:{e} ")
            return render(request,'register.html')
        
        
    return render(request,'register.html')






def log(request):
    if request.method == 'POST':
        
   
        email=request.POST.get('email')
        password=request.POST.get('password')
        
        try:
            user = Register.objects.filter(
                email=email,
                password=password
            ).first()
            if user :
                messages.success(request,"Login sucessfully")
                return redirect('index')
            else:
                messages.error(request,"plaese enter valid email or password")
                return render(request,'login.html')
            
        except Exception as e:
            messages.error(request,f"Login Failed:{str(e)}")
            return render(request, 'login.html')
        
        
    return render(request,'login.html')

def index(request):
    return render(request,'index.html')


from django.shortcuts import render
from .models import Cart


def get_session_key(request):
    """Return session key, create if not exists"""
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def cart(request):
    session_key = get_session_key(request)

    cart_items = Cart.objects.filter(
        session_key=session_key
    ).select_related('product')

    subtotal = 0

    for item in cart_items:
        # ⭐ subtotal calculate
        item.subtotal = item.product.price * item.quantity
        subtotal += item.subtotal

    shipping = 50 if subtotal > 0 else 0
    total = subtotal + shipping

    context = {
        "items": cart_items,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total,
    }

    return render(request, "cart.html", context)
    


def checkout(request):
    session_key = get_session_key(request)

    cart_items = Cart.objects.filter(
        session_key=session_key
    ).select_related('product')

    subtotal = 0
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
        subtotal += item.total_price

    shipping = 50 if subtotal > 0 else 0
    total_with_shipping = subtotal + shipping

    if request.method == 'POST':
        Checkout.objects.create(
            first_name=request.POST.get('firstname', ''),
            last_name=request.POST.get('lastname', ''),
            company_name=request.POST.get('companyname', ''),
            address=request.POST.get('address', ''),
            city=request.POST.get('city', ''),
            country=request.POST.get('country', ''),
            pin_code=request.POST.get('pincode') or None,
            mobile=request.POST.get('mobile') or None,
            email=request.POST.get('email', ''),
            create_an_account=True if request.POST.get('Accounts') else False,
            different_address=request.POST.get('Address', ''),
            notes=request.POST.get('notes', '')
        )

        Cart.objects.filter(session_key=session_key).delete()

        return redirect("place_order")

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total_with_shipping': total_with_shipping
    }

    return render(request, 'checkout.html', context)

def place_order(request):

    if request.method == "POST":
        return redirect("order_confirm")

    # page open
    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    cart_items = Cart.objects.filter(
        session_key=session_key
    ).select_related('product')

    subtotal = 0

    for item in cart_items:
        item.total_price = item.product.price * item.quantity
        subtotal += item.total_price

    shipping = 50 if subtotal > 0 else 0
    total = subtotal + shipping

    return render(request, "place_order.html", {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "shipping": shipping,
        "total": total,
    })    
    
def orderconfirm(request):

    if not request.session.session_key:
        request.session.create()

    session_key = request.session.session_key

    cart_items = Cart.objects.filter(
        session_key=session_key
    ).select_related('product')

    subtotal = 0
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
        subtotal += item.total_price

    shipping = 50 if subtotal > 0 else 0
    total = subtotal + shipping

    return render(request, 'order_confirm.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total
    })
    
    
def Contact(request):
    return render(request,'contact.html')

def Home(request):
    return render(request,'home.html')

def shop(request):
    category = request.GET.get('category')  # fruit / vegetable
 
    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()
 
    return render(request, "shop.html", {
        "products": products,
        "selected_category": category
    })
 
def shop_detail(request):
    return render(request, 'shop-detail.html')


def shopdetail(request):
    return render(request,'shop-detail.html')

def Testimonial(request):
    return render(request,'testimonial.html')


def plus_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_items = Cart.objects.filter(
        product=product,
        session_key=session_key
    )

    if cart_items.exists():
        cart_item = cart_items.first()
        cart_item.quantity += 1
        cart_item.save()

       
        cart_items.exclude(id=cart_item.id).delete()

    return redirect('cart')

def minus_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_item = get_object_or_404(
        Cart,
        product=product,
        session_key=session_key
    )

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')
 
def remove_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Cart.objects.filter(product=product).delete()
    return redirect('cart')


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_item, created = Cart.objects.get_or_create(
        product=product,
        session_key=session_key,
        defaults={'quantity': 1}
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')  




def search_item(request):
    query = request.GET.get('q', '').strip()
 
    if not query:
        return redirect('shop')
 
    products = Product.objects.filter(
        Q(name__icontains=query) 
        # FIXED field name
    )
 
    return render(request, 'shop.html', {
        'products': products,
        
    })
 



