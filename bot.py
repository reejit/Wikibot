import time
import wikipedia

from telebot import TeleBot, types

bot_token = ''  # Paste your token API
bot = TeleBot(token=bot_token)
error = 'Wrong word, use /title'
error2 = 'Wrong word, use /suggest'
word = " for the word..."


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(chat_id=message.chat.id, text='Greetings! Welcome, I am WikiBot.', reply_markup=main_keyboard())


@bot.message_handler(commands=['extra'])
def send_welcome(message):
    text = 'A bunch of <b>extra commands</b> I provide: \n\n' \
           '/dev - provides information about my creator\n' \
           '/source - my source code\n' \
           '/contributions - to contribute to this project\n' \
           '/issues - to submit problems/issues\n' \
           '/purpose - shows the purpose why I was made'
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='html', reply_markup=main_extra())


@bot.message_handler(commands=['purpose'])
def purpose(message):
    text = 'I was made with the purpose to make wikipedia accessible with a bot.'
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=main_keyboard())


@bot.message_handler(commands=['dev'])
def dev(message):
    text = 'I was made with ❤ by @themagicalmammal.'
    bot.send_message(chat_id=message.chat.id, text=text, reply_markup=main_keyboard())


@bot.message_handler(commands=['source'])
def dev(message):
    text = 'This is an Open Source Project. My code is ' \
           '<a href="https://github.com/themagicalmammal/WikiBot">here</a>. '
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='html', reply_markup=main_keyboard())


@bot.message_handler(commands=['issues'])
def dev(message):
    text = 'If you have problems or want to submit a issue, go <a ' \
           'href="https://github.com/themagicalmammal/WikiBot/issues">here</a>. '
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='html', reply_markup=main_keyboard())


@bot.message_handler(commands=['contributions'])
def dev(message):
    text = 'href="https://github.com/themagicalmammal/WikiBot/pulls">Contributions</a> are happily accepted.'
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='html', reply_markup=main_keyboard())


@bot.message_handler(commands=['help'])
def aid(message):
    text = 'You can use the following commands: \n\n' \
           '<b>Primary</b> \n' \
           '/definition - fetches definition of the word you want \n' \
           '/title - fetches a bunch of related titles for a word \n' \
           '/url - gives the URL for the wiki page of the word \n' \
           '<b>Secondary</b> \n' \
           '/map - location in map with wiki database \n' \
           '/nearby - locations near a coordinate \n' \
           '/random - fetches a random title from the wiki page \n' \
           '/suggest - returns a suggested word or none if not found \n\n' \
           '<b>Others</b> \n' \
           '/extra - some extra set of commands \n'\
           '/titles - fetches all possible titles for a word \n\n' \
           '<b>UnSafe</b> \n' \
           '/lang - set the language you want, wrong prefix will break commands (<a ' \
           'href="https://meta.wikimedia.org/wiki/List_of_Wikipedias">list of languages</a>)'
    bot.send_message(chat_id=message.chat.id, text=text, parse_mode='html', reply_markup=main_keyboard())


@bot.message_handler(commands=['title'])
def title(message):
    title_msg = bot.reply_to(message, "<b>Title</b>" + word, parse_mode='html')
    bot.register_next_step_handler(title_msg, process_title)


def process_title(message):
    # noinspection PyBroadException
    try:
        title_msg = str(message.text)
        title_result = wikipedia.search(title_msg, results=4)
        bot.send_message(chat_id=message.chat.id, text="Possible titles are...",
                         parse_mode='html')
        for i in title_result:
            bot.send_message(chat_id=message.chat.id, text=i.replace(title_msg, "<b>" + title_msg + "</b>"),
                             parse_mode='html', reply_markup=main_keyboard())
    except Exception:
        bot.send_message(chat_id=message.chat.id, text=error2, reply_markup=main_keyboard())


@bot.message_handler(commands=['titles'])
def titles(message):
    titles_msg = bot.reply_to(message, "<b>Titles</b>" + word, parse_mode='html')
    bot.register_next_step_handler(titles_msg, process_titles)


def process_titles(message):
    # noinspection PyBroadException
    try:
        titles_msg = str(message.text)
        titles_result = wikipedia.search(titles_msg)
        bot.send_message(chat_id=message.chat.id, text="All possible titles are...",
                         parse_mode='html')
        for i in titles_result:
            bot.send_message(chat_id=message.chat.id, text=i.replace(titles_msg, "<b>" + titles_msg + "</b>"),
                             parse_mode='html', reply_markup=main_keyboard())
    except Exception:
        bot.send_message(chat_id=message.chat.id, text=error2, reply_markup=main_keyboard())


@bot.message_handler(commands=['url'])
def url(message):
    url_msg = bot.reply_to(message, "<b>URL</b>" + word, parse_mode='html')
    bot.register_next_step_handler(url_msg, process_url)


def process_url(message):
    # noinspection PyBroadException
    try:
        url_message = str(message.text)
        url_str = wikipedia.page(url_message)
        url_result = str(url_str.url)
        pre = "URL for the word <b>" + url_message + "</b> is \n\n"
        bot.send_message(chat_id=message.chat.id, text=pre + url_result, parse_mode= 'html',
                         reply_markup=main_keyboard())
    except Exception:
        bot.send_message(chat_id=message.chat.id, text=error, reply_markup=main_keyboard())


