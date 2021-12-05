import requests
import os

from my_app.sitesettings import API_KEY

class ActorInfo:
    BASE_URL = "https://imdb8.p.rapidapi.com/"
    
    def __init__(self, api_key):
        self.api_key = api_key

    def build_url(self, params):
        if params == "id":
            url = self.BASE_URL + "auto-complete"
        elif params == "actor_data":
            url = self.BASE_URL + "actors/get-all-filmography"
        return url

    def create_querystring(self, params, data):
        print(params, data)
        if params == "id":
            querystring = {"q":f'{data}'}
        elif params == "actor_data":
            querystring = {"nconst":f"{data}"}
        return querystring

    def get_data(self, params, data):
        headers = {
        'x-rapidapi-host': "imdb8.p.rapidapi.com",
        'x-rapidapi-key': self.api_key
        }
        response = requests.request("GET", url=self.build_url(params), headers=headers, params=self.create_querystring(params, data))
        content = response.json()
        return content

    def get_actors_ids(self, fullname):
        data = []
        actor_id = self.get_data("id", fullname)
        print(actor_id)
        print(self.api_key)
        id = actor_id["d"]
        for el in id:
            if el.get("i"):
                actor = {}
                actor = {"name": el["l"], "id": el["id"], "image": el['i']["imageUrl"]}
                data.append(actor)
        print(data) # !
        return data
    
    def get_actor_info(self, id):
        info = self.get_data("actor_data", id)
        return info

    def get_actor_filmography(self,id):
        filmography = self.get_actor_info(id)["filmography"]
        lst_of_filmography = []
        for el in filmography:
            if el["category"]=="actress" or el["category"]=="actor":
                movie = {}
                movie = {"title": el["title"], "id": el["id"]}
                lst_of_filmography.append(movie)
        return lst_of_filmography
