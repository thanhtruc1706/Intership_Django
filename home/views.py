from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return HttpResponse("Đây là trang chủ từ view `index`.")

def hello(request):
    return HttpResponse("<h1>Xin chào Django!</h1>")

def welcome(request):
    return render(request, 'welcome.html')
