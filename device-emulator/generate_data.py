import random
import json
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
from tqdm import tqdm


SERIAL_NUMBER = "1"
COORDINATES = (47.224860, 39.702285)
LIGHTING_CLASS = "B1"
START_DATETIME = datetime.now() - relativedelta(months=6)
DEFAULT_DIMMING = 0

WEATHER_CHOISES = {
    "CLEAR": 'clear',
    "CLOUDS": "clouds",
    "RAIN": 'rain',
    "FOG": 'fog'
}

MAX_CARS_COUNT = 80
MAX_PEDS_COUNT = 40

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)

def hour_generator(date):
    current = datetime(date.year, date.month, date.day, 0, 0, 0)
    end = current + timedelta(days=1)
    while current < end:
        yield current
        current += timedelta(hours=1)


def generate_data(datetime: datetime, weather: str):
    ambient_light_multiplier = 1
    ambient_light_edges = [0, 200]

    cars_multiplier = 1
    cars_edges = [0, 10]

    traffic_speed_multiplier = 1
    traffic_speed_edges = (10, 60)

    peds_multiplier = 1
    peds_edges = [0, 5]

    hour = datetime.hour

    if weather == WEATHER_CHOISES.get("CLOUDS"):
        ambient_light_multiplier -= 0.1
        peds_multiplier -= 0.1
    elif weather == WEATHER_CHOISES.get("RAIN"):
        cars_multiplier -= 0.1
        ambient_light_multiplier -= 0.2
        peds_multiplier -= 0.5
        traffic_speed_multiplier -= 0.3
    elif weather == WEATHER_CHOISES.get("FOG"):
        cars_multiplier -= 0.3
        ambient_light_multiplier -= 0.3
        peds_multiplier -= 0.3
        traffic_speed_multiplier -= 0.4

    if 6 <= hour <= 8:
        ambient_light_edges = (6000, 10000)
    elif 8 <= hour <= 9:
        ambient_light_edges = (10000, 20000)
    elif 9 <= hour <= 10:
        ambient_light_edges = (20000, 40000)
    elif 10 <= hour <= 12:
        ambient_light_edges = (40000, 80000)
    elif 12 <= hour <= 14:
        ambient_light_edges = (80000, 100000)
    elif 14 <= hour <= 16:
        ambient_light_edges = (10000, 50000)
    elif 16 <= hour <= 18:
        ambient_light_edges = (200, 10000)

    if 7 <= hour <= 9 or 17 <= hour <= 19:
        cars_edges = [40, MAX_CARS_COUNT]
        peds_edges = [10, MAX_PEDS_COUNT]
    elif 0 <= hour <= 5:
        cars_edges = [0, 10]
        peds_edges = [0, 5]
    else:
        cars_edges = [10, 40]
        peds_edges = [5, 20]

    cars = round(random.randint(cars_edges[0], cars_edges[1]) * cars_multiplier)
    peds = round(random.randint(peds_edges[0], peds_edges[1]) * peds_multiplier)

    speed = (random.uniform(traffic_speed_edges[0], traffic_speed_edges[1]) if cars > 0 else 0) * traffic_speed_multiplier
    traffic_density = min(cars / MAX_CARS_COUNT, 1.0)
    pedestrian_density = min(peds / MAX_PEDS_COUNT, 1.0)

    ambient_light = random.uniform(ambient_light_edges[0], ambient_light_edges[1]) * ambient_light_multiplier

    return {
        "timestamp": datetime.isoformat(),
        "serial_number": SERIAL_NUMBER,
        "latitude": COORDINATES[0],
        "longitude": COORDINATES[1],
        "car_count": cars,
        "traffic_speed": round(speed, 2),
        "traffic_density": round(traffic_density, 2),
        "pedestrian_count": peds,
        "pedestrian_density": round(pedestrian_density, 2),
        "ambient_light": round(ambient_light),
        "dimming_level": DEFAULT_DIMMING,
        "lighting_class": LIGHTING_CLASS,
        "lamp_power": DEFAULT_DIMMING * 1.5,
        "weather": weather
    }

def get_day_weather():
    values = [WEATHER_CHOISES.get("CLEAR"), WEATHER_CHOISES.get("CLOUDS"), WEATHER_CHOISES.get("RAIN"), WEATHER_CHOISES.get("FOG")]
    weights = [45, 30, 20, 5]

    first_weather = random.choices(values, weights=weights, k=1)[0]
    second_weather = random.choices(values, weights=weights, k=1)[0]
    first_weather_start_hour = random.randint(0, 23)

    result_array = []

    if (first_weather_start_hour + 12 > 23):
        for i in range(24): 
            if (first_weather_start_hour <= i <= 23) or (0 <= i < (first_weather_start_hour + 12) % 24):
                result_array.append(first_weather)
            else: 
                result_array.append(second_weather)
    else:   
        for i in range(24):
            if first_weather_start_hour <= i < first_weather_start_hour + 12:
                result_array.append(first_weather)
            else:
                result_array.append(second_weather)

    return result_array

def generate_last_three_monthes_data():
    now = datetime.now()
    start_date = now - relativedelta(months=3)
    three_monthes_data = []

    for curr_date in tqdm(daterange(start_date, now)):
        day_weather = get_day_weather()
        for curr_hour_date in tqdm(hour_generator(curr_date)):
            current_weather = day_weather[curr_hour_date.hour]
            data = generate_data(curr_hour_date, current_weather)
            three_monthes_data.append(data)


    return three_monthes_data

def main():
    generated_data = generate_last_three_monthes_data()
    # json_data = json.dumps(generated_data, indent=2)
    with open('data.json','w+') as buf:
        json.dump(generated_data,buf)

if __name__ =='__main__':
    main()