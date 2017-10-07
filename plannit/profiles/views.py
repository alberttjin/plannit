from django.shortcuts import render, redirect
from django.http import Http404
from django.http import HttpResponse
from django.contrib.auth.views import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views import generic
from django.views.generic import View
from .forms import regForm, scheduleForm, eventForm
from .models import *

# Create your views here.
def index(request):
    return

def loadprof(request, profile_id):
    try:
        user = person.objects.get(id=profile_id)
    except person.DoesNotExist:
        raise Http404("The profile you are looking for does not exist.")
    return render(request, 'profile.html', {'user': user})

class RegFormView(View):
    form_class = regForm
    template_name = 'register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit = False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username = username, password = password)

            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('/newprofile')
        return render(request, self.template_name, {'form': form})

def login_view(request):
    return render(request, "login.html", {})

#def register_view(request):
#    if request.method == "POST":
#        form = UserCreationForm(request.POST)
#        if form.is_valid():
#            form.save()
#            return redirect("/profiles")
#    else:
#        form = UserCreationForm()
#    return render(request, "register.html", {'form': form})


def logout_view(request):
    return render(request, "login.html", {})

class ScheduleFormView(View):
    form_class = scheduleForm
    template_name = 'new_schedule.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            schedule  = form.save(commit = False)
            title  = form.cleaned_data['title']
            place = form.cleaned_data['place']
            date = form.cleaned_data['date']
            schedule.save()
        if schedule:
            # TODO: Add events url
            return redirect('/events/')

        return render(request, self.template_name, {'form': form})

class EventFormView(View):
    form_class = eventForm
    template_name = 'new_schedule.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):


        if form.is_valid():
            #TODO: Add schedule info from parent 
            event  = form.save(commit = False)
            title  = form.cleaned_data['title']
            start = form.cleaned_data['start']
            end  = form.cleaned_data['end']
            location  = form.cleaned_data['location']
            event.save()

        return render(request, self.template_name, {'form': form})
