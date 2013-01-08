from gi.repository import Gtk, Gio, Gdk
from timer import Timer
from logger import Logger
import os

class Window(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self, title="Pomodoro+",
                                      application=app,
                                      hide_titlebar_when_maximized=True)
        self.set_default_size(680, 460)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_icon_from_file(self.get_icon_path())
        
        css = Gtk.CssProvider()
        css.load_from_path(self.get_css_file())
        
        context = Gtk.StyleContext()
        context.add_provider_for_screen(Gdk.Screen.get_default(),
                                        css,
                                        Gtk.STYLE_PROVIDER_PRIORITY_USER)
        
        self.box = box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.notebook = notebook = Gtk.Notebook()        
        self.toolbar = toolbar = Toolbar()
        
        self.box.pack_start(toolbar, False, False, 0)
        self.box.pack_start(notebook, True, True, 0)
        self.add(box)
        
        notebook.set_show_border(False)
        notebook.set_show_tabs(False)

        eventbox = Gtk.EventBox()
        eventbox.get_style_context().add_class('white-bg')
        self.timer = timer = Timer()
        eventbox.add(timer)
        notebook.append_page(eventbox, Gtk.Label('Timer'))
        notebook.set_current_page(-1)
        
        self.show_all()
        eventbox.grab_focus()
        
    def get_icon_path(self):
        path = os.getcwd()+'/data/pomodoro+.png'
        if os.path.exists(path):
            return path
        else:
            return '/usr/share/icons/hicolor/scalable/apps/pomodoro+.png'
            
    def get_css_file(self):
        path = os.getcwd()+'/data/gtk-style.css'
        if os.path.exists(path):
            return path
        else:
            return '/usr/share/pomodoro+/gtk-style.css'

        
class Toolbar(Gtk.Toolbar):
    def __init__(self):
        Gtk.Toolbar.__init__(self)
        self.get_style_context().add_class('menubar')
        self.set_size_request(-1, 42)
        self.set_can_focus(False)
        
        empty = Gtk.ToolItem()
        
        
        spacer = Gtk.ToolItem()
        spacer.set_expand(True)
                          
        center = Gtk.Box()
        #center.get_style_context().add_class('linked')
        pomodoro = Gtk.Button('Pomodoro')
        #pomodoro.get_style_context().add_class('silver')
        pomodoro.set_relief(Gtk.ReliefStyle.NONE)
        pomodoro.set_can_focus(False)
        shortbreak = Gtk.Button('Short Break')
        #shortbreak.get_style_context().add_class('silver')
        shortbreak.set_relief(Gtk.ReliefStyle.NONE)
        shortbreak.set_can_focus(False)
        longbreak = Gtk.Button('Long Break')
        #longbreak.get_style_context().add_class('silver')
        longbreak.set_relief(Gtk.ReliefStyle.NONE)
        longbreak.set_can_focus(False)
        sep1 = Gtk.SeparatorToolItem()
        sep2 = Gtk.SeparatorToolItem()
        center.pack_start(pomodoro, False, False, 6)
        center.pack_start(sep1, False, False, 6)
        center.pack_start(shortbreak, False, False, 6)
        center.pack_start(sep2, False, False, 6)
        center.pack_start(longbreak, False, False, 6)
        center_item = Gtk.ToolItem()
        center_item.add(center)
        
        spacer2 = Gtk.ToolItem()
        spacer2.set_expand(True)
        
        clear = Gtk.ToolButton()
        clear.get_style_context().add_class('silver')
        clear.set_label('Clear')
        clear.set_can_focus(False)
        
        self.insert(empty, -1)
        self.insert(spacer, -1)
        self.insert(center_item, -1)
        self.insert(spacer2, -1)        
        self.insert(clear, -1)        
        
        pomodoro.connect('clicked', self.on_pomodoro)
        shortbreak.connect('clicked', self.on_short_break)
        longbreak.connect('clicked', self.on_long_break)
        clear.connect('clicked', self.on_clear)

    def on_pomodoro(self, btn):
        window = self.get_parent().get_parent()
        window.timer.pomodoro()
                        
    def on_short_break(self, btn):
        window = self.get_parent().get_parent()
        window.timer.short_break()
        
    def on_long_break(self, btn):
        window = self.get_parent().get_parent()
        window.timer.long_break()
        
    def on_clear(self, btn):
        window = self.get_parent().get_parent()
        window.timer.clear()
        
class App(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self)
        
    def do_activate(self):
        win = Window(self)
        win.present()
