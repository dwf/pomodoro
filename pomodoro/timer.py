from gi.repository import Gtk, GObject, Notify
import time

LABEL_MARKUP = "<span font_desc=\"64.0\">%02i:%02i</span>"


class Timer(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self)
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.time_label = Gtk.Label('')
        self.time_label.set_markup(LABEL_MARKUP % (0, 0))
        self.time = 0
        center = Gtk.Box()
        center.pack_start(self.time_label, True, True, 0)
        self.pack_start(center, True, True, 0)
        self.timeout_id = None
        self.short_break_total_seconds = 0.25 * 60
        self.long_break_total_seconds = 15 * 60
        self.pomodoro_total_seconds = 25 * 60
        self.current_state = None

    def pomodoro(self):
        self._start_common(self.pomodoro_total_seconds)

    def short_break(self):
        self._start_common(self.short_break_total_seconds)

    def long_break(self):
        self._start_common(self.long_break_total_seconds)

    def _start_common(self, duration):
        if self.timeout_id:
            GObject.source_remove(self.timeout_id)
        self.time_label.set_markup(LABEL_MARKUP % divmod(duration, 60))
        self.time = duration
        self.timeout_id = GObject.timeout_add(1000, self.count_down)

    def count_down(self):
        if self.time == 0:
            GObject.source_remove(self.timeout_id)
            window = self.get_parent().get_parent().get_parent()
            window.set_urgency_hint(True)
            return False
        else:
            self.time -= 1
            m, s = divmod(self.time, 60)
            h, m = divmod(m, 60)
            self.time_label.set_markup(LABEL_MARKUP % (m, s))
        return True

    def clear(self):
        if self.timeout_id:
            GObject.source_remove(self.timeout_id)
        self.time_label.set_markup(LABEL_MARKUP % (0, 0))

class Alert():
    def __init__(self):
        Notify.init('Pomodoro')
        self.n = Notify.Notification.new('Pomodoro', 'Ding !', None)
        
    def show(self):
        self.n.show()
        time.sleep(15)
        #Notify.uninit()
        self.n.close()
