from tkinter import *
from PIL import ImageTk, Image
import requests

url = 'https://api.openweathermap.org/data/2.5/weather'
api_key = 'e7d3d96a313812a4dcd17266f0fcee82'
icon_url = 'https://openweathermap.org/img/wn/{}@2x.png'

def getWeather(city):
    params = {'q': city, 'appid': api_key, 'lang': 'tr'}
    data = requests.get(url, params=params).json()
    if data['cod'] == 200:
        city = data['name'].capitalize()
        country = data['sys']['country']
        temp = int(data['main']['temp'] - 273.15)
        icon = data['weather'][0]['icon']
        condition = data['weather'][0]['description']
        return city, country, temp, icon, condition
    else:
        return None

def main():
    city = cityEntry.get()
    weather = getWeather(city)
    if weather:
        locationLabel['text'] = '{}, {}'.format(weather[0], weather[1])
        tempLabel['text'] = '{}°C'.format(weather[2])
        conditionLabel['text'] = weather[4].capitalize()
        icon_img = ImageTk.PhotoImage(Image.open(requests.get(icon_url.format(weather[3]), stream=True).raw))
        iconLabel.configure(image=icon_img)
        iconLabel.image = icon_img  # Keep a reference to avoid garbage collection
    else:
        locationLabel['text'] = 'Şehir bulunamadı'
        tempLabel['text'] = ''
        conditionLabel['text'] = ''
        iconLabel.configure(image='')

app = Tk()
app.geometry('350x500')
app.title('Hava Durumu')
app.configure(bg='#003366')  # Dark blue background

cityEntry = Entry(app, justify='center', font=("Arial", 14), bg='#cccccc')
cityEntry.pack(fill=BOTH, ipady=10, padx=20, pady=20)
cityEntry.focus()

search = Button(app, text='Arama', font=("Arial", 15), command=main, bg='#007acc', fg='white')
search.pack(fill=BOTH, ipady=10, padx=20)

iconLabel = Label(app, bg='#003366')
iconLabel.pack(pady=10)

locationLabel = Label(app, font=("Arial", 25), bg='#003366', fg='white')
locationLabel.pack()

tempLabel = Label(app, font=("Arial", 35, 'bold'), bg='#003366', fg='white')
tempLabel.pack()

conditionLabel = Label(app, font=("Arial", 20), bg='#003366', fg='white')
conditionLabel.pack(pady=10)

app.mainloop()
