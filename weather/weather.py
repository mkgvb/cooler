import requests, json
import datetime
import logging


class weather_api():

    def __init__(self, _api_key):

        api_key = _api_key
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        zipCode = "23454"
        self.complete_url = base_url + "appid=" + api_key + "&zip=" + zipCode + '&units=imperial'
        self.api_cooldown = datetime.datetime.now()
        self.last_data = { "temp": 0, "pressure":0, "humidity": 0}
        print(self.complete_url)
    

    def get_weather(self):
        if datetime.datetime.now() < self.api_cooldown:
            return self.last_data
        
        logging.debug("Access API")
        self.api_cooldown = datetime.datetime.now() + datetime.timedelta(minutes=1)
        response = requests.get(self.complete_url)
        x = response.json()
        
        if x["cod"] != "404":
        
            # store the value of "main"
            # key in variable y
            self.last_data = x["main"]
            return self.last_data
        
        else:
            print(" City Not Found ")

if __name__ == "__main__":
    w = weather_api()
    print( w.get_weather())