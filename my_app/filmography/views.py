from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import ActorUserRequestForm, CustomUserCreationForm
from .models import *
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from django.db.models.functions import TruncDate
import json


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("dashboard"))
    else:
        form = CustomUserCreationForm()
    context = {
            'form':form,
        }
    return render(request, "users/register.html", context)

@login_required
def dashboard(request):
    if request.method == 'POST':
        form = ActorUserRequestForm(request.POST) #initial={'user':request.user}
        form.user = request.user
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user.userprofile
            obj.save()
            print(form.user)
            print(request.user.userprofile)
            return redirect("actorrequesthistory", request.user.userprofile)
        else:
            context = {
            'form':form,
        }
    else:
        form = ActorUserRequestForm()
        context = {
            'form':form,
            'actors':Actor.objects.all(),
            'useractors':ActorUser.objects.filter(user=request.user.userprofile)
        }
    return render(request, "users/dashboard.html", context)



class UserProfileView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = "users/userprofile_detail.html"
    

class UpdateUserProfile(LoginRequiredMixin, UpdateView):
    model = UserProfile
    
    fields = ['first_name', 'last_name', 'avatar']
    success_url ="/"

    template_name = "users/userprofile_form.html"

""""

class ApiRequestHistoryList(LoginRequiredMixin, ListView):
    model = ActorUser
    context_object_name = 'actors'
    template_name = "users/apirequesthistory_list.html"

    def get_queryset(self):
        return ActorUser.objects.filter(
            user=self.request.user.userprofile, phrase=self.kwargs['phrase']
        )
"""

class ApiRequestHistoryList(LoginRequiredMixin, ListView):
    model = Actor
    context_object_name = 'actors'
    template_name = "users/apirequesthistory_list.html"

    def get_queryset(self):
        return Actor.objects.filter(fullname__icontains=self.kwargs['phrase']
        )


class ActorRequestHistoryList(LoginRequiredMixin, ListView):
    model = ActorUserRequest
    context_object_name = 'actors'
    template_name = "users/actorrequesthistory_list.html"
    def get_queryset(self):
        return ActorUserRequest.objects.filter(
            user=self.request.user.userprofile
        ).order_by('-datetime')

class ActorListView(LoginRequiredMixin, ListView):
    model = Actor
    template_name = "users/actor_list.html"

    def get_queryset(self):
        pass 

    
class ActorMovieListView(LoginRequiredMixin, ListView):
    model = ActorMovie
    context_object_name = 'movies'
    template_name = "users/actor_movie_list.html"
    def get_queryset(self):
        return ActorMovie.objects.filter(actor=self.kwargs['actor'])

def actoruserrequestview(request, pk):
    return render(request, "users/actoruserrequest_detail.html")

def usaged_api_chart(request):
    labels = []
    data = []

    queryset = ActorUserRequest.objects.all().filter(user=request.user.userprofile).annotate(date=TruncDate('datetime')).values('date').annotate(**{'dailyusage': Count('date')})
    for entry in queryset:
        labels.append(entry['date'])
        data.append(entry['dailyusage'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

def like(request):
    if request.method == 'POST':
        actor_id = request.POST['actor_id']
        likedactors = Actor.objects.get(id=actor_id)
        actors=ActorUser.objects.get(actor=likedactors, user=request.user.userprofile)
        if actors.liked == False:
            actors.liked = True
            actors.save()
            r={"action": "added"}
            return JsonResponse(r)
        else:
            actors.liked = False
            a=actors
            a.save()
            r={"action": "removed"}
            return JsonResponse(r)