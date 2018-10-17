import requests
import threading
import calendar
import flask


class User:

    def __init__(self, userid: str, lang: int):
        self.userid = userid
        self.lang = lang

class Command:

    def __init__(self, name: str, info: str):
        self.name = name
        self.info = info
        self._bot = None

    @property
    def mark(self):
        return len(self.name) + 1

    def onCall(self, user: User, command: str):
        command = command[self.mark+1:]

    def getBot(self):
        return self._bot

class SlugBot:
    def __init__(self, token: str):
        self.token = token
        self.commands = []

    def appendCommand(self, command: Command):
        self.commands.append(command)
        command._bot = self

    def runCommand(self, user: User, command: str):
        flag = False
        for cmd in self.commands:
            if command.startswith(cmd.name):
                if command == cmd.name:
                    cmd.onCall(user, command)
                    flag = True
                elif len(command) > cmd.mark:
                    if command[cmd.mark-1] == ' ':
                        cmd.onCall(user, command)

                else:
                    self.smart_send_msg(user, cmd.info)
                flag = True
                break
        return flag


    def send_msg(self, user: User, msg):
        data = {'recipient': {'id': user.userid},
                'message': {'text': msg}
                }
        print('sending message')
        r = requests.post('https://graph.facebook.com/v2.10/me/messages?access_token=' + self.token, json=data)
        print(r.content)

    def smart_send_msg(self, user: User, msg):
        if len(msg) == 0:
            return
        else:
            for i in range(int(len(msg) / 600) + 1):
                self.send_msg(user, msg[600 * i:600 * (i + 1)])

    def send_img(self, user: User, url):
        data = {'recipient': {'id': user.userid},
                'message': {'attachment': {'type': 'image', 'payload': {'url': url}}}
                }
        print('sending image')
        r = requests.post('https://graph.facebook.com/v2.10/me/messages?access_token=' + self.token, json=data)
        print(r.content)

    def handle_message(self):
        pass


def timestring(formattype, time):
    if formattype == 0:
        result = str(time['year']) + '/' + str(time['month']) + '/' + str(time['day']) + ' ' + str(
            time['hour']) + ':' + str(time['minute']) + ':' + str(time['second'])
        return result
    if formattype == 1:
        hour = str((time['hour'] - 1) % 12 + 1)
        minute = str(time['minute'])
        second = str(time['second'])
        mark = ' AM CST'
        if time['hour'] > 12 or time['hour'] == 0:
            mark = ' PM CST'
        if len(minute) == 1:
            minute = '0' + minute
        if len(second) == 1:
            second = '0' + second
        result = calendar.month_name[time['month']] + ' ' + str(time['day']) + ', ' + str(
            time['year']) + ' ' + hour + ':' + minute + ':' + second + mark
        return result
    return ''






