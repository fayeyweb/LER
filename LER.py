import pygame
import sys
import cv2
import random
import math


# ---------------- INITIALIZATION (Pagsisimula) ----------------
pygame.init() 
pygame.mixer.init() 

# ---------------- SCREEN SETUP (Configuration ng Window) ----------------
width = 1152
height = 648
screen = pygame.display.set_mode((width, height)) 
pygame.display.set_caption("LOST EXIT REALM") 

clock = pygame.time.Clock()

# ---------------- COLORS (Standard RGB values) ----------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MOSSY_BRICK = (38, 55, 53)
MOSSY_GLOW = (74, 103, 91)
NETHER_BRICK = (60, 20, 20) 
CYAN = (0, 255, 255)
GOLD = (255, 215, 0)
RED = (200, 0, 0)

# ================ MUSIC PLAYLIST IN GAME=================
music_playlist = [
    "data/MAIN_MUSICGAME.mp3", # original na BGM
    "data/Pixelland.mp3", 
    "data/Up In My Jam.mp3", 
]

# Title ng song para sa UI
music_titles = [
    "8bit Dungeon Level",
    "Pixelland",
    "Up In My Jam",
]

# =================SOUND EFFECTS =================
click_sfx = pygame.mixer.Sound("data/CLICK.wav") 
enemy1_hit_sfx = pygame.mixer.Sound("data/ENEMY1HIT.wav")
enemy2_hit_sfx = pygame.mixer.Sound("data/ENEMY2HIT.wav")
hero_shoot_sfx = pygame.mixer.Sound("data/HEROSHOOT.wav")
hero_spawn_sfx = pygame.mixer.Sound("data/SPAWNHERO.wav")
hero_hit_enemy_sfx = pygame.mixer.Sound("data/HEROHIT.wav")
player_hurt_sfx = pygame.mixer.Sound("data/PLAYERHURT.wav")
jumphero_sfx = pygame.mixer.Sound("data/JUMPHERO.wav")
enemydead_sfx = pygame.mixer.Sound("data/ENEMYDEAD.wav")
collect_sfx = pygame.mixer.Sound("data/COLLECT.wav")
dash_warrior_sfx = pygame.mixer.Sound("data/DASH.wav")
warrior_aim_sfx = pygame.mixer.Sound("data/AIM_WARRIOR.wav") 
tutorial_next_sfx = pygame.mixer.Sound("data/STEPS_EFFECTS.mp3")
hero_death_blink_sfx = pygame.mixer.Sound("data/DEATH_BLINK.mp3")
exit_sound_sfx = pygame.mixer.Sound("data/EXIT_SOUND.mp3")
victory_sound_sfx = pygame.mixer.Sound("data/VICTORY_SOUND.mp3")
defeat_sound_sfx = pygame.mixer.Sound("data/DEFEAT_SOUND.mp3")
hover_buttons_sfx = pygame.mixer.Sound("data/HOVER_BUTTONS.mp3")
super_saiyan_sfx = pygame.mixer.Sound("data/SUPER_SAIYAN.mp3")
ssj_channel = pygame.mixer.Channel(5)
ssj_channel.set_volume(1.0)

# =================ZOOM & CAMERA SETTINGS =================
zoom_level = 1.5
camera_follow_enabled = True
internal_res = (int(width / zoom_level), int(height / zoom_level))
display_surface = pygame.Surface(internal_res) 

camera_x = 0
camera_y = 0
camera_smoothing = 0.1

show_platforms = False

# =================VIDEO BACKGROUND MAIN MENU CONFIG =================
video_path = "data/moving bg.mp4"
cap = cv2.VideoCapture(video_path)

def get_video_frame():
    success, frame = cap.read()
    if not success:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        success, frame = cap.read()
    
    if success:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.transpose(frame)
        frame = pygame.surfarray.make_surface(frame)
        frame = pygame.transform.scale(frame, (width, height))
        return frame
    return None


# ---------------- MAIN BUTTONS LOADING ----------------
start_img = pygame.image.load("data/START_BTN.png")
exit_img = pygame.image.load("data/EXIT_BTN.png")
start_img = pygame.transform.scale(start_img, (280, 90))
exit_img = pygame.transform.scale(exit_img, (280, 90))
music_on_img = pygame.image.load("data/MUSIC_ON.png")
music_off_img = pygame.image.load("data/MUSIC_OFF.png")
info_img = pygame.image.load("data/INFO_BTN.png")

music_on_img = pygame.transform.scale(music_on_img, (110, 55))
music_off_img = pygame.transform.scale(music_off_img, (110, 55))
info_img = pygame.transform.scale(info_img, (58, 58))

music_btn_rect = music_on_img.get_rect(topright=(width - 20, 20))
info_rect = info_img.get_rect(topright=(width - 25, 85))
current_music_idx = 0
music_box_rect = pygame.Rect(width - 240, 85, 220, 55) 
prev_music_rect = pygame.Rect(width - 235, 100, 30, 30)
next_music_rect = pygame.Rect(width - 55, 100, 30, 30)
# =================================================================

