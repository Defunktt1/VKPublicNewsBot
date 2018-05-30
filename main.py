from telegram.ext import Updater, CommandHandler
from env import token, chat_id, vk_token
import requests
from time import sleep

token = token
chat_id = chat_id
vk_token = vk_token


def start(bot, update):
    update.message.reply_text('Welcome!')


def telebot():
    updater = Updater(token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()


def get_content():
    link = 'https://api.vk.com/method/wall.get?v=5.7&filter=owner&count=2&owner_id=-110594796&access_token={0}'.format(
        vk_token)

    return requests.get(link).json()


def parse_post(post):
    data = post['response']['items'][1]
    text = data['text']
    if 'attachments' in data:
        attachments = data['attachments']
        photo = attachments[0]['photo']
        index = list(photo.keys())[7]
        photo = photo[index]
        text = text + '\n' + photo

    return text


def main():
    old_text = ''
    while True:
        response = get_content()
        response = parse_post(response)
        if old_text != response:
            for id in chat_id:
                send_link = 'https://api.telegram.org/bot{0}/sendMessage?chat_id={1}&text={2}'.format(
                    token,
                    id,
                    response
                )
                print(send_link)
                requests.get(send_link)
            old_text = response
            print('new text = ' + old_text, sep='')
        sleep(60)
        print('current text = ' + old_text, sep='')


if __name__ == '__main__':
    main()
