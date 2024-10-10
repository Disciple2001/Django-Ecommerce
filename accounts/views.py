from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from accounts.forms import RegistrationForm, LoginForm
from accounts.models import CustomUser

# Email packages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

from ecommerce.models import CartItem, Cart
from ecommerce.views import _get_or_create_session_id

import requests


# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            username = email.split('@')[0]

            user = CustomUser.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                password=password
            )

            user.phone_number = phone_number
            user.save()

            # USER ACTIVATION
            # usign the local host
            current_site = get_current_site(request)
            mail_subject = 'Please activate your new account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            # messages.success(request, 'Thank you for registering with us.We have sent you a verification email to your email address.Please verify it.')
            return redirect('/accounts/login/?command=verification&email='+email)
    else:
        form = RegistrationForm()

    context = {
        'form': form
    }

    return render(request, 'accounts/register.html', context)


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            try:
                cart = Cart.objects.get(cart_id=_get_or_create_session_id(request))
                is_cart_product_exist = CartItem.objects.filter(cart=cart).exists()

                if is_cart_product_exist:
                    cart_items = CartItem.objects.filter(cart=cart)

                    product_variation = []
                    for item in cart_items:
                        variations = item.variations.all()
                        product_variation.append(list(variations))

                    cart_items = CartItem.objects.filter(user=user)
                    ex_var_list = []
                    id = []
                    for item in cart_items:
                        existing_variations = item.variations.all()
                        ex_var_list.append(list(existing_variations))
                        id.append(item.id)

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_items = CartItem.objects.filter(cart=cart)
                            for item in cart_items:
                                item.user = user
                                item.save()

                    # for item in cart_items:
                    #     item.user = user
                    #     item.save()
            except:
                print('except login')
                pass

            auth.login(request, user)
            messages.success(request, 'User authenticated successfully')
            url = request.META.get('HTTP_REFERER')
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split('=') for x in query.split('&'))
                if 'next' in params:
                    nextPage = params['next']
                    return redirect(nextPage)
            except:
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            redirect('login')

    form = LoginForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/login.html', context)


@login_required(login_url='login')
def logout(request):
    auth.logout(request, )
    messages.success(request, 'You are logged out')
    return redirect('login')


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')
