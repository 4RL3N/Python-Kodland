import pgzrun
import math
import random
from pygame import Rect
from pgzero.actor import Actor

TITLE = "Jogo Cyber Jumper"
WIDTH = 800
HEIGHT = 600

GRAVITY = 0.5
JUMP_STRENGTH = -14
PLAYER_SPEED = 5
ENEMY_SPEED = 2
ANIMATION_DELAY = 8

game_state = "MENU"
sound_enabled = True

level = 1
level_platforms = []
enemies = []
boss = None
boss_projectiles = []

STARTING_LIVES = 3

class AnimatedEntity:
    def __init__(self, x, y, idle_images, move_images):
        self.x = x
        self.y = y
        self.idle_images = idle_images
        self.move_images = move_images
        
        try:
            self.actor = Actor(idle_images[0], (x, y))
            self.has_images = True
        except:
            self.actor = Actor("p1_idle", (x, y)) 
            self.has_images = False
            
        self.frame_index = 0
        self.timer = 0
        self.facing_right = True
        self.is_moving = False

    def animate(self):
        self.timer += 1
        current_images = self.move_images if self.is_moving else self.idle_images
        
        if not current_images or not self.has_images: return

        if self.timer >= ANIMATION_DELAY:
            self.timer = 0
            self.frame_index = (self.frame_index + 1) % len(current_images)
            try:
                self.actor.image = current_images[self.frame_index]
                self.actor.flip_x = not self.facing_right
            except:
                pass 

    def draw(self):
        if self.has_images:
            self.actor.draw()