start_rect = start_img.get_rect(center=(width//2, height - 180))
exit_rect = exit_img.get_rect(center=(width//2, height - 85))
second_bg = pygame.image.load("data/SECONDBG.jpg")
second_bg = pygame.transform.scale(second_bg, (width, height))

back_img = pygame.image.load("data/BACK_BTN.png")
back_img = pygame.transform.scale(back_img, (75, 50))
back_rect = back_img.get_rect(topleft=(20, 20))

level1_img = pygame.image.load("data/LEVEL1_BTN.png")
level2_img = pygame.image.load("data/LEVEL2_BTN.png")
level3_img = pygame.image.load("data/LEVEL3_BTN.png")

level1_select = pygame.image.load("data/LEVEL1_SELECT.png")
level2_select = pygame.image.load("data/LEVEL2_SELECT.png")
level3_select = pygame.image.load("data/LEVEL3_SELECT.png")

start_level_img = pygame.image.load("data/START_LEVEL.png") 

level1_img = pygame.transform.scale(level1_img, (240, 330))
level2_img = pygame.transform.scale(level2_img, (240, 320))
level3_img = pygame.transform.scale(level3_img, (240, 320))

level1_select = pygame.transform.scale(level1_select, (240, 320))
level2_select = pygame.transform.scale(level2_select, (240, 320))
level3_select = pygame.transform.scale(level3_select, (240, 320))

start_level_img = pygame.transform.scale(start_level_img, (220, 70))

level1_rect = level1_img.get_rect(center=(width//2 - 300, height//2 + 50))
level2_rect = level2_img.get_rect(center=(width//2, height//2 + 50))
level3_rect = level3_img.get_rect(center=(width//2 + 300, height//2 + 50))
start_level_rect = start_level_img.get_rect(center=(width//2, height - 52))
character_bg = pygame.image.load("data/CHARACTERBG.png") 
character_bg = pygame.transform.scale(character_bg, (width, height))
show_character_screen = False 
left_arrow_img = pygame.image.load("data/LEFT_ARROW.png")
right_arrow_img = pygame.image.load("data/RIGHT_ARROW.png")
confirm_char_img = pygame.image.load("data/CONFIRM_CHARACTER.png")
left_arrow_img = pygame.transform.scale(left_arrow_img, (140, 120))
right_arrow_img = pygame.transform.scale(right_arrow_img, (140, 120))
confirm_char_img = pygame.transform.scale(confirm_char_img, (220, 60))
warrior_name_img = pygame.image.load("data/SELECTING_WARRIOR.png")
hero_name_img = pygame.image.load("data/SELECTING_HERO.png")
warrior_name_img = pygame.transform.scale(warrior_name_img, (300, 300))
hero_name_img = pygame.transform.scale(hero_name_img, (250, 300))
warrior_name_rect = warrior_name_img.get_rect(center=(width//2 + 10, height//2 + 40))
hero_name_rect = hero_name_img.get_rect(center=(width//2 + 15, height//2 + 30))
# =====================================================================

left_arrow_rect = left_arrow_img.get_rect(center=(width//2 - 265, height//2 + 30))
right_arrow_rect = right_arrow_img.get_rect(center=(width//2 + 265, height//2 + 30))
confirm_char_rect = confirm_char_img.get_rect(center=(width//2, height - 45))
skip_img = pygame.image.load("data/SKIP_BTN.jpg")
skip_img = pygame.transform.scale(skip_img, (100, 45)) 
skip_rect = skip_img.get_rect(bottomright=(width - 40, height - 60)) 

show_second_menu = False
show_story_screen = False
selected_level = 0 
game_world_size = (2500, 1200) 
game_bg1 = pygame.transform.scale(pygame.image.load("data/BGGAME_LEVEL1.jpg"), (width, height))
game_bg2 = pygame.transform.scale(pygame.image.load("data/BGGAME_LEVEL2.jpg"), (width, height))
game_bg3 = pygame.transform.scale(pygame.image.load("data/BGGAME_LEVEL3.jpg"), (width, height))

show_actual_game = False 

hero_orig = pygame.image.load("data/HERO.png")
hero_right = pygame.transform.scale(hero_orig, (45, 65)).convert_alpha()
hero_left = pygame.transform.flip(hero_right, True, False)

hero_aiming = pygame.image.load("data/HERO AIMING.png")
hero_aiming_right = pygame.transform.scale(hero_aiming, (45, 65)).convert_alpha()
hero_aiming_left = pygame.transform.flip(hero_aiming_right, True, False)

Orbs = pygame.image.load("data/ORBS.png")

warrior_orig = pygame.image.load("data/WARRIOR.png")
warrior_right = pygame.transform.scale(warrior_orig, (75, 80)).convert_alpha()
warrior_left = pygame.transform.flip(warrior_right, True, False)

warrior_aiming = pygame.image.load("data/WARRIOR AIMING.png")
warrior_aiming_right = pygame.transform.scale(warrior_aiming, (75, 80)).convert_alpha()
warrior_aiming_left = pygame.transform.flip(warrior_aiming_right, True, False)

# ================= CHARACTER SELECTION VARIABLES =================
# 0 = Warrior, 1 = Hero
selected_char_index = 0 
active_hero_right = warrior_right
active_hero_left = warrior_left
active_aiming_right = warrior_aiming_right
active_aiming_left = warrior_aiming_left
# ==========================================================================

# ================= ORB SYSTEM CLASS & VARIABLES =================
orb_game_img = pygame.transform.scale(Orbs, (25, 25))
orb_ui_img = pygame.transform.scale(Orbs, (35, 35))
collected_orbs = 0
orb_font = pygame.font.SysFont("Arial", 28, bold=True)

# ================= KEYS SYSTEM CLASS & VARIABLES =================
key_orig = pygame.image.load("data/KEYS.png").convert_alpha()
key_game_img = pygame.transform.scale(key_orig, (25, 35)) 
key_ui_img = pygame.transform.scale(key_orig, (25, 35))
collected_keys = 0

victory = pygame.image.load("data/VICTORY.png").convert_alpha()
tuts_complete_img = pygame.image.load("data/TUTS_COMPLETE.png").convert_alpha()
is_coming_from_tutorial = False


class CollectibleOrb:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = orb_game_img.get_rect(center=(x, y))
        self.hover_timer = random.random() * 10
        self.alive = True

    def update(self):
        self.hover_timer += 0.1
        self.offset = math.sin(self.hover_timer) * 5

    def draw(self, surface, cam_x, cam_y):
        if self.alive:
            surface.blit(orb_game_img, (self.rect.x - cam_x, self.rect.y + self.offset - cam_y))
            glow = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.circle(glow, (200, 100, 255, 100), (15, 15), 12)
            surface.blit(glow, (self.rect.x - 3 - cam_x, self.rect.y + self.offset - 3 - cam_y), special_flags=pygame.BLEND_RGB_ADD)

class CollectibleKey:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = key_game_img.get_rect(center=(x, y))
        self.hover_timer = random.random() * 10
        self.alive = True

    def update(self):
        self.hover_timer += 0.1
        self.offset = math.sin(self.hover_timer) * 6 

    def draw(self, surface, cam_x, cam_y):
        if self.alive:
            surface.blit(key_game_img, (self.rect.x - cam_x, self.rect.y + self.offset - cam_y))

dropped_orbs = []
dropped_keys = []

# ================= ENEMY EFFECTS CLASSES =================
class ExplosionParticle:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.color = color
        self.vx, self.vy = random.uniform(-6, 6), random.uniform(-6, 6)
        self.lifetime = 45
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
    def draw(self, surface, cam_x, cam_y):
        if self.lifetime > 0:
            alpha = min(255, self.lifetime * 6)
            p_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(p_surf, (*self.color, alpha), (3, 3), 3)
            surface.blit(p_surf, (self.x - cam_x, self.y - cam_y))

explosion_particles = []

def trigger_explosion(x, y):
    for _ in range(30):
        explosion_particles.append(ExplosionParticle(x, y, (255, 100, 0)))
        explosion_particles.append(ExplosionParticle(x, y, (255, 255, 255)))

enemy1_orig = pygame.image.load("data/ENEMY1.png").convert_alpha()
enemy1_left_surf = pygame.transform.scale(enemy1_orig, (40, 55))
enemy1_right_surf = pygame.transform.flip(pygame.transform.scale(enemy1_orig, (40, 55)), True, False)

class Enemy1Bullet:
    def __init__(self, x, y, direction):
        self.x, self.y = x, y
        self.speed = 6
        self.direction = direction
        self.radius = 5
    def update(self):
        self.x += self.speed * self.direction
    def draw(self, surface, cam_x, cam_y):
        pygame.draw.circle(surface, (255, 50, 50), (int(self.x - cam_x), int(self.y - cam_y)), self.radius)
        glow = pygame.Surface((self.radius*4, self.radius*4), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 0, 0, 80), (self.radius*2, self.radius*2), self.radius*2)
        surface.blit(glow, (self.x - self.radius*2 - cam_x, self.y - self.radius*2 - cam_y))

class Enemy1Stationary:
    def __init__(self, x, y, image_surf, is_right_side=False):
        self.image = image_surf
        self.rect = self.image.get_rect(topleft=(x, y))
        self.shoot_timer = 0
        self.slant_angle = 0
        self.is_right_side = is_right_side 

        if selected_level == 3:
            self.health = 300
        elif selected_level == 2:
            self.health = 400
        else:
            self.health = 100
            
        self.max_health = self.health
        self.flash_timer = 0
        self.alive = True

    def take_damage(self, amount):
        self.health -= amount
        self.flash_timer = 5
        if self.health <= 0:
            self.health = 0
            self.alive = False
            trigger_explosion(self.rect.centerx, self.rect.centery)
            enemydead_sfx.play()

            if self.is_right_side:
                dropped_keys.append(CollectibleKey(self.rect.centerx - 25, self.rect.centery))
                dropped_orbs.append(CollectibleOrb(self.rect.centerx + 25, self.rect.centery))
            else:
                dropped_orbs.append(CollectibleOrb(self.rect.centerx, self.rect.centery))

    def update(self, p_x):
        if not self.alive: return
        self.shoot_timer += 1
        if self.shoot_timer > 90:
            self.slant_angle = 15 if p_x < self.rect.x else -15
        else:
            self.slant_angle = 0
        if self.shoot_timer >= 120:
            direction = -1 if p_x < self.rect.centerx else 1
            enemy1_bullets.append(Enemy1Bullet(self.rect.centerx, self.rect.centery, direction))
            self.shoot_timer = 0
        
        if self.flash_timer > 0: self.flash_timer -= 1

    def draw(self, surface, cam_x, cam_y):
        if not self.alive: return
        
        draw_img = self.image
        if self.flash_timer > 0:
            draw_img = self.image.copy()
            draw_img.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_ADD)

        rotated_enemy = pygame.transform.rotate(draw_img, self.slant_angle)
        new_rect = rotated_enemy.get_rect(center=self.rect.center)
        surface.blit(rotated_enemy, (new_rect.x - cam_x, new_rect.y - new_rect.height//2 + self.rect.height//2 - cam_y))

        if self.health < self.max_health:
            bar_w = 40
            bx = self.rect.centerx - 20 - cam_x
            by = self.rect.top - 15 - cam_y
            pygame.draw.rect(surface, (100, 0, 0), (bx, by, bar_w, 5))
            pygame.draw.rect(surface, (0, 255, 100), (bx, by, int((self.health/self.max_health)*bar_w), 5))

enemy1_bullets = []
enemy2_orig = pygame.image.load("data/ENEMY2.png").convert_alpha()
enemy2_surf = pygame.transform.scale(enemy2_orig, (80, 80))
enemy2_surf_right = pygame.transform.flip(enemy2_surf, True, False)
enemy2_shh_orig = pygame.image.load("data/ENEMY2_SHH.png").convert_alpha()
enemy2_shh_surf = pygame.transform.scale(enemy2_shh_orig, (80, 80))
enemy2_shh_right = pygame.transform.flip(enemy2_shh_surf, True, False)

class Enemy2Bullet:
    def __init__(self, x, y, angle):
        self.x, self.y = x, y
        self.speed = 4
        self.angle = angle 
        self.size = 12
    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
    def draw(self, surface, cam_x, cam_y):
        points = [
            (self.x - cam_x, self.y - cam_y - self.size),
            (self.x - cam_x + self.size//2, self.y - cam_y),
            (self.x - cam_x, self.y - cam_y + self.size),
            (self.x - cam_x - self.size//2, self.y - cam_y)
        ]
        pygame.draw.polygon(surface, (74, 103, 91), points) # MOSSY_GLOW color
        pygame.draw.polygon(surface, (150, 255, 150), points, 1) # Inner Glow

class Enemy2Stationary:
    def __init__(self, x, y):
        self.image_normal = enemy2_surf_right
        self.image_shh = enemy2_shh_right
        self.image = self.image_normal
        self.rect = self.image.get_rect(topleft=(x, y))
        self.shoot_timer = 0

        if selected_level == 3:
            self.health = 350
        elif selected_level == 2:
            self.health = 450
        else:
            self.health = 150
            
        self.max_health = self.health
        self.alive = True
        self.flash_timer = 0
        self.anim_timer = 0
        self.is_shh = False

    def take_damage(self, amount):
        self.health -= amount
        self.flash_timer = 5
        if self.health <= 0:
            self.alive = False
            trigger_explosion(self.rect.centerx, self.rect.centery)
            enemydead_sfx.play()
            dropped_orbs.append(CollectibleOrb(self.rect.centerx, self.rect.centery))

    def update(self):
        if not self.alive: return
        self.shoot_timer += 1
        self.anim_timer += 1
        if self.anim_timer >= 480: 
            self.is_shh = not self.is_shh
            self.image = self.image_shh if self.is_shh else self.image_normal
            self.anim_timer = 0

        if self.shoot_timer >= 200:
            enemy2_hit_sfx.play() 
            angles = [0, math.pi/2, math.pi, 3*math.pi/2] 
            wand_x = self.rect.x + 20 
            wand_y = self.rect.y + 30
            for a in angles:
                enemy2_bullets.append(Enemy2Bullet(wand_x, wand_y, a))
            self.shoot_timer = 0
        if self.flash_timer > 0: self.flash_timer -= 1

    def draw(self, surface, cam_x, cam_y):
        if not self.alive: return
        draw_img = self.image
        if self.flash_timer > 0:
            draw_img = self.image.copy()
            draw_img.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_ADD)
        
        surface.blit(draw_img, (self.rect.x - cam_x, self.rect.y - cam_y))
        
        # Enemy 2 Health Bar
        if self.health < self.max_health:
            bx, by = self.rect.x - cam_x + 10, self.rect.y - cam_y - 10
            pygame.draw.rect(surface, (100, 0, 0), (bx, by, 60, 5))
            pygame.draw.rect(surface, (0, 255, 100), (bx, by, int((self.health/self.max_health)*60), 5))

enemy2_bullets = []
enemy3_orig = pygame.image.load("data/ENEMY3.png").convert_alpha()
enemy3_surf = pygame.transform.scale(enemy3_orig, (60, 60)) 

class Enemy3Jumping:
    def __init__(self, x, y):
        self.image = enemy3_surf
        self.rect = self.image.get_rect(topleft=(x, y))
        if selected_level == 3:
            self.health = 400
        elif selected_level == 2:
            self.health = 300
        else:
            self.health = 200
            
        self.max_health = self.health
        self.alive = True
        self.flash_timer = 0
        self.vel_y = 0
        self.vel_x = 0
        self.gravity = 0.3
        self.jump_timer = 0
        self.is_rolling = False
        self.roll_angle = 0
        self.ground_y = y

    def take_damage(self, amount):
        self.health -= amount
        self.flash_timer = 5
        hero_hit_enemy_sfx.play()
        if self.health <= 0:
            self.alive = False
            trigger_explosion(self.rect.centerx, self.rect.centery)
            enemydead_sfx.play() 
            dropped_orbs.append(CollectibleOrb(self.rect.centerx, self.rect.centery))

    def update(self, p_x, p_y):
        if not self.alive: return
        self.vel_y += self.gravity
        self.rect.y += self.vel_y
        
        if self.rect.y >= self.ground_y:
            self.rect.y = self.ground_y
            self.vel_y = -6 
    
        if abs(p_y - self.rect.y) < 50:
            self.is_rolling = True
            if p_x < self.rect.x:
                self.vel_x = -4
            else:
                self.vel_x = 4
        else:
            self.is_rolling = False
            self.vel_x = 0
            
        if self.is_rolling:
            self.rect.x += self.vel_x
            self.roll_angle += 15 
            
        if self.flash_timer > 0: self.flash_timer -= 1

    def draw(self, surface, cam_x, cam_y):
        if not self.alive: return
        draw_img = self.image
        if self.flash_timer > 0:
            draw_img = self.image.copy()
            draw_img.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_ADD)
            
        rotated_enemy = pygame.transform.rotate(draw_img, self.roll_angle)
        new_rect = rotated_enemy.get_rect(center=self.rect.center)
        surface.blit(rotated_enemy, (new_rect.x - cam_x, new_rect.y - new_rect.height//2 + self.rect.height//2 - cam_y))
        
        # Enemy 3 Health Bar
        if self.health < self.max_health:
            bx, by = self.rect.x - cam_x, self.rect.y - cam_y - 15
            pygame.draw.rect(surface, (100, 0, 0), (bx, by, 60, 5))
            pygame.draw.rect(surface, (0, 255, 100), (bx, by, int((self.health/self.max_health)*60), 5))

stationary_enemies = [
    Enemy1Stationary(30, 427, enemy1_left_surf), 
    Enemy1Stationary(1005, 72, enemy1_right_surf, is_right_side=True),
    Enemy2Stationary(100, 100)
]


dropped_keys.append(CollectibleKey(220, 140))

# ================= VICTORY DOOR SYSTEM =================
door_orig = pygame.image.load("data/RIGHT_DOOR.png").convert_alpha()
door_img = pygame.transform.scale(door_orig, (60, 60))
door_rect = door_img.get_rect(bottomright=(885, 430)) 

is_victory = False
victory_anim_timer = 0
show_victory_screen = False

# ---------------- PLAYER PHYSICS (MAY HEALTH NA) ----------------
hero_x, hero_y = 100, 500
hero_vel_y = 0
hero_speed = 4
gravity = 0.5
jump_height = -13
is_jumping = False
jump_count = 0
jump_buffer_used = False
facing_right = True
is_hit_aiming = False 

# ---  HEALTH VARIABLES ---
hero_max_health = 200
hero_health = 200
invincibility_timer = 0

# --- DEATH ANIMATION STATE ---
is_dead = False
death_blink_phase = False 
death_timer = 0
death_blink_timer = 0

# ================= SPAWN ANIMATION LOGIC=================
hero_spawn_alpha = 255  
is_spawning = False
spawn_timer = 0
spawn_fx_particles = []

# ================= SUPER POWER VARIABLES (MAGE)=================
charge_value = 0
is_charging = False
power_active = False
power_timer = 0
particles = [] 
shockwaves = []

# =================DASH MECHANIC VARIABLES =================
last_click_time = 0
dash_cooldown = 0
is_dashing = False
dash_timer = 0
dash_direction = 1 
ghost_trails = []  
scarf_particles = [] 
hero_tilt = 0
target_tilt = 0

# --- EFFECTS & HOVER VARIABLES ---
hover_timer = 0
hover_offset = 0

# ================= TUTORIAL SYSTEM VARIABLES =================
tutorial_active = False
tutorial_step = 0
previous_tutorial_step = -1
tutorial_prompts = [
    "Press A and D to Move",            # Step 0
    "Press W or SPACE to Jump",         # Step 1
    "Double Click LEFT MOUSE to Dash",  # Step 2
    "Right Click to Aim and Shoot",     # Step 3
    "ELIMINATE ENEMIES AND FIND ALL THE KEYS", # Step 4
    "ALL ENEMIES ARE ELIMINATED!",      # Step 5 
    "YOU HAVE FOUND ALL THE KEYS!",     # Step 6
    "LOCATE THE HIDDEN EXIT"            # Step 7 (Final Mission)
]

# ======================================================================

def create_particles(x, y, color=CYAN):
    for _ in range(2):
        particles.append([[x + 25, y + 40], [random.randint(-20, 20) / 10, random.randint(-20, 20) / 10], random.randint(4, 8), color])

# ================= MAGIC BALA & EFFECT =================
class Bullet:
    def __init__(self, x, y, target_x, target_y, is_laser=False):
        self.x = x
        self.y = y
        self.is_laser = is_laser
        self.speed = 15 if is_laser else 8 
        self.angle = math.atan2(target_y - y, target_x - x) 
        self.dx = math.cos(self.angle) * self.speed
        self.dy = math.sin(self.angle) * self.speed
        self.radius = 4 if is_laser else 7 
        self.distance_traveled = 0
        self.max_range = 250 if is_laser else 180 

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.distance_traveled += self.speed
        if self.distance_traveled > self.max_range:
            return False
        return True

    def draw(self, surface, cam_x, cam_y):
        if self.is_laser:
            line_length = 15
            end_x = self.x + math.cos(self.angle) * line_length
            end_y = self.y + math.sin(self.angle) * line_length
            pygame.draw.line(surface, WHITE, (self.x - cam_x, self.y - cam_y), (end_x - cam_x, end_y - cam_y), 3)
            glow_surf = pygame.Surface((width, height), pygame.SRCALPHA)
            pygame.draw.line(glow_surf, (255, 255, 255, 100), (self.x - cam_x, self.y - cam_y), (end_x - cam_x, end_y - cam_y), 6)
            surface.blit(glow_surf, (0, 0))
        else:
            for i in range(2):
                r = self.radius + (i * 4)
                s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
                pygame.draw.circle(s, (200, 100, 255, 120), (r, r), r)
                surface.blit(s, (self.x - r - cam_x, self.y - r - cam_y))
            pygame.draw.circle(surface, WHITE, (int(self.x - cam_x), int(self.y - cam_y)), self.radius)

bullets = []
shoot_cooldown = 0

class MagicOrb:
    def draw(self, surface, x, y):
        for i in range(3):
            r = 18 + random.randint(0, 10)
            glow = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
            pygame.draw.circle(glow, (180, 50, 255, 100), (r, r), r)
            surface.blit(glow, (x - r, y - r), special_flags=pygame.BLEND_RGB_ADD)
        pygame.draw.circle(surface, WHITE, (x, y), 10)
        pygame.draw.circle(surface, (200, 100, 255), (x, y), 13, 2)

magic_visual = MagicOrb()

# =================ENEMY CLASS =================
class Enemy:
    def __init__(self, x, y, patrol_range):
        self.rect = pygame.Rect(x, y, 50, 75)
        self.start_x = x
        self.patrol_range = patrol_range
        self.speed = 3
        self.direction = 1
        self.alive = True

    def update(self, player_x, player_y):
        if not self.alive: return
        dist = math.hypot(player_x - self.rect.x, player_y - self.rect.y)
        if dist < 250:
            if player_x < self.rect.x: self.rect.x -= self.speed + 1
            else: self.rect.x += self.speed + 1
        else:
            self.rect.x += self.speed * self.direction
            if abs(self.rect.x - self.start_x) > self.patrol_range:
                self.direction *= -1

    def draw(self, surface, cam_x, cam_y):
        if self.alive:
            pygame.draw.rect(surface, (30, 0, 0), (self.rect.x - cam_x, self.rect.y - cam_y, self.rect.width, self.rect.height))
            pygame.draw.rect(surface, RED, (self.rect.x - cam_x, self.rect.y - cam_y, self.rect.width, self.rect.height), 2)
            pygame.draw.circle(surface, RED, (self.rect.x - cam_x + 15, self.rect.y - cam_y + 20), 4)
            pygame.draw.circle(surface, RED, (self.rect.x - cam_x + 35, self.rect.y - cam_y + 20), 4)

enemies = []

# ================= PINALAWAK NA PLATFORMS (TRUE=Solid, FALSE=One-way) =================
platforms = [

    [pygame.Rect(0, 580, 2500, 100), True],
    [pygame.Rect(0, 480, 128, 30), False],
    [pygame.Rect(0, 372, 120, 30), True],
    [pygame.Rect(0, 0, 2500, 60), True],
    [pygame.Rect(0, 60, 289, 42), True],

    [pygame.Rect(224, 295, 165, 90), True],

    [pygame.Rect(0, 372, 125, 30), False],
    [pygame.Rect(0, 255, 115, 30), True],
    [pygame.Rect(0, 172, 490, 55), True],

    [pygame.Rect(243, 480, 193, 30), True],
    [pygame.Rect(375, 127, 61, 354), True],

    [pygame.Rect(630, 127, 80, 455), True],

    [pygame.Rect(570, 490, 68, 15), False], #ito
    [pygame.Rect(570, 360, 68, 10), False], #ito
    [pygame.Rect(580, 230, 68, 50), True],

    [pygame.Rect(435, 420, 65, 15), False], #ito
    [pygame.Rect(435, 303, 65, 15), False], #ito

    [pygame.Rect(709, 128, 60, 15), True],
    [pygame.Rect(779, 215, 60, 15), True],
    [pygame.Rect(893, 140, 60, 15), True],
    [pygame.Rect(946, 128, 140, 15), True],

    [pygame.Rect(990, 139, 80, 350), True],
    [pygame.Rect(710, 430, 280, 70), True],

    [pygame.Rect(830, 310, 60, 15), True],
    [pygame.Rect(760, 340, 200, 15), True],

    [pygame.Rect(1131, 206, 40, 10), False],
    [pygame.Rect(1070, 287, 30, 10), False],
    [pygame.Rect(1128, 368, 30, 15), False],
    [pygame.Rect(1070, 454, 30, 15), False]
]

select_level_img = pygame.image.load("data/PLSSELECT_LEVEL.png")
select_level_img = pygame.transform.scale(select_level_img, (400, 260))
show_warning = False
warning_alpha = 0
warning_timer = 0
fade_in = True

# ---------------- TEXT FADE ----------------
font_big = pygame.font.SysFont(None, 34)
text_alpha = 0 
fade_speed = 2
story_text = "Are you brave enough to overcome the shadows and find the way out?"

# AUTO-TRANSITION TIMER ---
story_display_timer = 0
story_max_duration = 100 

# ---------------- LOADING BAR ----------------
loading_progress = 0
loading_speed = 5
loading_done = False

# ---------------- MUSIC SETTINGS ----------------
pygame.mixer.music.load("data/BGMUSIC.mp3")
pygame.mixer.music.set_volume(0.5) #music
music_started = False
is_muted = False 

# ---------------- OVERLAYS / POPUPS ----------------
exit_popup = pygame.image.load("data/MAINMENU_BLUR.png")
exit_popup = pygame.transform.scale(exit_popup, (width, height))
second_blur = pygame.image.load("data/SECONDBG_BLUR.png")
second_blur = pygame.transform.scale(second_blur, (width, height))


show_exit_popup = False 
show_exit_confirm = False 

# Info Panel Setup
press_info = pygame.image.load("data/PRESS_INFO.png")

show_info_panel = False
blink_timer = 0
blink_visible = True
font = pygame.font.SysFont(None, 26)

# Exit Panel Setup
panel_exit = pygame.image.load("data/PANEL_EXIT.png")
panel_exit = pygame.transform.scale(panel_exit, (450, 270))
askexit_img = pygame.image.load("data/ASKEXIT.png")
askcancel_img = pygame.image.load("data/ASKCANCEL.png")
askexit_img = pygame.transform.scale(askexit_img, (160, 65))
askcancel_img = pygame.transform.scale(askcancel_img, (160, 65))

panel_rect = panel_exit.get_rect(center=(width//2, height//2))
askexit_rect = askexit_img.get_rect(center=(width//2 - 100, height//2 + 55))
askcancel_rect = askcancel_img.get_rect(center=(width//2 + 100, height//2 + 55))

defeat = pygame.image.load("data/DEFEAT.png")

# ================= MAIN GAME LOOP =================

running = True
while running:

    mouse_pos = pygame.mouse.get_pos() 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release() 
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if show_actual_game and not is_dead and not is_victory and not show_victory_screen:
                if event.key == pygame.K_w or event.key == pygame.K_SPACE:
                    if not is_jumping: 
                        hero_vel_y = jump_height
                        is_jumping = True
                        jump_count += 1
                        jumphero_sfx.play()
                        shockwaves.append([hero_x + 22, hero_y + 60, 5, 200])

            if event.key == pygame.K_ESCAPE: 
                cap.release()
                pygame.quit()
                sys.exit()
            if show_info_panel and event.key == pygame.K_SPACE: 
                show_info_panel = False
                show_exit_popup = False

            if show_actual_game and not is_victory and not is_dead:
                if event.key == pygame.K_e:
                    dist_to_door = math.hypot(hero_x - door_rect.centerx, hero_y - door_rect.centery)
                    if selected_level == 3:
                        required_keys = 4
                    elif selected_level == 2:
                        required_keys = 3
                    else:
                        required_keys = 2

                    if dist_to_door < 80 and collected_keys >= required_keys:
                        is_victory = True
                        victory_anim_timer = 120 
                        pygame.mixer.music.stop()
                        exit_sound_sfx.play()
            
            if is_dead:
                if event.key == pygame.K_SPACE:
                    defeat_sound_sfx.stop()
                    ssj_channel.stop()
                    hero_health = 200
                    invincibility_timer = 0   
                    death_blink_phase = False  
                    is_dead = False        
                    hero_vel_y = 0
                    hero_x, hero_y = 100, 400
                    is_dead = False
                    death_blink_phase = False
                    show_actual_game = False
                    show_second_menu = True 
                    selected_level = 0
                    bullets.clear()
                    enemy1_bullets.clear()
                    enemy2_bullets.clear()
                    dropped_keys.clear()
                    dropped_orbs.clear() 
                    stationary_enemies.clear() 
                    stationary_enemies.append(Enemy1Stationary(30, 427, enemy1_left_surf))
                    stationary_enemies.append(Enemy1Stationary(1005, 72, enemy1_right_surf, is_right_side=True))
                    stationary_enemies.append(Enemy2Stationary(100, 100))
                    
                    dropped_keys.append(CollectibleKey(220, 140))
                    camera_x = 0
                    camera_y = 0
                    collected_keys = 0
                    collected_orbs = 0
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("data/BGMUSIC.mp3")
                    if not is_muted: pygame.mixer.music.play(-1)

            if show_victory_screen:
                if event.key == pygame.K_SPACE:
                    victory_sound_sfx.stop()
                    show_victory_screen = False
                    is_coming_from_tutorial = False
                    show_actual_game = False
                    show_second_menu = True
                    selected_level = 0
                    bullets.clear()
                    enemy1_bullets.clear()
                    enemy2_bullets.clear()
                    dropped_keys.clear()
                    dropped_orbs.clear()
                    stationary_enemies.clear()
                    stationary_enemies.append(Enemy1Stationary(30, 427, enemy1_left_surf))
                    stationary_enemies.append(Enemy1Stationary(1005, 72, enemy1_right_surf, is_right_side=True))
                    stationary_enemies.append(Enemy2Stationary(100, 100))
                    dropped_keys.append(CollectibleKey(220, 140))
                    camera_x, camera_y = 0, 0
                    collected_keys, collected_orbs = 0, 0
                    hero_health = 100
                    hero_x, hero_y = 100, 400

                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("data/BGMUSIC.mp3")
                    if not is_muted: pygame.mixer.music.play(-1)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if loading_done and not is_dead and not show_victory_screen: 
                if loading_done:
                    if show_actual_game and event.button == 1:
                        current_time = pygame.time.get_ticks()
                        if selected_char_index == 0:
                            if current_time - last_click_time < 300 and dash_cooldown <= 0:
                                is_dashing = True
                                dash_timer = 15
                                dash_cooldown = 60
                                dash_direction = 1 if facing_right else -1
                                dash_warrior_sfx.play()
                            last_click_time = current_time

                    if selected_char_index != 0 and event.button == 1:
                        is_charging = True
                        if selected_char_index == 1: 
                            if show_actual_game: 
                                is_charging = True
                                if selected_char_index == 1: 
                                    if not ssj_channel.get_busy():
                                        ssj_channel.set_volume(1.0)
                                        ssj_channel.play(super_saiyan_sfx)
                
                if show_actual_game and event.button == 3:
                    is_hit_aiming = True
                    is_charging = False
                    charge_value = 0

                if show_actual_game and not show_exit_popup:
                    if prev_music_rect.collidepoint(event.pos):
                        click_sfx.play()
                        current_music_idx = (current_music_idx - 1) % len(music_playlist)
                        pygame.mixer.music.load(music_playlist[current_music_idx])
                        if not is_muted: pygame.mixer.music.play(-1)
                        
                    if next_music_rect.collidepoint(event.pos):
                        click_sfx.play()
                        current_music_idx = (current_music_idx + 1) % len(music_playlist)
                        pygame.mixer.music.load(music_playlist[current_music_idx])
                        if not is_muted: pygame.mixer.music.play(-1)

                if music_btn_rect.collidepoint(event.pos):
                    click_sfx.play() # DAGDAG: CLICK SFX
                    is_muted = not is_muted
                    pygame.mixer.music.set_volume(0 if is_muted else 0.5)
                    continue

                if show_exit_confirm:
                    if askexit_rect.collidepoint(event.pos): 
                        click_sfx.play()
                        cap.release()
                        pygame.quit()
                        sys.exit()
                    elif askcancel_rect.collidepoint(event.pos): 
                        click_sfx.play() 
                        show_exit_popup = False
                        show_exit_confirm = False
                    continue

                if show_info_panel: continue 

                if show_story_screen:
                    if skip_rect.collidepoint(event.pos):
                        click_sfx.play() 
                        ssj_channel.stop()
                        show_story_screen = False
                        show_actual_game = True

                        hero_health = 200        
                        hero_x, hero_y = 100, 400
                        collected_keys = 0
                        collected_orbs = 0
                        bullets.clear()
                        enemy1_bullets.clear()
                        enemy2_bullets.clear()
                        dropped_keys.clear()
                        dropped_orbs.clear()
                        stationary_enemies.clear()
                        stationary_enemies.append(Enemy1Stationary(30, 427, enemy1_left_surf))
                        stationary_enemies.append(Enemy1Stationary(1005, 72, enemy1_right_surf, is_right_side=True))
                        stationary_enemies.append(Enemy2Stationary(100, 100))
                        dropped_keys.append(CollectibleKey(220, 140))
                        selected_level = 1
                        selected_char_index = 0
                        tutorial_active = True
                        tutorial_step = 0
                        active_hero_right, active_hero_left = warrior_right, warrior_left
                        active_aiming_right, active_aiming_left = warrior_aiming_right, warrior_aiming_left
                        if not is_muted:
                            pygame.mixer.music.load("data/MAIN_MUSICGAME.mp3")
                            pygame.mixer.music.play(-1)
                    continue

                if show_actual_game:
                    if tutorial_active and skip_rect.collidepoint(event.pos):
                        click_sfx.play()
                        tutorial_active = False
                        tutorial_step = 0 
                        hero_x, hero_y = 100, 400 
                        hero_health = 200       
                        collected_keys = 0       
                        collected_orbs = 0        
                        bullets.clear()
                        enemy1_bullets.clear()
                        enemy2_bullets.clear()
                        dropped_keys.clear()
                        dropped_orbs.clear()
                        stationary_enemies.clear()
                        stationary_enemies.append(Enemy1Stationary(30, 427, enemy1_left_surf))
                        stationary_enemies.append(Enemy1Stationary(1005, 72, enemy1_right_surf, is_right_side=True))
                        stationary_enemies.append(Enemy2Stationary(100, 100))
                        dropped_keys.append(CollectibleKey(220, 140))
                        show_actual_game = False
                        show_second_menu = True 

                        selected_level = 0
                        
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load("data/BGMUSIC.mp3")
                        if not is_muted: pygame.mixer.music.play(-1)
                    continue

                if show_second_menu:
                    if not is_dead: 
                        if back_rect.collidepoint(event.pos): 
                            click_sfx.play() 
                            show_second_menu = False
                            selected_level = 0 
                        elif info_rect.collidepoint(event.pos): 
                            click_sfx.play() 
                            show_exit_popup = True
                            show_info_panel = True
                        elif level1_rect.collidepoint(event.pos):
                            click_sfx.play() 
                            selected_level = 1
                        elif level2_rect.collidepoint(event.pos):
                            click_sfx.play()
                            selected_level = 2
                        elif level3_rect.collidepoint(event.pos):
                            click_sfx.play() 
                            selected_level = 3
                        elif start_level_rect.collidepoint(event.pos):
                            click_sfx.play() 
                            if selected_level != 0:
                                show_second_menu = False
                                show_character_screen = True
                            else:
                                show_warning = True
                                warning_alpha = 0
                                warning_timer = 60
                                fade_in = True
                        continue

                if show_character_screen:
                    if back_rect.collidepoint(event.pos): 
                        click_sfx.play() 
                        show_character_screen = False
                        show_second_menu = True 
                    elif info_rect.collidepoint(event.pos):
                        click_sfx.play() 
                        show_exit_popup = True
                        show_info_panel = True
                    elif left_arrow_rect.collidepoint(event.pos) or right_arrow_rect.collidepoint(event.pos):
                        click_sfx.play() 
                        selected_char_index = 1 if selected_char_index == 0 else 0
                    elif confirm_char_rect.collidepoint(event.pos):
                        click_sfx.play() 
                        ssj_channel.stop()
                        show_character_screen = False
                        show_actual_game = True
                        tutorial_active = False 
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load(music_playlist[current_music_idx])
                        if not is_muted:
                            pygame.mixer.music.play(-1)
                    
                        if selected_char_index == 0:
                            active_hero_right, active_hero_left = warrior_right, warrior_left
                            active_aiming_right, active_aiming_left = warrior_aiming_right, warrior_aiming_left
                        else:
                            active_hero_right, active_hero_left = hero_right, hero_left
                            active_aiming_right, active_aiming_left = hero_aiming_right, hero_aiming_left
                        
                        hero_x, hero_y = 100, 400
                        hero_health = 200
                        is_dead = False
                        is_victory = False
                        is_spawning = True
                        hero_spawn_alpha = 0
                        spawn_timer = 60
                        hero_spawn_sfx.play()
                        
                        if selected_level == 2:
                            face_left_img = pygame.transform.flip(enemy1_left_surf, True, False)
                            stationary_enemies.append(Enemy1Stationary(1040, 530, face_left_img))
                            dropped_keys.append(CollectibleKey(880, 550))
                
                        if selected_level == 3:
                            face_left_img = pygame.transform.flip(enemy1_left_surf, True, False)
                            mid_enemy = Enemy1Stationary(1040, 530, face_left_img)
                            stationary_enemies.append(mid_enemy)
                            stationary_enemies.append(Enemy2Stationary(830, 235))
                            stationary_enemies.append(Enemy3Jumping(500, 530))
                            dropped_keys.append(CollectibleKey(880, 550))
                            dropped_keys.append(CollectibleKey(805, 320))
                            hero_spawn_sfx.play()
                    continue

                if info_rect.collidepoint(event.pos):
                    click_sfx.play() 
                    show_exit_popup = True
                    show_info_panel = True
                elif start_rect.collidepoint(event.pos):
                    click_sfx.play() 
                    show_story_screen = True
                    text_alpha = 0 
                    story_display_timer = 0 
                    tutorial_step = 0      
                    pygame.mixer.music.stop()
                elif exit_rect.collidepoint(event.pos):
                    click_sfx.play() 
                    show_exit_popup = True
                    show_exit_confirm = True

        if event.type == pygame.MOUSEBUTTONUP:
            if show_actual_game:
                if event.button == 1:
                    is_charging = False
                    if charge_value >= 100:
                        power_active = True
                        power_timer = 120 
                        shockwaves.append([hero_x + 27, hero_y + 40, 10, 255])
                    else:
                        ssj_channel.stop() 
                    charge_value = 0
                
                if event.button == 3:
                    is_hit_aiming = False

    screen.fill(BLACK) 

    if not loading_done:
        pygame.draw.rect(screen, WHITE, (0, height - 10, loading_progress, 5))
        loading_progress += loading_speed
        if loading_progress >= width:
            loading_done = True
            if not music_started:
                pygame.mixer.music.play(-1)
                music_started = True

    elif show_actual_game:

        if tutorial_active:
            if tutorial_step != previous_tutorial_step:
                tutorial_next_sfx.play()  
                previous_tutorial_step = tutorial_step 
            keys_tut = pygame.key.get_pressed()
            

            alive_enemies_count = len([e for e in stationary_enemies if e.alive])
            
            if selected_level == 3: required_keys = 4
            elif selected_level == 2: required_keys = 3
            else: required_keys = 2

            if tutorial_step == 0:
                if keys_tut[pygame.K_a] or keys_tut[pygame.K_d]: tutorial_step = 1
            elif tutorial_step == 1:
                if keys_tut[pygame.K_w] or keys_tut[pygame.K_SPACE]: tutorial_step = 2
            elif tutorial_step == 2:
                if is_dashing: tutorial_step = 3
            elif tutorial_step == 3:
                if is_hit_aiming: tutorial_step = 4
            
            elif tutorial_step == 4:
                if alive_enemies_count == 0:
                    tutorial_step = 5
                elif collected_keys >= required_keys:
                    tutorial_step = 6
                    
            elif tutorial_step == 5:
                if collected_keys >= required_keys:
                    tutorial_step = 7
                
            elif tutorial_step == 6:
                if alive_enemies_count == 0:
                    tutorial_step = 7

            elif tutorial_step == 7: 
                dist_to_door = math.hypot(hero_x - door_rect.centerx, hero_y - door_rect.centery)
                if dist_to_door < 80:
                    is_victory = True 
                    victory_anim_timer = 120
                    is_coming_from_tutorial = True 
                    tutorial_active = False 
                    
                    pygame.mixer.music.stop()
                    exit_sound_sfx.play()

        if camera_follow_enabled:
            target_cam_x = hero_x - (internal_res[0] // 2)
            target_cam_y = hero_y - (internal_res[1] // 2)

            camera_x += (target_cam_x - camera_x) * camera_smoothing
            camera_y += (target_cam_y - camera_y) * camera_smoothing

            if camera_x < 0: camera_x = 0
            if camera_y < 0: camera_y = 0

            max_x = width - internal_res[0]
            max_y = height - internal_res[1]

            if camera_x > max_x: camera_x = max_x
            if camera_y > max_y: camera_y = max_y
        else:
            camera_x = 0
            camera_y = 0

        if is_spawning:
            spawn_timer -= 1
            if hero_spawn_alpha < 255: hero_spawn_alpha += 5
            for _ in range(2):
                p_angle = random.uniform(0, math.pi*2)
                p_dist = random.randint(40, 100)
                px = hero_x + 22 + math.cos(p_angle) * p_dist
                py = hero_y + 32 + math.sin(p_angle) * p_dist
                spawn_fx_particles.append([[px, py], [(hero_x+22-px)*0.1, (hero_y+32-py)*0.1], random.randint(2, 5)])
            if spawn_timer <= 0:
                is_spawning = False
                hero_spawn_alpha = 255
                shockwaves.append([hero_x + 22, hero_y + 32, 10, 200])

        if is_victory:
            victory_anim_timer -= 1
            hero_x += (door_rect.centerx - 22 - hero_x) * 0.1
            hero_y += (door_rect.centery - 32 - hero_y) * 0.1
            hero_tilt += 20
            
            if victory_anim_timer <= 0:
                is_victory = False
                show_victory_screen = True 
                victory_sound_sfx.play()

        if hero_health <= 0:
            hero_health = 0
            if tutorial_active:
                hero_health = 200
                hero_x, hero_y = 100, 400
                hero_vel_y = 0
                invincibility_timer = 60 
                hero_spawn_sfx.play()
            elif not is_dead and not death_blink_phase:
                death_blink_phase = True
                invincibility_timer = 999 
                death_timer = 150 
                pygame.mixer.music.stop()
                player_hurt_sfx.play()
                hero_death_blink_sfx.play()
            
        if not is_dead and not is_victory and not show_victory_screen: 
            current_speed = hero_speed * 2 if power_active else hero_speed
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or keys[pygame.K_SPACE]:
                if not is_jumping and not jump_buffer_used:
                    hero_vel_y = jump_height
                    is_jumping = True
                    jump_buffer_used = True 
                    jumphero_sfx.play()
                    shockwaves.append([hero_x + 22, hero_y + 60, 5, 200])
            else:
                jump_buffer_used = False
            
            if not is_dead and not is_victory:
                if keys[pygame.K_a]: 
                    hero_x -= current_speed
                    facing_right = False
                if keys[pygame.K_d]: 
                    hero_x += current_speed
                    facing_right = True

            if is_dashing:
                dash_speed = 15
                hero_x += dash_speed * dash_direction
                
                hero_rect_dash = pygame.Rect(hero_x, hero_y, 45, 65)
                for plat_data in platforms:
                    plat_rect = plat_data[0]
                    is_solid = plat_data[1]
                    if is_solid and hero_rect_dash.colliderect(plat_rect):
                        if dash_direction > 0: 
                            hero_x = plat_rect.left - 45
                        else: 
                            hero_x = plat_rect.right
                        is_dashing = False 
                        break

                dash_timer -= 1
                if dash_timer % 3 == 0:
                    t_surf = active_hero_right.copy() if facing_right else active_hero_left.copy()
                    t_surf.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_ADD)
                    ghost_trails.append([t_surf, (hero_x, hero_y), 150])
                if dash_timer <= 0:
                    is_dashing = False
            if dash_cooldown > 0:
                dash_cooldown -= 1

            if hero_x < 0: hero_x = 0
            if hero_x > width - 45: hero_x = width - 45
            
            hero_rect_active = pygame.Rect(hero_x, hero_y, 45, 65)
            for plat_data in platforms:
                plat_rect = plat_data[0]
                is_solid = plat_data[1]
                if is_solid and hero_rect_active.colliderect(plat_rect):
                    if hero_rect_active.centerx < plat_rect.centerx: 
                        hero_x = plat_rect.left - 45
                    else: 
                        hero_x = plat_rect.right
                    hero_rect_active.x = hero_x

            if not is_victory:
                hero_vel_y += gravity
                hero_y += hero_vel_y
            
            on_ground = False
            hero_rect_active = pygame.Rect(hero_x, hero_y, 45, 65)
            
            for plat_data in platforms:
                plat_rect = plat_data[0]
                is_solid = plat_data[1]
                if hero_rect_active.colliderect(plat_rect):
                    if is_solid:
                        if hero_vel_y > 0:
                            hero_y = plat_rect.top - 65
                            hero_vel_y = 0
                            is_jumping = False
                            jump_count = 0
                            on_ground = True
                        elif hero_vel_y < 0: 
                            hero_y = plat_rect.bottom
                            hero_vel_y = 0
                    else:
                        # ONE-WAY LOGIC
                        if hero_vel_y > 0:
                            if (hero_y + 65 - hero_vel_y) <= plat_rect.top + 10:
                                hero_y = plat_rect.top - 65
                                hero_vel_y = 0
                                is_jumping = False
                                on_ground = True
                    hero_rect_active.y = hero_y 

            if not on_ground:
                is_jumping = True

            if invincibility_timer > 0:
                invincibility_timer -= 1

            if selected_char_index == 0:
                hover_offset = 0

                if not is_dead and not is_victory:
                    if random.random() < 0.4: 
                        flame_x = hero_x + 22 + random.randint(-12, 12)
                        flame_y = hero_y + 5 
                        particles.append([
                            [flame_x, flame_y], 
                            [random.uniform(-0.5, 0.5), random.uniform(-1.5, -0.5)],
                            random.randint(6, 9), 
                            (255, 255, 255) 
                        ])
            else:
                hover_timer += 0.08
                hover_offset = math.sin(hover_timer) * 6 
                
                if not is_dead and not is_victory:
                    is_moving = (keys[pygame.K_a] or keys[pygame.K_d])
                    spawn_chance = 0.4 if is_moving else 0.15
                    if random.random() < spawn_chance:
                        p_color = CYAN if not power_active else GOLD
                        particles.append([
                            [hero_x + 22 + random.randint(-8, 8), hero_y + 60 + hover_offset],
                            [random.randint(-10, 10) / 10, random.randint(10, 30) / 10], 
                            random.randint(3, 5),
                            p_color
                        ])
                    
                    if not is_moving and not is_jumping:
                        if random.random() < 0.1: 
                            spark_color = MOSSY_GLOW if not power_active else WHITE
                            particles.append([
                                [hero_x + random.randint(0, 45), hero_y + 65 + hover_offset],
                                [random.uniform(-0.5, 0.5), random.uniform(-1.5, -0.5)], 
                                random.randint(2, 4),
                                spark_color
                            ])
            # ======================================================

            if not is_dead and not is_victory:
                if selected_char_index != 0:
                    if is_charging and charge_value < 100:
                        charge_value += 2
                        create_particles(hero_x, hero_y, CYAN)
                
                if is_hit_aiming:
                    mouse_world_x = (mouse_pos[0] / zoom_level) + camera_x
                    mouse_world_y = (mouse_pos[1] / zoom_level) + camera_y
                    
                    facing_right = True if mouse_world_x > hero_x + 32 else False
                    
                    if shoot_cooldown <= 0:
                        hand_x = hero_x + 50 if facing_right else hero_x + 5
                        hand_y = hero_y + 35 + hover_offset
                        
                        if selected_char_index == 0:
                            bullets.append(Bullet(hand_x, hand_y, mouse_world_x, mouse_world_y, is_laser=True))
                            warrior_aim_sfx.play() 
                            shoot_cooldown = 20
                        else: 
                            bullets.append(Bullet(hand_x, hand_y, mouse_world_x, mouse_world_y, is_laser=False))
                            hero_shoot_sfx.play() 
                            shoot_cooldown = 30
                            
                    shoot_cooldown -= 1

            if power_active:
                power_timer -= 1
                create_particles(hero_x, hero_y, GOLD)
                if power_timer <= 0: 
                    power_active = False
                    if selected_char_index == 1:
                        ssj_channel.stop()
                
            if not is_dead and not is_victory:
                if keys[pygame.K_a]:
                    target_tilt = 10 
                elif keys[pygame.K_d]:
                    target_tilt = -10 
                else:
                    target_tilt = 0
                hero_tilt += (target_tilt - hero_tilt) * 0.1

                shake_x = 0
            shake_y = 0
            if is_charging and selected_char_index != 0:
                intensity = int(charge_value / 20) 
                shake_x = random.randint(-intensity, intensity)
                shake_y = random.randint(-intensity, intensity)
            # ---------------------------------------------

                if selected_char_index != 0:
                    is_moving = (keys[pygame.K_a] or keys[pygame.K_d])
                    if is_moving or power_active:
                        trail_chance = 0.3 if power_active else 0.15
                        if random.random() < trail_chance:
                            t_surf = active_hero_right.copy() if facing_right else active_hero_left.copy()
                            if power_active: t_surf.fill(GOLD, special_flags=pygame.BLEND_RGB_ADD)
                            ghost_trails.append([t_surf, (hero_x, hero_y + hover_offset), 150])

        display_surface.fill(BLACK)
        if selected_level == 1: display_surface.blit(game_bg1, (0 - camera_x, 0 - camera_y))
        elif selected_level == 2: display_surface.blit(game_bg2, (0 - camera_x, 0 - camera_y))
        elif selected_level == 3: display_surface.blit(game_bg3, (0 - camera_x, 0 - camera_y))

        for plat_data in platforms:
            plat = plat_data[0]
            if show_platforms:
                pygame.draw.rect(display_surface, MOSSY_BRICK, (plat.x - camera_x, plat.y - camera_y, plat.width, plat.height))
                pygame.draw.rect(display_surface, MOSSY_GLOW, (plat.x - camera_x, plat.y - camera_y, plat.width, plat.height), 2)

        if is_victory:
            victory_door = door_img.copy()
            alpha_glow = min(255, (120 - victory_anim_timer) * 4.0) 
            victory_door.fill((alpha_glow, alpha_glow, alpha_glow), special_flags=pygame.BLEND_RGB_ADD)
            display_surface.blit(victory_door, (door_rect.x - camera_x, door_rect.y - camera_y))
        else:
            display_surface.blit(door_img, (door_rect.x - camera_x, door_rect.y - camera_y))
        

        dist_to_door = math.hypot(hero_x - door_rect.centerx, hero_y - door_rect.centery)
        if dist_to_door < 80 and not is_victory:
            circle_y = door_rect.top - 30 - camera_y
            pygame.draw.circle(display_surface, BLACK, (door_rect.centerx - int(camera_x), int(door_rect.top - 30 - camera_y)), 18)
            
            if selected_level == 3:
                required_keys = 4
            elif selected_level == 2:
                required_keys = 3
            else:
                required_keys = 2
            pygame.draw.circle(display_surface, GOLD if collected_keys >= required_keys else RED, (door_rect.centerx - int(camera_x), int(door_rect.top - 30 - camera_y)), 18, 2)
            
            msg = "E" if collected_keys >= required_keys else "LOCKED"
            msg_font = pygame.font.SysFont("Arial", 18, bold=True)
            txt = msg_font.render(msg, True, WHITE)
            display_surface.blit(txt, txt.get_rect(center=(door_rect.centerx - camera_x, door_rect.top - 30 - camera_y)))

        for se in stationary_enemies:
            if isinstance(se, Enemy2Stationary):
                se.update()
            elif isinstance(se, Enemy3Jumping):
                se.update(hero_x, hero_y)
                if se.alive and not is_dead and hero_health > 0 and not is_victory and hero_rect_active.colliderect(se.rect):
                    if invincibility_timer <= 0:
                        player_hurt_sfx.play()
                        hero_health -= 15
                        invincibility_timer = 50
                        hero_vel_y = -10
                        hero_x += -15 if hero_x < se.rect.centerx else 15
            else:
                se.update(hero_x)
            se.draw(display_surface, camera_x, camera_y)

        for orb in dropped_orbs[:]:
            orb.update()
            orb.draw(display_surface, camera_x, camera_y)
            if not is_dead and hero_rect_active.colliderect(orb.rect):
                collected_orbs += 1
                collect_sfx.play()
                dropped_orbs.remove(orb)
                particles.append([[orb.rect.centerx, orb.rect.centery], [0, -2], 10, WHITE])
        
        for k in dropped_keys[:]:
            k.update()
            k.draw(display_surface, camera_x, camera_y)
            if not is_dead and hero_rect_active.colliderect(k.rect):
                collected_keys += 1
                collect_sfx.play()
                dropped_keys.remove(k)
                for _ in range(8):
                    particles.append([[k.rect.centerx, k.rect.centery], [random.uniform(-2,2), random.uniform(-2,2)], 5, GOLD])

        for eb in enemy1_bullets[:]:
            eb.update()
            eb.draw(display_surface, camera_x, camera_y)
            eb_rect = pygame.Rect(eb.x - eb.radius, eb.y - eb.radius, eb.radius*2, eb.radius*2)
            hit_wall = False
            for plat_data in platforms:
                plat_rect = plat_data[0]
                if eb_rect.colliderect(plat_rect):
                    hit_wall = True
                    enemy1_hit_sfx.play()
                    for _ in range(5):
                        particles.append([[eb.x, eb.y], [random.uniform(-2, 2), random.uniform(-2, 2)], random.randint(2, 4), RED])
                    break
            
            if hit_wall:
                if eb in enemy1_bullets: enemy1_bullets.remove(eb)
                continue

            if not is_dead and hero_health > 0 and not is_victory and eb_rect.colliderect(hero_rect_active):
                if invincibility_timer <= 0:
                    hero_health -= 20
                    enemy1_hit_sfx.play()
                    player_hurt_sfx.play()
                    invincibility_timer = 50
                    hero_vel_y = -8
                    hero_x += (eb.direction * 10)
                if eb in enemy1_bullets: enemy1_bullets.remove(eb)
            elif eb.x < 0 or eb.x > game_world_size[0]:
                if eb in enemy1_bullets: enemy1_bullets.remove(eb)


        for e2b in enemy2_bullets[:]:
            e2b.update()
            e2b.draw(display_surface, camera_x, camera_y)
            e2b_rect = pygame.Rect(e2b.x - e2b.size//2, e2b.y - e2b.size//2, e2b.size, e2b.size)
            
            if not is_dead and not is_victory and e2b_rect.colliderect(hero_rect_active):
                if invincibility_timer <= 0:
                    hero_health -= 30
                    player_hurt_sfx.play() 
                    invincibility_timer = 50
                    # KNOCK UP (ENEMY 2 BULLET) ---
                    hero_vel_y = -7
                    for _ in range(8):
                        particles.append([[e2b.x, e2b.y], [random.uniform(-2, 2), random.uniform(-2, 2)], random.randint(3, 5), MOSSY_GLOW])
                if e2b in enemy2_bullets: enemy2_bullets.remove(e2b)
            elif e2b.x < -100 or e2b.x > game_world_size[0] + 100 or e2b.y < -100 or e2b.y > game_world_size[1] + 100:
                if e2b in enemy2_bullets: enemy2_bullets.remove(e2b)

        for trail in ghost_trails[:]:
            img, pos, alpha = trail
            img.set_alpha(alpha)
            display_surface.blit(img, (pos[0] - camera_x, pos[1] - camera_y))
            trail[2] -= 15 
            if trail[2] <= 0: ghost_trails.remove(trail)

      
        for sp in scarf_particles[:]:
            sp[0][0] += sp[1][0]; sp[0][1] += sp[1][1]; sp[2] -= 0.1
            pygame.draw.rect(display_surface, sp[3], (int(sp[0][0] - camera_x), int(sp[0][1] - camera_y), int(sp[2]), int(sp[2])))
            if sp[2] <= 0: scarf_particles.remove(sp)

        for b in bullets[:]:
            is_alive = b.update()
            if not is_alive:
                if b in bullets: bullets.remove(b)
                continue 

            b.draw(display_surface, camera_x, camera_y)
            

            bullet_rect = pygame.Rect(b.x - b.radius, b.y - b.radius, b.radius*2, b.radius*2)
            for se in stationary_enemies:
                if se.alive and se.rect.colliderect(bullet_rect):

                    damage_val = 30 if b.is_laser else 20
                    se.take_damage(damage_val) 
                    hero_hit_enemy_sfx.play() 
                    if b in bullets: bullets.remove(b)
                    break

            for ene in enemies:
                if ene.alive and ene.rect.collidepoint(b.x, b.y):
                    ene.alive = False
                    enemydead_sfx.play()
                    hero_hit_enemy_sfx.play() 
                    if b in bullets: bullets.remove(b)
                    break
            if b.x < 0 or b.x > game_world_size[0] or b.y < 0 or b.y > game_world_size[1]:
                if b in bullets: bullets.remove(b)

        for ene in enemies:
            if ene.alive:
                ene.update(hero_x, hero_y)
                ene.draw(display_surface, camera_x, camera_y)
                if not is_dead and not is_victory and hero_rect_active.colliderect(ene.rect):
                    if invincibility_timer <= 0:
                        hero_health -= 15
                        invincibility_timer = 50 
                        hero_vel_y = -10
                        if hero_x < ene.rect.x: hero_x -= 20
                        else: hero_x += 20

        for p in particles[:]:
            p[0][0] += p[1][0]; p[0][1] += p[1][1]; p[2] -= 0.2
            pygame.draw.circle(display_surface, p[3], (int(p[0][0] - camera_x), int(p[0][1] - camera_y)), int(p[2]))
            if p[2] <= 0: particles.remove(p)
            

        for ep in explosion_particles[:]:
            ep.update()
            ep.draw(display_surface, camera_x, camera_y)
            if ep.lifetime <= 0: explosion_particles.remove(ep)

        for sfp in spawn_fx_particles[:]:
            sfp[0][0] += sfp[1][0]; sfp[0][1] += sfp[1][1]; sfp[2] -= 0.1
            pygame.draw.circle(display_surface, WHITE, (int(sfp[0][0]-camera_x), int(sfp[0][1]-camera_y)), int(sfp[2]))
            if sfp[2] <= 0: spawn_fx_particles.remove(sfp)

        for s in shockwaves[:]:
            s[2] += 12; s[3] -= 10
            if s[3] <= 0: shockwaves.remove(s); continue
            shock_rect = pygame.Rect(s[0] - s[2], s[1] - s[2], s[2]*2, s[2]*2)
            for ene in enemies:
                if ene.alive and shock_rect.colliderect(ene.rect): ene.alive = False 
            temp_surf = pygame.Surface((s[2]*2, s[2]*2), pygame.SRCALPHA)
            pygame.draw.circle(temp_surf, (0, 255, 255), (s[2], s[2]), s[2], 8)
            temp_surf.set_alpha(s[3])
            display_surface.blit(temp_surf, (s[0] - s[2] - camera_x, s[1] - s[2] - camera_y))

        if is_hit_aiming:
            char_disp = active_aiming_right.copy() if facing_right else active_aiming_left.copy()
            # Visual effects based on class
            if selected_char_index != 0: # Hero magic
                magic_visual.draw(display_surface, (hero_x + 50 if facing_right else hero_x + 5) - camera_x, (hero_y + 35 + hover_offset) - camera_y)
            else: # Warrior Laser Sparkle at hand
                pygame.draw.circle(display_surface, WHITE, (int((hero_x + 60 if facing_right else hero_x) - camera_x), int(hero_y + 35 - camera_y)), random.randint(3, 8))
        else:
            char_disp = active_hero_right.copy() if facing_right else active_hero_left.copy()

        if selected_char_index != 0:
            if power_active:
                char_disp.fill((255, 215, 0), special_flags=pygame.BLEND_RGB_ADD)
            elif is_charging and not is_hit_aiming:
                char_disp.fill((charge_value * 2, 255, 255), special_flags=pygame.BLEND_RGB_ADD)

        if is_victory:
            v_scale = max(0.1, victory_anim_timer / 120)
            char_disp = pygame.transform.scale(char_disp, (int(45*v_scale), int(65*v_scale)))

        rotated_hero = pygame.transform.rotate(char_disp, hero_tilt)
        new_rect = rotated_hero.get_rect(center=char_disp.get_rect(topleft=(hero_x, hero_y + hover_offset)).center)

        is_visible = True
        if death_blink_phase:
            death_timer -= 1
            if (death_timer // 4) % 2 == 0: 
                is_visible = False
            
            if death_timer <= 0:
                death_blink_phase = False
                if not is_dead: 
                    defeat_sound_sfx.play() 
                is_dead = True 
        # --------------------------------------------------------

        if not is_dead and is_visible:
            rotated_hero.set_alpha(hero_spawn_alpha)
            if invincibility_timer > 0 and (invincibility_timer // 5) % 2 == 0:
                if (invincibility_timer // 5) % 2 == 0:
                    hit_surf = rotated_hero.copy()
                    hit_surf.fill((255, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)
                    display_surface.blit(hit_surf, (new_rect.x - camera_x + shake_x, new_rect.y - camera_y + shake_y))
                else:
                    rotated_hero.set_alpha(100)
                    display_surface.blit(rotated_hero, (new_rect.x - camera_x + shake_x, new_rect.y - camera_y + shake_y))
            else: 
                display_surface.blit(rotated_hero, (new_rect.x - camera_x + shake_x, new_rect.y - camera_y + shake_y))

        
        if not is_victory and is_charging and selected_char_index != 0:
            bar_w = 40
            pygame.draw.rect(display_surface, BLACK, (hero_x - camera_x - 3, hero_y + hover_offset - camera_y - 30, bar_w + 6, 10))
            pygame.draw.rect(display_surface, CYAN, (hero_x - camera_x, hero_y + hover_offset - camera_y - 27, (charge_value/100) * bar_w, 4))

        if is_victory:
            if victory_anim_timer > 5:
                
                for _ in range(5):
                    p_angle = random.uniform(0, math.pi * 2)
                    p_dist = random.randint(30, 100)
                    p_x = door_rect.centerx + math.cos(p_angle) * p_dist
                    p_y = door_rect.centery + math.sin(p_angle) * p_dist
                    vx = (door_rect.centerx - p_x) * 0.12
                    vy = (door_rect.centery - p_y) * 0.12
                    particles.append([[p_x, p_y], [vx, vy], random.randint(2, 5), WHITE])

        screen.blit(pygame.transform.scale(display_surface, (width, height)), (0, 0))
        
        
        # HEALTH BAR
        bar_x, bar_y = 25, 25
        bar_width, bar_height = 200, 20
        
        # Background (Dark Red/Gray) Para pag nabawasan, kita yung kulang
        pygame.draw.rect(screen, (50, 0, 0), (bar_x, bar_y, bar_width, bar_height)) 
        
        # Health (Green) 
        health_ratio = max(0, hero_health) / hero_max_health
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, int(health_ratio * bar_width), bar_height)) 
        
        # Border (White) Outline ng bar
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)

        #  ORB COUNTER UI
        orb_ui_rect = orb_ui_img.get_rect(topleft=(25, 80))
        screen.blit(orb_ui_img, orb_ui_rect)
        orb_count_txt = orb_font.render(f"x {collected_orbs}", True, GOLD)
        screen.blit(orb_count_txt, (orb_ui_rect.right + 10, orb_ui_rect.top + 5))

        # KEY COUNTER UI
        key_ui_rect = key_ui_img.get_rect(topleft=(25, 125))
        screen.blit(key_ui_img, key_ui_rect)
        
        if selected_level == 3:
            required_keys = 4
        elif selected_level == 2:
            required_keys = 3
        else:
            required_keys = 2
        
        key_color = GOLD if collected_keys >= required_keys else WHITE
        key_count_txt = orb_font.render(f"{collected_keys}/{required_keys}", True, key_color)
        screen.blit(key_count_txt, (key_ui_rect.right + 10, key_ui_rect.top + 5))

        # =================TUTORIAL OVERLAY UI =================
        if tutorial_active:
            tut_box_surf = pygame.Surface((550, 65), pygame.SRCALPHA)
            tut_box_surf.fill((0, 0, 0, 200))
            tut_box_rect = tut_box_surf.get_rect(center=(width//2, 80))
            screen.blit(tut_box_surf, tut_box_rect)
            
            border_color = (0, 255, 100) if tutorial_step in [5, 6] else CYAN
            pygame.draw.rect(screen, border_color, tut_box_rect, 2)
            
            tut_font = pygame.font.SysFont("Arial", 20, bold=True)
            
            text_color = (150, 255, 150) if tutorial_step in [5, 6] else WHITE
            tut_txt = tut_font.render(tutorial_prompts[tutorial_step], True, text_color)
            screen.blit(tut_txt, tut_txt.get_rect(center=tut_box_rect.center))

            if skip_rect.collidepoint(mouse_pos):
                sk_h = pygame.transform.scale(skip_img, (110, 50))
                screen.blit(sk_h, sk_h.get_rect(center=skip_rect.center))
            else:
                screen.blit(skip_img, skip_rect)

        current_music_img = music_off_img if is_muted else music_on_img
        if music_btn_rect.collidepoint(mouse_pos) and not show_exit_popup:
            m_hover = pygame.transform.scale(current_music_img, (120, 62))
            screen.blit(m_hover, m_hover.get_rect(center=music_btn_rect.center))
        else:
            screen.blit(current_music_img, music_btn_rect)
        
        # ================= MUSIC PLAYER UI RENDERING =================
        if not show_story_screen and not show_exit_popup and not is_dead and not show_victory_screen:
            # Transparent Background Box (Longer Square style)
            s = pygame.Surface((220, 55), pygame.SRCALPHA)
            pygame.draw.rect(s, (0, 0, 0, 150), s.get_rect()) # Square design (no border radius)
            pygame.draw.rect(s, WHITE, s.get_rect(), 1) # White border
            screen.blit(s, (width - 240, 85))
            
            # Left Arrow Triangle
            pygame.draw.polygon(screen, WHITE, [(width - 230, 115), (width - 215, 105), (width - 215, 125)])
            # Right Arrow Triangle
            pygame.draw.polygon(screen, WHITE, [(width - 40, 115), (width - 55, 105), (width - 55, 125)])
            
            song_font = pygame.font.SysFont("Arial", 14, bold=True)
            limit_text = music_titles[current_music_idx]
            if len(limit_text) > 20: limit_text = limit_text[:17] + "..."
            
            title_surf = song_font.render(limit_text, True, CYAN)
            title_rect = title_surf.get_rect(center=(width - 130, 115))
            screen.blit(title_surf, title_rect)
            
            now_playing = pygame.font.SysFont("Arial", 11).render("NOW PLAYING:", True, WHITE)
            screen.blit(now_playing, (width - 230, 90))
        
        if is_dead:
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180)) 
            screen.blit(overlay, (0, 0))
            
            defeat_scaled = pygame.transform.scale(defeat, (550, 390 ))
            defeat_rect = defeat_scaled.get_rect(center=(width//2, height//2 - 50))
            screen.blit(defeat_scaled, defeat_rect)
            
            death_blink_timer += 1
            if (death_blink_timer // 35) % 2 == 0:
                any_key_font = pygame.font.SysFont("Arial", 20, bold=True)
                any_key_txt = any_key_font.render("PRESS SPACEBAR TO EXIT", True, WHITE)
                any_key_rect = any_key_txt.get_rect(center=(width//2, height//2 + 200))
                screen.blit(any_key_txt, any_key_rect)
    
        if show_victory_screen:
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160)) 
            screen.blit(overlay, (0, 0))
            
            if is_coming_from_tutorial:
                img_to_blit = tuts_complete_img
            else:
                img_to_blit = victory

            final_scaled = pygame.transform.scale(img_to_blit, (550, 390))
            final_rect = final_scaled.get_rect(center=(width//2, height//2 - 50))
            screen.blit(final_scaled, final_rect)
            
            # 3. Slow Blinking Text
            death_blink_timer += 1
            if (death_blink_timer // 35) % 2 == 0:
                v_font = pygame.font.SysFont("Arial", 20, bold=True)
                v_txt = v_font.render("PRESS SPACEBAR TO EXIT", True, WHITE)
                v_txt_rect = v_txt.get_rect(center=(width//2, height//2 + 200))
                screen.blit(v_txt, v_txt_rect)

        if show_exit_popup:
            screen.blit(second_blur, (0, 0))
            if show_info_panel:
                forced_scale = 0.10
                orig_w = press_info.get_width()
                orig_h = press_info.get_height()
                new_w = int(orig_w * forced_scale)
                new_h = int(orig_h * forced_scale)
                press_info_small = pygame.transform.scale(press_info, (new_w, new_h))
                rect_center = press_info_small.get_rect(center=(1152 // 2, 648 // 2))
                screen.blit(press_info_small, rect_center)
                blink_timer += 1
                if blink_timer > 40:
                    blink_visible = not blink_visible
                    blink_timer = 0
                if blink_visible:
                    txt = font.render("Press Spacebar To Back", True, WHITE)
                    screen.blit(txt, txt.get_rect(center=(width//2, height - 70)))

    elif show_character_screen:
        screen.blit(character_bg, (0, 0))
        if selected_char_index == 0:
            screen.blit(warrior_name_img, warrior_name_rect)
        else:
            screen.blit(hero_name_img, hero_name_rect)

        if left_arrow_rect.collidepoint(mouse_pos) and not show_exit_popup:
            la_h = pygame.transform.scale(left_arrow_img, (155, 135))
            screen.blit(la_h, la_h.get_rect(center=left_arrow_rect.center))
        else:
            screen.blit(left_arrow_img, left_arrow_rect)

        if right_arrow_rect.collidepoint(mouse_pos) and not show_exit_popup:
            ra_h = pygame.transform.scale(right_arrow_img, (155, 135))
            screen.blit(ra_h, ra_h.get_rect(center=right_arrow_rect.center))
        else:
            screen.blit(right_arrow_img, right_arrow_rect)

        if confirm_char_rect.collidepoint(mouse_pos) and not show_exit_popup:
            cc_h = pygame.transform.scale(confirm_char_img, (240, 75))
            screen.blit(cc_h, cc_h.get_rect(center=confirm_char_rect.center))
        else:
            screen.blit(confirm_char_img, confirm_char_rect)

        if back_rect.collidepoint(mouse_pos) and not show_exit_popup:
            b_hover = pygame.transform.scale(back_img, (85, 58))
            screen.blit(b_hover, b_hover.get_rect(center=back_rect.center))
        else:
            screen.blit(back_img, back_rect)

        current_music_img = music_off_img if is_muted else music_on_img
        if music_btn_rect.collidepoint(mouse_pos) and not show_exit_popup:
            m_hover = pygame.transform.scale(current_music_img, (120, 62))
            screen.blit(m_hover, m_hover.get_rect(center=music_btn_rect.center))
        else:
            screen.blit(current_music_img, music_btn_rect)
        
            if not show_character_screen: # <--- DAGDAG MO ITONG LINE NA ITO
                if info_rect.collidepoint(mouse_pos) and not show_exit_popup:
                    i_hover = pygame.transform.scale(info_img, (65, 65))
                    screen.blit(i_hover, i_hover.get_rect(center=info_rect.center))
                else:
                    screen.blit(info_img, info_rect)
            
        if show_exit_popup:
            screen.blit(second_blur, (0, 0))
            if show_info_panel:
                forced_scale = 0.10
                orig_w = press_info.get_width()
                orig_h = press_info.get_height()
                new_w = int(orig_w * forced_scale)
                new_h = int(orig_h * forced_scale)
                press_info_small = pygame.transform.scale(press_info, (new_w, new_h))
                rect_center = press_info_small.get_rect(center=(1152 // 2, 648 // 2))
                screen.blit(press_info_small, rect_center)
                blink_timer += 1
                if blink_timer > 40:
                    blink_visible = not blink_visible
                    blink_timer = 0
                if blink_visible:
                    txt = font.render("Press Spacebar To Back", True, WHITE)
                    screen.blit(txt, txt.get_rect(center=(width//2, height - 70)))

    else:
        frame_surf = get_video_frame()
        if frame_surf:
            screen.blit(frame_surf, (0, 0))
        else:
            screen.fill(BLACK) 

        if start_rect.collidepoint(mouse_pos) and not show_story_screen and not show_exit_popup and not show_second_menu:
            s_hover = pygame.transform.scale(start_img, (300, 100))
            screen.blit(s_hover, s_hover.get_rect(center=start_rect.center))
        else:
            screen.blit(start_img, start_rect)

        if exit_rect.collidepoint(mouse_pos) and not show_story_screen and not show_exit_popup and not show_second_menu:
            e_hover = pygame.transform.scale(exit_img, (300, 100))
            screen.blit(e_hover, e_hover.get_rect(center=exit_rect.center))
        else:
            screen.blit(exit_img, exit_rect)
        
        current_music_img = music_off_img if is_muted else music_on_img
        if music_btn_rect.collidepoint(mouse_pos) and not show_exit_popup and not show_story_screen:
            m_hover = pygame.transform.scale(current_music_img, (120, 62))
            screen.blit(m_hover, m_hover.get_rect(center=music_btn_rect.center))
        else:
            screen.blit(current_music_img, music_btn_rect)
        
        if info_rect.collidepoint(mouse_pos) and not show_exit_popup and not show_story_screen:
            i_hover = pygame.transform.scale(info_img, (65, 65))
            screen.blit(i_hover, i_hover.get_rect(center=info_rect.center))
        else:
            screen.blit(info_img, info_rect)

        if show_second_menu:
            screen.blit(second_bg, (0, 0))
            if selected_level == 1:
                screen.blit(level1_select, level1_select.get_rect(center=level1_rect.center))
            elif level1_rect.collidepoint(mouse_pos) and not show_exit_popup:
                l1_h = pygame.transform.scale(level1_img, (260, 340))
                screen.blit(l1_h, l1_h.get_rect(center=level1_rect.center))
            else:
                screen.blit(level1_img, level1_rect)

            if selected_level == 2:
                screen.blit(level2_select, level2_rect)
            elif level2_rect.collidepoint(mouse_pos) and not show_exit_popup:
                l2_h = pygame.transform.scale(level2_img, (260, 340))
                screen.blit(l2_h, l2_h.get_rect(center=level2_rect.center))
            else:
                screen.blit(level2_img, level2_rect)

            if selected_level == 3:
                screen.blit(level3_select, level3_rect)
            elif level3_rect.collidepoint(mouse_pos) and not show_exit_popup:
                l3_h = pygame.transform.scale(level3_img, (260, 340))
                screen.blit(l3_h, l3_h.get_rect(center=level3_rect.center))
            else:
                screen.blit(level3_img, level3_rect)

            if start_level_rect.collidepoint(mouse_pos) and not show_exit_popup:
                sl_h = pygame.transform.scale(start_level_img, (230, 80))
                screen.blit(sl_h, sl_h.get_rect(center=start_level_rect.center))
            else:
                screen.blit(start_level_img, start_level_rect)

            if back_rect.collidepoint(mouse_pos) and not show_exit_popup:
                b_hover = pygame.transform.scale(back_img, (85, 58))
                screen.blit(b_hover, b_hover.get_rect(center=back_rect.center))
            else:
                screen.blit(back_img, back_rect)

            if music_btn_rect.collidepoint(mouse_pos) and not show_exit_popup:
                m_hover = pygame.transform.scale(current_music_img, (120, 62))
                screen.blit(m_hover, m_hover.get_rect(center=music_btn_rect.center))
            else:
                screen.blit(current_music_img, music_btn_rect)

            if info_rect.collidepoint(mouse_pos) and not show_exit_popup:
                i_hover = pygame.transform.scale(info_img, (65, 65))
                screen.blit(i_hover, i_hover.get_rect(center=info_rect.center))
            else:
                screen.blit(info_img, info_rect)

            if show_warning:
                if fade_in:
                    warning_alpha += 9 
                    if warning_alpha >= 255:
                        warning_alpha = 255
                        fade_in = False
                else:
                    if warning_timer > 0:
                        warning_timer -= 1
                    else:
                        warning_alpha -= 9 
                        if warning_alpha <= 0:
                            warning_alpha = 0
                            show_warning = False

                select_level_img.set_alpha(warning_alpha)
                warning_rect = select_level_img.get_rect(center=(width//2, height//2))
                screen.blit(select_level_img, warning_rect)

        if show_story_screen:
            screen.fill(BLACK)
            
            if text_alpha < 255:
                text_alpha += fade_speed 
            
            rendered_text = font_big.render(story_text, True, WHITE)
            rendered_text.set_alpha(text_alpha)
            text_rect = rendered_text.get_rect(center=(width//2, height//2))
            screen.blit(rendered_text, text_rect)
            
            if text_alpha >= 255:
                story_display_timer += 1
            
            if story_display_timer >= story_max_duration:
                show_story_screen = False
                show_actual_game = True
                selected_level = 1
                selected_char_index = 0 
                tutorial_active = True
                tutorial_step = 0
                active_hero_right, active_hero_left = warrior_right, warrior_left
                active_aiming_right, active_aiming_left = warrior_aiming_right, warrior_aiming_left
                
                if not is_muted:
                    pygame.mixer.music.load("data/MAIN_MUSICGAME.mp3")
                    pygame.mixer.music.play(-1)

            # Skip Button Rendering (Existing na ito, pero check mo kung tama)
            if skip_rect.collidepoint(mouse_pos):
                sk_hover = pygame.transform.scale(skip_img, (110, 50))
                screen.blit(sk_hover, sk_hover.get_rect(center=skip_rect.center))
            else:
                screen.blit(skip_img, skip_rect)

        if show_exit_popup:
            screen.blit(second_blur if (show_second_menu or show_character_screen or show_actual_game) else exit_popup, (0, 0))
            
            if show_info_panel:
                forced_scale = 0.10
                orig_w = press_info.get_width()
                orig_h = press_info.get_height()
                new_w = int(orig_w * forced_scale)
                new_h = int(orig_h * forced_scale)
                press_info_small = pygame.transform.scale(press_info, (new_w, new_h))
                screen.blit(press_info_small, press_info_small.get_rect(center=(1152 // 2, 648 // 2)))
                blink_timer += 1
                if blink_timer > 40:
                    blink_visible = not blink_visible
                    blink_timer = 0
                if blink_visible:
                    txt = font.render("Press Spacebar To Back", True, WHITE)
                    screen.blit(txt, txt.get_rect(center=(width//2, height - 70)))

            if show_exit_confirm:
                screen.blit(panel_exit, panel_rect)
                
                if askexit_rect.collidepoint(mouse_pos): 
                    ae_hover = pygame.transform.scale(askexit_img, (175, 75))
                    screen.blit(ae_hover, ae_hover.get_rect(center=askexit_rect.center))
                else:
                    screen.blit(askexit_img, askexit_rect)
                
                if askcancel_rect.collidepoint(mouse_pos): 
                    ac_hover = pygame.transform.scale(askcancel_img, (175, 75))
                    screen.blit(ac_hover, ac_hover.get_rect(center=askcancel_rect.center))
                else:
                    screen.blit(askcancel_img, askcancel_rect)

    pygame.display.update() 
    clock.tick(60)