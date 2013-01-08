from gi.repository import Gtk, Gio, GObject, Notify
import time

LABEL_MARKUP = "<span font_desc=\"64.0\">%02i:%02i</span>"

class Timer(Gtk.Box):
    def __init__(self):
        Gtk.Box.__init__(self)
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.time_label = time_label = Gtk.Label('')
        self.time = 0
        self.alert = Alert()
        upper_space = Gtk.Label('')
        bottom_space = Gtk.Label('')        
        right_space = Gtk.Label('')
        left_space = Gtk.Label('')
        center = Gtk.Box()
        center.pack_start(left_space, True, True, 0)
        center.pack_start(time_label, True, True, 0)
        center.pack_start(right_space, True, True, 0)
        self.pack_start(upper_space, False, True, 24)
        self.pack_start(center, True, True, 0)
        self.pack_start(bottom_space, True, True, 0)
        
        time_label.set_markup(LABEL_MARKUP % (0, 0))
        
        self.timeout_id = None

    def pomodoro(self):
        if self.timeout_id:
            GObject.source_remove(self.timeout_id)
        self.time_label.set_markup(LABEL_MARKUP % (25, 0))
        self.time = 25 * 60
        self.timeout_id = GObject.timeout_add(1000, self.count_down)
        
    def short_break(self):
        if self.timeout_id:
            GObject.source_remove(self.timeout_id)
        self.time_label.set_markup(LABEL_MARKUP % (5, 0))
        self.time = 5 * 60
        self.timeout_id = GObject.timeout_add(1000, self.count_down)
        
    def long_break(self):
        if self.timeout_id:
            GObject.source_remove(self.timeout_id)
        self.time_label.set_markup(LABEL_MARKUP % (15, 0))
        self.time = 15 * 60
        self.timeout_id = GObject.timeout_add(1000, self.count_down)
        
    def count_down(self):
        if self.time == 0:
            GObject.source_remove(self.timeout_id)
            #self.alert.show()
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
