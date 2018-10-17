import json
import requests
import configs
import urllib.parse
from slugbot import botutils
import facebook
import random


class PagePost:
    def __init__(self, post:dict):
        self.time = ''
        self.id = ''
        self.message = ''
        if 'created_time' in post:
            self.time = post['created_time']
        if 'id' in dict:
            self.id = post['id']
        if 'message' in post:
            self.message = post['message']

class CrawlingSlug:
    def __init__(self, page_id: str, token: str):
        self.page_id = page_id
        self.token = token
        self.requestLimit = 100

    def crawl(self, url='') -> dict:
        if url == '':
            url = 'https://graph.facebook.com/v2.10/{}/posts?limit={}&access_token={}'.format(self.page_id,
                                                                                              self.requestLimit,
                                                                                              self.token)
        try:
            req = requests.get(url)
        except Exception:
            print('connection error')
            return {}

        return req.json()

    def find(self, wannafind: str, max_posts=4096, exclusion=False) -> list:

        goodies = self.crawl()
        posts = []
        res = []
        cnt = 0
        while True:

            if 'data' in goodies:
                posts = goodies['data']

            for post in posts:
                if 'message' in post:
                    msg = str(post['message'])

                    if cnt >= max_posts:
                        return res

                    if exclusion:
                        gab = msg.find('\n')
                        mic = msg.rfind('\n')
                        if gab != -1 and mic != -1 and gab != mic:
                            msg = msg[gab+1:mic]

                    if msg.find(wannafind) != -1:
                        res.append(post)
                        cnt += 1

            if 'paging' in goodies:
                if 'next' in goodies['paging']:
                    goodies = self.crawl(goodies['paging']['next'])
                else:
                    break
            else:
                break

        return res

    def view(self, trgt: str, solo=False) -> list:
        goodies = self.crawl()
        posts = []
        res = []
        while True:

            if 'data' in goodies:
                posts = goodies['data']

            for post in posts:
                if 'message' in post:

                    msg = str(post['message'])
                    mic = msg.find('\n')

                    if mic != -1:
                        msg = msg[0:mic]

                    if msg == trgt:
                        res.append(post)
                        if solo:
                            return res

            if 'paging' in goodies:
                if 'next' in goodies['paging']:
                    goodies = self.crawl(goodies['paging']['next'])
                else:
                    break
            else:
                break

        return res

    def view_comments(self, post_id) -> list:
        url = 'https://graph.facebook.com/v2.10/{}/comments?access_token={}'.format(post_id, self.token)
        res = []

        try:
            goodies = requests.get(url).json()
        except Exception:
            return res

        while True:

            if 'data' in goodies:
                for cmt in goodies['data']:
                    res.append(cmt)

            if 'paging' in goodies:
                if 'next' in goodies['paging']:
                    try:
                        goodies = requests.get(goodies['paging']['next']).json()
                    except Exception:
                        goodies = {}
                else:
                    break
            else:
                break

        return res

class EasterEggHandler:
    def __init__(self, bot: botutils.SlugBot):
        self._bot = bot
        self.easter_names = {}
        with open('source/easter/name.json', 'r') as f:
            self.easter_names = json.load(f)

    @property
    def the_bot(self):
        return self._bot

    def on_message(self, user: botutils.User, message: str):

        value = 0
        for name in self.easter_names:
            if message.find(name) != -1:
                self.the_bot.smart_send_msg(user, self.easter_names[name])
                value = 1

class ChatHandler:
    def __init__(self, bot: botutils.SlugBot):
        self._bot = bot
        self.list_chat = []
        with open('source/text/chitchat.json', 'r') as f:
            self.list_chat = json.load(f)

    @property
    def the_bot(self):
        return self._bot

    def on_message(self, user: botutils.User, message: str):
        #TEMPORARY
        #TODO implement natural language processing
        self.the_bot.smart_send_msg(random.choice(user, self.list_chat[user.lang]))

def get_slug(site):
    if site in slug_map:
        return slug_map[site]
    else:
        s = ''
        for entry in slug_map:
            s += entry + '\n'
        return s


def localize(user: botutils.User):
    lang = 0
    users = []
    with open('userstat.json', 'r') as f:
        users = json.load(f)

    if user.userid in users:
        lang = users[user.userid]['lang']
    else:
        users[user.userid] = {'score': 0, 'lang': 0}
        with open('userstat.json', 'w') as f:
            json.dump(users, f)
    user.lang = lang


def page_post(ID, access_token, msg):
    id = urllib.parse.quote(ID)
    nmsg = urllib.parse.quote(msg)
    r = requests.post('https://graph.facebook.com/v2.10/{}/feed?message={}&access_token={}'.format(id, nmsg,
                                                                                                   access_token))
    return r.content

def find_in_saved(filename, target):
    saved = []
    with open('source/parsed/' + filename, 'r') as f:
        saved = json.load(f)

    for sv in saved:
        pass



aqua_slug = CrawlingSlug(configs.PAGE_ID[0], configs.ACCESS_TOKEN)
ignis_slug = CrawlingSlug(configs.PAGE_ID[1], configs.ACCESS_TOKEN)
flamma_slug = CrawlingSlug(configs.PAGE_IDS['hn'], configs.ACCESS_TOKEN)
terra_slug = CrawlingSlug(configs.PAGE_IDS['c8'], configs.ACCESS_TOKEN)
aer_slug = CrawlingSlug(configs.PAGE_IDS['h8'], configs.ACCESS_TOKEN)

tenebrae_slug = CrawlingSlug(configs.PAGE_IDS['hhchs'], configs.ACCESS_TOKEN)
lux_slug = CrawlingSlug(configs.PAGE_IDS['chchs'], configs.ACCESS_TOKEN)

test_slug = CrawlingSlug('1181443615334961', configs.ACCESS_TOKEN)


slug_map = {

    'cn': aqua_slug,
    'hn': flamma_slug,
    'c8': terra_slug,
    'h8': aer_slug,
    'hhchs': tenebrae_slug,
    'chchs': lux_slug,
    'test30182384': test_slug
}

