import telebot
from telebot import types

import pandas as pd



#data = {'Заявитель' : [], 'Текст заявки' : [], 'Член студсовета' : [], 'Статус заявки' : []}
#tablet = pd.DataFrame(data = data, index = False)
#tablet.to_csv('data.csv')
#print(tablet)

#print(qwer['Заявитель'])




bot = telebot.TeleBot("5853959402:AAHjGNpuk1w5KSZlTYbY7iV8PRqnJukm-eI")

Helpersfile = open('Список членов студсовета.txt', 'r',encoding='utf8')
helpers = {}
for line in Helpersfile:
    line = line.replace('\n', '')
    helpers[line] = {}
Helpersfile.close()
print(helpers)


@bot.message_handler(commands=['register'])
def reg(message):
    if '@' + str(message.from_user.username) not in helpers:
        bot.send_message(message.from_user.id, 'Вас нет в списке помощников.')
    else:
        helpers['@' + str(message.from_user.username)]['id'] = message.from_user.id
        print(helpers)
        keyboard = types.ReplyKeyboardMarkup(row_width=1)
        button = types.KeyboardButton('/check')
        keyboard.add(button)
        msg = bot.send_message(message.from_user.id, 'Вы успешно прошли регистрацию', reply_markup=keyboard)





@bot.message_handler(commands=['start'])
def send_keyboard(message, text="Здравствуйте, что я могу для вас сделать? (Вы не можете иметь больше трех необработанных заявок)"):


    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    application1 = types.KeyboardButton('Оставить заявку')
    application2 = types.KeyboardButton('Список моих заявок')
    application3 = types.KeyboardButton('Удалить заявку')
    application4 = types.KeyboardButton("Очистить список заявок")
    application5 = types.KeyboardButton('До свидания')
    keyboard.add(application1, application2)
    keyboard.add(application3, application4)
    keyboard.add(application5)

    msg = bot.send_message(message.from_user.id, text=text, reply_markup=keyboard)

        # отправим этот вариант в функцию, которая его обработает
    bot.register_next_step_handler(msg, callback_worker)
application_base = {}
applications_time = {}
user_names = {}
def add_application(mesinfo):
    if mesinfo.from_user.id not in application_base.keys():
        application_base[mesinfo.from_user.id] = {1: str(mesinfo.text)}
        applications_time[mesinfo.from_user.id] = {1: int(mesinfo.date)}
    else:
        if set(application_base[mesinfo.from_user.id].keys()) == set():
            application_base[mesinfo.from_user.id] = {1: str(mesinfo.text)}
            applications_time[mesinfo.from_user.id] = {1: int(mesinfo.date)}
        elif set(application_base[mesinfo.from_user.id].keys()) == {1, 2, 3}:
            x = 'Дождитесь рассмотрения предыдущих 3 заявок, ' + str(mesinfo.from_user.first_name)
            bot.send_message(mesinfo.from_user.id, x)
        elif set(application_base[mesinfo.from_user.id].keys()) == {1, 2}:
            application_base[mesinfo.from_user.id][3] = str(mesinfo.text)
            applications_time[mesinfo.from_user.id][3] = int(mesinfo.date)
        elif set(application_base[mesinfo.from_user.id].keys()) == {1}:
            application_base[mesinfo.from_user.id][2] = str(mesinfo.text)
            applications_time[mesinfo.from_user.id][2] = int(mesinfo.date)
    z = telebot.types.ReplyKeyboardRemove()
    bot.send_message(mesinfo.from_user.id, 'Для продолжения нажмите /start', reply_markup = z)
    user_names[mesinfo.from_user.id] = mesinfo.from_user.username
    return

