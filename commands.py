from slugbot.botutils import User, Command, SlugBot
import lang
from utils import aqua_slug, ignis_slug
import configs
import requests
import threading
import json
import random



def init_bot(bot: SlugBot):
    command_list = \
    [
        CommandHelp(),
        CommandViewH(),
        CommandView(),
        CommandFindN(),
        CommandLang(),
        CommandSlug()
    ]
    for command in command_list:
        bot.appendCommand(command)


class CommandHelp(Command):
    def __init__(self):
        super(CommandHelp, self).__init__('/help', '/help')

    def onCall(self, user: User, command: str):
        super(CommandHelp, self).onCall(user, command)
        self.getBot().smart_send_msg(user, lang.INFORMATION[user.lang])


class CommandView(Command):
    def __init__(self):
        super(CommandView, self).__init__('/view', '/view 314256')

    def onCall(self, user: User, command: str):
        self.getBot().smart_send_msg(user, lang.TEXT_0[user.lang])

        target = configs.HEAD[0] + command[self.mark:]
        posts = aqua_slug.view(target, solo=True)
        reply = ''
        for post in posts:
            if 'message' in post:
                reply = reply + post['message'] + '\n'

        if len(reply) == 0:
            self.getBot().smart_send_msg(user, lang.TEXT_2_0[user.lang] + target + lang.TEXT_2_1[user.lang])
        else:
            self.getBot().smart_send_msg(user, reply)


class CommandViewH(CommandView):
    def __init__(self):
        super(CommandViewH, self).__init__()
        self.name = '/viewh'
        self.info = '/viewh 3115'


    def onCall(self, user: User, command: str):
        self.getBot().smart_send_msg(user, lang.TEXT_0[user.lang])

        target = configs.HEAD[1] + command[self.mark:]
        posts = ignis_slug.view(target, solo=True)
        reply = ''
        for post in posts:
            if 'message' in post:
                reply = reply + post['message']

        if len(reply) == 0:
            self.getBot().smart_send_msg(user, lang.TEXT_2_0[user.lang] + target + lang.TEXT_2_1[user.lang])
        else:
            self.getBot().smart_send_msg(user, reply)



class CommandFind(Command):
    def __init__(self):
        super(CommandFind, self).__init__('/find', '/find 班長')

    def onCall(self, user: User, command: str):
        self.getBot().smart_send_msg(user, lang.TEXT_0[user.lang])

        target = command[self.mark:]
        posts = aqua_slug.find(target, exclusion=True)
        reply = ''
        for post in posts:
            if 'message' in post:
                msg = str(post['message'])
                if msg.find('\n') != -1 and msg.startswith(configs.HEAD[0]):
                    reply = reply + msg[:msg.find('\n')] + '\n'

        if len(reply) == 0:
            self.getBot().smart_send_msg(user, lang.TEXT_2_0[user.lang] + target + lang.TEXT_2_1[user.lang])
        else:
            self.getBot().smart_send_msg(user, reply)


class CommandFindH(CommandFind):
    def __init__(self):
        super(CommandFindH, self).__init__()
        self.name = '/findh'
        self.info = '/findh 老師'

    def onCall(self, user: User, command: str):
        self.getBot().smart_send_msg(user, lang.TEXT_0[user.lang])

        target = command[self.mark:]
        posts = ignis_slug.find(target, exclusion=True)
        reply = ''
        for post in posts:
            if 'message' in post:
                msg = str(post['message'])
                if msg.find('\n') != -1:
                    reply = reply + msg[:msg.find('\n')] + '\n'
        if len(reply) == 0:
            self.getBot().smart_send_msg(user, lang.TEXT_2_0[user.lang] + target + lang.TEXT_2_1[user.lang])
        else:
            self.getBot().smart_send_msg(user, reply)


class CommandFindN(CommandFind):
    def __init__(self):
        self.name = '/find'
        self.info = '/find <site> keyword; e.g. /find cn 南投人'

    def onCall(self, user: User, command: str):
        self.getBot().smart_send_msg(user, lang.TEXT_0[user.lang])

        args = command[self.mark:].split()
        site = args[0]
        target = args[1]
        
        slug = utils.get_slut(site)

        if type(slug) != str:
            posts = slug.find(target, exclusion=True)
            reply = ''
            for post in posts:
                if 'message' in post:
                    msg = str(post['message'])
                    if msg.find('\n') != -1:
                        reply = reply + msg[:msg.find('\n')] + '\n'
            if len(reply) == 0:
                    self.getBot().smart_send_msg(user, lang.TEXT_2_0[user.lang] + target + lang.TEXT_2_1[user.lang])
            else:
                self.getBot().smart_send_msg(user, reply)
        else:
            self.getBot().smart_send_msg(user, slug)


class CommandSlug(Command):
    def __init__(self):
        super(CommandSlug, self).__init__('/slug', '/slug')
        self.name = '/slug'
        self.info = '/slug'

    def onCall(self, user: User, command: str):
        with open('source/image/slug.json') as f:
            images = json.load(f)

        image_url = random.choice(images)
        self.getBot().send_img(user, image_url)


class CommandLang(Command):
    def __init__(self):
        super(CommandLang, self).__init__('/lang', 'lang zh')
        self.name = '/lang'
        self.info = '/lang zh'
        self.langmap = {'en': 0, 'zh': 1, 'es': 2}
        self.rmap = ['en', 'zh', 'es']

    def onCall(self, user: User, command: str):
        rlang = command[self.mark:]
        nlang = rlang.strip().lower()

        if nlang in self.langmap:
            user.lang = self.langmap[nlang]
            self.getBot().smart_send_msg(user, lang.TEXT_7[user.lang])

            userstat = {}
            with open('userstat.json', 'r') as f:
                userstat = json.load(f)

            if user.userid in userstat:
                #userstat[user.userid]['lang'] = user.lang
                userstat[user.userid]['lang'] = self.rmap[user.lang]

        else:
            self.getBot().smart_send_msg(user, 'en, zh, es')


