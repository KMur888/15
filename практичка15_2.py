from tkinter import *
from urllib.parse import urlencode
from urllib.request import urlopen
import json

API_KEY = '5ae2e3f221c38a28845f05b6a6a8154a98cdad20bb3609b7567f3340'

def fetch_json(url: str, params: dict) -> dict:
    full_url = f"{url}?{urlencode(params)}"
    with urlopen(full_url, timeout=10) as resp:
        print(full_url)
        return json.loads(resp.read().decode("utf-8"))

def get_attractions():
    city = cityField.get()

    geo = fetch_json('https://api.opentripmap.com/0.1/ru/places/geoname', {'name': city,'format': 'json', 'apikey': API_KEY})

    lat = geo['lat']
    lon = geo['lon']

    places_params = {'lat': lat,'lon': lon,'radius': 5000,'kind': 'interesting','format': 'json', 'apikey': API_KEY, 'limit': 10}

    places_url = f"https://api.opentripmap.com/0.1/ru/places/radius&quot;

    places = fetch_json(places_url, places_params)

    attractions = []
    for feature in places['features'][:2]:
        props = feature.get('properties', {})
        name = props.get('name', 'Без названия')
        kinds = props.get('kinds', '').split(',')[0] if props.get('kinds') else 'объект'
        attractions.append(f"• {name} ({kinds})")

    result_text = f"{city}:\n\n" + "\n".join(attractions)
    info['text'] = result_text

root = Tk()
root['bg'] = '#fafafa'
root.title('Достопримечательности города')
root.geometry('350x300')
root.resizable(width=False, height=False)

frame_top = Frame(root, bg='#ffb700', bd=5)
frame_top.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.3)

cityField = Entry(frame_top, bg='white', font=('Arial', 14))
cityField.pack(pady=10, padx=10, fill='x')

btn = Button(frame_top, text='Найти достопримечательности', command=get_attractions, font=('Arial', 12), bg='#fafafa')
btn.pack(pady=5)

frame_bottom = Frame(root, bg='#ffb700', bd=5)
frame_bottom.place(relx=0.1, rely=0.45, relwidth=0.8, relheight=0.45)

info = Label(frame_bottom, bg='#ffb700', font=('Arial', 11), wraplength=280, justify='left')
info.pack(expand=True, fill='both', padx=10, pady=10)

root.mainloop()