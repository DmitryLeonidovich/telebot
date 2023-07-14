"""
How are we going to call it? Please choose a name for your bot.
taller_bot

Now let's choose a username for your bot. It must end in `bot`. Like this, for example: TetrisBot or tetris_bot.
Tallers_bot

Use this token to access the HTTP API:
5945616553:AAFU_h6Kg3JuHOx-Chppj1tD8JF1s932N5Q
Keep your token secure and store it safely, it can be used by anyone to control your bot.

t.me/Tallers_bot
"""

import telebot
# import requests

TOKEN = "5945616553:AAFU_h6Kg3JuHOx-Chppj1tD8JF1s932N5Q"

bot = telebot.TeleBot(TOKEN)

# @bot.message_handler(filters)
# def function_name(message):
#     bot.reply_to(message, "This is a message handler")


# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    print(type(message))
    rawstr = ''
    print('Пришел запрос:', message)
    name = str(message.chat.first_name)
    bot.send_message(message.chat.id, 'Привет тебе, ' + name + ', забредший сюда.')


@bot.message_handler(commands=['temp'])
def handle_start_help(message):
    # print(type(message))
    name = str(message.chat.first_name)
    print('Пришел запрос температуры от ', name)
    bot.send_message(message.chat.id, 'Температуру пока не показываем.')
    data_str = b'$KE,TMP\r\n'
    if len(data_str) > 0:
        for i in range(0, len(data_str)):
            s = data_str[i]
            print(hex(s), '\t', chr(s))
    # r = requests.post('http://192.168.10.101:2424', timeout=(2, 5), data=b'$KE,TMP\r\n')
    # print(r)


# Обрабатывается все документы и аудиозаписи
@bot.message_handler(content_types=['document', 'audio'])
def handle_docs_audio(message):
    pass


bot.polling(none_stop=True)


"""
{
'content_type': 'text',
'id': 48,
'message_id': 48,
'from_user': {
                'id': 463882236,
                'is_bot': False,
                'first_name': '.V.aSko.V.',
                'username': 'kitty1ket',
                'last_name': None,
                'language_code': 'ru',
                'can_join_groups': None,
                'can_read_all_group_messages': None,
                'supports_inline_queries': None,
                'is_premium': None,
                'added_to_attachment_menu': None
             },
'date': 1689316154,
'chat': {
            'id': 463882236,
            'type': 'private',
            'title': None,
            'username': 'kitty1ket',
            'first_name': '.V.aSko.V.',
            'last_name': None,
            'is_forum': None,
            'photo': None,
            'bio': None,
            'join_to_send_messages': None,
            'join_by_request': None,
            'has_private_forwards': None,
            'has_restricted_voice_and_video_messages': None,
            'description': None,
            'invite_link': None,
            'pinned_message': None,
            'permissions': None,
            'slow_mode_delay': None,
            'message_auto_delete_time': None,
            'has_protected_content': None,
            'sticker_set_name': None,
            'can_set_sticker_set': None,
            'linked_chat_id': None,
            'location': None,
            'active_usernames': None,
            'emoji_status_custom_emoji_id': None,
            'has_hidden_members': None,
            'has_aggressive_anti_spam_enabled': None
        },
'sender_chat': None,
'forward_from': None,
'forward_from_chat': None,
'forward_from_message_id': None,
'forward_signature': None,
'forward_sender_name': None,
'forward_date': None,
'is_automatic_forward': None,
'reply_to_message': None,
'via_bot': None,
'edit_date': None,
'has_protected_content': None,
'media_group_id': None,
'author_signature': None,
'text': '/start',
'entities': [<telebot.types.MessageEntity object at 0x0338CE38>],
'caption_entities': None,
'audio': None,
'document': None,
'photo': None,
'sticker': None,
'video': None,
'video_note': None,
'voice': None,
'caption': None,
'contact': None,
'location': None,
'venue': None,
'animation': None,
'dice': None,
'new_chat_member': None,
'new_chat_members': None,
'left_chat_member': None,
'new_chat_title': None,
'new_chat_photo': None,
'delete_chat_photo': None,
'group_chat_created': None,
'supergroup_chat_created': None,
'channel_chat_created': None,
'migrate_to_chat_id': None,
'migrate_from_chat_id': None,
'pinned_message': None,
'invoice': None,
'successful_payment': None,
'connected_website': None,
'reply_markup': None,
'message_thread_id': None,
'is_topic_message': None,
'forum_topic_created': None,
'forum_topic_closed': None,
'forum_topic_reopened': None,
'has_media_spoiler': None,
'forum_topic_edited': None,
'general_forum_topic_hidden': None,
'general_forum_topic_unhidden': None,
'write_access_allowed': None,
'user_shared': None,
'chat_shared': None,
'json':
        {
            'message_id': 48,
            'from':
                    {
                        'id': 463882236,
                        'is_bot': False,
                        'first_name': '.V.aSko.V.',
                        'username': 'kitty1ket',
                        'language_code': 'ru'
                    },
            'chat': {
                        'id': 463882236,
                        'first_name': '.V.aSko.V.',
                        'username': 'kitty1ket',
                        'type': 'private'},
            'date': 1689316154,
            'text': '/start',
            'entities': [{
                            'offset': 0,
                            'length': 6,
                            'type': 'bot_command'
                         }
                        ]
            }
        }
"""