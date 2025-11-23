import pgzero
from pgzero.builtins import Actor, animate, keyboard, clock
from pygame import rect
import math
class Bow:


    def __init__(self, x, y):
        self.actor = Actor("bow", (x, y))
        self.actor.angle = 0

    def draw(self):
        self.actor.draw()
    
    def update(self, enemies):
        self.aim_at(enemies)
#----------------------------------------------------------------------------------------------------------------------------
class arrow:
    def __init__(self, x, y):
        self.actor = Actor("arrow", (x, y))
        self.speed = 6
        self.damage = 7
        self.radius = 10

        # These will be filled when the arrow is fired
        self.dx = 0
        self.dy = 0

    def draw(self):
        self.actor.draw()

    def update(self, enemies):
        # Move arrow
        self.actor.x += self.dx * self.speed
        self.actor.y += self.dy * self.speed

        # Check collision
        for enemy in enemies:
            if self.actor.colliderect(enemy.actor):
                enemy.receive_damage(self.damage)
                return True  # tell main game to remove this arrow
        
        return False

    def aim_at(self, enemies):
        if not enemies:
            return None

        closest = min(enemies, key=lambda e:
            math.hypot(e.actor.x - self.actor.x, e.actor.y - self.actor.y))

        tx, ty = closest.actor.x, closest.actor.y
        dx = tx - self.actor.x
        dy = ty - self.actor.y

        dist = math.hypot(dx, dy)

        if dist == 0:
            return None

        #Note: Normalize (convert to unit vector)
        self.dx = dx / dist
        self.dy = dy / dist

        # Set rotation, the arrow image points to the top-right by default
        angle = math.degrees(math.atan2(-dy, dx))
        self.actor.angle = angle - 45

        return closest
