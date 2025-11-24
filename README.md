# Introduction 
Herobrine Survivors is a personal project inspired by Vampire Survivors and Minecraft. It is made in the roguelike genre, trying to look like Vampire Survivors’ gameplay with Minecraft elements (weapons, characters, enemies, etc.). It is programmed in Python with the Pygame Zero library, using VS Code as the text editor.

If I have to say a version, I think it is 0.2.1, but I don’t know if I want to continue in this language, these paradigms, etc. The main objective was to participate in an assignment for Koodland that needed a game made in Pygame Zero.
## How to test it?
As I said before, I used VS Code as the text editor, so the tutorial below will use it too, obviously :).
### 1- I nstall Pygame Zero.
Open the terminal in your project folder and type:
``` python
pip install pgzero
```
``Note: your Python version has to be 3.12.``
### 2- Run the Project.
Normally, you would have to type ``pgzrun 'fileName'.py`` in the terminal, but the command **pgzrun.go()** in the last line of the main file makes VS Code run the project when pressing **F5**.

### 3- Enjoy :)
Enjoy  :)

## Next additions (if there are any, lol):
### Characters
**Steve:**
- Passive: every ?8? XP levels, gains a damage enchantment on weapons.
- Max: 3
- Sharpness I – 2 damage
- Gunpowder (TNT) – 2 damage
- Rust(Anvil) – applies poison
- Poison: 1 damage per second
  
  *Status*
- 20 health
- Regeneration: 0.034 → 1 health every 30 seconds
- Stone Sword

**Alex:**
Passive: every 4 levels, gains –0.2 cooldown on all weapons.
16 health
Regeneration: 0.067 → 1 health every 15 seconds
Bow and Arrow

### Weapons – Max 2
**Active:**
Stone Sword – player direction – crescent slash
Damage: 5
Use speed: 2 sec

Bow and Arrow – nearest enemy – single target
Damage: 7
Use speed: 3 sec

TNT – random direction – area damage
Damage: 15
Use speed: 10 sec

Anvil – random – area damage
Damage: 12
Use speed: 8 sec

Shield – blocks one attack every 10 sec

Trident – random – pierces enemies
Damage: 7
Cooldown: 9 sec

**Passive Items:**
Enchanted Apple – increases max health by 2
Golden Apple – increases regeneration by 20%
Enchanted Book – projectile speed, greater range
Luck

### Map and Enemies:
Overworld

**Zombie (levels 6 to …)**
Damage: 3
Health: 13
XP: 3–4

**Small Slime (levels 1–10)**
Damage: 1 (if two stack)
Health: 2
XP: 1–2

**Medium Slime (levels 5–15)**
Damage: 2
Health: 8
Splits into 1–4 small slimes
XP: 2–3

**Big Slime (levels 9 to …)**
Damage: 4
Health: 19
Splits into 1–4 medium slimes
XP: 5–9

### Items:
**Chests:**
- Wooden – one upgrade – 85% chance
- Copper – three upgrades – 10% chance
- Ender – five upgrades – 4.85% chance
- Shulker Box – one extra weapon – 0.15% chance

Steak – restores health

### Experience and Leveling:
When leveling up, two options will appear for choosing weapons or upgrades to the ones you already have.

**Leveling function: (Like Minecraft)** 
- 2 × current_level + 7 (levels 0–15)
- 5 × current_level – 38 (levels 16–30)??
- 9 × current_level – 158 (levels 31+)??

### Sounds:
**Hit**
- Player damage
- Monster damage
- Weapons
**Music**
- C418
