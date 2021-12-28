import pyglet
from pyglet.window import key

initial_animation = pyglet.image.load_animation("/home/pi/Desktop/robot face/face.gif")
animation_1 = pyglet.image.load_animation("/home/pi/Desktop/robot face/happy.gif")
animation_2 = pyglet.image.load_animation("/home/pi/Desktop/robot face/sound.gif")

animSprite = pyglet.sprite.Sprite(initial_animation)

w = animSprite.width
h = animSprite.height

window = pyglet.window.Window(width=w, height=h, resizable=True)


@window.event
def on_key_press(symbol, modifiers):
    if symbol == key.A:
        animSprite.image = animation_1

    elif symbol == key.B:
        animSprite.image = animation_2
    
    elif symbol == key.C:
        animSprite.image = initial_animation
        
    elif symbol == key.ENTER:
        print("Enter Key Was Pressed")


@window.event
def on_draw():
    window.clear()
    animSprite.draw()


pyglet.app.run()