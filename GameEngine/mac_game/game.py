import pyglet, math
from pyglet.window import key

game_window = pyglet.window.Window(800, 600)

main_batch = pyglet.graphics.Batch()
pyglet.resource.path = ['../images']
pyglet.resource.reindex() 
player_image = pyglet.resource.image("player.png") #images go here

def center_image(image):
	"""Sets an image's anchor point to its center"""
	image.anchor_x = image.width/2
	image.anchor_y = image.height/2

center_image(player_image) #center all images on middle point

level_label = pyglet.text.Label(text="This Is Not Mario", x=400, y=575, anchor_x='center', batch=main_batch) #level label

class PhysicalObject(pyglet.sprite.Sprite):
	def __init__(self, *args, **kwargs):
		super(PhysicalObject, self).__init__(*args, **kwargs)

		self.velocity_x, self.velocity_y = 0.0, 0.0

	def update(self, dt):
		self.x += self.velocity_x * dt
		self.y += self.velocity_y * dt
		self.velocity_y -= 75.0 #gravity

class Player(PhysicalObject): 
	def __init__(self, *args, **kwargs):
		super(Player, self).__init__(img=player_image, *args, **kwargs)
		self.speed = 300.0
		self.keys = dict(left=False, right=False, up=False)

	def on_key_press(self, symbol, modifiers):
		if symbol == key.UP: 
			self.keys['up'] = True 
		elif symbol == key.LEFT: 
			self.keys['left'] = True 
		elif symbol == key.RIGHT: 
			self.keys['right'] = True 

	def on_key_release(self, symbol, modifiers):
		if symbol == key.UP: 
			self.keys['up'] = False 
		elif symbol == key.LEFT: 
			self.keys['left'] = False 
		elif symbol == key.RIGHT: 
			self.keys['right'] = False

	def grounded(self):
		if self.y <= 100:
			return True
		else:
			return False

	def update(self, dt):
		super(Player, self).update(dt) 
		if self.keys['left']: 
			self.velocity_x = -self.speed
		elif self.keys['right']: 
			self.velocity_x = self.speed
		else:
			self.velocity_x = 0

		if self.keys['up']:
			if self.grounded():
				self.velocity_y += 150

		if self.grounded():
			self.velocity_y = 0


player = Player(x=400, y=100, batch=main_batch)

game_objects = [player]
game_window.push_handlers(player)

############### starting the game ##############
def update(dt):
	for obj in game_objects: 
		obj.update(dt)

@game_window.event
def on_draw(): # draw things here
	game_window.clear()

	main_batch.draw()

if __name__ == '__main__': 
	pyglet.clock.schedule_interval(update, 1/120.0)
	pyglet.app.run()