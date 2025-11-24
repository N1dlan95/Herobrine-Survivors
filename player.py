from pgzero.builtins import Actor, animate, keyboard,sounds
from bow_arrow import Bow

class Player:

    def __init__(self, x, y):
        self.actor = Actor("steve-1", (x, y))
        self.max_health = 20.0
        self.health = self.max_health
        self.invulnerable = 0   # time until he can be hit again
        self.speed = 1.2
        self.actor.images = ["steve-1", "steve-2", "steve-3", "steve-4"]
        self.iddle_image = ["steve_iddle1", "steve_iddle2", "steve_iddle3", "steve_iddle1"]
        self.actor.height = 64
        self.actor.width = 64
        self.frame_index = 0
        self.animation_timer = 0
        self.radius = 18  #radius for collision
        self.xp = 0
        self.level = 0
        self.weapons = []

    def gain_xp(self, amount):
        self.xp += amount
        if self.xp >= (2*self.level + 7):
            self.xp -= (2*self.level + 7)
            self.level_up()

    def level_up(self):
        self.level += 1
        if self.level % 2 == 0:
            self.max_health += 1
        if self.level % 3 == 0:
            self.heal(0.5)
        self.speed += 0.1
        print("Level up! New level: {}".format(self.level))#test

    def draw(self):
        self.actor.draw()
    
    def update_player(self,dt, keyboard):
        moving = False
        if keyboard.w:
            if self.actor.y  > 20:
                self.actor.y -= self.speed
                moving = True
        if keyboard.s:
            if self.actor.y <580:
                self.actor.y += self.speed
                moving = True
        if keyboard.a:
            if self.actor.x > 20:
                self.actor.x -= self.speed
                moving = True
        if keyboard.d:
            if self.actor.x < 880:
                self.actor.x += self.speed
                moving = True
        
        self.update_player_animation(dt, moving)


    def update_player_animation(self, dt, moving):
        self.animation_timer += dt

        if not moving:
            if self.animation_timer >= 0.25:  # a cada 0.25s
                self.animation_timer = 0
                self.frame_index = (self.frame_index + 1) % 4
                self.actor.image = self.iddle_image[self.frame_index]
        elif moving:        
            if self.animation_timer >= 0.25:  # a cada 0.25s
                self.animation_timer = 0
                self.frame_index = (self.frame_index + 1) % 4
                self.actor.image = self.actor.images[self.frame_index]


    def receive_bow(self,bow):#unseless
        bow.actor.pos = (self.actor.x + 30, self.actor.y - 30)
        
 
    def receive_weapon(self,weapon):#unseless
        self.weapons.append(weapon)
        if isinstance(weapon, Bow):
            self.receive_bow(weapon)
        

    def receive_damage(self, damage):
        self.health -= damage
        print("Player received {} damage! Current health: {}/{}".format(damage, self.health, self.max_health))#test
        if self.health < 0:
            self.health = 0
            return "dead"
        
    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
    