import pyglet
 
win = pyglet.window.Window()
 
@win.event
def on_draw():
    win.clear()
 
pyglet.app.run()		