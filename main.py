import editdistance
from random import choice
from logic import BOT_CONFIG, quotes
import telebot
from mistralai import Mistral

import dotenv
import os
dotenv.load_dotenv()

client = telebot.TeleBot(os.getenv("TELEGRAM_API_KEY"))

def ask_gpt(content):
    client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))
    chat_response = client.chat.complete(
        model= "mistral-large-latest",
        messages = [
            {
                "role": "user",
                "content": content,
            },
        ]
    )
    return chat_response.choices[0].message.content



def clean(text):
    output_text = ''
    for s in text.lower():
        if s in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя abcdefghijklmnopqrstuvwxyz':
            output_text += s
    return output_text

def get_intent(text):
    for intent in BOT_CONFIG['intents'].keys():
        for example in BOT_CONFIG['intents'][intent]['examples']:
            text1 = clean(example)
            text2 = clean(text)
            if editdistance.eval(text1, text2) / max(len(text1), len(text2)) < 0.4:
                return intent
    return 'Не удалось определить интент'

def bot(text):
    intent = get_intent(text)
    if intent != 'Не удалось определить интент':
        return choice(BOT_CONFIG['intents'][intent]['responces'])
    else:
        return 'Извините, я ничего не понял, я просто глупый бот'
    


@client.message_handler(content_types = ['text'])
def lalala(message):
    
    if message.text[0:4] == '@gpt':
        a = message.text.replace('@gpt','')
        client.send_message(message.chat.id, ask_gpt(a), parse_mode='HTML')
    elif message.text == 'получить цитату':
        client.send_message(message.chat.id,choice(quotes))
    else:
        client.send_message(message.chat.id,bot(message.text))

if __name__ == '__main__':
    client.infinity_polling()