@bot.message_handler(commands=['random'])
def random(message):
    # noinspection PyBroadException
    try:
        random_title = str(wikipedia.random(pages=1))
        bot.send_message(chat_id=message.chat.id, text=random_title, reply_markup=main_keyboard())
    except Exception:
        bot.send_message(chat_id=message.chat.id, text=error, reply_markup=main_keyboard())


@bot.message_handler(commands=['definition'])
def definition(message):
    def_msg = bot.reply_to(message, "<b>Definition</b>" + word, parse_mode='html')
    bot.register_next_step_handler(def_msg, process_definition)


def process_definition(message):
    try:
        def_msg = str(message.text)
        def_str = str(wikipedia.summary(def_msg, sentences=20, auto_suggest=True, redirect=True))
        bot.send_message(chat_id=message.chat.id, text="<b>" + def_msg + "</b> \n\n" + def_str, parse_mode='html',
                         reply_markup=main_keyboard())
    except Exception as c:
        bot.send_message(chat_id=message.chat.id, text=c, reply_markup=main_keyboard())


@bot.message_handler(commands=['map'])
def map(message):
    co_msg = bot.reply_to(message, "<b>Location</b> of the place...", parse_mode='html')
    bot.register_next_step_handler(co_msg, process_co)


def process_co(message):
    # noinspection PyBroadException
    try:
        co_msg = str(message.text)
        lat, lon = wikipedia.WikipediaPage(co_msg).coordinates
        bot.send_location(chat_id=message.chat.id, latitude=lat, longitude=lon, reply_markup=main_keyboard())
    except Exception:
        bot.send_message(chat_id=message.chat.id, text="Not a location.", reply_markup=main_keyboard())


@bot.message_handler(commands=['nearby'])
def geo(message):
    geo_msg = bot.reply_to(message, "Send me the <b>coordinates</b>...", parse_mode='html')
    bot.register_next_step_handler(geo_msg, process_geo)


def process_geo(message):
    # noinspection PyBroadException
    try:
        lat, lan = (str(message.text).replace('E', '').replace('W', '').replace('N', '').replace('S', '').
                    replace('° ', '').replace('°', '').replace(',', '').replace('  ', ' ').split(" "))
        for i in wikipedia.geosearch(latitude=lat, longitude=lan, results=5, radius=1000):
            bot.send_message(chat_id=message.chat.id, text=i, reply_markup=main_keyboard())
    except Exception:
        bot.send_message(chat_id=message.chat.id, text="Not a location.", reply_markup=main_keyboard())


@bot.message_handler(commands=['suggest'])
def suggest(message):
    suggest_msg = bot.reply_to(message, "You want <b>suggestion</b> for...", parse_mode='html')
    bot.register_next_step_handler(suggest_msg, process_suggest)


def process_suggest(message):
    # noinspection PyBroadException
    try:
        suggest_msg = str(message.text)
        suggest_str = str(wikipedia.suggest(suggest_msg))
        pre = "The suggestion for the word <b>" + suggest_msg + "</b> is"
        bot.send_message(chat_id=message.chat.id, text=pre, parse_mode='html', reply_markup=main_keyboard())
        bot.send_message(chat_id=message.chat.id, text=suggest_str, reply_markup=main_keyboard())
    except Exception:
        bot.send_message(chat_id=message.chat.id, text="No Suggestions", reply_markup=definition(message))


@bot.message_handler(commands=['back'])
def back(message):
    bot.send_message(chat_id=message.chat.id, text="Going <b>Back</b>...", parse_mode='html',
                     reply_markup=main_keyboard())


@bot.message_handler(commands=['lang'])
def ln(message):
    ln_msg = bot.reply_to(message, "Type the prefix of you <b>language</b>...", parse_mode='html')
    bot.register_next_step_handler(ln_msg, process_ln)


def process_ln(message):
    # noinspection PyBroadException
    try:
        ln_msg = str(message.text)
        ln_str = str(wikipedia.set_lang(ln_msg))
        if ln_str == "None":
            ln_str = "Done"
        bot.send_message(chat_id=message.chat.id, text=ln_str, reply_markup=main_keyboard())
    except Exception:
        bot.send_message(chat_id=message.chat.id, text="Error, setting language", reply_markup=definition(message))


def main_extra():
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True, one_time_keyboard=True)
    texts = ['/dev', '/source', '/contributions', '/issues', '/purpose', '/back']
    buttons = []
    for text in texts:
        button = types.KeyboardButton(text)
        buttons.append(button)
    markup.add(*buttons)
    return markup


def main_keyboard():
    markup = types.ReplyKeyboardMarkup(row_width=5, resize_keyboard=True, one_time_keyboard=True)
    texts = ['/definition', '/title', '/url', '/map', '/nearby', '/random', '/suggest', '/help', '/lang', '/extra']
    buttons = []
    for text in texts:
        button = types.KeyboardButton(text)
        buttons.append(button)
    markup.add(*buttons)
    return markup


while True:
    # noinspection PyBroadException
    try:
        bot.enable_save_next_step_handlers(delay=2)
        bot.load_next_step_handlers()
        bot.polling()
    except Exception:
        time.sleep(5)
