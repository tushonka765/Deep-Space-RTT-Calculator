import telebot
from telebot import types
import math


SPEED_OF_LIGHT_KMS = 299792.458 
BOT_TOKEN = 'PAST YOUR TOKEN'

bot = telebot.TeleBot(BOT_TOKEN)

user_data = {} 



def seconds_to_hms(seconds):
    """Конвертирует общее количество секунд в формат ЧЧ:ММ:СС или дни."""
    if seconds < 60:
        return f"{seconds:.2f} секунд"
    elif seconds < 3600: #меньше часа
        minutes = math.floor(seconds / 60)
        secs = seconds % 60
        return f"{minutes} минут {secs:.2f} секунд"
    elif seconds < 86400: #меньше суток
        hours = math.floor(seconds / 3600)
        minutes = math.floor((seconds % 3600) / 60)
        secs = seconds % 60
        return f"{hours} ч {minutes} мин {secs:.2f} сек"
    else: #больше суток
        days = math.floor(seconds / 86400)
        remaining_seconds = seconds % 86400
        hours = math.floor(remaining_seconds / 3600)
        minutes = math.floor((remaining_seconds % 3600) / 60)
        secs = remaining_seconds % 60
        return f"{days} дней, {hours} ч {minutes} мин (или {seconds / 86400:.2f} дней)"



@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """Обработчик команд /start и /help."""
    welcome_text = (
        "Привет! Я бот для расчета времени ответа радиосообщения между Землей и другой планетой (туда и обратно).\n\n"
        "Радиоволны распространяются со скоростью света.\n\n"
        "Чтобы начать, отправьте команду /calculate или просто нажмите кнопку ниже."
    )
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn_calc = types.KeyboardButton('/calculate')
    markup.add(btn_calc)
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(commands=['calculate'])
def start_calculation(message):
    """Начало процесса расчета."""
    chat_id = message.chat.id
    user_data[chat_id] = {'step': 1} 
    
    msg = bot.send_message(chat_id, 
                           "Введите расстояние до планеты/объекта. "
                           "Укажите число, а затем единицу измерения (например, '150 млн км', '5 а.е.', '4.2 св. года').")
    bot.register_next_step_handler(msg, get_distance)

def get_distance(message):
    """Получение и обработка расстояния от пользователя."""
    chat_id = message.chat.id


    if message.text.startswith('/'):
        bot.send_message(chat_id, "Вы прервали расчет. Начните снова с /calculate.")
        if chat_id in user_data:
             del user_data[chat_id]
        return 
  
 
            
    try:
        text = message.text.lower().replace(',', '.').strip()
        distance_km = 0.0

        
        if 'млн км' in text or 'миллионов км' in text:
            num_str = text.split('млн км')[0].strip()
            num = float(num_str)
            distance_km = num * 1e6
            unit = 'млн км'
            
        elif 'млрд км' in text or 'миллиардов км' in text:
            num_str = text.split('млрд км')[0].strip()
            num = float(num_str)
            distance_km = num * 1e9
            unit = 'млрд км'


        elif 'а.е.' in text or 'ае' in text:
            AE_TO_KM = 149597870.7
            num_str = text.split('а.е.')[0].strip() if 'а.е.' in text else text.split('ае')[0].strip()
            num = float(num_str)
            distance_km = num * AE_TO_KM
            unit = 'а.е.'

        elif 'св. год' in text or 'св год' in text or 'световых лет' in text:
            LY_TO_KM = 9.461e12 
            num_str = text.split('св.')[0].strip() if 'св.' in text else text.split('световых')[0].strip()
            num = float(num_str)
            distance_km = num * LY_TO_KM
            unit = 'св. лет'

        elif 'км' in text:
            num_str = text.split('км')[0].strip()
            num = float(num_str)
            distance_km = num
            unit = 'км'
            
        else:
            num = float(text)
            distance_km = num
            unit = 'км'

        if distance_km <= 0:
            raise ValueError("Расстояние должно быть положительным числом.")

        time_one_way_sec = distance_km / SPEED_OF_LIGHT_KMS
        
        time_total_sec = time_one_way_sec * 2

        time_one_way_hms = seconds_to_hms(time_one_way_sec)
        time_total_hms = seconds_to_hms(time_total_sec)
        
        result_text = (
            f"Расчет для расстояния: {num:,.2f} {unit.upper()}\n\n"
            f"Скорость радиосигнала (свет): {SPEED_OF_LIGHT_KMS:,.2f} км/с\n\n"
            f"Время в одну сторону:\n"
            f"  {time_one_way_hms}\n\n"
            f"Общее время ответа (Туда и обратно):\n"
            f"  {time_total_hms}\n\n"
        ).replace(',', ' ') 

        bot.send_message(chat_id, result_text, parse_mode='Markdown')



    except ValueError:
        bot.send_message(chat_id, 
                         "Ошибка: Введите корректное число и единицу измерения. "
                         "Попробуйте снова. Пример: 225 млн км, 5.2 а.е., 4.2 св. года.")
        bot.register_next_step_handler(message, get_distance)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        bot.send_message(chat_id, "Произошла непредвиденная ошибка. Попробуйте /calculate еще раз.")
        
    finally:
        if chat_id in user_data:
            del user_data[chat_id] 



print("Бот запущен...")

while True:
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Ошибка polling: {e}")
        import time
        time.sleep(5)
        
bot.infinity_polling()

