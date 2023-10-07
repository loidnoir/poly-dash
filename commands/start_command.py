from telegram import (InlineKeyboardButton, ReplyKeyboardMarkup, Update,
                      constants)
from telegram.ext import ContextTypes

from commands.class_command import class_command
from commands.menu_command import message_response
from user import User


async def start_command(update: Update, context: ContextTypes):
    group_menu = [InlineKeyboardButton('Գործ 1'), InlineKeyboardButton('Գործ 2'), InlineKeyboardButton('Գործ 3')],
    group_reply_markup = ReplyKeyboardMarkup(group_menu, resize_keyboard=True)
    await update.message.reply_text(f'👋 Բարև <b>{update.effective_user.first_name}</b>, քեզ ողջունում է <b>Poly Dash</b> չատ-բոտը հատուկ ստեղծված Ծրագրային Ճարտարագիտության բաժնի համար, բոտը լիովին անվճար է և ստեղծված է քանի որ մեկը գիշերը մնացել էր պարապ։\n\n🪪 Խնդրում եմ պատասխանեք մի քանի հարցերի, որպեսզի կազմեմ ձեր դասացուցակը։ Ընտրեք ձեր գործ-ի համարը', reply_markup=group_reply_markup, parse_mode=constants.ParseMode.HTML)

async def start_button_response(update: Update, context: ContextTypes):
    text = update.message.text

    if text.startswith('Գործ'):
        lab_menu = [InlineKeyboardButton('Լաբ 1'), InlineKeyboardButton('Լաբ 2'), InlineKeyboardButton('Լաբ 3'), InlineKeyboardButton('Լաբ 4'), InlineKeyboardButton('Լաբ 5')],
        lab_reply_markup = ReplyKeyboardMarkup(lab_menu, resize_keyboard=True)
        user = User.get_or_none(id=update.effective_user.id)
        group = int(text.split(' ')[1])

        if group < 1 or group > 3:
            await update.message.reply_text('❌ Սխալ գործի համաև, փորձեք նորից։')
        else:
            if user is None:
                User.create(id=update.effective_user.id, group=group, lab=0).save()
            else:
                User.update(group=group).where(User.id == update.effective_user.id).execute()
            await update.message.reply_text(f'✅ Դուք ընտրեցիք համար {group} գործը։\n\n❇️ Հիմա ընտրեք լաբի համարը։', reply_markup=lab_reply_markup)

    elif text.startswith('Լաբ'):
        lab = int(text.split(' ')[1])
        eng_menu = [
            [InlineKeyboardButton('▶️ Հեքիմյան'), InlineKeyboardButton('▶️ Խարբերտյան')],
            [InlineKeyboardButton('▶️ Հուսիկյան'), InlineKeyboardButton('▶️ Դադոյան')],
            [InlineKeyboardButton('▶️ Տուֆեկչյան'), InlineKeyboardButton('▶️ Հասրաթյան'), InlineKeyboardButton('▶️ Թովմասյան')]
        ]
        eng_reply_markup = ReplyKeyboardMarkup(eng_menu, resize_keyboard=True)

        if lab < 1 or lab > 5:
            await update.message.reply_text('❌ Սխալ լաբի համար, փորձեք նորից։')
        else:
            user = User.get_or_none(id=update.effective_user.id)

            if user is None:
                User.create(id=update.effective_user.id, group=0, lab=lab).save()
            else:
                User.update(lab=lab).where(User.id == update.effective_user.id).execute()
            await update.message.reply_text(f'✅ Դուք ընտրեցիք {lab} լաբը։\n\n❇️ Հիմա ընտրեք անգլերենի դասախոսին', reply_markup=eng_reply_markup)

    elif text.startswith('▶️'):
        user = User.get_or_none(id=update.effective_user.id)
        english_group = text.split(' ')[1]
        english_group = 0 if english_group == 'Հեքիմյան' else 1 if english_group == 'Խարբերտյան' else 2 if english_group == 'Հուսիկյան' else 3 if english_group == 'Դադոյան' else 4 if english_group == 'Տուֆեկչյան' else 5 if english_group == 'Հասրաթյան' else 6

        if user is None:
                User.create(id=update.effective_user.id, group=group, lab=0).save()
        else:
            User.update(english=english_group).where(User.id == update.effective_user.id).execute()
        await update.message.reply_text(f'✅ Դուք ընտրեցիք {english_group}-ին։\n\n🥳 Վերջ, ամեն ինչ պատրաստ է, հրամանները տեսնելու համար օգտագործեք /menu հրամանը։')

    else: await message_response(update, context)