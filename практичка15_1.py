from tkinter import *
from urllib.parse import urlencode
from urllib.request import urlopen
import json

def fetch_json(url: str, params: dict) -> dict:
    full_url = f"{url}?{urlencode(params)}"
    with urlopen(full_url, timeout=10) as resp:
        print(full_url)
        return json.loads(resp.read().decode("utf-8"))

def get_weather():
    city = cityField.get()
    geo = fetch_json('https://geocoding-api.open-meteo.com/v1/search', {'name': city, 'count': 1, 'format': 'json', 'language': 'ru'})
    res = geo['results'][0]
    lat, lon = res["latitude"], res["longitude"]
    fullname = f'{res["name"]}, {res["country"]}'
    weather = fetch_json('https://api.open-meteo.com/v1/forecast', {'latitude': lat, 'longitude': lon, 'current_weather': 'true','wind_speed_unit': 'ms', 'hourly': 'relative_humidity_2m'})

    temp = weather["current_weather"]["temperature"]
    wind_speed = weather["current_weather"]["windspeed"]
    humidity = weather['hourly']['relative_humidity_2m'][0]

    info['text'] = f'{fullname}: \n Температура: {temp}°C \n Влажность: {humidity}% \n Ветер: {wind_speed} м/с'

root = Tk()

root['bg'] = '#fafafa'
root.title('Погодное приложение')
root.geometry('350x250')
root.resizable(width=False, height=False)

frame_top = Frame(root, bg='#ffb700', bd=5)
frame_top.place(relx=0.15, rely=0.15, relwidth=0.7, relheight=0.25)

frame_bottom = Frame(root, bg='#ffb700', bd=5)
frame_bottom.place(relx=0.15, rely=0.55, relwidth=0.7, relheight=0.4)

cityField = Entry(frame_top, bg='white', font=30)
cityField.pack()

btn = Button(frame_top, text='Посмотреть погоду', command=get_weather)
btn.pack()

info = Label(frame_bottom, text='Погода в городе', bg='#ffb700', font=40)
info.pack()

root.mainloop()