from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class FormView(LoginRequiredMixin, View):
    template_name = 'solo/form.html'

    def get(self, request):
        result = request.session.get('result', False)
        if result: del(request.session['result'])
        return render(request, self.template_name, {'result': result})
    
    def post(self, request):
        if request.POST.get('field1') or request.POST.get('field2'):
            rev_field1 = request.POST.get('field1').strip().upper()[::-1]
            rev_field2 = request.POST.get('field2').strip().upper()[::-1]
            result = f'{rev_field2} {rev_field1}'
            request.session['result'] = result
        return redirect(request.path)