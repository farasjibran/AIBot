import myToken
import telebot
import pyowm
import pyowm.exceptions
import emojis
import RPi.GPIO as GPIO
from gpiozero import LED
from news import get_article
from weather import get_forecast
from pyowm.exceptions import api_response_error
from telebot import apihelper
from telebot import types

# Setting Lampu
lampu = 4
lPin = LED(2)

# Setting GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(lampu, GPIO.OUT)
GPIO.output(lampu, GPIO.LOW)

# TOKEN
TOKEN = myToken.TOKEN

# BOT
MyBot = telebot.TeleBot(TOKEN)

# Create A Class
class myBot:
    def __init__(self):
        self.message
        
# Message START        
@MyBot.message_handler(commands=['start'])
def start(message):
    teks = myToken.KALIMAT + " I was created by @Farasjibran. I am still in development. if you have suggestions and criticisms, please chat privately to my developer." +\
           "\n\n Available features: " + "\n - See the Latest News 'Via BBC' " + "\n - See Today's Weather" + "\n Turn On And Turn Off The Lamp" + "\n\n Available commands:" + "\n - /start to start the bot" +\
           "\n - /help to ask for help if trouble" + "\n - /berita to see the latest news" + "\n - /cuaca to see today's weather" + "\n - /hidupkan to turn on the lamp" + "\n - /matikan to turn off the lamp"
    MyBot.reply_to(message, teks)
    
# Message HELP  
@MyBot.message_handler(commands=['help'])
def help_command(message):
    teks = emojis.encode(":pushpin: This is for help : \n\n Available features: ") + "\n - See the Latest News 'Via BBC' " + "\n - See Today's Weather" + "\n\n Available commands:" + "\n - /start to start the bot" +\
           "\n - /help to ask for help if trouble" + "\n - /berita to see the latest news" + "\n - /cuaca to see today's weather" + "\n - /hidupkan to turn on the lamp" + "\n - /matikan to turn off the lamp"
    MyBot.reply_to(message, teks)
    
# Message BERITA  
@MyBot.message_handler(commands=['berita'])
def command_news(message):
    MyBot.send_message(message.chat.id, emojis.encode(':book: Berita Terbaru Sumber (BBC):\n'))
    MyBot.send_message(message.chat.id, get_article(), parse_mode='HTML')
    
# Message CUACA
@MyBot.message_handler(commands=['cuaca'])
def command_weather(message):
    sent = MyBot.send_message(message.chat.id, emojis.encode(":office: Masukkan pilihan kota \n:mag: Dengan format :  Jakarta atau depok"))
    MyBot.register_next_step_handler(sent, send_forecast)
    
def send_forecast(message):
    try:
        get_forecast(message.text)
    except pyowm.exceptions.api_response_error.NotFoundError:
        MyBot.send_message(message.chat.id, "❌ Tempat yang anda pilih salah, Silahkan coba lagi!")
    forecast = get_forecast(message.text)
    MyBot.send_message(message.chat.id, forecast)
    
# Message Lampu On    
@MyBot.message_handler(commands=['hidupkan'])
def on_lamp(message):
    GPIO.output(lampu, GPIO.HIGH)
    lPin.on()
    MyBot.send_message(message.chat.id, emojis.encode(':bulb: Lampu Sudah Menyala'))
    
# Message Lampu Off    
@MyBot.message_handler(commands=['matikan'])
def off_lamp(message):
    GPIO.output(lampu, GPIO.LOW)
    lPin.off()
    MyBot.send_message(message.chat.id, emojis.encode(':new_moon: Lampu Sudah Mati'))
    
    
print("-- Bot sedang berjalan --")
MyBot.polling(none_stop=True)