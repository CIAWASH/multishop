# from django.shortcuts import render
from django.views.generic import TemplateView
from time import sleep

# Create your views here.

class Home(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        self.request.session['my_name'] = "Ciawash"
        del self.request.session['my_name']
        sleep(10)
        return context