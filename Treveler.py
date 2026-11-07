import pygame
import sys
import os


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)
def start_game(chosen_level):
    pygame.init()

    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 600
    FPS = 60
    
    COLOR_TEXT = (255, 255, 255)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Medieval Coin Quest")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)

    TILE_WIDTH = 40
    TILE_HEIGHT = 40
    
    player_start_x = 0
    player_start_y = 0
    
    need_load_level = True
    camera_x = 0


    bg_image = pygame.image.load(resource_path("img/bg_image.png")).convert()
    ladder_image = pygame.image.load(resource_path("img/ladder.png")).convert_alpha()
    dirt_image = pygame.image.load(resource_path("img/dirt.png")).convert_alpha()
    player_image = pygame.image.load(resource_path("img/player_image.png")).convert_alpha()
    enemy_image = pygame.image.load(resource_path("img/enemy.png")).convert_alpha()
    coin_image = pygame.image.load(resource_path("img/coin.png")).convert_alpha()
    
    pygame.mixer.init()
    pygame.mixer.music.load(resource_path("music/ELIE ELADIS.mp3"))
    frames = [pygame.image.load(resource_path(f"coin_{i}.png")).convert_alpha() for i in range(1, 5)]
    if isinstance(chosen_level, list):
        chosen_level = chosen_level[0] if chosen_level else "Level1"

    try:
        current_level_num = int(str(chosen_level).replace("Level", "").strip())
    except (ValueError, TypeError):
        current_level_num = 1

    if current_level_num not in (1, 2, 3, 4):
        current_level_num = 1

    score = 0
    lives = 3
    game_state = "PLAY"  

    walls = []
    ladders = []  
    coins = []
    enemies = []  

    player_rect = pygame.Rect(0, 0, 40, 40)
    player_speed = 4
    enemy_speed = 2
    
    
    gravity = 0.2
    vertical_momentum = 0
    is_on_ground = False
    is_on_ladder = False
    jump_power = -10

    player_start_x = 0
    player_start_y = 0
    
    need_load_level = True

    while True:
          
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if game_state in ["WIN", "GAME_OVER", "LEVEL_UNAVAILABLE"]:
                    if event.key == pygame.K_SPACE:
                        return
            
                    
                
            

        if game_state == "PLAY":
            if need_load_level:
                walls.clear()
                ladders.clear()
                coins.clear()
                enemies.clear()
                lines = []

                if current_level_num == 1:
                    with open(resource_path("level/level1.txt"), "r") as f:
                        lines = f.readlines()
                elif current_level_num == 2:
                    with open(resource_path("level/level2.txt"), "r") as f:
                        lines = f.readlines()
                elif current_level_num == 3:
                    with open(resource_path("level/level3.txt"), "r") as f:
                        lines = f.readlines()
                elif current_level_num == 4:
                    with open(resource_path("level/level4.txt"), "r") as f:
                        lines = f.readlines()
                else:
                    game_state = "WIN"
                    need_load_level = False
                    continue
                
                camera_x = player_rect.x - SCREEN_WIDTH // 2
                
                if camera_x < 0:
                    camera_x = 0
                

                
                bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
                ladder_scaled = pygame.transform.scale(ladder_image, (TILE_WIDTH, TILE_HEIGHT))
                dirt_scaled = pygame.transform.scale(dirt_image, (TILE_WIDTH, TILE_HEIGHT))
                player_scaled = pygame.transform.scale(player_image, (40, 40))
                enemy_scaled = pygame.transform.scale(enemy_image, (40, 40))
                coin_scaled = pygame.transform.scale(coin_image, (25, 25))
                
                pygame.mixer.music.play(-1)  
                pygame.mixer.music.set_volume(0.5)
                
                
                for row_idx, line in enumerate(lines):
                    for col_idx, char in enumerate(line.strip()):
                        x = col_idx * TILE_WIDTH
                        y = row_idx * TILE_HEIGHT
                        
                        if char == "W":  
                            walls.append(pygame.Rect(x, y, TILE_WIDTH, TILE_HEIGHT))
                        elif char == "L":  
                            ladders.append(pygame.Rect(x, y, TILE_WIDTH, TILE_HEIGHT))
                        elif char == "P":
                            player_start_x = x + (TILE_WIDTH - player_rect.width) // 2
                            player_start_y = y + (TILE_HEIGHT - player_rect.height) // 2
                            player_rect.x = player_start_x
                            player_rect.y = player_start_y
                        elif char == "C":
                            coins.append(pygame.Rect(x + (TILE_WIDTH - 25) // 2, y + (TILE_HEIGHT - 25) // 2, 25, 25))
                        elif char == "E":
                            enemies.append({
                                "rect": pygame.Rect(x + (TILE_WIDTH - 40) // 2, y + (TILE_HEIGHT - 40) // 2, 40, 40),
                                "dir": 1,
                                "y_momentum": 0
                            })
                need_load_level = False

            keys = pygame.key.get_pressed()
            dx = 0
            dy = 0
            if keys[pygame.K_1] or keys[pygame.K_r]:
                current_level_num = 1
                need_load_level = True 

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx = -player_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = player_speed

            is_on_ladder = any(player_rect.colliderect(lad) for lad in ladders)

            if is_on_ladder:
                vertical_momentum = 0  
                if keys[pygame.K_UP] or keys[pygame.K_w]:
                    dy = -player_speed
                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    dy = player_speed
            else:
                if (keys[pygame.K_UP] or keys[pygame.K_w]) and is_on_ground:
                    vertical_momentum = jump_power
                    is_on_ground = False
                
                vertical_momentum += gravity
                if vertical_momentum > 10: 
                    vertical_momentum = 10
                dy = vertical_momentum

           
            player_rect.x += dx
            for wall in walls:
                if player_rect.colliderect(wall):
                    if dx > 0: player_rect.right = wall.left
                    if dx < 0: player_rect.left = wall.right

            
            is_on_ground = False
            player_rect.y += dy
            for wall in walls:
                if player_rect.colliderect(wall):
                    if dy > 0:  
                        player_rect.bottom = wall.top
                        vertical_momentum = 0
                        is_on_ground = True
                    elif dy < 0:  
                        player_rect.top = wall.bottom
                        vertical_momentum = 0

            
            for enemy in enemies:
                turn_around = False

                
                enemy["rect"].x += enemy_speed * enemy["dir"]

                
                for wall in walls:
                    if enemy["rect"].colliderect(wall):
                        if enemy["dir"] > 0:
                            enemy["rect"].right = wall.left
                        else:
                            enemy["rect"].left = wall.right
                        turn_around = True

                
                probe_x = enemy["rect"].centerx + (enemy["dir"] * (TILE_WIDTH // 2))
                probe_y = enemy["rect"].bottom + 2

                has_floor = any(wall.collidepoint(probe_x, probe_y) for wall in walls)

                
                if not has_floor and abs(enemy.get("y_momentum", 0)) < 1:
                    turn_around = True
                    enemy["rect"].x -= enemy_speed * enemy["dir"]  

                
                if turn_around:
                    enemy["dir"] *= -1

                
                enemy["y_momentum"] += gravity
                if enemy["y_momentum"] > 10:
                    enemy["y_momentum"] = 10

                enemy["rect"].y += enemy["y_momentum"]

                
                for wall in walls:
                    if enemy["rect"].colliderect(wall):
                        if enemy["y_momentum"] > 0: 
                            enemy["rect"].bottom = wall.top
                            enemy["y_momentum"] = 0
                        elif enemy["y_momentum"] < 0:  
                            enemy["rect"].top = wall.bottom
                            enemy["y_momentum"] = 0
           
            for coin in coins[:]:  
                if player_rect.colliderect(coin):
                    coins.remove(coin)
                    score += 10

            if len(coins) == 0:
                current_level_num += 1
                need_load_level = True

           
            for enemy in enemies[:]:
                if player_rect.colliderect(enemy["rect"]):
                    if vertical_momentum > 0 and player_rect.bottom <= enemy["rect"].centery + 10:
                        enemies.remove(enemy)
                        score += 50
                        vertical_momentum = jump_power * 0.7  
                    else:
                        lives -= 1
                        if lives <= 0:
                            game_state = "GAME_OVER"
                        else:
                            player_rect.x = player_start_x
                            player_rect.y = player_start_y
                            vertical_momentum = 0

        
        screen.blit(bg_image, (camera_x, 0))

        if game_state == "PLAY":
            for lad in ladders:
                screen.blit(ladder_scaled, (lad.x - camera_x, lad.y))

            for wall in walls:
                screen.blit(dirt_scaled, (wall.x - camera_x, wall.y))

            for coin in coins:
                frame_index = (pygame.time.get_ticks() // 200) % len(frames)
                coin_scaled = pygame.transform.scale(frames[frame_index], (25, 25))
                screen.blit(coin_scaled, (coin.x - camera_x, coin.y))
                

            for enemy in enemies:
               
               screen.blit(enemy_scaled, (enemy["rect"].x - camera_x, enemy["rect"].y))

            
            COLOR_TEXT = (0, 0, 0)
            screen.blit(player_scaled, (player_rect.x, player_rect.y))

            ui_text = f"Level: {current_level_num}   Score: {score}   Live: {lives}"
            text_surface = font.render(ui_text, True, COLOR_TEXT)
            screen.blit(text_surface, (20, 20))

        elif game_state == "WIN":
            win_text = "Congratulations! You completed all levels!"
            text_surface = font.render(win_text, True, COLOR_TEXT)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT // 2 - text_surface.get_height() // 2))
        elif game_state == "GAME_OVER":
            game_over_text = "Game Over! Press SPACE to return to the launcher."
            text_surface = font.render(game_over_text, True, COLOR_TEXT)
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT // 2 - text_surface.get_height() // 2))

        pygame.display.flip()
        clock.tick(FPS)
        
        
            

