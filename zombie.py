import pgzero
import random
from pgzero.builtins import Actor, animate, keyboard

class Zombies:

    zombie_frames = ["zombie-1", "zombie-2", "zombie-3", "zombie-4"]

    def __init__(self, x, y):
        self.actor = Actor(self.zombie_frames[0], (x, y))
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.3  # troca de frame a cada 0.3s
        self.speed = 0.6
    
    def update_animation(self, dt):
        # Atualizar animação
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.zombie_frames)
            self.actor.image = self.zombie_frames[self.frame_index]

    def walking_zombie(self, dt, player):
        # Movimento até o player
        if self.actor.x < player.x:
            self.actor.x += self.speed
        if self.actor.x > player.x:
            self.actor.x -= self.speed
        if self.actor.y < player.y:
            self.actor.y += self.speed
        if self.actor.y > player.y:
            self.actor.y -= self.speed
        self.update_animation(dt)


    def draw(self):
        self.actor.draw()


    def spawn_zombie(self):
        side = random.choice(['left', 'right', 'top', 'bottom'])
        if side == 'left':
            x = random.randint(0,50)
            y = random.randint(0,600)
        elif side == 'right':
            x = random.randint(750,800)
            y = random.randint(0,600)
        elif side == 'top':
            x = random.randint(0,800)
            y = random.randint(0,50)
        else:  # bottom
            x = random.randint(0,800)
            y = random.randint(550,600)  
        value = x,y
        return value
    
    def create_zombie_tsunami(self):
        zombieb = Zombies(0,0)
        tsunami = []
        for i in range(10):
            entity = Zombies(zombieb.spawn_zombie()[0], zombieb.spawn_zombie()[1])
            tsunami.append(entity)
        return tsunami
    