def show_app_list(mesinfo):
    if mesinfo.from_user.id not in application_base.keys():
        z = telebot.types.ReplyKeyboardRemove()
        bot.send_message(mesinfo.from_user.id, 'У вас нет активных заявок. Для продолжения нажмите /start', reply_markup = z)
    else:
        if set(application_base[mesinfo.from_user.id].keys()) == set():
            z = telebot.types.ReplyKeyboardRemove()
            bot.send_message(mesinfo.from_user.id, 'У вас нет активных заявок. Для продолжения нажмите /start', reply_markup = z)
        elif set(application_base[mesinfo.from_user.id].keys()) == {1, 2, 3}:
            a = '1: ' + application_base[mesinfo.from_user.id][1]
            b = '2: ' + application_base[mesinfo.from_user.id][2]
            c = '3: ' + application_base[mesinfo.from_user.id][3]
            bot.send_message(mesinfo.from_user.id, a)
            bot.send_message(mesinfo.from_user.id, b)
            bot.send_message(mesinfo.from_user.id, c)
            z = telebot.types.ReplyKeyboardRemove()
            bot.send_message(mesinfo.from_user.id, 'Для продолжения нажмите /start', reply_markup = z)
        elif set(application_base[mesinfo.from_user.id].keys()) == {1, 2}:
            a = '1: ' + application_base[mesinfo.from_user.id][1]
            b = '2: ' + application_base[mesinfo.from_user.id][2]
            bot.send_message(mesinfo.from_user.id, a)
            bot.send_message(mesinfo.from_user.id, b)
            z = telebot.types.ReplyKeyboardRemove()
            bot.send_message(mesinfo.from_user.id, 'Для продолжения нажмите /start', reply_markup = z)
        elif set(application_base[mesinfo.from_user.id].keys()) == {1}:
            a = 'У вас всего одна заявка: ' + application_base[mesinfo.from_user.id][1]
            bot.send_message(mesinfo.from_user.id, a)
            z = telebot.types.ReplyKeyboardRemove()
            bot.send_message(mesinfo.from_user.id, 'Для продолжения нажмите /start', reply_markup = z)
            user_names[mesinfo.from_user.id] = mesinfo.from_user.username
    return

def del_all_app(mesinfo):
    application_base[mesinfo.from_user.id] = {}
    applications_time[mesinfo.from_user.id] = {}
    z = telebot.types.ReplyKeyboardRemove()
    bot.send_message(mesinfo.from_user.id, 'Готово. Для продолжения нажмите /start', reply_markup = z)
    return

def del_app(mesinfo):
    if mesinfo.from_user.id not in application_base.keys():
        z = telebot.types.ReplyKeyboardRemove()
        bot.send_message(mesinfo.from_user.id, 'У вас нет активных заявок. Для продолжения нажмите /start', reply_markup = z)
    else:
        if set(application_base[mesinfo.from_user.id].keys()) == set():
            z = telebot.types.ReplyKeyboardRemove()
            bot.send_message(mesinfo.from_user.id, 'У вас нет активных заявок. Для продолжения нажмите /start', reply_markup = z)
        elif set(application_base[mesinfo.from_user.id].keys()) == {1, 2, 3}:
            if int(mesinfo.text) not in {1, 2, 3}:
                z = telebot.types.ReplyKeyboardRemove()
                bot.send_message(mesinfo.from_user.id, 'Заявки с таким номером не существует. Для продолжения нажмите /start', reply_markup = z)
            elif int(mesinfo.text) == 1:
                a = application_base[mesinfo.from_user.id][2]
                b = application_base[mesinfo.from_user.id][3]
                A = applications_time[mesinfo.from_user.id][2]
                B = applications_time[mesinfo.from_user.id][3]
                application_base[mesinfo.from_user.id] = {1: a, 2: b}
                applications_time[mesinfo.from_user.id] = {1: A, 2: B}
                z = telebot.types.ReplyKeyboardRemove()
                bot.send_message(mesinfo.from_user.id, 'Готово. Для продолжения нажмите /start', reply_markup = z)
            elif int(mesinfo.text) == 2:
                a = application_base[mesinfo.from_user.id][1]
                b = application_base[mesinfo.from_user.id][3]
                A = applications_time[mesinfo.from_user.id][1]
                B = applications_time[mesinfo.from_user.id][3]
                application_base[mesinfo.from_user.id] = {1: a, 2: b}
                applications_time[mesinfo.from_user.id] = {1: A, 2: B}
                z = telebot.types.ReplyKeyboardRemove()
                bot.send_message(mesinfo.from_user.id, 'Готово. Для продолжения нажмите /start', reply_markup = z)
            else:
                a = application_base[mesinfo.from_user.id][1]
                b = application_base[mesinfo.from_user.id][2]
                A = applications_time[mesinfo.from_user.id][1]
                B = applications_time[mesinfo.from_user.id][2]
                application_base[mesinfo.from_user.id] = {1: a, 2: b}
                applications_time[mesinfo.from_user.id] = {1: A, 2: B}
                z = telebot.types.ReplyKeyboardRemove()
                bot.send_message(mesinfo.from_user.id, 'Готово. Для продолжения нажмите /start', reply_markup = z)
        elif set(application_base[mesinfo.from_user.id].keys()) == {1, 2}:
            if int(mesinfo.text) not in {1, 2}:
                z = telebot.types.ReplyKeyboardRemove()
                bot.send_message(mesinfo.from_user.id, 'Заявки с таким номером не существует. Для продолжения нажмите /start', reply_markup = z)
            elif int(mesinfo.text) == 1:
                a = application_base[mesinfo.from_user.id][2]
                A = applications_time[mesinfo.from_user.id][2]
                application_base[mesinfo.from_user.id] = {1: a}
                applications_time[mesinfo.from_user.id] = {1: A}
                z = telebot.types.ReplyKeyboardRemove()
                bot.send_message(mesinfo.from_user.id, 'Готово. Для продолжения нажмите /start', reply_markup = z)
            else:
                a = application_base[mesinfo.from_user.id][1]
                A = applications_time[mesinfo.from_user.id][1]
                application_base[mesinfo.from_user.id] = {1: a}
                applications_time[mesinfo.from_user.id] = {1: A}
                z = telebot.types.ReplyKeyboardRemove()
                bot.send_message(mesinfo.from_user.id, 'Готово. Для продолжения нажмите /start', reply_markup = z)
        elif set(application_base[mesinfo.from_user.id].keys()) == {1}:
            application_base[mesinfo.from_user.id] = {}
            applications_time[mesinfo.from_user.id] = {}
    return

