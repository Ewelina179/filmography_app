from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import ActorForm, CustomUserCreationForm
from filmography.models import *
from filmography.get_from_imdb import actor
from django.contrib import messages
from django.http import HttpResponse

def register(request):
    if request.method == "GET":
        return render(request, "users/register.html", {"form": CustomUserCreationForm})
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("dashboard"))
        else:
            for msg in form.error_messages:
                #messages.error(request, f"{msg}: {form.error_messages[msg]}")
                messages.add_message(request, messages.ERROR, 'Username is already taken.')
            return render(request = request,
                          template_name = "users/register.html",
                          context={"form":CustomUserCreationForm})

@login_required
def dashboard(request):
    if request.method == 'POST':
        form = ActorForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('Your answer has been saved!')
    else:
        form = ActorForm()
        context = {
            'form':form,
        }
    return render(request, "users/dashboard.html", context)

""""

def get_actor(request):
    print("Hej, tu powinien być formularz!")
    from filmography.get_from_imdb import actor
    cont = []
    if request.method == 'POST':
        form = ActorForm(request.POST)
        if form.is_valid():
            actor_form = form.cleaned_data['actor']
            print(actor_form)
            try:
                lst_of_actors_with_the_same_fullname = actor.get_actors_ids(actor_form)
                for el in lst_of_actors_with_the_same_fullname:
                    actor = {"name": el["name"], "id": el["id"], "image": el["image"]}
                    cont.append(actor)
                print(cont)
            except:
                print("Wprowadzono błędne dane do formularza. Nie ma aktora/aktorki.")
            return redirect("actors", cont=cont) 
            #lst_of = cont
    else:
        form = ActorForm()
    return render(request, 'users/search.html', {'form': form})

def actors(request, cont):# to co wpada to lista. niech ją wyświetli. każdy rekord to hiperłącze do kolejnej pds
    for el in cont:
        print (el)
    return render(request, 'users/lst_of_actors.html')

def actor_detail(request, nm, fullname): # inaczej te parametry chyba i jak?????????
    print(f"nm to {nm}")
    from filmography.get_from_imdb import actor
    user = User.objects.get(pk=1)
    actors = Actor.objects.all()
    actors.delete()
    try:
        obj = Actor.objects.get(nm=nm)
        print(f"obiekt z bazy {obj.nm}")
    except Actor.DoesNotExist:
        x = actor.get_actor_filmography(nm) # SET API KEY!!!!!!!!!!!!!!!!!!!!!!!!!!!1
        obj = Actor(nm=nm, fullname=fullname) # tutaj też musi podać fullname - muszą być przekazane dwa parametry razem
        obj.save()
        for el in x:
            print(el)
            try:
                movie = Movie.objects.get(title=el)
            except Movie.DoesNotExist:
                movie = Movie(title=el)
                movie.save()
            actor = Actor.objects.get(nm=nm)
            actor.movies.add(movie)
            actor.save()
        print(obj.fullname)
        print(Actor.objects.get(nm=nm))

    obj = Actor.objects.get(nm=nm)
    print(obj)
# jeśli obiekty w bazie już sprzężone (był ulubiony, nie był i teraz znów ulubiony)
    objj, created = Favourite.objects.update_or_create(
    user=user, actor=obj, is_favourite=True)

    print(user.actors.all())
    print(obj.user_set.all())
    for el in obj.movies.all():
        print(el.title)
    # znaleźć tego usera aktora ulubionego i jego filmy wypisać - NIE ZROBIONE
    xyz = user.actors.filter(fullname="HarrisonFord")
    z = [x.movies.all() for x in xyz] # a powinno być inaczej. jeden aktor i dla niego lst compr z tytułów
    print(z)
    actor_detail = "tutaj będą filmy i inne kwestie dotyczące konkretnego aktora"
    return render(request, "users/actor.html", {'actor_detail': actor_detail})
"""