import json 
import requests
# from .code import weather_report
import time
import urllib, urllib2
from dictionary import dictionary
from weather import weather_report
from msg import send_sms




TOKEN = "<your-teleram-bot-token>"
# TOKEN = "424627845:AAHppocG8Mrr7ulGYA0hLVS33z8X-ffKGxc"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)


def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


# def get_updates():
#     url = URL + "getUpdates"
#     # url = URL + "getme"
#     js = get_json_from_url(url)
#     return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    name = updates["result"][last_update]["message"]["from"]["first_name"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id, name)


def send_message(text, chat_id, name):
    if 'weather' in text:
        place = text.split(' ')[0]
        data = weather_report(place)
        if data[1] == True:
            msg = """
            {} weather status
            temperature: {}C
            status: {}
            wind: {}
            humidity: {}
            """.format(str(data[0]['plc']), str(data[0]['temp']), str(data[0]['status']), str(data[0]['wind']), str(data[0]['hm']))
        else:
            msg = "Weather report for {} not found!".format(place)
    elif text in ['/help', '/Help', '/HELP']:
        msg = """
        Available Commands:
      1. 'place-name' weather
      2. 'word' meaning
      3. /sms <message>@<number>
      4. /help
      5. /start
        """
    elif 'meaning' in text:
        if len(text.split(' ')) == 2:
            if dictionary(text.split(' ')[0])[0] == 200:
                meaning = dictionary(text.split(' ')[0])[1]
                msg = """
                {} : 
                {}
                """.format(text.split(' ')[0], meaning[0])
            else:
                msg = "sorry that word could not be found"
        else:
            msg = "please use the format '<word> meaning', type /help for more."

    elif '/start' in text:
        msg = "Welcome {} to AI Assistant, I am here to help you, if you are new type '/help' for available commands".format(name)

    elif '/sms' in text:
        data = text.split("@")
        sms = data[0][5:]
        number = data[1]
        if len(sms) > 110:
            msg = "the message length should not exceed 120"
        elif len(number) != 10:
            msg = "the mobile number should be of 10 digits, don't use +91."
        else:
            s = 'from {} using AI BOT : {}'.format(name, sms)
            status = send_sms(s, number)
            if status == 200:
                msg = "Your sms successfully sent to {}".format(number)
            else:
                msg = "Sorry, your sms was not sent" 
    else: 
        msg = "wrong command type '/help' for available commands"
    
    url = URL + "sendMessage?text={}&chat_id={}".format(msg, chat_id)
    print get_url(url)
    
# print get_updates()
# text, chat = get_last_chat_id_and_text(get_updates())
# send_message(text, chat)

# def main():
#     last_textchat = (None, None, None)
#     while True:
#         # print "called"
#         text, chat, name = get_last_chat_id_and_text(get_updates())
#         if (text, chat, name) != last_textchat:
#             text = urllib.parse.quote_plus(text)
#             send_message(text, chat, name)
#             last_textchat = (text, chat, name)
#         time.sleep(0.5)


def reply(updates):
    for update in updates["result"]:
        try:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]
            name = update["message"]["from"]["first_name"]
            send_message(text, chat, name)
        except Exception as e:
            print(e)


def main():
    with open('last_id.txt', 'rb') as last_id:
        last_update_id = int(last_id.read())
    # last_update_id = None
    while True:
        print "run"
        print last_update_id
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            with open('last_id.txt', 'wb') as last_id:
                last_id.write(str(last_update_id));
            reply(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    main()
