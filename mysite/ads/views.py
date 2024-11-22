from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db.models import Q

from ads.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView

from ads.models import Ad, Comment, Fav
from ads.forms import CreateForm, CommentForm

class AdListView(OwnerListView):
    model = Ad
    template_name = 'ads/ad_list.html'

    def get(self, request):
        ad_list = Ad.objects.all()
        favorites = list()
        if request.user.is_authenticated:
            # rows = [{'id': 2}, {'id': 4} ...] list of rows
            rows = request.user.favorite_ads.values('id')
            # favorites = [2, 4, ...] using list comprehension
            favorites = [row['id'] for row in rows]

        # Get the value of a GET variable called "search", but if doesn't exist return False
        # This will be the search query a user enters
        strval = request.GET.get("search", False)
        if strval:
            # Simple title-only search
            # objects = Post.objects.filter(title__contains=strval).select_related().distinct().order_by('-updated_at')[:10]

            # Multi-field search
            # __icontains for case-insensitive search
            # Q objects allow for complex querying: https://docs.djangoproject.com/en/5.1/topics/db/queries/#complex-lookups-with-q-objects
            # in this case, it allows for an OR statement
            query = Q(title__icontains=strval)
            query.add(Q(text__icontains=strval), Q.OR)
            # The above code is equivalent to:
            # query = Q(title__icontains=strval) | Q(text__icontains=strval)

            # select_related() will grab Foreign Key object data https://docs.djangoproject.com/en/5.1/ref/models/querysets/#django.db.models.query.QuerySet.select_related
            # distinct() eliminates duplicate rows from the query results https://docs.djangoproject.com/en/5.1/ref/models/querysets/#django.db.models.query.QuerySet.distinct
            ad_search_list = Ad.objects.filter(query).select_related().distinct().order_by('-updated_at')[:10]
        else:
            ad_search_list = Ad.objects.all().order_by('-updated_at')[:10]

        for obj in ad_search_list:
            obj.natural_updated = naturaltime(obj.updated_at)

        ctx = {
                'ad_list': ad_list,
                'favorites': favorites, 
                'ad_search_list': ad_search_list,
                'search': strval
              }
        return render(request, self.template_name, ctx)

class AdDetailView(OwnerDetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'

    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk)
        comments = Comment.objects.filter(ad=ad).order_by('-updated_at')
        comment_form = CommentForm()
        context = {'ad': ad, 
                   'comments': comments, 
                   'comment_form': comment_form
                  }
        return render(request, self.template_name, context)

# These new views don't inherit from owner.py 
# because they manage the owner column in the get() and post() methods.
class AdCreateView(LoginRequiredMixin, View):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk=None):
        form = CreateForm()
        context = {'form':form}
        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        form = CreateForm(request.POST, request.FILES or None)

        if not form.is_valid():
            context = {'form':form}
            return render(request, self.template_name, context)

        # Add owner to the model before saving
        ad = form.save(commit=False)
        ad.owner = self.request.user
        ad.save()
        return redirect(self.success_url)


class AdUpdateView(OwnerUpdateView):
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:all')

    def get(self, request, pk):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(instance=ad)
        context = {'form':form}
        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        ad = get_object_or_404(Ad, id=pk, owner=self.request.user)
        form = CreateForm(request.POST, request.FILES or None, instance=ad)

        if not form.is_valid():
            context = {'form':form}    
            return render(request, self.template_name, context)

        ad = form.save(commit=False)
        ad.save()
    
        return redirect(self.success_url)

class AdDeleteView(OwnerDeleteView):
    model = Ad

def stream_file(request, pk):
    ad = get_object_or_404(Ad, id=pk)
    response = HttpResponse()
    response['Content-Type'] = ad.content_type
    response['Content-Length'] = len(ad.picture)
    response.write(ad.picture)
    return response

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        ad = get_object_or_404(Ad, id=pk)
        comment = Comment(text=request.POST['comment'], owner=request.user, ad=ad)
        comment.save()
        return redirect(reverse('ads:ad_detail', args=[pk]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = 'ads/ad_comment_delete.html'

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        ad = self.object.ad
        return reverse('ads:ad_detail', args=[ad.id])

# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print(f"Add PK {pk}")
        ad = get_object_or_404(Ad, id=pk)
        fav = Fav(user=request.user, ad=ad)
        try: 
            fav.save() # In case of duplicate key
        except IntegrityError:
            pass
        return HttpResponse()
    
@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        print(f"Delete PK {pk}")
        ad = get_object_or_404(Ad, id=pk)
        try:
            Fav.objects.get(user=request.user, ad=ad).delete()
        except Fav.DoesNotExist:
            pass
        return HttpResponse()
    
