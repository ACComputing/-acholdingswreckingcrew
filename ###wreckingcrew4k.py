import pygame
import sys
import random

# --- CONSTANTS ---
TILE_SIZE = 48  # Scale 16x16 sprites by 3x
SCREEN_WIDTH = 20 * TILE_SIZE  # 960
SCREEN_HEIGHT = 15 * TILE_SIZE # 720
FPS = 60

# --- FAMICOM PALETTE ---
C_BG = (0, 0, 0)
C_TEXT = (255, 255, 255)

# Pixel Art Colors
COLORS = {
    '.': (0, 0, 0, 0),       # Transparent
    'R': (248, 56, 0),       # Classic NES Red
    'Y': (248, 184, 0),      # Classic NES Yellow
    'S': (248, 216, 112),    # Skin Tone
    'B': (0, 0, 0, 255),     # Black / Outlines
    'W': (255, 255, 255),    # White
    'C': (0, 184, 248),      # Ladder Cyan
    'c': (0, 136, 136),      # Ladder Shadow
    'G': (188, 188, 188),    # Wall Base Gray
    'D': (116, 116, 116),    # Wall Dark Gray
    'L': (252, 252, 252),    # Wall Light Gray
    'r': (188, 56, 0),       # Brick Red
    'h': (252, 152, 56),     # Hammer handle
    'm': (252, 252, 252),    # Hammer metal
    'M': (116, 116, 116),    # Hammer shadow
}

# --- 16x16 PROCEDURAL SPRITES ---
ASCII_ART = {
    'mario_idle': [
        "......RRRRR.....",
        ".....RRRRRRRR...",
        ".....SSSSSBB....",
        "....SWSBSSBBB...",
        "....SSSSSSBBB...",
        "......BBBBBB....",
        ".....RYYYYR.....",
        "....RRYYYYRR....",
        "...RRRYYYYRRR...",
        "...RRRYRYYRRR...",
        "....R.RRRR.R....",
        "......RRRR......",
        ".....RR..RR.....",
        "....BB....BB....",
        "...BBB....BBB...",
        "................"
    ],
    'mario_walk': [
        "......RRRRR.....",
        ".....RRRRRRRR...",
        ".....SSSSSBB....",
        "....SWSBSSBBB...",
        "....SSSSSSBBB...",
        "......BBBBBB....",
        ".....RYYYYR.....",
        "....RRYYYYRR....",
        "...RRRYYYYRRR...",
        "...RRRYRYYRRR...",
        "....R.RRRR.R....",
        "......RRRR......",
        "......RR.RR.....",
        ".......BB.BB....",
        "......BBB.BBB...",
        "................"
    ],
    'enemy_idle': [
        ".....RRRRRR.....",
        "...RRRRRRRRRR...",
        "..RRRRRRRRRRRR..",
        "..RRWWWRRRWWWR..",
        "..RRWBWRRRWBWR..",
        "..RRWWWRRRWWWR..",
        "..RRRRRRRRRRRR..",
        "...RRRRRRRRRR...",
        "....RRRRRRRR....",
        "...RRRRRRRRRR...",
        "..RRR.RRRR.RRR..",
        "..RR..RRRR..RR..",
        "......RRRR......",
        ".....RR..RR.....",
        "....BB....BB....",
        "................"
    ],
    'enemy_walk': [
        ".....RRRRRR.....",
        "...RRRRRRRRRR...",
        "..RRRRRRRRRRRR..",
        "..RRWWWRRRWWWR..",
        "..RRWBWRRRWBWR..",
        "..RRWWWRRRWWWR..",
        "..RRRRRRRRRRRR..",
        "...RRRRRRRRRR...",
        "....RRRRRRRR....",
        "...RRRRRRRRRR...",
        "..RRR.RRRR.RRR..",
        "..RR..RRRR..RR..",
        "......RRRR......",
        ".......RRRR.....",
        "........BBBB....",
        "................"
    ],
    'wall': [
        "LLLLLLLLLLLLLLLL",
        "LGGGGGGGGGGGGGGG",
        "LGGGGGGGGGGGGGGG",
        "LGGDDDDDDDDDDGGG",
        "LGGDDDDDDDDDDGGG",
        "LGGDGGGGGGDGGGGG",
        "LGGDGGGGGGDGGGGG",
        "LGGDDDDDDDDDDGGG",
        "LGGDDDDDDDDDDGGG",
        "LGGDGGGGGGDGGGGG",
        "LGGDGGGGGGDGGGGG",
        "LGGDDDDDDDDDDGGG",
        "LGGDDDDDDDDDDGGG",
        "LGGGGGGGGGGGGGGG",
        "LGGGGGGGGGGGGGGG",
        "DDDDDDDDDDDDDDDD"
    ],
    'floor': [
        "WWWWWWWWWWWWWWWW",
        "WrrrrrrrBWrrrrrr",
        "WrrrrrrrBWrrrrrr",
        "BBBBBBBBBBBBBBBB",
        "WWWWWWWWWWWWWWWW",
        "rrrBWrrrrrrrBWrr",
        "rrrBWrrrrrrrBWrr",
        "BBBBBBBBBBBBBBBB",
        "WWWWWWWWWWWWWWWW",
        "WrrrrrrrBWrrrrrr",
        "WrrrrrrrBWrrrrrr",
        "BBBBBBBBBBBBBBBB",
        "WWWWWWWWWWWWWWWW",
        "rrrBWrrrrrrrBWrr",
        "rrrBWrrrrrrrBWrr",
        "BBBBBBBBBBBBBBBB"
    ],
    'ladder': [
        "...CC......CC...",
        "...cc......cc...",
        "...CC......CC...",
        "...CCCCCCCCCC...",
        "...cccccccccc...",
        "...CC......CC...",
        "...cc......cc...",
        "...CC......CC...",
        "...CCCCCCCCCC...",
        "...cccccccccc...",
        "...CC......CC...",
        "...cc......cc...",
        "...CC......CC...",
        "...CCCCCCCCCC...",
        "...cccccccccc...",
        "...CC......CC..."
    ],
    'hammer': [
        "................",
        ".......mm.......",
        "......mmmm......",
        ".....mmmmmm.....",
        ".....mmmmmm.....",
        ".....mmmmmm.....",
        "......MMMM......",
        ".......hh.......",
        ".......hh.......",
        ".......hh.......",
        ".......hh.......",
        ".......hh.......",
        ".......hh.......",
        ".......hh.......",
        ".......hh.......",
        "................"
    ]
}

