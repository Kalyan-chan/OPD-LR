import telebot

bot = telebot.TeleBot("7359387197:AAEILOqZeG9pVmxt22OEWJ96SCGE_nE_DC8")

users = {}

races = {
    "1": "Полумарафон",
    "2": "Классический марафон",
    "3": "Ультрамарафон"
}

@bot.message_handler(commands=['start'])
def start(msg):
    cid = msg.chat.id
    users[cid] = {"step": "fio"}
    bot.send_message(cid, "Здравствуйте! Введите своё ФИО.")

@bot.message_handler(func=lambda m: True)
def handle(msg):
    cid = msg.chat.id

    step = users[cid]["step"]

    if step == "fio":
        users[cid]["fio"] = msg.text.strip()
        users[cid]["step"] = "race"
        bot.send_message(cid,
            "Выберите тип забега:\n1. Полумарафон\n2. Классический марафон\n3. Ультрамарафон.\nОтправьте цифру.")

    elif step == "race":
        n = msg.text.strip()
        if n not in races:
            bot.send_message(cid, "Введите 1 2 или 3.")
            return

        fio = users[cid]["fio"]
        race = races[n]
        write(cid, f"{fio} - {race}")
        bot.send_message(cid, "Ответ записан.")
        users.pop(cid)

def write(cid, text):
    lines = []
    updated = False
    try:
        with open("sport.txt", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith(f"{cid}:"):
                    lines.append(f"{cid}: {text}\n")
                    updated = True
                else:
                    lines.append(line)
    except FileNotFoundError:
        pass

    if not updated:
        lines.append(f"{cid}: {text}\n")

    with open("sport.txt", "w", encoding="utf-8") as f:
        f.writelines(lines)

bot.polling()
