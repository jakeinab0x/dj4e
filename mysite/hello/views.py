from django.shortcuts import render, HttpResponse

# Create your views here.
def myview(req):
    resp = HttpResponse("bla bla")
    resp.set_cookie('dj4e_cookie', '11808b3e', max_age=1000)
    return resp
