import json
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "6907816424:AAFtptMbHmk8FH4w39qBW7Zy1533IKPiPEM"
bot = telebot.TeleBot(TOKEN)

markup = ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(KeyboardButton('Часто'))
markup.add(KeyboardButton('Иногда'))
markup.add(KeyboardButton('Никогда(редко)'))

filename = "user_data.json"


def load_data():
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except:
        data = {}
    return data


def save_data(data):
    with open(filename, "w") as f:
        json.dump(data, f)


questions = {
    1: "Как часто вы задумываетесь о смысле существования человека, как разумного существа?",
    2: "Как часто вы задумываетесь о том, что вы превратитесь в венома?",
    3: "Как часто вы задумываетесь о том, что Ъ нельзя поизнести?",
    4: "Как часто вы задумываетесь о том, что киты в 3 раза вкуснее, чем люди?",
    5: "Как часто вы задумываетесь о добавлении гравитонов в теорию всего?",
}


@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.chat.id
    msg = bot.send_message(message.chat.id, 'Напишите как вас зовут')
    data = load_data()
    data[user_id] = {"question1": "", "question2": "", 'question3': "", 'question4': "", 'question5': ""}
    save_data(data)
    bot.register_next_step_handler(msg, test1)


def ask_question(user_id, question_number):
    question = questions[question_number]
    msg = bot.send_message(user_id, f'{question}\n1)Часто\n2)Иногда\n3)Никогда(редко)')
    return msg


def test1(message):
    user_id = message.chat.id
    msg = bot.send_message(message.chat.id, 'Да здравствует огонь, сказал бог, а я скажу: ДА ЗДРАСТВУЕТ '
                                            'НАУКА.\nПредлагаю '
                                            'перейти к тестам. Центр развития будет вас тестировать по следствию '
                                            'ответов на '
                                            'вопросы о моральной недостаточности и, или умственного развития.\n')
    data = load_data()
    data[str(user_id)]["question1"] = message.text
    save_data(data)
    msg = ask_question(user_id, 1)
    bot.register_next_step_handler(msg, test2)


def test2(message):
    user_id = message.chat.id
    data = load_data()
    data[str(user_id)]["question1"] = message.text
    save_data(data)
    msg = ask_question(user_id, 2)
    bot.register_next_step_handler(msg, test3)


def test3(message):
    user_id = message.chat.id
    data = load_data()
    data[str(user_id)]["question2"] = message.text
    save_data(data)
    msg = ask_question(user_id, 3)
    bot.register_next_step_handler(msg, test4)


def test4(message):
    user_id = message.chat.id
    data = load_data()
    data[str(user_id)]["question3"] = message.text
    save_data(data)
    msg = ask_question(user_id, 4)
    bot.register_next_step_handler(msg, test5)


def test5(message):
    user_id = message.chat.id
    data = load_data()
    data[str(user_id)]["question4"] = message.text
    save_data(data)
    msg = ask_question(user_id, 5)
    bot.register_next_step_handler(msg, final_step)


def final_step(message):
    user_id = message.chat.id
    data = load_data()
    data[str(user_id)]["question5"] = message.text
    save_data(data)
    points = sum(int(data[str(user_id)][f"question{i}"]) for i in range(1, 6))

    if points == 15:
        bot.send_message(message.chat.id, f'Поздравляю, {points} баллов. Скорее всего вы обычный человек.\n Не по повуду '
                                          f'теста, все сообщения записаны '
                                          f'зарание, игнорируйте не заслужанные комплименты.')
    elif 5 < points < 15:
        bot.send_message(message.chat.id, f'Поздравляю, {points} баллов. Скорее всего вы любопытный и (или) начитанный '
                                          f'человек.\n Не по повуду теста, все сообщения записаны '
                                          f'зарание, игнорируйте не заслужанные комплименты.')
    elif points == 5:
        bot.send_message(message.chat.id, f'Поздравляю, {points} баллов. Скорее всего ОЧЕНЬ любознательны (или вы просто '
                                          f'ученый) '
                                          f'человек.\n Не по повуду теста, все сообщения записаны '
                                          f'зарание, игнорируйте не заслужанные комплименты.')
    else:
        bot.send_message(message.chat.id, 'Скорее всего вы решили ввести не то число, ну вот, теперь вам придеться '
                                          'проходить анкету заново.')


if __name__ == "__main__":
    bot.polling(none_stop=True)  # я хотел добавить сюда еще и кнопки, но не смог.
