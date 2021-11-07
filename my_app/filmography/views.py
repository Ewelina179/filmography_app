from django.shortcuts import render

from filmography.models import *

def home(request):
    return render(request, "home.html")

def dashboard(request):
    from filmography.get_from_imdb import actor

    # zalogowany user. aktor z formularza
    user = User.objects.get(pk=1)
    print(user)

    # get or create/update
    try:
        obj = Actor.objects.get(fullname='Felicity Jones')
    except Actor.DoesNotExist:
        x = actor.get_actor_filmography("Felicity Jones") # raczej powinno być get_actor_info i uzupełnienie tabeli actor o więcej danych, zapewniających rozróżnienie aktorów o tym samym fullname
        if x:
            obj = Actor(fullname='Felicity Jones')
            obj.save()
    # gdzie trzymać queries i całe metody z nimi powiązane ??? jak napisać klasę?
    # dodanie do bazy aktora tak po prostu - a to znaczy, że może zostać rekord aktora nie przypisany do usera (jest many to many), jeśli np. user skasowany) - zaśmiecanie bazy - jak to rowiązać???
    # gdyby było one to many user aktor to usunięcie sierot rozwiązałoby problem. ale to z góry więcej rekordów
        for el in x:
            print(el)
            try:
                movie = Movie.objects.get(title=el)
            except Movie.DoesNotExist:
                movie = Movie(title=el)
                movie.save()
            actor = Actor.objects.get(fullname='Felicity Jones')
            actor.movies.add(movie)
            actor.save()
    print(obj.fullname)
    print(Actor.objects.get(fullname='Felicity Jones'))
    f = Favourite(user=user, actor=obj, is_favourite=True)
    f.save()
    print(user.actors.all())
    print(obj.user_set.all())
    for el in obj.movies.all():
        print(el.title)

    return render(request, "users/dashboard.html")