from django.shortcuts import render, redirect

def home_page(request):
    return render(request, 'home.html')

def new_item(request):
    return redirect('/')
