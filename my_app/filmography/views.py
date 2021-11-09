from django.shortcuts import render, redirect
from .forms import ActorForm
from filmography.models import *
from filmography.get_from_imdb import actor

def home(request):
    return render(request, "home.html")

def dashboard(request):
    
    user = User.objects.get(pk=1)
    print(user)
        # gdzie trzymać queries i całe metody z nimi powiązane ??? jak napisać klasę?
        # dodanie do bazy aktora tak po prostu - a to znaczy, że może zostać rekord aktora nie przypisany do usera (jest many to many), jeśli np. user skasowany) - zaśmiecanie bazy - jak to rowiązać???
    print("Tutaj ma być link do wyszukiwania(?), do konta usera i lista ulubionych do edycji i podglądu")
    return render(request, "users/dashboard.html")

def get_actor(request):
    print("Hej, tu powinien być formularz!")
    from filmography.get_from_imdb import actor
    cont = {}
    if request.method == 'POST':
        form = ActorForm(request.POST)
        if form.is_valid():
            actor_form = form.cleaned_data['actor']
            print(actor_form)
            try:
                lst_of_actors_with_the_same_fullname = actor.get_actors_ids(actor_form) # musi dać listę wyników dla tego
                for el in lst_of_actors_with_the_same_fullname:
                    actor = {"name": el["name"], "id": el["id"], "image": el["image"]}
                    cont.update(actor)
                    print(cont)
            except:
                print("Wprowadzono błędne dane do formularza. Nie ma aktora/aktorki.")
            return redirect("actors", lst_of = cont)
    else:
        form = ActorForm()
    return render(request, 'users/search.html', {'form': form})

def actors(request, lst_of):# to co wpada to lista. niech ją wyświetli. każdy rekord to hiperłącze do kolejnej pds
    for el in lst_of:
        print(el)
    return render(request, 'users/lst_of_actors.html')

# to z hiperłącza muszą przyjść dane - które fullname
def actor_detail(request, nm):
    print(nm) # nie mogę przyjąć id, nie wiem czemu
    #nm = "nm0000148"
    from filmography.get_from_imdb import actor
    user = User.objects.get(pk=1)
    try:
        obj = Actor.objects.get(nm=nm)
    except Actor.DoesNotExist:
        x = actor.get_actor_filmography("nm0000148") # SET API KEY!!!!!!!!!!!!!!!!!!!!!!!!!!!1
        obj = Actor(nm=nm)
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
    #f = Favourite(user=user, actor=obj, is_favourite=True)
    #f.save()
    print(user.actors.all())
    print(obj.user_set.all())
    for el in obj.movies.all():
        print(el.title)
    # znaleźć tego usera aktora ulubionego i jego filmy wypisać - NIE ZROBIONE
    actor_detail = "tutaj będą filmy i inne kwestie dotyczące konkretnego aktora"
    return render(request, "users/actor.html", {'actor_detail': actor_detail})