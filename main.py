# This is 'test' Branch 
import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)
    def player_input(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.rect.bottom >= 300 :
            self.gravity = -20
            self.jump_sound.play()
    def apply_gravity(self):          
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:   
            self.rect.bottom = 300
    def animation_state(self):
        self.movement = 0.1
        if int(pygame.time.get_ticks()/500)%25 == 0:
            self.player_index += self.movement
        if self.rect.bottom < 300:self.player_jump
        else:
            self.player_index += self.movement
            if self.player_index >= len(self.player_walk) : self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]
    def levels_walk(self):
        if score%25 == 0:
            self.movement += 0.1
    def update(self):                                                     
        self.player_input()
        self.apply_gravity()
        self.animation_state()
        self.levels_walk()

class Obstacles(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == 'fly':
            fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300
        
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))
    def animation_state(self):
        self.animation = 0.1
        if int(pygame.time.get_ticks()/500)%25 == 0:
            self.animation += 0.1
        self.animation_index += self.animation
        if self.animation_index >= len(self.frames) : self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    def update(self):
        self.animation_state() 
        self.rect.x -= 5
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks()/500) - start_score
    score_surf = font.render(f'Score: {current_time}', False, (64,64,64))
    score_react = score_surf.get_rect(center = (400, 50))
    screen.blit(score_surf, score_react)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            movement = 2
            if int(pygame.time.get_ticks()/500)%25 == 0:
                movement += 2
            obstacle_rect.x -= movement
            if obstacle_rect.bottom == 300: screen.blit(snail_surf, obstacle_rect)
            else:screen.blit(fly_surf, obstacle_rect)

            

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else: return []

def collisions(player, obstacles):
    if obstacles:
        for obstacles_rect in obstacles:
            if player.colliderect(obstacles_rect): return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else: return True         
    
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption('The Ultimate Runner')
    clock = pygame.time.Clock()
    font = pygame.font.Font('font/Pixeltype.ttf', 50)
    bg_music = pygame.mixer.Sound('audio/music.wav')
    bg_music.set_volume(0.1)
    bg_music.play(loops= -1)

    sky_surf = pygame.image.load('graphics/Sky.png').convert()
    ground_surf = pygame.image.load('graphics/ground.png').convert()
    ground_surf_rect = ground_surf.get_rect(midtop = (400, 300))
    # Groups
    player = pygame.sprite.GroupSingle()
    player.add(Player())

    obstacle_group = pygame.sprite.Group()

    start_score = 0
    score = 0
    game_active = False


    # Snail
    snail_frame1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
    snail_frame2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
    snail_frames = [snail_frame1, snail_frame2]
    snail_index = 0
    snail_surf =snail_frames[snail_index]

    # Flies
    fly_frame1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
    fly_frame2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
    fly_frames = [fly_frame1, fly_frame2]
    fly_index = 0
    fly_surf = fly_frames[fly_index]

    obstacle_react_list = []



    # Intro Screen
    player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
    player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
    player_stand_react = player_stand.get_rect(center = (400, 200))
    pygame.display.set_icon(player_stand)


    game_name = font.render('The Ultimate Runner', False, (111, 196, 169))
    game_name_react = game_name.get_rect(center = (400, 90))

    instruction_ = font.render('To start the game press \"Space"', False, (111, 196, 169))
    instruction_react = instruction_.get_rect(center = (400, 340))

    # Game Over
    game_over = font.render('Game Over!', False, (111, 196, 169))
    game_over_react = game_over.get_rect(center = (400, 90))


    # Timer
    timer = 2000
    if int(score/500)%25 == 0:
        timer -= 50
    if timer<= 800:
        timer += 50
    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer, timer)

    snail_animation_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(snail_animation_timer, 500)

    fly_animation_timer = pygame.USEREVENT + 3
    pygame.time.set_timer(fly_animation_timer, 200)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            #Restarting
            if event.type == pygame.KEYDOWN and game_active == False:
                if event.key == pygame.K_SPACE and game_active == False:
                    game_active = True
                    
                    start_score = int(pygame.time.get_ticks()/500) 
                    score = start_score 

            # Obstacles 
            if game_active:
                if event.type == obstacle_timer:      
                    obstacle_group.add(Obstacles(choice(['fly', 'snail', 'snail', 'snail'])))
        # Running Game

        if game_active:
            screen.blit((sky_surf), (0, 0))
            screen.blit((ground_surf), ground_surf_rect)
            score = display_score()
            
            
            #Player
            player.draw(screen)
            player.update()

            # Obstales
            obstacle_react_list = obstacle_movement(obstacle_react_list)
            obstacle_group.draw(screen)
            obstacle_group.update()

            
            # Collision
            game_active = collision_sprite()
            
        else : 
            screen.fill((94,129,162))  
            screen.blit(player_stand, player_stand_react)
            obstacle_react_list.clear()
            player_stand_react.midbottom = (400, 300)
            player_gravity = 0
            
            score_made = font.render(f'You created: {score} score', False, (111, 196, 169))
            score_made_react = score_made.get_rect(center = (400, 340))
            if score != 0:
                screen.blit(score_made , score_made_react)
                screen.blit(game_over, game_over_react)
            else:
                screen.blit(instruction_ , instruction_react)
                screen.blit(game_name, game_name_react)
            


        pygame.display.update()
        clock.tick(60)
