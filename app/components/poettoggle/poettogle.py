from kivy.clock import Clock
from kivy.properties import BooleanProperty, NumericProperty, StringProperty
from kivy.uix.togglebutton import ToggleButton

from app.components.bioview.bioview import BioView


class PoetToggle(ToggleButton):
    __events__ = ("on_long_press", )

    long_press_time = NumericProperty(1)
    pressed = BooleanProperty(False)
    poet_name = StringProperty("Poet Name")
    poet_bio = StringProperty("Poet Bio")

    def __init__(self, **kwargs):
        super(PoetToggle, self).__init__(**kwargs)
    
    def on_press(self):
        self.pressed = True

        if self.state == "down":
            press_time = self.long_press_time
            self._clockev = Clock.schedule_once(self._do_long_press, press_time)
        else:
            self._clockev.cancel()

    def on_release(self):
        self.pressed = False

    def _do_long_press(self, dt):
        if self.pressed == True:
            self.dispatch('on_long_press')
        
    def on_long_press(self, *largs):
        self.show_bio()

    def show_bio(self):
        bio_view = BioView(poet_name=self.poet_name, poet_bio=self.poet_bio)
        bio_view.open()
