import datetime

from telegram import Update
from telegram.ext import ContextTypes

from config.classes import classes
from user import User


async def class_command(update: Update, context: ContextTypes, day_=None, next_=False):
    user = User.get_or_none(id=update.effective_user.id)
    day = day_ if day_ is not None else datetime.datetime.today().weekday()
    up = []
    down = []

    days = [
        'Երկուշաբթի',
        'Երեքշաբթի',
        'Չորեքշաբթի',
        'Հինգշաբթի',
        'Ուրբաթ',
    ]

    known_date = datetime.datetime(2023, 9, 4)
    known_week = known_date.isocalendar()[1]

    weeks_later = (datetime.datetime.today().isocalendar()[1] - known_week) + 1
    status = weeks_later % 2

    if next_:
        day += 1

    if day >= 5:
        day = 0
        status = 1 if status == 0 else 0

    list = classes[day]

    try:
        eng_room = user.english
    except:
        eng_room = 7

    eng_rooms = ['9703', '2127', '9706', '9708', '2353ա', '2353', '2338', 'Չեք նշել, նորից անցեք /start']


    for das in list['up']:
        das = das.split(';')
        group = int(das[0])
        lab = int(das[1])
        name, time, room = das[3], das[4], das[5]
        if group == int(user.group) or group == 0:
            up.append(f"|{time}| {name} ({room.replace('[english_room]', eng_rooms[eng_room])}) {f'(գործ {group})' if group != 0 else ''}")
        if lab == int(user.lab):
            up.append(f"|{time}| {name} ({room.replace('[english_room]', eng_rooms[eng_room])}) (լաբ {user.lab})")

    for das in list['down']:
        das = das.split(';')
        group = int(das[0])
        lab = int(das[1])
        name, time, room = das[3], das[4], das[5]
        if group == int(user.group) or group == 0:
            down.append(f"|{time}| {name} ({room.replace('[english_room]', eng_rooms[eng_room])}) {f'(գործ {group})' if group != 0 else ''}")
        if lab == int(user.lab) or lab == 0:
            down.append(f"|{time}| {name} ({room.replace('[english_room]', eng_rooms[eng_room])}) (լաբ {user.lab})")

    final_classes = up if status == 0 else down

    if day_ is not None:
        await update.message.reply_text(f'📍 Ձեր դասերը, {days[day]}\n\n{"✅" if status == 0 else "❌"} Համարիչ\n' + "\n".join(up) + f'\n\n{"✅" if status == 1 else "❌"} Հայտարար\n' + "\n".join(down))
    else:
        await update.message.reply_text(f'📍 Ձեր դասերը, {days[day]}\n\n{"🔼 Համարիչ" if status == 0 else "🔽 Հայտարար"}\n' + "\n".join(final_classes))
