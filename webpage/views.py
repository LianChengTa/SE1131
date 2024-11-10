from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import loginform,registerform,profile_edit_form,password_edit_form
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.views import PasswordChangeView


@csrf_exempt
def login_page(request):
    if request.method == 'POST':
        form = loginform(data=request.POST)
        print('Request data:', request.POST)  # 打印请求数据
        print(form)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print('Attempting to log in...')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, '登入成功')
                print('Login successful!')
                return redirect('get_main_page')
            else:
                messages.error(request, "登入失敗")
                print('Authentication failed for user:', username)
        else:
            print('Form is not valid:', form.errors)  # 打印表单错误信息
    else:
        form = loginform()
    return render(request, 'login.html', {'form': form})

@csrf_exempt
def register_page(request):
    if request.method == 'POST':
        form = registerform(request.POST)
        print(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, '賬號創建成功！你現在可以登入。')
            return redirect('login')  # 註冊成功後自動跳轉到登入頁面
        else:
            print(form.errors)
    else:
        form = registerform()

    return render(request, 'register.html', {'form': form})

@login_required
@csrf_exempt
def get_profile_edit(request):
    if request.method == 'POST':
        form = profile_edit_form(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_edit')
    else:
        form=profile_edit_form(instance=request.user)
    return render(request,'profile_edit.html',{'form':form})

@method_decorator(csrf_exempt,name='dispatch')
class password_edit(LoginRequiredMixin,PasswordChangeView):
    template_name='password_edit.html'
    success_url=reverse_lazy('profile_edit')
    form_class= password_edit_form


@login_required
@csrf_exempt
def get_main_page(request):
    return render(request,'homepage.html')


@login_required
@csrf_exempt
def get_event_detail(request):


    
    return render(request,'eventDetails.html')