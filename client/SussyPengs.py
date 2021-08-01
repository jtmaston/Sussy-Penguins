import math
from sys import modules

from kivy import Config
from kivy.graphics import Rectangle, Color
from kivy.support import install_twisted_reactor
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.modalview import ModalView
from kivy.uix.widget import Widget

Config.set('graphics', 'maxfps', '60')

# Config.set('graphics', 'width', f'{math.floor(3800 / 2.5)}')
# Config.set('graphics', 'height', f'{math.floor(2400 / 2.5)}')

Config.set('graphics', 'width', f'{1441}')
Config.set('graphics', 'height', f'{752}')
from kivymd.app import MDApp
from kivy.core.window import Window as KVWindow
from kivy.clock import Clock

if 'twisted.internet.reactor' in modules:
    del modules['twisted.internet.reactor']
install_twisted_reactor()  # integrate twisted with kivy

from twisted.internet import reactor
from networking import *

loading_text = "As temperatures worldwide continue to rise, Club Penguin is under threat from melting. In a " \
               "last ditch effort to preserve what little is left, the Elite Penguin Force has devised a new form of " \
               "energy. Dubbed Puffle Power, it relies on the black puffles, fed with O'berries, to generate more " \
               "power. \n \n \nThey gathered, ready to build this magical machine, not knowing that among them lay " \
               "an impostor. A representative of Clam Petroleum, posing as a regular agent, attempts what he can to " \
               "destroy the effort of the Penguins. Can the penguins stop him and save the island?"


class TasksPopup(ModalView):
    pass


class RightPenguin(Widget):
    def __init__(self, penguin_color='blue', **kwargs):
        super(RightPenguin, self).__init__(**kwargs)
        self.penguin_color = penguin_color


class LeftPenguin(Widget):
    def __init__(self, penguin_color='blue', **kwargs):
        super(LeftPenguin, self).__init__(**kwargs)
        self.penguin_color = penguin_color


class ForwardPenguin(Widget):
    def __init__(self, penguin_color='blue', **kwargs):
        super(ForwardPenguin, self).__init__(**kwargs)
        self.penguin_color = penguin_color


class SussyPengs(MDApp):

    def __init__(self):
        super(SussyPengs, self).__init__()
        self.username = None
        self.viewport_size = (
            math.floor(3800 / 2.5),
            math.floor(2400 / 2.5)
        )
        self.factory = None
        self.penguin_color = None
        self.profession = 'Engineer'

    def open_tasks(self):
        popup = TasksPopup()
        popup.open()

    def build(self):
        super(SussyPengs, self).build()

        self.factory = ClientFactory(self)
        reactor.connectTCP("localhost", 8123, self.factory)
        self.root.ids.menu_text.text = loading_text
        self.root.current = 'welcome_screen'
        self.cutscene()
        self.root.ids.player_1.penguin_color = 'red'
        self.root.ids.player_2.penguin_color = 'yellow'

    def find_game(self):
        self.factory.client.transport.write(get_transportable_data({
            'sender': self.username,
            'color': self.penguin_color,
            'command': 'ask_game'
        }))

    def show_stats(self, stats):
        print(stats)
        self.root.ids.stats_block.text = f"Health: {stats['health']}," \
                              f" Repair: {stats['repair']}," \
                              f" Computer: {stats['computer']}," \
                              f" Technical: {stats['technical']}"
        self.root.current = 'stats'

    def cutscene(self):
        def advance_text(*args):
            app.root.ids.menu_text.pos[1] += 2

        self.cutscene_callback = Clock.schedule_interval(advance_text, 0.02)


if __name__ == '__main__':
    app = SussyPengs()
    app.run()
