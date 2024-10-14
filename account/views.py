from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, reverse
from django.views import View
from .forms import LoginForm, RegisterForm, CheckOtpForm, AddressCreationForm
# import ghasedak_sms
import ghasedakpack
from random import randint
from account.models import Otp, User
from django.utils.crypto import get_random_string
from uuid import uuid4

SMS = ghasedakpack.Ghasedak('fe2360610ce83f4bb3cebb1784e4ace4b694e80a2ae0e76634adcdaf558f27b3V5jW8SCKAHT3LQDh')



# SMS_api = ghasedak_sms.Ghasedak(baseurl="http://your_base_url/api/v1", apikey='fe2360610ce83f4bb3cebb1784e4ace4b694e80a2ae0e76634adcdaf558f27b3V5jW8SCKAHT3LQDh')

sms = ghasedakpack.Ghasedak("")



# Function Based View:
# def user_login(request):
#     return render(request, "account/contact.html")


# Class Based View:
class UserLogin(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "account/login.html", {'form': form})

    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['phone'], password=cd['password'])
            if user is not None:
                login(request, user)
                next_page = request.GET.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect("/")
            else: 
                form.add_error("phone", "invalid user data")

        else:
            form.add_error("phone", "invalid data")

        return render(request, "account/login.html", {'form': form})    
    

# class RegisterView():
#     def get(self, request):
#         form = RegisterForm()
#         return render(request, "account/register.html", {'form': form})

def OtpLoginView(request):
    if request.method == "GET":
        form = RegisterForm()
        return render(request, "account/otp_login.html", {'form': form})
    
    elif request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            randcode= randint(1000, 9999)
            SMS.verification({'receptor': cd["phone"], 'type': '1', 'template': 'randcode', 'param1': randcode})
            # token = get_random_string(length=100)
            token = str(uuid4())
            Otp.objects.create(phone=cd['phone'], code=randcode, token=token)
            print(randcode)
            return redirect(reverse('account:check_otp') + f'?token={token}')
            
        else:
            form.add_error("phone", "invalid data")

        return render(request, "account/otp_login.html", {'form': form}) 
    


class CheckOtpView(View):
    def get(self, request):
        form = CheckOtpForm()
        return render(request, "account/check_otp.html", {'form': form})
    
    def post(self, request):
        token = request.GET.get('token')
        form = CheckOtpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if Otp.objects.filter(code=cd['code'], token=token).exists():
                otp = Otp.objects.get(token=token)
                user, is_create = User.objects.get_or_create(phone=otp.phone)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                otp.delete()
                return redirect('/')

        else:
            form.add_error("phone", "invalid data")

        return render(request, "account/check_otp.html", {'form': form})    
    

class AddAddressView(View):
    def post(self, request):
        form = AddressCreationForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)


        return render(request, 'account/add_address.html', {'form': form})    
    
    def get(self, request):
        form = AddressCreationForm()
        return render(request, 'account/add_address.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('/')