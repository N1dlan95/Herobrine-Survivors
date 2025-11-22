from pgzero.builtins import Actor, animate, keyboard

class Player:

    def __init__(self, x, y):
        self.actor = Actor("steve-1", (x, y))
        self.health = 100
        self.speed = 1.2
        self.actor.images = ["steve-1", "steve-2", "steve-3", "steve-4"]
        self.actor.x = 32
        self.actor.y = 32
        self.actor.height = 64
        self.width = 64
        self.speed = 1.2
        self.frame_index = 0
        self.animation_timer = 0
        self.radius = 18  # raio para colisão

    def draw(self):
        self.actor.draw()
    
    def update_player(self,dt, keyboard):
        moving = False
        if keyboard.w:
            self.actor.y -= self.speed
            moving = True
        if keyboard.s:
            self.actor.y += self.speed
            moving = True
        if keyboard.a:
            self.actor.x -= self.speed
            moving = True
        if keyboard.d:
            self.actor.x += self.speed
            moving = True
        
        if moving:
            self.update_player_animation(dt)


    def update_player_animation(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= 0.25:  # a cada 0.25s
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % 4
            self.actor.image = self.actor.images[self.frame_index]