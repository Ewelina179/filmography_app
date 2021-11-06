import requests
import os

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
        #self.BASE_URL[8:-1] nie wygląda dobrze
        'x-rapidapi-key': self.api_key
        }
        response = requests.request("GET", url=self.build_url(params), headers=headers, params=self.create_querystring(params, data))
        content = response.json()
        return content

    def get_actor_id(self, data):
        actor_id = self.get_data("id", data)
        id = actor_id["d"][0]["id"]
        return id

    def get_actor_info(self, data):
        info = self.get_data("actor_data", self.get_actor_id(data)) # tu warunkować! jeśli id w bazie to z bazy, żeby nie robić niepotrzebnie requestu
        return info

    def get_actor_filmography(self, data):
        filmography = self.get_actor_info(data)["filmography"]
        #print(self.get_actor_info(data)["filmography"])
        lst_of_filmography = []
        for el in filmography:
            if el["category"]=="actress" or el["category"]=="actor":
                lst_of_filmography.append(el["title"]) # gdzie category: actress or actor
        return lst_of_filmography

actor = ActorInfo(os.getenv("API_KEY"))
#x = actor.get_actor_filmography("Felicity Jones")
#y = actor.get_actor_info("Felicity Jones")
#print(x)
#print(y)
