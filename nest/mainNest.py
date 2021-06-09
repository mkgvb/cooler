#https://developers.google.com/nest/device-access/authorize
import time
import requests
import logging
access_token = "bad-token"

def cToF(_celsius):
    return round(_celsius * 9/5 + 32,3)

class Nest():
    def __init__(self, _dict: dict):
        self.update(_dict)

    def update(self, _dict: dict):
        self.ambientHumidityPercent = _dict["sdm.devices.traits.Humidity"]["ambientHumidityPercent"]
        self.mode = _dict["sdm.devices.traits.ThermostatMode"]["mode"]
        self.ambientTemperatureF = cToF(_dict["sdm.devices.traits.Temperature"]["ambientTemperatureCelsius"])
        self.isHvacOn = False if _dict["sdm.devices.traits.ThermostatHvac"]["status"] == "OFF" else True
        self.coolF, self.heatF = 0,0
        if "COOL" in self.mode:
            self.coolF = cToF(_dict["sdm.devices.traits.ThermostatTemperatureSetpoint"]["coolCelsius"])
        if "HEAT" in self.mode:
            self.heatF = cToF(_dict["sdm.devices.traits.ThermostatTemperatureSetpoint"]["heatCelsius"])

class nest_api():
    def __init__(self, nest_client_id, nest_client_secret, nest_refresh_token, nest_project_id, nest_device_id):
        self.access_token = "Bad-token"
        self.nest_client_id = nest_client_id
        self.nest_client_secret=nest_client_secret
        self.nest_refresh_token=nest_refresh_token
        self.nest_project_id = nest_project_id
        self.nest_device_id = nest_device_id


    def get_access_token(self):
        new_token_params = dict(
            client_id=self.nest_client_id,
            client_secret=self.nest_client_secret,
            refresh_token=self.nest_refresh_token,
            grant_type="refresh_token"
        )
        print(new_token_params)
        token = requests.post(url="https://www.googleapis.com/oauth2/v4/token", params=new_token_params)
        self.access_token = token.json()['access_token']
        logging.info(f"Got nest access_token {self.access_token}")

    def get_nest_status(self):
        #project_id here https://console.nest.google.com/device-access/project-list
        url = f"https://smartdevicemanagement.googleapis.com/v1/enterprises/{self.nest_project_id}/devices/{self.nest_device_id}"
        headers = {
            "Content-Type": "application/json", 
            "Authorization": f"Bearer {self.access_token}"
        }
        req = requests.get(url=url,headers=headers, timeout=5)
        while req.status_code != 200:
            if req.status_code == 404:
                logging.error(f"404 Tried go to {url} headers={headers}")
                break
            if req.status_code == 401:
                print("401 bad token? trying a new one")
                self.get_access_token()
                headers["Authorization"] = f"Bearer {self.access_token}"
                #print(headers)
                req = requests.get(url=url,headers=headers)
                time.sleep(1)
        return req.json()['traits']


