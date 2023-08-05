from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from sql import *
from telegram.error import NetworkError, TimedOut
from time import sleep
CHANNELS = [("Siz buni blarmidingiz", -1001928509371, 'https://t.me/siz_buni_blarmidingiz')]
TOKEN = "6630912635:AAF1uTbHdYV7hmG6sPyFCh2WzOTYfoT36LM"


def text(language, command, user=None):
    dict = {
        'uzb': {
            1: f"Assalomu alaykum, {user.first_name}\nBu maxfiy bot boʻlib, u bilan oʻsha funksiyalarni ulashingiz mumkin!\n\nBot ishga tushishini xohlaysizmi?\n“Start” tugmasini bosing.",
            2: "Kerakli funktsiyani tanlash bilan boshlaylik:",
            3: "Ajoyib, boshlaymiz!\n\nInstagram usernamingizni kiriting:",
            4: "🤔ushbu botdan foydalanishni davom ettirish uchun homiylarimizning kanallariga obuna boʻlishingiz kerak\n\nUlar tufayli bizning botimiz mutlaqo bepul va sizdan hech qanday sarmoya talab qilmaydi!\n\nObuna boʻlgandan soʻng 'Подписался' tugmasini bosing.",
            5: "Xizmat ishga tushdi, Instagramni 24 soat ichida tekshiring.",
            6: "Siz hali barcha kanalarga obuna bo'lmadingiz!",
            7: "Suniy Intelektda yaratilgan bot tez, oson va qulay. \n\nSinab ko'ring: <a href='https://t.me/chatgpt_officia1_bot'>ChatGPT-3</a>"
        },
        "rus": {
            1: f"Привет, {user.first_name}\nЭто секретный бот с помощью которого, ты сможешь подключить те самые функции!\n\nХочешь, чтобы бот приступил к работе?\nТогда нажимай 'start'",
            2: 'Давай начнем с выбора нужной функции:',
            3: "Супер, приступим!\n\nВведите ник вашего профиля:",
            4: "🤔Упс.. чтобы продолжить пользоваться данным ботом, необходимо подписаться на каналы наших спонсоров\n\nБлагодаря им наш бот абсолютно бесплатный и не требует какого либо вложения средств с твоей стороны!\n\nПосле подписки жми кнопку 'Подписался'",
            5: "Сервис начал работу, проверьте Инстаграм в течении 24час.",
            6: "Вы еще не подписаны на все каналы!",
            7: "Бот, построенный на искусственном интеллекте, быстрый, простой и удобный. \n\nПопробуйте: <a href='https://t.me/chatgpt_officia1_bot'>ChatGPT-3</a>"
        }
    }
    return dict[language][command]


async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    old_user = get_user(user.id)
    if old_user is None:
        insert_user(user_id=user.id)
        await update.message.reply_text("🇷🇺 - Выберите язык!\n🇺🇿 - Tilni tanlang!", reply_markup=buttons(type='lang'))
    else:
        try:
            print(old_user)
            update_info(user_id=user.id, state=2)
            await update.message.reply_text(text(language=old_user[1], command=1, user=user), reply_markup=buttons(type='start'))
        except Exception as e:
            print(e)
            await update.message.reply_text("🇷🇺 - Выберите язык!\n🇺🇿 - Tilni tanlang!", reply_markup=buttons(type='lang'))


async def message_handler(update: Update, context: CallbackContext):
    user = update.effective_user
    old_user = get_user(user.id)
    if old_user[2] == 1:
        await update.message.reply_text(text(language=old_user[1], command=1, user=user))
        update_info(user.id, 2)
    elif old_user[2] == 4:
        await update.message.reply_text("Загрузка..")
        sleep(2)
        await update.message.reply_text("Анализ..")
        sleep(2)
        await update.message.reply_text(text(language=old_user[1], command=4, user=user),
                                        reply_markup=buttons(type='channels'))
        update_info(user_id=user.id, state=5)


async def inline_handler(update: Update, context: CallbackContext):
    user = update.effective_user
    old_user = get_user(user.id)
    query = update.callback_query
    if old_user[2] == 1:
        await query.message.delete()
        old_user = update_info(user_id=user.id, language=query.data, state=2)
        await query.message.reply_text(text(language=old_user[1], command=1, user=user), reply_markup=buttons(type='start'))
    elif old_user[2] == 2:
        await query.edit_message_reply_markup()
        await query.message.reply_text(text(language=old_user[1], command=2, user=user), reply_markup=buttons(type='insta'))
        update_info(user_id=user.id, state=3)
    elif old_user[2] == 3:
        await query.edit_message_reply_markup()
        await query.message.reply_text(text(language=old_user[1], command=3, user=user))
        update_info(user_id=user.id, state=4)
    elif old_user[2] == 5:
        await query.message.delete()
        btn = []
        count = 0
        for channel in CHANNELS:
            subscribed = await context.bot.getChatMember(user_id=user.id, chat_id=channel[1])
            if subscribed['status'] in ['member', 'creator', 'administrator']:
                count += 1
            else:
                btn.append(
                    [InlineKeyboardButton(text=channel[0], url=channel[2])]
                )
        if count != len(CHANNELS):
            btn.append([InlineKeyboardButton(text='Подписался✅', callback_data='check')])
            await update.callback_query.message.reply_text(text(old_user[2], 6, user),
                                                           reply_markup=InlineKeyboardMarkup(btn))
            return 0
        await update.callback_query.message.reply_text(text(old_user[1], 5, user))
        await update.callback_query.message.reply_text(text(old_user[1], 7, user), parse_mode='HTML')


def buttons(type=None):
    btn = []
    if type == "lang":
        btn = [[InlineKeyboardButton("Русский язык", callback_data='rus')], [InlineKeyboardButton('Uzbek tili', callback_data='uzb')]]
    elif type == 'start':
        btn = [[InlineKeyboardButton('start', callback_data='start')]]
    elif type == 'insta':
        btn = [[InlineKeyboardButton('Insta Function', callback_data='insta')]]
    elif type == 'check':
        btn = [[InlineKeyboardButton('Подписался', callback_data='check')]]
    elif type == 'channels':
        for i in CHANNELS:
            btn.append([InlineKeyboardButton(i[0], url=i[2])])
        btn.append([InlineKeyboardButton('Подписался', callback_data='check')])
    return InlineKeyboardMarkup(btn)


def main():
    try:
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler('start', start))
        application.add_handler(MessageHandler(filters.TEXT, message_handler))
        application.add_handler(CallbackQueryHandler(inline_handler))
        application.run_polling()
    except TimedOut:
        sleep(1)

if __name__ == '__main__':
    main()
