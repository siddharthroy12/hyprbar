from gi.repository import Gtk, GObject
from math import pi as PI
from widgets.module_container import ModuleContainer
import compositor

class WorkspacesDrawingArea(Gtk.DrawingArea):
    def __init__(self, config):
        super().__init__()
        self.circle_size = 5
        self.spacing = 10
        self.workspaces = []
        self.active_workspace = 1
        self.set_draw_func(self.on_draw)
        compositor.workspaces.add_listener(self.on_workspaces_change)
        compositor.active_workspace.add_listener(self.on_active_workspace_change)

        self.on_workspaces_change(self.workspaces)

    def on_active_workspace_change(self, active_workspace):
        self.active_workspace = active_workspace

        def after_sometime():
            self.queue_draw()
        GObject.timeout_add(100, after_sometime)

    def on_workspaces_change(self, workspaces):
        self.workspaces = workspaces
        def after_sometime():
            self.set_content_width(len(self.workspaces)*((self.circle_size*2)+self.spacing)-self.spacing/2)
            self.queue_draw()
        GObject.timeout_add(100, after_sometime)

    def tick(self):
        self.queue_draw()
        GObject.timeout_add(1, self.tick)

    def set_progress(self, progress):
        self.progress = progress
        self.queue_draw()

    def draw_circle(self, cr, r, x, y):
        color = (225, 225, 225)
        cr.new_sub_path()
        cr.set_source_rgb(*color)
        cr.arc(x, y, r, 0, 2.0 * PI)
        cr.stroke() 

    def on_draw(self, area, cr, width, height):
        cr.set_source_rgb(225, 225, 225)

        center_x = width / 2.0
        center_y = height / 2.0
        
        for index, workspace in enumerate(self.workspaces):
            x = (index*(self.circle_size*2+self.spacing)+self.circle_size+2)
            self.draw_circle(cr, self.circle_size, x, center_y)
            if workspace == self.active_workspace:
                self.draw_circle(cr, 2, x, center_y)

class Workspaces(ModuleContainer):
    def __init__(self, config, window):
        super().__init__(window)
        widget = WorkspacesDrawingArea(config)
        self.append(widget)


