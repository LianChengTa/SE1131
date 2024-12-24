from django.shortcuts import render,redirect ,get_object_or_404 #to get data from database from specific id
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import loginform,registerform,profile_edit_form,password_edit_form,add_event_form
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.views import PasswordChangeView
from django.conf import settings
from django.core.files.base import ContentFile
from django.http import JsonResponse
import json
#added from .models
from .models import add_event, user_account


@csrf_exempt
def login_page(request):
    if request.method == 'POST':
        form = loginform(data=request.POST)
        # print('Request data:', request.POST)  # 打印请求数据
        # print(form)
         
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # print('Attempting to log in...')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, '登入成功')
                # print('Login successful!')
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
        #(teacher or student)
        identity = request.POST.get('identity', None)
        # print('Selected identity:', identity)
        is_staff = True if identity == 'teacher' else False
        
        # print(request.POST)
        # print(form)
        if form.is_valid():
            form.save(is_staff=is_staff)
            messages.success(request, '賬號創建成功！你現在可以登入。')
            return redirect('login')  # 註冊成功後自動跳轉到登入頁面
        else:
            print(form.errors)
    else:
        form = registerform()

    return render(request, 'register.html', {'form': form})

@login_required
@csrf_exempt
def get_add_event(request):

    if request.method == 'POST':
        form = add_event_form(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)  # 延遲保存以便處理圖片
            # Assign the logged-in user to the event
            instance.user = request.user
            if not request.FILES.get('image'):  # 檢查是否有上傳圖片
                # print(settings.STATICFILES_DIRS[0])
                with open(settings.STATICFILES_DIRS[0] + '/ntou_logo.png', 'rb') as f:
                    instance.image.save('default_image.jpg', ContentFile(f.read()), save=False)
            instance.save()
            print("File URL:", instance.image.url)  # 打印保存的圖片URL
            return redirect('get_main_page')  # Redirect after saving
        else:
            print(form.errors)  # 打印表單錯誤
    else:
        form = add_event_form()

    return render(request, 'add_event_page.html', {'form': form})



@login_required
@csrf_exempt
def get_profile_edit(request):
    if request.method == 'POST':
        form = profile_edit_form(request.POST, instance=request.user)
        # print(form)
        if form.is_valid():
            form.save()
            # print(f"Updated first_name: {request.user.first_name}")  # Debugging print
            messages.success(request, '個人資料已成功更新！')
            return redirect('profile_edit')
    else:
        # print(f"Form errors: {form.errors}") 
        form = profile_edit_form(instance=request.user)
    
    return render(request, 'profile_edit.html', {'form': form})


@method_decorator(csrf_exempt, name='dispatch')
class password_edit(LoginRequiredMixin, PasswordChangeView):
    template_name = 'password_edit.html'
    success_url = reverse_lazy('profile_edit')
    form_class = password_edit_form

    def form_valid(self, form):
        # 添加成功提示消息
        messages.success(self.request, '密碼已成功更新！')
        return super().form_valid(form)


@csrf_exempt
def get_main_page(request):
    is_teacher = request.user.is_staff
    
    events = add_event.objects.all()

    # 獲取搜索查詢
    search_query = request.GET.get('search', None)
    if search_query: 
        events = events.filter(title__icontains=search_query)

    return render(request, 'homepage.html', {
        'events': events,
        'is_teacher': is_teacher,
        'search_query': search_query or '',
    })


@login_required
@csrf_exempt
def get_event_detail(request, event_id):
    event = get_object_or_404(add_event, id=event_id)
    has_participated = event.participants.filter(id=request.user.id).exists()
    
    return render(request, 'details.html', {
        'event': event,
        'is_teacher': request.user.is_staff,  # 假設有這個屬性來判斷是否是教師
        'has_participated': has_participated,
    })
@login_required
@csrf_exempt
def delete_event(request, event_id):
    event = get_object_or_404(add_event, id=event_id)
    
    if request.method == 'POST':
        event.delete()  # 刪除活動
        
        # 返回成功的 JsonResponse
        return JsonResponse({'success': True, 'message': '活動已成功刪除。', 'redirect_url': '/webpage/mainpage'})  # 返回重定向 URL
    
    return JsonResponse({'success': False, 'error': '無效的請求'}, status=400)
    
@login_required
@csrf_exempt
def get_student_event(request):
    # 获取当前登录的用户
    user = request.user

    # 查询用户已参与的活动
    participated_events = add_event.objects.filter(participants=user)

    return render(request, 'event_list_page.html', {'events': participated_events})



@login_required
@csrf_exempt
def participate_event(request, event_id):
    event = get_object_or_404(add_event, id=event_id)
    if request.method == 'POST':
        event.participants.add(request.user)
        event.save()
        return JsonResponse({'success': True, 'message': '您已成功報名此活動！'})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
@csrf_exempt
def edit_event(request, event_id):
    event = get_object_or_404(add_event, id=event_id)

    if request.method == 'POST':
        form = add_event_form(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()  # 保存表單，這會處理圖片的更新
            return redirect('detail', event_id=event.id)
    else:
        form = add_event_form(instance=event)

    return render(request, 'edit_event.html', {'form': form, 'event': event})

@login_required
@csrf_exempt
def cancel_registration(request, event_id):
    event = get_object_or_404(add_event, id=event_id)
    if request.method == 'POST':
        event.participants.remove(request.user)
        event.save()
        return JsonResponse({'success': True, 'message': '取消報名成功'})
    return JsonResponse({'error': 'Invalid request'}, status=400)



@csrf_exempt
def search_events(request):
    search_query = request.GET.get('search', '')
    if search_query:
        # 根據活動標題進行模糊匹配
        events = add_event.objects.filter(title__icontains=search_query)
    else:
        events = add_event.objects.all()  # 沒有搜索詞時顯示所有活動

    # 只返回活動部分的 HTML
    return render(request, 'event_list.html', {'events': events})

