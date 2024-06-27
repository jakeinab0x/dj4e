from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.urls import reverse_lazy

from autos.models import Auto, Make
# from autos.forms import MakeForm # not needed with generic.edit views

# LoginRequiredMixin = login required to view this page - this is always first param
class MainView(LoginRequiredMixin, View):
    """Main list view for Autos app with count"""
    def get(self, request):
        mc = Make.objects.count() # get count of all objs
        al = Auto.objects.all() # get all objs

        # context - allows us to parse in the above objs
        # to the html template
        ctx = {'make_count': mc, 'auto_list': al} 
        # render gathers all the above and creates the 
        # HttpReponse (the formatted page you see with data)
        return render(request, 'autos/auto_list.html', ctx) 


# TODO:
# - would this work as ListView?
class MakeView(LoginRequiredMixin, View):
    def get(self, request):
        ml = Make.objects.all()
        ctx = {'make_list':ml}
        return render(request, 'autos/make_list.html', ctx)

        

class MakeCreate(LoginRequiredMixin, CreateView):
    model = Make
    fields = '__all__'
    success_url = reverse_lazy('autos:all')

# ---------- Manual logic ----------
# class MakeCreate(LoginRequiredMixin, View):
    # template = 'autos/make_form.html'
# csev NOTE:
# We use reverse_lazy() because we are in "constructor attribute" code
# that is run before urls.py is completely loaded 
    # success_url = reverse_lazy('autos:all')

    # def get(self, request):
    #     form = MakeForm()
    #     ctx = {'form':form}
    #     return render(request, self.template, ctx)

    # def post(self, request):
    #     form = MakeForm(request.POST)
    #     if not form.is_valid():
    #         ctx = {'form':form}
    #         return render(request, self.template, ctx)

    #     make = form.save()
    #     return redirect(self.success_url)



class MakeUpdate(LoginRequiredMixin, UpdateView):
    model = Make
    fields = '__all__'
    success_url = reverse_lazy('autos:all')

# ---------- Manual logic ----------
# csev NOTE:
# MakeUpdate has code to implement the get/post/validate/store flow
# AutoUpdate (below) is doing the same thing with no code
# and no form by extending UpdateView
# class MakeUpdate(LoginRequiredMixin, View):
#     model = Make # model we are pulling data from
#     success_url = reverse_lazy('autos:all') # where we will be taken to after success
#     template = 'autos.make_form.html' 

#     def get(self, request, pk): # pk = primary key, used to pull out one specific object
#         make = get_object_or_404(self.model, pk=pk) # pulls object data else returns 404 page
#         form = MakeForm(instance=make)
#         ctx = {'form':form} # form made from Make data to be shunted into html
#         return render(request, self.template, ctx)

#     def post(self, request, pk):
#         make = get_object_or_404(self.model, pk=pk)
#         form = MakeForm(request.POST, instance=make) # create form instance from POST data
#         if not form.is_valid(): # return old data
#             ctx = {'form':form}
#             return render(request, self.template, ctx)

#         form.save()
#         return redirect(self.success_url)


class MakeDelete(LoginRequiredMixin, DeleteView):
    model = Make
    fields = '__all__'
    success_url = reverse_lazy('autos:all')

# ---------- Manual logic ----------
# class MakeDelete(LoginRequiredMixin, View):
#     model = Make
#     success_url = reverse_lazy('autos:all')
#     template = 'autos/make_confirm_delete.html'

#     def get(self, request, pk): 
#         make = get_object_or_404(self.model, pk=pk)
#         ctx = {'make': make}
#         return render(request, self.template, ctx)

#     def post(self, request, pk):
#         make = get_object_or_404(self.model, pk=pk)
#         make.delete()
#         return redirect(self.success_url)
    
# csev NOTE:
# Take the easy way out on the main table
# These views do not need a form because CreateView, etc.
# Build a form object dynamically based on the fields
# value in the constructor attributes
class AutoCreate(LoginRequiredMixin, CreateView):
    model = Auto
    fields = '__all__'
    success_url = reverse_lazy('autos:all')
    
    
class AutoUpdate(LoginRequiredMixin, UpdateView):
    model = Auto
    fields = '__all__'
    success_url = reverse_lazy('autos:all')


class AutoDelete(LoginRequiredMixin, DeleteView):
    model = Auto
    fields = '__all__'
    success_url = reverse_lazy('autos:all')

# https://docs.djangoproject.com/en/4.2/ref/class-based-views/generic-editing/#createview