class Player(AnimatedEntity):
    def __init__(self, x, y):
        idle_imgs = ["p1_idle", "p1_idle2"]
        walk_imgs = ["p1_walk1", "p1_walk2", "p1_walk3"]
        super().__init__(x, y, idle_imgs, walk_imgs)
        self.velocity_y = 0
        self.is_jumping = False
        self.rect = Rect(x, y, 40, 60)
        self.lives = STARTING_LIVES
        self.invulnerable_timer = 0

    def update(self, platforms):
        self.handle_movement()
        self.apply_gravity()
        self.handle_collisions(platforms)
        self.animate()
        
        self.actor.pos = (self.rect.centerx, self.rect.centery)
        
        if self.invulnerable_timer > 0:
            self.invulnerable_timer -= 1

    def handle_movement(self):
        self.is_moving = False
        if keyboard.left:
            self.rect.x -= PLAYER_SPEED
            self.facing_right = False
            self.is_moving = True
        elif keyboard.right:
            self.rect.x += PLAYER_SPEED
            self.facing_right = True
            self.is_moving = True

        if keyboard.up and not self.is_jumping:
            self.velocity_y = JUMP_STRENGTH
            self.is_jumping = True
            if sound_enabled:
                try: sounds.jump.play()
                except: pass

    def apply_gravity(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

    def handle_collisions(self, platforms):
        for plat in platforms:
            if self.rect.colliderect(plat) and self.velocity_y > 0:
                if self.rect.bottom - self.velocity_y < plat.bottom:
                    self.rect.bottom = plat.top
                    self.velocity_y = 0
                    self.is_jumping = False

        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > WIDTH: self.rect.right = WIDTH
        if self.rect.top > HEIGHT: self.die()

    def die(self):
        global game_state
        game_state = "GAMEOVER"
        if sound_enabled:
            try: sounds.lose.play()
            except: pass

    def take_damage(self):
        if self.invulnerable_timer > 0: return
        self.lives -= 1
        self.invulnerable_timer = 90
        self.velocity_y = -6
        if sound_enabled:
            try: sounds.hit.play()
            except: pass
        if self.lives <= 0: self.die()
            
    def draw(self):
        if self.invulnerable_timer > 0 and (self.invulnerable_timer % 10 < 5):
            return
        if self.has_images:
            super().draw()
        else:
            screen.draw.filled_rect(self.rect, "green")

class Enemy(AnimatedEntity):
    def __init__(self, x, y, patrol_distance):
        idle_imgs = ["enemy_idle1", "enemy_idle2"]
        walk_imgs = ["enemy_walk1", "enemy_walk2"]
        super().__init__(x, y, idle_imgs, walk_imgs)
        self.start_x = x
        self.max_dist = patrol_distance
        self.direction = 1
        self.rect = Rect(x, y, 40, 40)
        self.is_moving = True

    def update(self):
        move_amount = ENEMY_SPEED * self.direction
        self.rect.x += move_amount
        dist_traveled = abs(self.rect.x - self.start_x)
        if dist_traveled > self.max_dist: self.direction *= -1
        self.facing_right = (self.direction > 0)
        self.actor.pos = (self.rect.centerx, self.rect.centery)
        self.animate()
    
    def draw(self):
        if self.has_images:
            super().draw()
        else:
            screen.draw.filled_rect(self.rect, "red")

class Boss(AnimatedEntity):
    def __init__(self, x, y):
        idle_imgs = ["boss_idle1", "boss_idle2", "boss_idle3"] 
        walk_imgs = ["boss_walk1", "boss_walk2"]
        super().__init__(x, y, idle_imgs, walk_imgs)
        
        self.rect = Rect(x, y, 80, 80)
        self.health = 5
        self.attack_cooldown = 0
        self.is_flashing = 0

    def update(self, player_rect):
        if self.attack_cooldown <= 0:
            if random.random() < 0.03: 
                self.shoot_at(player_rect)
                self.attack_cooldown = 60
        else:
            self.attack_cooldown -= 1
        
        if self.is_flashing > 0: self.is_flashing -= 1
        self.actor.pos = (self.rect.centerx, self.rect.centery)
        self.animate()

    def shoot_at(self, target_rect):
        sx, sy = self.rect.centerx, self.rect.centery
        dx, dy = target_rect.centerx - sx, target_rect.centery - sy
        dist = math.hypot(dx, dy) or 1.0
        speed = 6.0
        boss_projectiles.append({
            "rect": Rect(sx, sy, 15, 15), "x": sx, "y": sy,
            "vx": (dx/dist)*speed, "vy": (dy/dist)*speed
        })

    def take_damage(self):
        if self.is_flashing > 0: return
        self.health -= 1
        self.is_flashing = 10
        if sound_enabled:
            try: sounds.hit.play()
            except: pass

    def draw(self):
        if self.is_flashing > 0:
            screen.draw.filled_rect(self.rect, "red")
        # Se tem imagens, desenha o boss normal
        elif self.has_images:
            self.actor.draw()
        # Se NÃO tem imagens, desenha AZUL (Garante que você veja o boss correto)
        else:
            screen.draw.filled_rect(self.rect, "blue")

class Button:
    def __init__(self, text, x, y, width, height, callback):
        self.rect = Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.is_hovered = False

    def draw(self):
        color = (80, 80, 250) if self.is_hovered else (50, 50, 200)
        screen.draw.filled_rect(self.rect, color)
        screen.draw.text(self.text, center=self.rect.center, fontsize=30, color="white")

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)

    def check_click(self, pos):
        if self.rect.collidepoint(pos): self.callback()

def start_game():
    global game_state, player, enemies, level_platforms, boss, level, boss_projectiles
    game_state = "GAME"
    level = 1
    boss = None
    boss_projectiles = []
    player = Player(100, 400)
    
    # Level 1
    level_platforms = [Rect(0, 500, 800, 100), Rect(200, 400, 150, 20),
                       Rect(450, 300, 150, 20), Rect(100, 200, 100, 20)]
    enemies = [Enemy(250, 360, 50), Enemy(500, 260, 60), Enemy(400, 460, 100)]

def setup_level_two():
    global level, level_platforms, enemies, boss, boss_projectiles
    level = 2
    boss_projectiles = []
    level_platforms = [Rect(0, 520, 800, 80), Rect(120, 420, 120, 20),
                       Rect(320, 340, 120, 20), Rect(540, 260, 120, 20),
                       Rect(680, 180, 100, 20)]
    enemies = [Enemy(140, 380, 80), Enemy(370, 300, 100)]
    boss = Boss(WIDTH - 100, 150)

