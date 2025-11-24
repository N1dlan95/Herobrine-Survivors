import math
import random
import pgzero 
import pgzrun
from pgzero.builtins import Actor, keyboard, clock, sounds
from zombie import Zombies #import my zombie class
from player import Player #import my player class
from bow_arrow import  Bow, arrow #import my bow class

WIDTH = 900
HEIGHT = 600
TITLE = "Minecraft Survivor Test"


    

#--------------------Menu functions------------------------

btn_play = Actor("btn_play", center=(WIDTH//2, HEIGHT//2 + 50))
btn_sounds = Actor("btn_sounds_on", topleft=(WIDTH - 120,10))
btn_sounds.images = ["btn_sounds_on", "btn_sounds_off"]
btn_exit = Actor("btn_exit", center=(WIDTH//2, HEIGHT//2 + 150))
menu_sign = Actor("menu_sign", center=(WIDTH//2, HEIGHT//2 - 120))
sounds_are_on = True
game_state = "menu"
music_has_started = False
current_track = None  # name of the music that is currently playing

def music_play(game_state):
    global music_has_started, current_track

    if not sounds_are_on:
        music.stop()
        current_track = None
        music_has_started = False
        return

    wanted_track = "menu_music" if game_state == "menu" else "game_music"

    # If the correct music is already playing, do nothing
    if current_track == wanted_track and music.is_playing(wanted_track):
        return

    # Otherwise switch tracks
    music.stop()
    music.play(wanted_track)
    current_track = wanted_track



def draw_menu():
    screen.clear()
    screen.fill((0, 0, 0))
    bg = Actor("bg_menu", center=(WIDTH//2, HEIGHT//2))
    bg.draw()
    menu_sign.draw()
    btn_play.draw()
    btn_sounds.draw()
    btn_exit.draw()

def update_menu():
    global game_state

def on_mouse_down(pos):
    global game_state

    if game_state == "menu":
        if btn_play.collidepoint(pos):
            reset_game()
            game_state = "playing"
            if sounds_are_on:
                sounds.button_sound.play()
        elif btn_sounds.collidepoint(pos):
            toggle_sounds()
            if sounds_are_on:
                sounds.button_sound.play()
        elif btn_exit.collidepoint(pos):
            if sounds_are_on:
                sounds.button_sound.play()
            exit()   # closes the game

    if game_state == "gameover":
        if btn_play.collidepoint(pos):
            reset_game()
            sounds.button_sound.play()
            game_state = "playing"
        elif btn_exit.collidepoint(pos):
            sounds.button_sound.play()
            exit()   # closes the game

def reset_game():
    global player, horda, arrows, arrow_cooldown, horda_cooldown 
    global texto_xp, texto_vida, chicken_spawn_timer, chickens, texto_tempo, time
    #player
    player = Player(WIDTH//2, HEIGHT//2)
    arrows = []
    arrow_cooldown = 3.0
    texto_xp = "Player level: {} \nXP: {}/{}".format(player.level, player.xp, (2*player.level + 7))
    texto_vida = "Player Health: {}/{}".format(player.health, player.max_health)

    #zombies
    zombieb = Zombies(0,0,player)
    horda_cooldown = 15.0
    horda = zombieb.create_zombie_tsunami(player)

    time = 0
    texto_tempo = "Time: {:.1f} s".format(time)
    chickens = []
    chicken_spawn_timer = 20.0
    

def toggle_sounds():
    global sounds_are_on
    sounds_are_on = not sounds_are_on  # flip True/False
    if sounds_are_on:
        music.play("menu_music")
    else:
        music.stop()
    btn_sounds.image = "btn_sounds_on" if sounds_are_on else "btn_sounds_off"
#--------------------Game functions------------------------
def draw_game():
    screen.clear()
    #background has to be drawn first
    for grass in forest:
        grass.draw()
    for zombie in horda:
        zombie.draw()
    player.draw()
    for arr in arrows:
        arr.draw()

    for chicken in chickens:
        chicken.draw()
    screen.draw.text(texto_xp, (10, 10), color="white")
    screen.draw.text(texto_vida, (10, 50), color="white")
    screen.draw.text(texto_tempo, (WIDTH//2, 10), color="white")

def update_game(dt):
    global player, horda, arrows, arrow_cooldown, horda_cooldown
    global texto_xp, texto_vida, chicken_spawn_timer, chickens, texto_tempo, time, game_state
    texto_xp = "Player level: {} \nXP: {}/{}".format(player.level, player.xp, (2*player.level + 7))
    texto_vida = "Player Health: {}/{}".format(player.health, player.max_health)

    time += dt
    texto_tempo = "Time: {:.1f} s".format(time)
    if horda_cooldown <= 0:
        new_horda = zombieb.create_zombie_tsunami(player)
        horda.extend(new_horda)
        horda_cooldown = 15.0
    horda_cooldown -= dt
    separate_enemies(horda, player)


    chicken_spawn_timer -= dt
    if chicken_spawn_timer <= 0 and random.randint(0,10)% 2 == 0:
        chicken = Actor("chicken", topleft=(random.randint(0, WIDTH-50),random.randint(0, HEIGHT-50)))
        chicken.radius = 20
        chicken.heal = 5
        chickens.append(chicken)
        chicken_spawn_timer = 20.0

    for chicken in chickens[:]:
        dx = chicken.x - player.actor.x
        dy = chicken.y - player.actor.y
        dist = math.hypot(dx, dy)

        if dist < chicken.radius + player.radius:
            chickens.remove(chicken)
            player.heal(chicken.heal)
            if sounds_are_on:
                sounds.healing.play()
            print("Player has been healed.") #test


    for zombie in horda:
        zombie.walking_zombie(dt, player)
        if zombie.life <= 0:
            horda.remove(zombie)
        dx = zombie.actor.x - player.actor.x
        dy = zombie.actor.y - player.actor.y
        dist = math.hypot(dx, dy)

        if dist < zombie.radius + player.radius and player.invulnerable <= 0:
            if sounds_are_on:
                    sounds.player_damage.play()
            if player.receive_damage(zombie.damage)=="dead":
                
                print("Player has died! Game Over.") #test
                game_state = "gameover"
            player.actor.image = "steve_damage"
            player.invulnerable = 1.0  # 1.0 seconds of invulnerability
        player.invulnerable -= dt

    # Moviment
    player.update_player(dt, keyboard)
    if arrow_cooldown <= 0:
        new_arrow = arrow(player.actor.x, player.actor.y)
        new_arrow.aim_at(horda)   # sets dx, dy, angle
        arrows.append(new_arrow)
        arrow_cooldown = 3.5 - player.level * 0.5
        if arrow_cooldown < 0.7:
            arrow_cooldown = 0.7

    arrow_cooldown -= dt

    for arr in arrows[:]:
        if arr.update(horda,sounds_are_on):
            arrows.remove(arr)


def draw_game_over():
    screen.clear()
    screen.fill((0, 0, 0))
    bg = Actor("bg_game_over", center=(WIDTH//2, HEIGHT//2))
    bg.draw()
    btn_exit.draw()
    btn_play.draw()

#--------------------Game setup------------------------
#in game background

forest = []
for j in range(5):
    for i in range(5):
        forest.append(
            Actor('grass_bg', topleft=(images.grass_bg.get_width() * i, images.grass_bg.get_height() * j))
        )
chickens = []
chicken_spawn_timer = 20.0


#player
player = Player(WIDTH//2, HEIGHT//2)
arrows = []
arrow_cooldown = 3.0
texto_xp = "Player level: {} \nXP: {}/{}".format(player.level, player.xp, (2*player.level + 7))
texto_vida = "Player Health: {}/{}".format(player.health, player.max_health)





# function to separate enemies, and not overlap. Generated with help from ChatGPT
def separate_enemies(enemies,player):
    for i in range(len(enemies)):
        for j in range(i + 1, len(enemies)):
            a = enemies[i]
            b = enemies[j]

            # separate enemy from player 
            pdx = player.actor.x - b.actor.x
            pdy = player.actor.y - b.actor.y
            pdist = math.hypot(pdx, pdy)
            min_pdist = b.radius + player.radius
            if pdist < min_pdist and pdist != 0:
                poverlap = min_pdist - pdist
                pnx = pdx / pdist
                pny = pdy / pdist

                # push the enemy away from the player
                b.actor.x -= pnx * poverlap
                b.actor.y -= pny * poverlap

            # separate enemies from each other
            dx = b.actor.x - a.actor.x
            dy = b.actor.y - a.actor.y
            dist = math.hypot(dx, dy) # Note: math.hypot computes sqrt(dx*dx + dy*dy)
            min_dist = a.radius + b.radius

            if dist < min_dist and dist != 0:# Note: create a normal vector
                overlap = min_dist - dist
                nx = dx / dist
                ny = dy / dist

                # push each enemy 50% of the overlap
                a.actor.x -= nx * overlap * 0.5
                a.actor.y -= ny * overlap * 0.5
                b.actor.x += nx * overlap * 0.5
                b.actor.y += ny * overlap * 0.5

#zombies
zombieb = Zombies(0,0,player)
horda_cooldown = 15.0
horda = zombieb.create_zombie_tsunami(player)

time = 0
texto_tempo = "Time: {:.1f} s".format(time)

#Update function ------------------------------------------------------
def update(dt):
    global game_state
    music_play(game_state)
    if game_state == "menu":
        update_menu()
    elif game_state == "playing":
        update_game(dt)
    elif game_state == "gameover":
        pass
    

#Draw function 
def draw():
    screen.clear()
    global game_state
    if game_state == "menu":
        draw_menu()
    elif game_state == "playing":
        draw_game()
    elif game_state == "gameover":
        draw_game_over()
        
    



pgzrun.go()