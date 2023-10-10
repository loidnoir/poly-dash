from telegram import Update
from telegram.ext import ContextTypes

from config.exams import exams
from user import User


async def exams_command(update: Update, context: ContextTypes):
    user = User.get_or_none(id=update.effective_user.id)
    group = user.group

    if group is None:
        await update.message.reply_text('❌ Դուք չեք ընտրել ձեր գործ-ընկերությունը')
        return

    data = exams[group - 1]
    await update.message.reply_text(f'🤡 Քննության օրեր (գործ {group})\n\n' + "\n".join(data))