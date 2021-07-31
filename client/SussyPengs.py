import math

from kivy import Config
from kivy.uix.modalview import ModalView

Config.set('graphics', 'maxfps', '60')

# Config.set('graphics', 'width', f'{math.floor(3800 / 2.5)}')
# Config.set('graphics', 'height', f'{math.floor(2400 / 2.5)}')

Config.set('graphics', 'width', f'{1441}')
Config.set('graphics', 'height', f'{752}')
from kivymd.app import MDApp
from kivy.core.window import Window as KVWindow
from kivy.clock import Clock

loading_text = "As temperatures worldwide continue to rise, Club Penguin is under threat from melting. In a " \
               "last ditch effort to preserve what little is left, the Elite Penguin Force has devised a new form of " \
               "energy. Dubbed Puffle Power, it relies on the black puffles, fed with O'berries, to generate more " \
               "power. \n \n \nThey gathered, ready to build this magical machine, not knowing that among them lay " \
               "an impostor. A representative of Clam Petroleum, posing as a regular agent, attempts what he can to " \
               "destroy the effort of the Penguins. Can the penguins stop him and save the island?"

class TasksPopup(ModalView):
    pass

class SussyPengs(MDApp):

    def __init__(self):
        super(SussyPengs, self).__init__()
        self.username = None
        self.viewport_size = (
            math.floor(3800 / 2.5),
            math.floor(2400 / 2.5)
        )

    def open_tasks(self):
        popup = TasksPopup()
        popup.open()

    def build(self):
        super(SussyPengs, self).build()
        self.root.ids.menu_text.text = loading_text
        self.root.current = 'game_screen'
        self.cutscene()

    def cutscene(self):
        def advance_text(*args):
            app.root.ids.menu_text.pos[1] += 2

        callback = Clock.schedule_interval(advance_text, 0.02)


if __name__ == '__main__':
    app = SussyPengs()
    app.run()
