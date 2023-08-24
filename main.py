import telebot
import requests
from telebot import types
import openpyxl


TOKEN = '6096937364:AAF83XErtkuYB6bbuDf5R8x2Gp_bTaZkzT4'  # telegram api-key
bot = telebot.TeleBot(TOKEN)  # bot init


def fahrenheit_to_celsius(kelvin):  # function to transfer farengheit to celsius
    celsius = kelvin - 273.15
    return celsius


def get_weather(city_name):  # function to  reqest to openweathermap for receive json array
    api_key = '3b07b96d75a94547fe19c8889a258076'  # openwearhermap api-key
    base_url = f'https://api.openweathermap.org/data/2.5/find?q={city_name}&type=like&APPID={api_key}'  # url form to
    # request

    response = requests.get(base_url)  # variable for request
    data = response.json()  # get lson from request

    if response.status_code == 200 and data['count'] > 0:  # if request is succesful code 200
        city_data = data['list'][0]  # take data from json array
        city = city_data['name']  # take name
        humidity = city_data['main']['humidity']  # take humidity
        weather_description = city_data['weather'][0]['description']  # take weather description
        temperature_f = city_data['main']['temp']  # take temperature
        temperature_c = fahrenheit_to_celsius(temperature_f)  # call function to transfer temperature
        return f"Город: {city.capitalize()}\n" \
               f"Влажность: {humidity}%\n" \
               f"Погода: {weather_description}\n" \
               f"Температура: {temperature_c:.1f}°C"  # base for reponse for user
    else:
        return "Не удалось получить данные о погоде."  # if request is unsuccesful thorw this message


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    item1 = types.KeyboardButton("Кишинев")
    item2 = types.KeyboardButton("Бельцы")
    markup.add(item1, item2)

    bot.reply_to(message, "Привет! Я погодный бот. Выберите город из списка ниже:", reply_markup=markup)


@bot.message_handler(func=lambda message: True, )
def handle_city_choice(message):
    if message.text == "Кишинев":
        city_name = "Chisinau"
    elif message.text == "Бельцы":
        city_name = "Balti"
    else:
        bot.reply_to(message, "Выберите город из предложенных вариантов. ")
        return

    user_name = message.from_user.first_name
    weather_info = get_weather(city_name)
    save_to_excel(user_name, city_name)
    bot.reply_to(message, weather_info)


def save_to_excel(user_name, city_name):
    excel_path = 'users_data.xlsx'
    try:
        wb = openpyxl.load_workbook(excel_path)
        sheet = wb.active
    except FileNotFoundError:
        wb = openpyxl.Workbook()
        sheet = wb.active
        sheet.append(["Имя пользователя", "Выбранный город"])

    sheet.append([user_name, city_name])
    wb.save(excel_path)


bot.polling()