def toggle_sound():
    global sound_enabled
    sound_enabled = not sound_enabled
    buttons[1].text = "Som: Ligado" if sound_enabled else "Som: Desligado"

def exit_game():
    exit()

buttons = [
    Button("Começar o jogo", 300, 200, 200, 50, start_game),
    Button("Som: Ligado", 300, 280, 200, 50, toggle_sound),
    Button("Sair do jogo", 300, 360, 200, 50, exit_game) 
]

player = None

def update():
    global game_state, enemies, boss, level

    if game_state == "GAME":
        player.update(level_platforms)
        if level == 1 and len(enemies) == 0: setup_level_two()

        for enemy in enemies[:]:
            enemy.update()
            if player.rect.colliderect(enemy.rect):
                if player.velocity_y > 0 and player.rect.bottom < enemy.rect.bottom:
                    enemies.remove(enemy)
                    player.velocity_y = -8
                    if sound_enabled:
                        try: sounds.kill.play()
                        except: pass
                else:
                    player.take_damage()
  
        if boss:
            boss.update(player.rect)
            for proj in boss_projectiles[:]:
                proj["x"] += proj["vx"]
                proj["y"] += proj["vy"]
                proj["rect"].topleft = (int(proj["x"]), int(proj["y"]))
                
                if not Rect(0,0,WIDTH,HEIGHT).colliderect(proj["rect"]):
                    boss_projectiles.remove(proj)
                elif proj["rect"].colliderect(player.rect):
                    boss_projectiles.remove(proj)
                    player.take_damage()

            if player.rect.colliderect(boss.rect):
                if player.velocity_y > 0 and player.rect.bottom < boss.rect.bottom - 10:
                    boss.take_damage()
                    player.velocity_y = -12
                    
                    if boss.health <= 0:
                        game_state = "VICTORY"
                        if sound_enabled:
                            try: sounds.win.play()
                            except: pass
                else:
                    player.take_damage()

def draw():
    screen.clear()
    if game_state == "MENU":
        screen.fill((20, 20, 40))
        screen.draw.text("CYBER JUMPER", center=(WIDTH/2, 100), fontsize=60, color="cyan")
        screen.draw.text("Derrote os capangas e o chefe final pulando eles!", center=(WIDTH/2, 150), fontsize=20, color="white")
        for btn in buttons: btn.draw()

    elif game_state == "GAME":
        screen.fill((10, 10, 30))
        for plat in level_platforms: screen.draw.filled_rect(plat, (100, 200, 100))
        player.draw()
        for enemy in enemies: enemy.draw()
        
        if boss:
            boss.draw()
            for proj in boss_projectiles: screen.draw.filled_rect(proj["rect"], "red")
            screen.draw.text(f"BOSS HP: {boss.health}", (WIDTH-160, 10), fontsize=24, color="red")
            
        screen.draw.text(f"Lives: {player.lives}", (10, 10), fontsize=28, color="white")
        screen.draw.text(f"Level: {level}", (10, 40), fontsize=20, color="white")

    elif game_state in ["GAMEOVER", "VICTORY"]:
        screen.fill((50, 10, 10) if game_state == "GAMEOVER" else (10, 50, 10))
        txt = "Você perdeu :(" if game_state == "GAMEOVER" else "VICTORY!"
        color = "red" if game_state == "GAMEOVER" else "gold"
        screen.draw.text(txt, center=(WIDTH/2, HEIGHT/2), fontsize=80, color=color)
        screen.draw.text("Aperte o botão de ESPAÇO no teclado para ir para o menu", center=(WIDTH/2, HEIGHT/2+60), fontsize=30, color="white")

def on_mouse_move(pos):
    if game_state == "MENU":
        for btn in buttons: btn.check_hover(pos)

def on_mouse_down(pos):
    if game_state == "MENU":
        for btn in buttons: btn.check_click(pos)

def on_key_down(key):
    global game_state
    if game_state in ("GAMEOVER", "VICTORY") and key == keys.SPACE:
        game_state = "MENU"

pgzrun.go()