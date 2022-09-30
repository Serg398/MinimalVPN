import telebot
from telebot import types
from telebot.formatting import hlink
from mongo import createPeerDB, getUserPeersDB, deletePeerDB, createUserDB
from wireguard import getFile


API_TOKEN = '*****'
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    print(message.from_user.id)
    createUserDB(telegramID=message.from_user.id)
    inMurkup = types.InlineKeyboardMarkup(row_width=1)
    but1 = types.InlineKeyboardButton("➕ Добавить новое устройство", callback_data='Добавить новое устройство')
    but2 = types.InlineKeyboardButton("📱 Мои устройства", callback_data="Мои устройства")
    but3 = types.InlineKeyboardButton("💳 Пополнить счет", callback_data="Пополнить счет")
    but4 = types.InlineKeyboardButton("📄 Инструкция", callback_data="Инструкция")
    inMurkup.add(but1, but2, but3, but4)
    bot.send_message(message.chat.id, text=f"Привет, {message.from_user.first_name}.", reply_markup=inMurkup)


@bot.callback_query_handler(func=lambda call: True)
def func(call):
    comand = call.data
    if comand == "Добавить новое устройство":
        name = createPeerDB(telegramID=call.from_user.id)
        if name == False:
            inMurkup = types.InlineKeyboardMarkup(row_width=1)
            but1 = types.InlineKeyboardButton("➕ Добавить новое устройство", callback_data='Добавить новое устройство')
            but2 = types.InlineKeyboardButton("📱 Мои устройства", callback_data="Мои устройства")
            but3 = types.InlineKeyboardButton("💳 Пополнить счет", callback_data="Пополнить счет")
            but4 = types.InlineKeyboardButton("📄 Инструкция", callback_data="Инструкция")
            inMurkup.add(but1, but2, but3, but4)
            print(f"{call.from_user.first_name} {call.from_user.last_name} добавил новое устройство: *{name}*")
            bot.send_message(call.message.chat.id,
                             f'*Максимальное количество устройств может быть не более 2.*',
                             reply_markup=inMurkup, parse_mode='Markdown')
            bot.answer_callback_query(callback_query_id=call.id)
        else:
            idPeer = str(name)[::-4]
            inMurkup = types.InlineKeyboardMarkup(row_width=1)
            but1 = types.InlineKeyboardButton("➕ Добавить новое устройство", callback_data='Добавить новое устройство')
            but2 = types.InlineKeyboardButton("📱 Мои устройства", callback_data="Мои устройства")
            but3 = types.InlineKeyboardButton("💳 Пополнить счет", callback_data="Пополнить счет")
            but4 = types.InlineKeyboardButton("📄 Инструкция", callback_data="Инструкция")
            inMurkup.add(but1, but2, but3, but4)
            print(f"{call.from_user.first_name} {call.from_user.last_name} добавил новое устройство: *{name}*")
            bot.send_message(388734819, f"Пользователь @{call.from_user.username} добавил новое устройство: *{name}*", reply_markup=inMurkup, parse_mode='Markdown')
            bot.send_message(call.message.chat.id, f'Вы добавили новое устройство: *{idPeer}*\nСкачать файл вы можете в разделе "Мои устройства"', reply_markup=inMurkup, parse_mode='Markdown')
            bot.answer_callback_query(callback_query_id=call.id)

## Мои устройства
    if comand == "Мои устройства":
        peersAll = getUserPeersDB(telegramID=call.from_user.id)
        if peersAll == []:
            inMurkup = types.InlineKeyboardMarkup(row_width=1)
            but1 = types.InlineKeyboardButton("🏠 Главное меню", callback_data='Главное меню')
            inMurkup.add(but1)
            bot.send_message(call.message.chat.id, text=f"Список пуст", reply_markup=inMurkup)
            bot.answer_callback_query(callback_query_id=call.id)
        else:
            inMurkup = types.InlineKeyboardMarkup(row_width=3)
            buttons = []
            but1 = types.InlineKeyboardButton("🏠 Главное меню", callback_data='Главное меню')
            for button in peersAll:
                idPeer = str(button['_id'])[::-4]
                buttons.append(types.InlineKeyboardButton(f"▪ {idPeer}", callback_data="Удалить"))
                buttons.append(types.InlineKeyboardButton("⬇ Скачать", callback_data="get, " + str(button['_id']) + ""))
                buttons.append(types.InlineKeyboardButton("⛔ Удалить", callback_data="del, " + str(button['_id']) + ""))
            inMurkup.add(*buttons, but1)
            bot.send_message(call.message.chat.id, text=f"📱 Список устройств:", reply_markup=inMurkup)
            bot.answer_callback_query(callback_query_id=call.id)