def callback_worker(call):
    print(call)
    print(application_base)
    if call.text == 'Оставить заявку':
        msg = bot.send_message(call.chat.id, 'Опишите свою проблему одним сообщением.')
        bot.register_next_step_handler(msg, add_application)
    elif call.text == 'Список моих заявок':
        show_app_list(call)
    elif call.text == 'Очистить список заявок':
        del_all_app(call)
    elif call.text == 'До свидания':
        z = telebot.types.ReplyKeyboardRemove()
        bot.send_message(call.chat.id, 'До свидания! Если хотите продолжить, то нажмите /start', reply_markup = z)
    elif call.text == 'Удалить заявку':
        msg = bot.send_message(call.chat.id, 'Укажите номер заявки(целое число).')
        bot.register_next_step_handler(msg, del_app)
    else:

        bot.send_message(call.chat.id, 'Введите заново команду. Чтобы ознакомиться с функционалом бота, нажмите /help.')
    return

@bot.message_handler(commands=['check'])
def check(message):
    if '@' + str(message.from_user.username) not in helpers:
        bot.send_message(message.from_user.id, 'У вас нет доступа к этой команде')
    elif helpers['@' + str(message.from_user.username)] == {}:
        bot.send_message(message.from_user.id, 'У вас нет доступа к этой команде')
    else:



        if set(applications_time.keys()) == set():

            bot.send_message(message.from_user.id, 'Заявок нет.')
        else:
            if applications_time == {x: {} for x in applications_time.keys() }:

                bot.send_message(message.from_user.id, 'Заявок нет.')
            else:
                try:

                    l = []
                    for x in applications_time.keys():
                        if applications_time[x] != {}:
                            l.append(x)
                    Q = [applications_time[x][1] for x in l]
                    t = min(Q)
                    H = []
                    for x in applications_time.keys():
                        if applications_time[x][1] == t:
                            H.append(x)
                    r = max(H)
                    H = []
                    text = 'Вы хотите принять заявку от @' + user_names[r] + '? Текст обращения: ' + application_base[r][1]
                    z = telebot.types.ReplyKeyboardRemove()
                    bot.send_message(message.from_user.id, text, reply_markup=z)
                    keyboard = types.ReplyKeyboardMarkup(row_width=2)
                    button1 = types.KeyboardButton('Принять заявку от id' + str(r))
                    button2 = types.InlineKeyboardButton('Отклонить')
                    keyboard.add(button1, button2)

                    msg = bot.send_message(message.from_user.id, 'Ваш ответ:', reply_markup=keyboard)

                    # отправим этот вариант в функцию, которая его обработает
                    bot.register_next_step_handler(msg, acception)
                except KeyError:
                    bot.send_message(message.from_user.id, 'Вашу заявку украли :)')
