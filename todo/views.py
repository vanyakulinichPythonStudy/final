from django.shortcuts import render


def entry(req):
    return render(req, 'dashboard.html')


def signin(req):
    return render(req, 'signin.html')


def signup(req):
    return render(req, 'signup.html')


def dashboard(req):
    return render(req, 'dashboard.html')
