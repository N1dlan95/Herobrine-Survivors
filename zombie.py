import random
from pgzero.builtins import Actor, animate, keyboard

class Zombies:

    def __init__(self, x, y,player):
        self.actor = Actor("zombie-1", (x, y))
        self.actor.images = ["zombie-1", "zombie-2", "zombie-3", "zombie-4"]
        self.frame_index = 0
        self.player = player #Improvisado
        self.animation_timer = 0
        self.animation_speed = 0.3  # troca de frame a cada 0.3s
        self.life = 13
        self.speed = 0.6
        self.radius = 18
        self.xp_value = random.randint(3,5)
        
          # raio para colisão
    
    def update_animation(self, dt):
        # Atualizar animação
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.actor.images)
            self.actor.image = self.actor.images[self.frame_index]

    def walking_zombie(self, dt, player):
        # Movimento até o player
        if self.actor.x < player.actor.x:
            self.actor.x += self.speed
        if self.actor.x > player.actor.x:
            self.actor.x -= self.speed
        if self.actor.y < player.actor.y:
            self.actor.y += self.speed
        if self.actor.y > player.actor.y:
            self.actor.y -= self.speed
        self.update_animation(dt)


    def draw(self):
        self.actor.draw()


    def spawn_zombie(self):
        side = random.choice(['left', 'right', 'top', 'bottom'])
        if side == 'left':
            x = random.randint(0,20)
            y = random.randint(0,700)
        elif side == 'right':
            x = random.randint(880,900)
            y = random.randint(0,700)
        elif side == 'top':
            x = random.randint(0,900)
            y = random.randint(0,20)
        else:  # bottom
            x = random.randint(0,900)
            y = random.randint(680,700)  
        value = x,y
        return value
    
    def create_zombie_tsunami(self,player):#improvisado-------------
        zombieb = Zombies(0,0,player)#improvisado---------------------
        tsunami = []
        for i in range(2*player.level + 2):#improvisado-----
            entity = Zombies(zombieb.spawn_zombie()[0], zombieb.spawn_zombie()[1],player)#imrovisado-----
            tsunami.append(entity)
        return tsunami
    
    def receive_damage(self, damage):
        self.life -= damage
        self.actor.image = "zombie_damage"
        if self.life < 0:
            self.life = 0
            self.drop_Xp()


    def drop_Xp(self):
        self.player.gain_xp(self.xp_value)
        print("Gained {} XP! Total XP: {}".format(self.xp_value, self.player.xp))
        
    def colliderect(self, other):
        return self.actor.colliderect(other.actor)