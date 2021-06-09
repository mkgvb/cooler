import pywemo
import datetime
import logging

class wemo():
    def __init__(self, _url='wemo.lc') -> None:
        
        url = pywemo.setup_url_for_address(_url,None)
        logging.info(f" Wemo at {url}")

        self.device = pywemo.Insight
        self.device = pywemo.discovery.device_from_description(url)
        self.control_cooldown = datetime.datetime.now()
        self.assumed_on = self.device.get_state()

    def cooldown_handler(self):
        now = datetime.datetime.now()
        if now > self.control_cooldown:
            logging.info(f"{now} > {self.control_cooldown}")
            self.control_cooldown = datetime.datetime.now() + datetime.timedelta(minutes=10)
            logging.info(f"Control cooldown reset to {self.control_cooldown}")
            return True
        return False

    def isOn(self) -> bool:
        _ison = self.device.get_state()
        self.assumed_on = bool(_ison)
        return bool(_ison)

    def turnOn(self):
        if self.cooldown_handler():
            self.device.on()
            self.assumed_on = True
            logging.info("Turned on")

    def turnOff(self):
        if self.cooldown_handler():
            self.device.off()
            self.assumed_on = False
            logging.info("Turned off")