def acception(call):
    qwer = pd.read_csv('data.csv')
    qwer_goy = pd.read_csv('data_for_goys.csv')
    if str(call.text) != 'Отклонить':
        x = int((str(call.text)).split('Принять заявку от id')[1])
        print(x)
        if user_names[x] in qwer['Заявитель'] and application_base[x][1] in qwer['Текст заявки']:
            z = telebot.types.ReplyKeyboardRemove()
            bot.send_message(call.from_user.id, 'Вы опоздали, кто-то уже принял вашу заявку', reply_markup=z)
        else:
            try:
                my_row = {'Заявитель': '@' + str(user_names[x]),'Текст заявки': application_base[x][1],'Член студсовета': '@' + str(call.from_user.username), 'Статус заявки': 'Обрабатывается'}
                my_row_goy = {'Текст заявки': application_base[x][1], 'Член студсовета': '@' + str(call.from_user.username), 'Статус заявки': 'Обрабатывается'}
                qwer = qwer.append(my_row, ignore_index = True)
                qwer_goy = qwer_goy.append(my_row_goy, ignore_index = True)
                z = telebot.types.ReplyKeyboardRemove()
                bot.send_message(call.from_user.id, 'Добавлено в таблицу. Нажмите /applies, чтобы получить файл таблицы.', reply_markup=z)
                bot.send_message(x, 'Заявка с текущим номером один обрабатывается. @' + str(call.from_user.username) + ' ей занят. Вы можете с ним связаться. Заявка будет удалена из вашего списка. Увидеть список заявок вы можете, введя команду /applies')
                qwer.to_csv('data.csv', index = False)
                qwer_goy.to_csv('data_for_goys.csv', index = False)
                if application_base[x].keys() == {1, 2, 3}:
                    A = application_base[x][2]
                    B = application_base[x][3]
                    a = applications_time[x][2]
                    b = applications_time[x][3]
                    application_base[x] = {1: A, 2: B}
                    applications_time[x] = {1: a, 2: b}
                elif application_base[x].keys() == {1, 2}:
                    A = application_base[x][2]
                    a = applications_time[x][2]
                    application_base[x] = {1: A}
                    applications_time[x] = {1: a}
                else:
                    application_base[x] = {}
                    applications_time[x] = {}
                print(qwer)
            except KeyError:
                bot.send_message(call.from_user.id, 'Вашу заявку украли :)')
    else:
        z = telebot.types.ReplyKeyboardRemove()
        bot.send_message(call.from_user.id, 'Хорошо.', reply_markup = z)
    return
@bot.message_handler(commands = ['applies'])
def applies(message):
    if '@' + str(message.from_user.username) not in helpers:
        filo = open('data_for_goys.csv', 'rb')
        bot.send_document(message.from_user.id, filo)
    elif helpers['@' + str(message.from_user.username)] == {}:
        filo = open('data_for_goys.csv', 'rb')
        bot.send_document(message.from_user.id, filo)
    else:
        filo = open('data.csv', 'rb')
        bot.send_document(message.from_user.id, filo)
@bot.message_handler(commands = ['help'])
def help(message):
    bot.send_message(message.from_user.id, '/start - меню для студента.')
    bot.send_message(message.from_user.id, '/register - функция, необходимая для того, чтобы члены студсовета получили доступ к обработке заявок.')
    bot.send_message(message.from_user.id, '/check - проверить актуальные заявки(доступна не всем).')
    bot.send_message(message.from_user.id, '/applies - Список принятых заявок.')
    bot.send_message(message.from_user.id, '/status - изменение статуса заявки(доступна не всем).')
    return
@bot.message_handler(commands = ['status'])
def status(message):
    if '@' + str(message.from_user.username) not in helpers:
        bot.send_message(message.from_user.id, 'Вас нет в списке помощников.')
    else:
        qwer = pd.read_csv('data.csv')
        l = []
        for i in range(len(qwer['Заявитель'])):
            if qwer['Член студсовета'][i] == '@' + str(message.from_user.username) and qwer['Статус заявки'][i] == 'Обрабатывается':
                l.append(i)
        print(l)
        if l == []:
            bot.send_message(message.from_user.id, 'Вы не обрабатываете ни одной заявки.')
        else:
            m = min(l)
            bot.send_message(message.from_user.id, 'Вы решили проблему ' + str(qwer['Заявитель'][m]) + ': ' + str(qwer['Текст заявки'][m]))

            keyboard = types.ReplyKeyboardMarkup(row_width=2)
            button1 = types.KeyboardButton('Заявка номер ' + str(m) + ' обработана.')
            button2 = types.InlineKeyboardButton('Нет')
            keyboard.add(button1, button2)
            m = 0

            msg = bot.send_message(message.from_user.id, 'Ваш ответ:', reply_markup=keyboard)

                # отправим этот вариант в функцию, которая его обработает
            bot.register_next_step_handler(msg, response)

def response(message):
    qwer = pd.read_csv('data.csv')
    qwer_goy = pd.read_csv('data_for_goys.csv')
    if str(message.text) != 'Нет':
        x = message.text
        x = x.replace('Заявка номер ', '')
        m = int(x.replace(' обработана.', ''))
        print(m)
        qwer['Статус заявки'][m] = 'Обработана'
        qwer_goy['Статус заявки'][m] = 'Обработана'
        qwer.to_csv('data.csv', index=False)
        qwer_goy.to_csv('data_for_goys.csv', index=False)
        z = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, 'Статус заявки изменен.', reply_markup=z)
bot.polling(none_stop=True)