from django.http import HttpResponse

def index(Request):
    return HttpResponse("Hello, world. You're at the polls index.")