## Главное меню
    if comand == "Главное меню":
        inMurkup = types.InlineKeyboardMarkup(row_width=1)
        but1 = types.InlineKeyboardButton("➕ Добавить новое устройство", callback_data='Добавить новое устройство')
        but2 = types.InlineKeyboardButton("📱 Мои устройства", callback_data="Мои устройства")
        but3 = types.InlineKeyboardButton("💳 Пополнить счет", callback_data="Пополнить счет")
        but4 = types.InlineKeyboardButton("📄 Инструкция", callback_data="Инструкция")
        inMurkup.add(but1, but2, but3, but4)
        bot.send_message(call.message.chat.id, text=f"🏠 Главное меню:", reply_markup=inMurkup)
        bot.answer_callback_query(callback_query_id=call.id)

    if call.data.startswith("del"):
        id = str(call.data).split(", ")[1]
        deletePeerDB(mongoID=id)
        print(f"{call.from_user.first_name} {call.from_user.last_name} удалил устройство: *{id}*")
        bot.send_message(388734819, f"Пользователь @{call.from_user.username} удалил устройство: *{id}*", parse_mode='Markdown')
        peersAll = getUserPeersDB(telegramID=call.from_user.id)
        if peersAll == []:
            inMurkup = types.InlineKeyboardMarkup(row_width=1)
            but1 = types.InlineKeyboardButton("🏠 Главное меню", callback_data='Главное меню')
            inMurkup.add(but1)
            bot.send_message(call.message.chat.id, text=f"📱 Список пуст", reply_markup=inMurkup)
            bot.answer_callback_query(callback_query_id=call.id)
        else:
            inMurkup = types.InlineKeyboardMarkup(row_width=3)
            buttons = []
            but1 = types.InlineKeyboardButton("🏠 Главное меню", callback_data='Главное меню')
            for button in peersAll:
                idPeer = str(button['_id'])[:-3]
                buttons.append(types.InlineKeyboardButton(f"▪ {idPeer}", callback_data="Удалить"))
                buttons.append(types.InlineKeyboardButton("⬇ Скачать", callback_data="get, " + str(button['_id']) + ""))
                buttons.append(types.InlineKeyboardButton("⛔ Удалить", callback_data="del, " + str(button['_id']) + ""))
            inMurkup.add(*buttons, but1)
            bot.send_message(call.message.chat.id, text=f"📱 Список устройств:", reply_markup=inMurkup)
            bot.answer_callback_query(callback_query_id=call.id)

    if call.data.startswith("get"):
        id = str(call.data).split(", ")[1]
        file = getFile(id)
        idPeer = str(id[::-4])
        bot.send_document(call.message.chat.id, file, visible_file_name=f"{idPeer}.conf")
        bot.answer_callback_query(callback_query_id=call.id)

    if comand == "Инструкция":
        inMurkup = types.InlineKeyboardMarkup(row_width=1)
        but1 = types.InlineKeyboardButton("➕ Добавить новое устройство", callback_data='Добавить новое устройство')
        but2 = types.InlineKeyboardButton("📱 Мои устройства", callback_data="Мои устройства")
        but3 = types.InlineKeyboardButton("💳 Пополнить счет", callback_data="Пополнить счет")
        but4 = types.InlineKeyboardButton("📄 Инструкция", callback_data="Инструкция")
        inMurkup.add(but1, but2, but3, but4)
        androidLink = hlink('Android', 'https://play.google.com/store/apps/details?id=com.wireguard.android&hl=ru&gl=US')
        iOSLink = hlink('iPhone', 'https://apps.apple.com/us/app/wireguard/id1441195209?ls=1')
        windowsLink = hlink('Windows', 'https://download.wireguard.com/windows-client/wireguard-installer.exe')
        text = f"1. Нажмите кнопку 'Добавить новое устройство'\n" \
               "2. Скачайте файл настроек в разделе 'Мои устройства'\n" \
               f"3. Установите приложение Wireguard для:\n{androidLink}, {iOSLink}, {windowsLink}.\n" \
               "4. Запустите программу Wireguard и нажмите ➕ внизу экрана справа\n" \
               "5. Нажмите кнопку “Импорт из файла или архива”, выберите скачанный конфиг файл из папки загрузок\n" \
               "6. Включите тумблер."
        bot.send_message(call.message.chat.id, text=text, reply_markup=inMurkup, parse_mode='HTML')
        bot.answer_callback_query(callback_query_id=call.id)


def sendServiceMessage(telegramID, send_message):
    inMurkup = types.InlineKeyboardMarkup(row_width=1)
    but1 = types.InlineKeyboardButton("➕ Добавить новое устройство", callback_data='Добавить новое устройство')
    but2 = types.InlineKeyboardButton("📱 Мои устройства", callback_data="Мои устройства")
    but3 = types.InlineKeyboardButton("💳 Пополнить счет", callback_data="Пополнить счет")
    but4 = types.InlineKeyboardButton("📄 Инструкция", callback_data="Инструкция")
    inMurkup.add(but1, but2, but3, but4)
    bot.send_message(telegramID, text=send_message, reply_markup=inMurkup)


bot.infinity_polling()
