from django.contrib.auth import authenticate


def authenticateUser(formData):
    username = formData.cleaned_data['username']
    password = formData.cleaned_data['password']
    return authenticate(username=username, password=password)