SPRITES = {}

def load_sprites():
    for name, lines in ASCII_ART.items():
        surf = pygame.Surface((16, 16), pygame.SRCALPHA)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                color = COLORS.get(char, (0, 0, 0, 0))
                surf.set_at((x, y), color)
        # Scale nearest-neighbor for crisp Famicom pixels
        SPRITES[name] = pygame.transform.scale(surf, (TILE_SIZE, TILE_SIZE))

# Game States
STATE_MENU = 0
STATE_PLAYING = 1
STATE_GAME_OVER = 2
STATE_VICTORY = 3

# --- LEVEL DESIGN ---
RAW_LEVEL = [
    "XXXXXXXXXXXXXXXXXXXX",
    "X                  X",
    "X        W         X",
    "XXXXLXXXXXWXXXXLXXXX",
    "X   L  E       L   X",
    "X W L  W    W  L W X",
    "XXXXLXXXXXLXXXXLXXXX",
    "X   L     L  E L   X",
    "X   L  W  L  W L   X",
    "XXXXLXXXXXLXXXXLXXXX",
    "X E L     L    L E X",
    "X   L  W  L  W L   X",
    "XXXXLXXXXXLXXXXLXXXX",
    "X P    W       W   X",
    "XXXXXXXXXXXXXXXXXXXX",
]

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Wrecking Crew - Famicom Edition")
        self.clock = pygame.time.Clock()
        
        # Load sprites to avoid external files
        load_sprites()
        
        self.font_large = pygame.font.SysFont('courier', 48, bold=True)
        self.font_small = pygame.font.SysFont('courier', 24, bold=True)
        
        self.state = STATE_MENU
        self.reset_game()

    def reset_game(self):
        self.grid = [list(row) for row in RAW_LEVEL]
        self.ladder_min_row_by_col = {}
        self.player = None
        self.enemies = []
        
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                char = self.grid[row][col]
                if char == 'P':
                    self.player = Player(col * TILE_SIZE, row * TILE_SIZE)
                    self.grid[row][col] = ' '
                elif char == 'E':
                    self.enemies.append(Enemy(col * TILE_SIZE, row * TILE_SIZE))
                    self.grid[row][col] = ' '
                    
        self.score = 0
        self.total_walls = sum(row.count('W') for row in self.grid)
        
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] == 'L':
                    prev = self.ladder_min_row_by_col.get(col)
                    self.ladder_min_row_by_col[col] = row if prev is None else min(prev, row)

    def get_solid_rects(self):
        rects = []
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                if self.grid[row][col] in ['X', 'W']:
                    rects.append(pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        return rects

    def is_ladder(self, rect):
        center_x = rect.centerx
        center_y = rect.centery
        col = center_x // TILE_SIZE
        row = center_y // TILE_SIZE
        if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]):
            min_row = self.ladder_min_row_by_col.get(col)
            if min_row is None:
                return False
            return row >= min_row
        return False

    def break_wall(self, col, row):
        if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]):
            if self.grid[row][col] == 'W':
                self.grid[row][col] = ' '
                self.score += 800
                self.total_walls -= 1
                if self.total_walls <= 0:
                    self.state = STATE_VICTORY

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if self.state == STATE_MENU:
                    if event.key == pygame.K_SPACE:
                        self.state = STATE_PLAYING
                
                elif self.state == STATE_PLAYING:
                    if event.key == pygame.K_SPACE:
                        if self.player.swing_cooldown <= 0 and self.player.vy == 0:
                            self.player.swing_cooldown = 20
                            target_col = (self.player.rect.centerx // TILE_SIZE) + self.player.facing
                            target_row = self.player.rect.centery // TILE_SIZE
                            self.break_wall(target_col, target_row)
                            
                elif self.state in [STATE_GAME_OVER, STATE_VICTORY]:
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        self.state = STATE_PLAYING

    def update(self):
        if self.state != STATE_PLAYING:
            return

        solid_rects = self.get_solid_rects()
        self.player.update(self, solid_rects)
        
        for enemy in self.enemies:
            enemy.update(solid_rects)
            
            # Shrunken collision box for fairness
            hitbox = self.player.rect.inflate(-10, -10)
            if hitbox.colliderect(enemy.rect):
                self.state = STATE_GAME_OVER

    def draw(self):
        self.screen.fill(C_BG)

        if self.state == STATE_MENU:
            self.draw_text("WRECKING CREW", self.font_large, C_TEXT, SCREEN_WIDTH//2, SCREEN_HEIGHT//3)
            self.draw_text("PRESS SPACE TO START", self.font_small, C_TEXT, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
            
        elif self.state == STATE_PLAYING:
            self.draw_level()
            self.player.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)
            
            self.draw_text(f"SCORE-{self.score:06d}", self.font_small, C_TEXT, 120, 20)
            self.draw_text(f"REST-{self.total_walls:02d}", self.font_small, C_TEXT, SCREEN_WIDTH - 100, 20)

        elif self.state == STATE_GAME_OVER:
            self.draw_level()
            self.draw_text("GAME OVER", self.font_large, COLORS['R'], SCREEN_WIDTH//2, SCREEN_HEIGHT//3)
            self.draw_text("PRESS SPACE TO RESTART", self.font_small, C_TEXT, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

        elif self.state == STATE_VICTORY:
            self.draw_level()
            self.draw_text("STAGE CLEAR", self.font_large, COLORS['Y'], SCREEN_WIDTH//2, SCREEN_HEIGHT//3)
            self.draw_text("PRESS SPACE FOR NEXT", self.font_small, C_TEXT, SCREEN_WIDTH//2, SCREEN_HEIGHT//2)

        pygame.display.flip()

    def draw_level(self):
        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                char = self.grid[row][col]
                x = col * TILE_SIZE
                y = row * TILE_SIZE
                
                if char == 'X':
                    self.screen.blit(SPRITES['floor'], (x, y))
                elif char == 'W':
                    self.screen.blit(SPRITES['wall'], (x, y))
                elif char == 'L':
                    min_row = self.ladder_min_row_by_col.get(col)
                    if min_row is None or row != min_row:
                        continue
                    # Tile ladder down
                    for ly in range(row, len(self.grid)):
                        self.screen.blit(SPRITES['ladder'], (x, ly * TILE_SIZE))

    def draw_text(self, text, font, color, x, y):
        # antialias=False for retro crisp pixel text
        surface = font.render(text, False, color)
        rect = surface.get_rect(center=(x, y))
        self.screen.blit(surface, rect)


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x + 4, y + 4, TILE_SIZE - 8, TILE_SIZE - 8)
        self.vx = 0
        self.vy = 0
        
        # Exact Famicom speeds - strict, rigid, non-floaty physics
        self.speed = 3           
        self.climb_speed = 2     
        self.gravity = 1.2       
        self.max_fall = 8
        
        self.facing = 1  
        self.climbing = False
        self.swing_cooldown = 0
        self.frame = 0

    def update(self, game, solid_rects):
        keys = pygame.key.get_pressed()
        
        if self.swing_cooldown > 0:
            self.swing_cooldown -= 1

        on_ladder = game.is_ladder(self.rect)
        up_pressed = keys[pygame.K_UP]
        down_pressed = keys[pygame.K_DOWN]
        left_pressed = keys[pygame.K_LEFT]
        right_pressed = keys[pygame.K_RIGHT]
        
        leaving_ladder = on_ladder and not up_pressed and not down_pressed and (left_pressed or right_pressed)

        # X-Axis Movement (Famicom lock: no moving mid-air or while swinging)
        if (not self.climbing or leaving_ladder) and self.swing_cooldown == 0:
            if self.vy == 0: 
                if left_pressed:
                    self.vx = -self.speed
                    self.facing = -1
                elif right_pressed:
                    self.vx = self.speed
                    self.facing = 1
                else:
                    self.vx = 0
        else:
            self.vx = 0 

        self.rect.x += self.vx
        self.handle_collisions_x(solid_rects)

        # Y-Axis Movement
        if on_ladder and self.swing_cooldown == 0:
            ladder_col = self.rect.centerx // TILE_SIZE

            if up_pressed:
                self.rect.centerx = (ladder_col * TILE_SIZE) + (TILE_SIZE // 2)
                self.climbing = True
                self.vy = -self.climb_speed
            elif down_pressed:
                self.rect.centerx = (ladder_col * TILE_SIZE) + (TILE_SIZE // 2)
                self.climbing = True
                self.vy = self.climb_speed
            else:
                if leaving_ladder:
                    self.climbing = False
                    self.vy = 0
                elif self.climbing:
                    self.vy = 0
        else:
            self.climbing = False

        if not self.climbing:
            self.vy = min(self.vy + self.gravity, self.max_fall)

        self.rect.y += self.vy
        self.handle_collisions_y(solid_rects)

        # Animation Frames
        if self.vx != 0 or (self.climbing and self.vy != 0):
            self.frame += 0.15
        else:
            self.frame = 0

    def handle_collisions_x(self, solid_rects):
        for solid in solid_rects:
            if self.rect.colliderect(solid):
                if self.vx > 0:
                    self.rect.right = solid.left
                elif self.vx < 0:
                    self.rect.left = solid.right

    def handle_collisions_y(self, solid_rects):
        for solid in solid_rects:
            if self.rect.colliderect(solid):
                if self.vy > 0:
                    self.rect.bottom = solid.top
                    self.vy = 0
                elif self.vy < 0:
                    self.rect.top = solid.bottom
                    self.vy = 0

    def draw(self, screen):
        img = SPRITES['mario_walk'] if int(self.frame) % 2 == 1 else SPRITES['mario_idle']
        if self.facing == -1:
            img = pygame.transform.flip(img, True, False)
            
        screen.blit(img, (self.rect.centerx - TILE_SIZE//2, self.rect.centery - TILE_SIZE//2))

        # Famicom-style hammer swing visualization
        if self.swing_cooldown > 0:
            ham = SPRITES['hammer']
            
            if self.swing_cooldown > 13:
                # Hammer lifted up
                ham = pygame.transform.rotate(ham, -45 if self.facing == 1 else 45)
                offset_x = 0
                offset_y = -30
            elif self.swing_cooldown > 6:
                # Hammer swinging down
                ham = pygame.transform.rotate(ham, -90 if self.facing == 1 else 90)
                offset_x = 30 if self.facing == 1 else -30
                offset_y = -10
            else:
                # Hammer striking block
                ham = pygame.transform.rotate(ham, -120 if self.facing == 1 else 120)
                offset_x = 35 if self.facing == 1 else -35
                offset_y = 10
                
            rect = ham.get_rect(center=(self.rect.centerx + offset_x, self.rect.centery + offset_y))
            screen.blit(ham, rect)


class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x + 4, y + 4, TILE_SIZE - 8, TILE_SIZE - 8)
        self.vx = 2
        self.vy = 0
        self.gravity = 1.2
        self.max_fall = 8
        self.direction = random.choice([-1, 1])
        self.frame = 0

    def update(self, solid_rects):
        self.vx = 2 * self.direction
        self.rect.x += self.vx
        
        for solid in solid_rects:
            if self.rect.colliderect(solid):
                if self.vx > 0:
                    self.rect.right = solid.left
                    self.direction = -1
                elif self.vx < 0:
                    self.rect.left = solid.right
                    self.direction = 1

        self.vy = min(self.vy + self.gravity, self.max_fall)
        self.rect.y += self.vy
        for solid in solid_rects:
            if self.rect.colliderect(solid):
                if self.vy > 0:
                    self.rect.bottom = solid.top
                    self.vy = 0
                elif self.vy < 0:
                    self.rect.top = solid.bottom
                    self.vy = 0

        self.frame += 0.1

    def draw(self, screen):
        img = SPRITES['enemy_walk'] if int(self.frame) % 2 == 1 else SPRITES['enemy_idle']
        if self.direction == -1:
            img = pygame.transform.flip(img, True, False)
            
        screen.blit(img, (self.rect.centerx - TILE_SIZE//2, self.rect.centery - TILE_SIZE//2))


if __name__ == "__main__":
    game = Game()
    game.run()
