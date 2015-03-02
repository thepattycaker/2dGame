import pyglet, math
from pyglet.window import key
from pyglet.gl import *
from pyglet import image
#from game import center_image

#game_window = pyglet.window.Window(800, 600)

main_batch = pyglet.graphics.Batch()
pyglet.resource.path = ['../images/Level_1_Graphics']
pyglet.resource.reindex()
pencil_image = pyglet.resource.image("Pencils.png")
computer_image = pyglet.resource.image("Computer.png")
desktop_image = pyglet.resource.image("Desktop.png")
#background_image = pyglet.resource.image("Background.png")

background = image.load("background.png")
width, height = background.width, background.height
game_window = pyglet.window.Window(width, height)


@game_window.event
def on_draw():
    game_window.clear()
    background.blit(0, 0, 0)

    #pencil_image.blit(0, 0)
    #computer_image.blit(0, 0)
    #Desktop_image.blit(0, 0)

pyglet.app.run()
