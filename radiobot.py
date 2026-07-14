import telebot
from telebot import types
import math
import re


SPEED_OF_LIGHT_KMS = 299792.458 
BOT_TOKEN = 'PASTE_YOUR_TOKEN'


bot = telebot.TeleBot(BOT_TOKEN)

user_data = {} 



def seconds_to_hms(seconds):
    """Converts the total number of seconds to the format Hours:Minutes:Seconds or days."""
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600: #less than hour
        minutes = math.floor(seconds / 60)
        secs = seconds % 60
        return f"{minutes} minutes {secs:.2f} seconds"
    elif seconds < 86400: #less than 1 day
        hours = math.floor(seconds / 3600)    
        minutes = math.floor((seconds % 3600) / 60)
        secs = seconds % 60
        return f"{hours} hours {minutes} minutes {secs:.2f} seconds"
    else: #more than 1 day
        days = math.floor(seconds / 86400)
        remaining_seconds = seconds % 86400
        hours = math.floor(remaining_seconds / 3600)
        minutes = math.floor((remaining_seconds % 3600) / 60)
        secs = remaining_seconds % 60
        return f"{days} days, {hours} hours {minutes} minutes (or {seconds / 86400:.2f} days)"



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Command handler /start and /help."""
    welcome_text = (
        "Hi! I am a bot for calculating the response time of a radio message between Earth and another planet (round trip).\n\n"
        "To get started, send the /calculate command or just click the button below."
    )
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_calc = types.KeyboardButton('/calculate')
    markup.add(btn_calc)
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(commands=['calculate'])
def start_calculation(message):
    """The beginning of the calculation process."""
    chat_id = message.chat.id    
    msg = bot.send_message(chat_id, 
                           "Enter the distance to the planet/object.\n"
                           "Specify the number and then the unit of measurement \n(for example, '150 million km', '5 au', '4.2 ly').")
    bot.register_next_step_handler(msg, get_distance)

def get_distance(message):
    """Receiving and processing distance from the user."""
    chat_id = message.chat.id

    if message.text.startswith('/'):
        bot.send_message(chat_id, "You have interrupted the calculation. Start again with /calculate.")
        if chat_id in user_data:
             del user_data[chat_id]
        return
            
    try:
        text = message.text.lower().replace(',', '.').strip()
        
        match = re.search(r'[\d\.]+', text)
        if not match:
            raise ValueError("Number not found")
            
        num = float(match.group())
        distance_km = 0.0


        if any(x in text for x in ['mm km', 'million km', 'mil km']):
            distance_km = num * 1e6
            unit = 'million km'
            
        elif any(x in text for x in ['bil km', 'billion km', 'bill km', 'bln km', 'b km']):
            distance_km = num * 1e9
            unit = 'billion km'

        elif any(x in text for x in ['ly', 'l.y.', 'light year', 'lyr']):
            LY_TO_KM = 9.461e12
            distance_km = num * LY_TO_KM
            unit = 'ly'

        elif any(x in text for x in ['au', 'astronomical unit', 'ua']):
            AU_TO_KM = 149597870.7
            distance_km = num * AU_TO_KM
            unit = 'au'

        elif 'km' in text:
            distance_km = num
            unit = 'km'
            
        else:
            distance_km = num
            unit = 'km'

        if distance_km <= 0:
            raise ValueError("The distance must be a positive number.")

        time_one_way_sec = distance_km / SPEED_OF_LIGHT_KMS
        time_total_sec = time_one_way_sec * 2

        time_one_way_hms = seconds_to_hms(time_one_way_sec)
        time_total_hms = seconds_to_hms(time_total_sec)
        
        result_text = (
            f"Calculation for distance: {num:,.2f} {unit.upper()}\n\n"
            f"The speed of the radio signal (light): {SPEED_OF_LIGHT_KMS:,.2f} km/s\n\n"
            f"One-way time:\n"
            f"  {time_one_way_hms}\n\n"
            f"Total response time (round trip):\n"
            f"  {time_total_hms}\n\n"
        )

        bot.send_message(chat_id, result_text, parse_mode='Markdown')

    except ValueError:
        bot.send_message(chat_id,  
                         "Error: Enter the correct number and unit of measurement. "
                         "Try again. Example: 225 million km, 5.2 au, 4.2 ly")
        bot.register_next_step_handler(message, get_distance)

    except Exception as e:
        print(f"An error has occurred: {e}")
        bot.send_message(chat_id, "An unexpected error has occurred. Try /calculate again.")
        
    finally:
        if chat_id in user_data:
            del user_data[chat_id] 
    




print("The bot is running...")

while True:
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Error polling: {e}")
        import time
        time.sleep(5)
