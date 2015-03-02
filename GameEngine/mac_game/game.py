import pyglet, math
from pyglet.window import key


main_batch = pyglet.graphics.Batch()
pyglet.resource.path = ['../images']
pyglet.resource.reindex()
player_image = pyglet.resource.image("player.png") #images go here
player_image_R = pyglet.resource.image("player_right.png")
player_image_L = pyglet.resource.image("player_left.png")
terrain_image = pyglet.resource.image("terrain.png")
background = pyglet.resource.image("background.png")
computer_image = pyglet.resource.image("Computer.png")
pencils_image = pyglet.resource.image("Pencils.png")
desktop_image = pyglet.resource.image("Desktop.png")

width, height = background.width, background.height
game_window = pyglet.window.Window(width, height)


def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width/2
    image.anchor_y = image.height/2

def distance(point_1=(0, 0), point_2=(0, 0)): 
    return math.sqrt( (point_1[0] - point_2[0]) ** 2 + (point_1[1] - point_2[1]) ** 2)

def collides_with(player_object, other_object): 
    collision_distance = player_object.image.width/2 + other_object.image.width/2 
    actual_distance = distance(player_object.position, other_object.position) 
    return (actual_distance <= collision_distance)

def collides_with_horizontal(player_object, other_object): 
    collision_distance = player_object.image.width/2 + other_object.image.width/2 
    actual_distance = abs(player_object.position[0] - other_object.position[0])
    return (actual_distance <= collision_distance)

def collides_with_vertical(player_object, other_object): 
    collision_distance = player_object.image.height/2 + other_object.image.height/2 
    actual_distance = abs(player_object.position[1] - other_object.position[1])
    return (actual_distance <= collision_distance)

center_image(player_image) #center all images on middle point
center_image(player_image_R)
center_image(player_image_L)
center_image(terrain_image)

level_label = pyglet.text.Label(text="This Is Not Mario", x=400, y=575, anchor_x='center', batch=main_batch) #level label

class PhysicalObject(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super(PhysicalObject, self).__init__(*args, **kwargs)

        self.velocity_x, self.velocity_y = 0.0, 0.0

    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

class Player(PhysicalObject):
    teletime = 0;

    def __init__(self, *args, **kwargs):
        super(Player, self).__init__(img=player_image, *args, **kwargs)
        self.speed = 300.0
        self.keys = dict(left=False, right=False, up=False, A=False, D=False)
        self.direction = "R"
        self.prior_x = self.x
        self.prior_y = self.y

    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP: 
            self.keys['up'] = True 
        elif symbol == key.LEFT:
            self.keys['left'] = True
            self.image = player_image_L
        elif symbol == key.RIGHT: 
            self.keys['right'] = True 
            self.image = player_image_R
        elif symbol == key.A:
            self.keys['A'] = True
            self.image = player_image_L
        elif symbol == key.D:
            self.keys['D'] = True
            self.image = player_image_R

    def on_key_release(self, symbol, modifiers):
        if symbol == key.UP: 
            self.keys['up'] = False 
        elif symbol == key.LEFT: 
            self.keys['left'] = False 
        elif symbol == key.RIGHT: 
            self.keys['right'] = False
        elif symbol == key.A:
            self.keys['A'] = False
        elif symbol == key.D:
            self.keys['D'] = False

    def within_bounds_x(self, other):
        if ((self.position[0] >= other.position[0] - other.width / 2) & (self.position[0] <= other.position[0] + other.width / 2)):
            return True
        if ((other.position[0] >= self.position[0] - self.width / 2) & (other.position[0] <= self.position[0] + self.width / 2)):
            return True
        else:
            return False

    def within_bounds_y(self, other):
        if ((self.position[1] >= other.position[1] - other.height / 2) & (self.position[1] <= other.position[1] + other.height / 2)):
            return True
        if ((other.position[1] >= self.position[1] - self.height / 2) & (other.position[1] <= self.position[1] + self.height / 2)):
            return True
        else:
            return False

    def grounded(self):
        if self.y <= 100:
            return True
        for i in range(1, len(game_objects)): 
            if (self.within_bounds_x(game_objects[i]) & collides_with_vertical(self, game_objects[i]) & (self.position[1] >= game_objects[i].position[1])):
                return True
        else:
            return False

    def update(self, dt):
        self.velocity_y -= 75.0 #gravity

        if self.keys['left']:
            self.velocity_x = -self.speed
            for i in range(1, len(game_objects)): 
                if self.within_bounds_y(game_objects[i]) & collides_with_horizontal(self, game_objects[i]) & (self.position[0] >= game_objects[i].position[0]):
                    self.velocity_x = 0
                    self.x = self.prior_x
                    self.y = self.prior_y
                else:
                    self.prior_x = self.x
                    self.prior_y = self.y
        elif self.keys['right']: 
            self.velocity_x = self.speed
            for i in range(1, len(game_objects)): 
                if self.within_bounds_y(game_objects[i]) & collides_with_horizontal(self, game_objects[i]) & (self.position[0] <= game_objects[i].position[0]):
                    self.velocity_x = 0
                    self.x = self.prior_x
                    self.y = self.prior_y
                else:
                    self.prior_x = self.x
                    self.prior_y = self.y
        else:
            self.velocity_x = 0

        if self.grounded():
            self.velocity_y = 0

        if self.keys['up']:
            if self.grounded():
                self.velocity_y += 850

        if self.teletime == 0:
            if self.keys['A']:
                self.velocity_x = 0
                self.x = self.x - 150
                self.teletime = 10

            if self.keys['D']:
                self.velocity_x = 0
                self.x = self.x + 150
                self.teletime = 10

        if self.teletime > 0:
            self.teletime = self.teletime - 1

        super(Player, self).update(dt)


player = Player(x=400, y=100, batch=main_batch)

box = PhysicalObject(img=terrain_image, x=0,y=100, batch=main_batch)
box2 = PhysicalObject(img=terrain_image, x=100,y=100, batch=main_batch)
box3 = PhysicalObject(img=terrain_image, x=200,y=100, batch=main_batch)
box4 = PhysicalObject(img=terrain_image, x=300,y=100, batch=main_batch)
#pencils = PhysicalObject(img=pencil_image, x=300, y=100, batch=main_batch)
#computer = PhysicalObject(img=computer_image, x=100, y=100, batch=main_batch)
#books = PhysicalObject(img=books
desktop = PhysicalObject(img=desktop_image, x=0, y=0, batch=main_batch)

game_objects = [player] + [box, box2, box3, box4] + [desktop]
#game_objects = [player] + [desktop]

game_window.push_handlers(player)

############### starting the game ##############
def update(dt):
    for obj in game_objects:
        obj.update(dt)

@game_window.event
def on_draw(): # draw things here
    game_window.clear()
    background.blit(0, 0, 0)

    main_batch.draw()

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/500.0)
    pyglet.app.run()

