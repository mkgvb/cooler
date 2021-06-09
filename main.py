import os
import glob
import time
import datetime
import wemo as we
import log
import logging
from weather import weather
from nest import mainNest
import yaml



def main():
    log.setup()
    logging.info("Starting")
    with open("secrets.yml", 'r') as s:
        secrets = yaml.load(s)
    
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')
    wemo = we.wemo()

    #pywemo setup


    
    base_dir = '/sys/bus/w1/devices/'
    try:
        simulate_thermometer=False
        device_folder = glob.glob(base_dir + '28*')[0]
        device_file = device_folder + '/w1_slave'
    except IndexError as e:
        simulate_thermometer=True

    
    def read_temp_raw():
        f = open(device_file, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp():
        if simulate_thermometer:
            logging.warn("Simulating a thermometer")
            return 72.999
        lines = read_temp_raw()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return round(temp_f,3)

    HOT = 76
    COLD = 73

    def calculate_schedule():
        START = datetime.datetime.now().replace(hour=8,minute=0,second=0)
        END = START + datetime.timedelta(hours=24)
        logging.info(f"New schedule: \n \tStart:{START} \n\t End:{END}")
        return (START,END)

    START,END = calculate_schedule()
    w_api = weather.weather_api(secrets["weather_api_key"])
    
    #omg google do you think this is enough stuff
    nest_api = mainNest.nest_api(
        nest_client_id = secrets["nest_client_id"], 
        nest_client_secret = secrets["nest_client_secret"], 
        nest_refresh_token = secrets["nest_refresh_token"], 
        nest_project_id = str(secrets["nest_project_id"]), 
        nest_device_id = secrets["nest_device_id"]
        )

    while True:
        nest = mainNest.Nest(nest_api.get_nest_status())
        HOT = nest.coolF + 1
        COLD = nest.coolF - 2
        temperature_f = read_temp()
        outside_weather = w_api.get_weather()
        logging.info(f"UPSTAIRS   temp={read_temp()}f humidity=??% ac_on={wemo.assumed_on} HOT={HOT} COLD={COLD}")
        logging.info(f"DOWNSTAIRS temp={nest.ambientTemperatureF}f humidity={nest.ambientHumidityPercent}% ac_on={nest.isHvacOn}")
        logging.info(f"OUTSIDE    temp={outside_weather['temp']}f humidity={outside_weather['humidity']}%" )
        logging.info(f"")
        now = datetime.datetime.now()

        if  now > START and now < END:
            if temperature_f > HOT:
                wemo.turnOn()
            elif temperature_f < COLD:
                wemo.turnOff()
        else:
            logging.info("Not active time")
            wemo.turnOff()

        if now > END:
            logging.info("Recalculate schedule")
            START,END = calculate_schedule()

        time.sleep(10)

if __name__ == "__main__":
    main()
