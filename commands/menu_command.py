from telegram import (InlineKeyboardButton, ReplyKeyboardMarkup, Update,
                      constants)
from telegram.ext import ContextTypes

from commands.class_command import class_command
from commands.exams_command import exams_command
from user import User

overall_menu = [
    [
        InlineKeyboardButton('📅 Դասացուցակ, այսօր'),
        InlineKeyboardButton('🗓️ Դասացուցակ, ընտրովի օր'),
        InlineKeyboardButton('📅 Դասացուցակ, վաղվա'),
    ],
    [
        InlineKeyboardButton('📚 Ֆեյկ գրադարան')
    ],
    [
        InlineKeyboardButton('🥰 Քննությունների օրացույց 🤓'),
    ]
]

overall_reply_markup = ReplyKeyboardMarkup(overall_menu, resize_keyboard=True)

async def menu_command(update: Update, context: ContextTypes):
    await update.message.reply_text('🔎 Ահա բոլոր առկա հրամանները։', reply_markup=overall_reply_markup)

async def message_response(update: Update, context: ContextTypes):
    text = update.message.text

    if text.endswith('Դասացուցակ, այսօր'):
        await class_command(update, context)

    elif text.endswith('Դասացուցակ, վաղվա'):
        await class_command(update, context, next_=True)

    elif text.endswith('Դասացուցակ, ընտրովի օր'):
        menu = [
            [
                InlineKeyboardButton('😭 Երկուշաբթի'),
                InlineKeyboardButton('😔 Երեքշաբթի'),
                InlineKeyboardButton('😒 Չորեքշաբթի'),
                InlineKeyboardButton('😏 Հինգշաբթի'),
                InlineKeyboardButton('😎 Ուրբաթ'),
            ],
            [
                InlineKeyboardButton('⬅ Գնալ հետ menu')
            ]
        ]
        reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True)
        await update.message.reply_text('🧐 Ընտրեք որ օրվա դասացուցակ ուղարկեմ', reply_markup=reply_markup)

    elif text.endswith('Երկուշաբթի'):
        await class_command(update, context, 0)
    elif text.endswith('Երեքշաբթի'):
        await class_command(update, context, 1)
    elif text.endswith('Չորեքշաբթի'):
        await class_command(update, context, 2)
    elif text.endswith('Հինգշաբթի'):
        await class_command(update, context, 3)
    elif text.endswith('Ուրբաթ'):
        await class_command(update, context, 4)

    elif text.endswith('Գնալ հետ menu'):
        await update.message.reply_text('⬅ Գնացինք հետ', reply_markup=overall_reply_markup)

    elif text.endswith('Ֆեյկ գրադարան'):
        menu = [
            [
                InlineKeyboardButton('🧮 ԱԵ և ԳՀ, գրքեր'),
                InlineKeyboardButton('📊 Մաթ անալիզ, գրքեր'),
                InlineKeyboardButton('💻 ԱԼ և Ծ, գրքեր')
            ],
            [
                InlineKeyboardButton('📖 Պատմություն, գրքեր'),
                InlineKeyboardButton('💡 Ֆիզիկա, գրքեր')
            ],
            [
                InlineKeyboardButton('⬅ Գնալ հետ menu')
            ]
        ]
        reply_markup = ReplyKeyboardMarkup(menu, resize_keyboard=True)
        await update.message.reply_text('🤯 Ընտրեք որ գիրքը ուղարկեմ', reply_markup=reply_markup)
    elif text.endswith('ԱԵ և ԳՀ, գրքեր'):
        await update.message.reply_text('<a href="https://t.me/tt319grqer/55">Խնդրեմ</a>', parse_mode=constants.ParseMode.HTML)
    elif text.endswith('Մաթ անալիզ, գրքեր'):
        await update.message.reply_text('<a href="https://t.me/tt319grqer/62">Խնդրեմ</a>', parse_mode=constants.ParseMode.HTML)
    elif text.endswith('ԱԼ և Ծ, գրքեր'):
        await update.message.reply_text('<a href="https://t.me/tt319grqer/58">Խնդրեմ</a>', parse_mode=constants.ParseMode.HTML)
    elif text.endswith('Պատմություն, գրքեր'):
        await update.message.reply_text('<a href="https://t.me/tt319grqer/59">Խնդրեմ</a>', parse_mode=constants.ParseMode.HTML)
    elif text.endswith('Ֆիզիկա, գրքեր'):
        await update.message.reply_text('<a href="https://t.me/tt319grqer/69">Խնդրեմ</a>', parse_mode=constants.ParseMode.HTML)
    elif text.startswith('announce-') and update.effective_user.id == 1062136096:
        group = int(text.split(' ')[0].split('-')[1])

        if group == 4:
            await update._bot.send_message(1062136096, text.split(f'announce-{group}')[1])
            return

        users = User.select()

        if group != 0:
            users = users.where(User.group == group)
        for user in users:
            await update._bot.send_message(user.id, text.split(f'announce-{group}')[1])

    elif text.startswith('🥰 Քննությունների օրացույց 🤓'):
        await exams_command(update, context)