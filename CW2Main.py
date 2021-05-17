# -*- coding: utf-8 -*-
"""
Created on Thu May 13 22:30:20 2021

@author: alext
"""

import pygame, sys, random
import numpy as np
import skfuzzy as fuzz

pygame.init()
clock = pygame.time.Clock()

#Dimension of game window
WIDTH = 1280
HEIGHT = 960
Screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CW2")

#Game Objects
ball = pygame.Rect(WIDTH/2 - 15, HEIGHT/2 - 15, 30, 30)
player = pygame.Rect(WIDTH - 20, HEIGHT/2 - 70, 10, 140)
opponent = pygame.Rect(10, HEIGHT/2 - 70, 10, 140)

#Colours
Background = (31, 31, 31)
light_gray = (200, 200, 200)

#Ball Properties
ball_speed_x = 3
ball_speed_y = 3

#Character Properties
player_speed = 0
opponent_speed = 7
current_diff = 8

#Score values
player_score = 0
opponent_score = 0
font = pygame.font.Font('freesansbold.ttf', 32)

#Timer values
ball_moving = False
score_time = True

#Fuzzy Properties
Difficulty = np.arange(1, 17, 1)
Distance = np.arange(0, 961, 1)

#Membership functions
diff_lo = fuzz.trimf(Difficulty, [1, 4, 8])
diff_md = fuzz.trimf(Difficulty, [5, 8, 12])
diff_hi = fuzz.trimf(Difficulty, [9, 12, 16])

dist_lo = fuzz.trimf(Distance, [0, 100, 100])
dist_md = fuzz.trimf(Distance, [100, 320, 320])
dist_hi = fuzz.trimf(Distance, [320, 640, 960])


#PONG CODE


def ball_properties():
    global  ball_speed_x, ball_speed_y, player_score, opponent_score, score_time
    
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    
    #Top and bottom boundary check    
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
    
    #Scoring conditions
    if ball.left <= 0:
        score_time = pygame.time.get_ticks()
        player_score += 1
        
    if  ball.right >= WIDTH:
        score_time = pygame.time.get_ticks()
        opponent_score += 1
    
    #Increases balls speed every hit        
    if ball.colliderect(player) or ball.colliderect(opponent):
        ball_speed_x *= -1.2
    
    #Ball collision physics
    if ball.colliderect(player) and ball_speed_x > 0:
        if abs(ball.right - player.left) < 10:
            ball_speed_x *= 1.2
        elif abs(ball.bottom - player.top) < 10 or abs(ball.top - player.bottom) < 10:
            ball_speed_y *= -1.2
            
    if ball.colliderect(opponent):
        if abs(ball.left - opponent.right) < 10 or abs(ball.right - player.left) < 10:
            ball_speed_x *= 1.2
        else:
            ball_speed_y *= 1.2
            
    
def player_properties():
    
    player.y += player_speed

    #Boundary check
    if player.top <= 0:
        player.top = 0
    if player.bottom >= HEIGHT:
        player.bottom = HEIGHT

        
def difficulty_set():
    global current_diff
    
    if(player_score == opponent_score) or ((player_score - 1) == opponent_score) or ((opponent_score - 1) == player_score): #Score range of 0 to 1
        current_diff = 8
        
    if((player_score - 2) == opponent_score) or ((player_score - 3) == opponent_score): #Score range of 2 to 3 in player favour
        current_diff = 10
        
    if((opponent_score - 2) == player_score) or ((opponent_score - 3) == player_score): #Score range of 2 to 3 in opponent favour
        current_diff = 6
        
    if((player_score - 4) == opponent_score) or ((player_score - 5) == opponent_score): #Score range of 4 to 5 in player favour
        current_diff = 12
        
    if((opponent_score - 4) == player_score) or ((opponent_score - 5) == player_score): #Score range of 4 to 5 in opponent favour
        current_diff = 4
        
    if((player_score - 6) == opponent_score) or ((player_score - 7) == opponent_score): #Score range of 6 to 7 in player favour
        current_diff = 14
        
    if((opponent_score - 6) == player_score) or ((opponent_score - 7) == player_score): #Score range of 6 to 7 in opponent favour
        current_diff = 2


def opponent_difficulty_set():
        
    opponent_pos = abs(ball.y - opponent.y) #Position of opponenet relative to the ball
    
    #Activation of membership functions
    diff_level_lo = fuzz.interp_membership(Difficulty, diff_lo, current_diff)
    diff_level_md = fuzz.interp_membership(Difficulty, diff_md, current_diff)
    diff_level_hi = fuzz.interp_membership(Difficulty, diff_hi, current_diff)
    
    dist_level_lo = fuzz.interp_membership(Distance, dist_lo, opponent_pos)
    dist_level_md = fuzz.interp_membership(Distance, dist_md, opponent_pos)
    dist_level_hi = fuzz.interp_membership(Distance, dist_hi, opponent_pos)
    
    #SLOWEST DIFFICULTY
    if (diff_level_lo <= 0.6) and (diff_level_md == 0) and (diff_level_hi == 0):
        print("slowest")
        if (dist_level_lo != 0) and (dist_level_md == 0) and (dist_level_hi == 0): #close
            print("slowest close")
            if opponent.top < ball.y:
                opponent.y += (opponent_speed * 0.3)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed * 0.3)
        if (dist_level_lo == 0) and (dist_level_md != 0) and (dist_level_hi == 0): #midrange
            print("slowest mid")
            if opponent.top < ball.y:
                opponent.y += (opponent_speed * 0.4)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed * 0.4)
        if (dist_level_lo == 0) and (dist_level_md == 0) and (dist_level_hi != 0): #further away
            print("slowest far")
            if opponent.top < ball.y:
                opponent.y += (opponent_speed * 0.5)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed * 0.5)
        else: #failsafe condition
            if opponent.top < ball.y:
                opponent.y += (opponent_speed * 0.4)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed * 0.4) 
    
    #SLOWER DIFFICULTY
    if (diff_level_lo >= 0.6) and (diff_level_md == 0) and (diff_level_hi == 0):
        print("slower")
        if (dist_level_lo != 0) and (dist_level_md == 0) and (dist_level_hi == 0): #close
            print("slower close")
            if opponent.top < ball.y:
                opponent.y += (opponent_speed *0.5)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed *0.5)
        if (dist_level_lo == 0) and (dist_level_md != 0) and (dist_level_hi == 0): #midrange
            print("slower mid")
            if opponent.top < ball.y:
                opponent.y += (opponent_speed *0.6)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed *0.6)
        if (dist_level_lo == 0) and (dist_level_md == 0) and (dist_level_hi != 0): #further away
            print("slower far")
            if opponent.top < ball.y:
                opponent.y += (opponent_speed *0.7)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed *0.7)
        else: #failsafe condition
            if opponent.top < ball.y:
                opponent.y += (opponent_speed *0.6)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed *0.6)
    
    
    #SLOW DIFFICULTY
    if (diff_level_md != 0) and (diff_level_lo != 0) and (diff_level_hi == 0):
        print("slow")
        if (dist_level_lo != 0) and (dist_level_md == 0) and (dist_level_hi == 0): #close
            print("slow close")
            if opponent.top < ball.y:
                opponent.y += (opponent_speed *0.7)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed *0.7)
        if (dist_level_lo == 0) and (dist_level_md != 0) and (dist_level_hi == 0): #midrange
            print("slow mid")
            if opponent.top < ball.y:
                opponent.y += (opponent_speed *0.8)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed *0.8)
        if (dist_level_lo == 0) and (dist_level_md == 0) and (dist_level_hi != 0): #further away
            print("slow far")
            if opponent.top < ball.y:
                opponent.y += (opponent_speed *0.9)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed *0.9)
        else: #failsafe condition
            if opponent.top < ball.y:
                opponent.y += (opponent_speed *0.8)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed *0.8)
    
    
    #DEFAULT DIFFICULTY
    if (diff_level_md != 0) and (diff_level_lo == 0) and (diff_level_hi == 0):
        print("default")
        if (dist_level_lo != 0) and (dist_level_md == 0) and (dist_level_hi == 0): #close
            print("default close")
            if opponent.top < ball.y:
                opponent.y += (opponent_speed * 0.9)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed * 0.9)
        if (dist_level_lo == 0) and (dist_level_md != 0) and (dist_level_hi == 0): #midrange
            print("default mid")
            if opponent.top < ball.y:
                opponent.y += opponent_speed
            if opponent.bottom > ball.y:
                opponent.y -= opponent_speed
        if (dist_level_lo == 0) and (dist_level_md == 0) and (dist_level_hi != 0): #further away
            print("default far")
            if opponent.top < ball.y:
                opponent.y += (opponent_speed * 1.1)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed * 1.1)
        else: #failsafe condition
            if opponent.top < ball.y:
                opponent.y += opponent_speed
            if opponent.bottom > ball.y:
                opponent.y -= opponent_speed
    
            
    #FAST DIFFICULTY
    if (diff_level_md != 0) and (diff_level_lo == 0) and (diff_level_hi != 0):
        print("fast")
        if (dist_level_lo != 0) and (dist_level_md == 0) and (dist_level_hi == 0): #close
            print("fast close")
            if opponent.top < ball.y:
                opponent.y += (opponent_speed *1.1)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed *1.1)
        if (dist_level_lo == 0) and (dist_level_md != 0) and (dist_level_hi == 0): #mid range
            print("fast mid")
            if opponent.top < ball.y:
                opponent.y += (opponent_speed *1.2)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed *1.2)
        if (dist_level_lo == 0) and (dist_level_md == 0) and (dist_level_hi != 0): #further away
            print("fast far")
            if opponent.top < ball.y:
                opponent.y += (opponent_speed *1.3)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed *1.3)
        else: #failsafe condition
            if opponent.top < ball.y:
                opponent.y += (opponent_speed *1.2)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed *1.2)
        
    #FASTER DIFFICULTY
    if (diff_level_hi > 0.6) and (diff_level_lo == 0) and (diff_level_md == 0):
        print("faster")
        if (dist_level_lo != 0) and (dist_level_md == 0) and (dist_level_hi == 0): #close
            print("faster close")
            if opponent.top < ball.y:
                opponent.y += (opponent_speed *1.3)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed *1.3)
        if (dist_level_lo == 0) and (dist_level_md != 0) and (dist_level_hi == 0): #mid range
            print("faster mid")
            if opponent.top < ball.y:
                opponent.y += (opponent_speed *1.4)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed *1.4)
        if (dist_level_lo == 0) and (dist_level_md == 0) and (dist_level_hi != 0): #further away
            print("faster far")
            if opponent.top < ball.y:
                opponent.y += (opponent_speed *1.5)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed *1.5)
        else: #failsafe condition
            if opponent.top < ball.y:
                opponent.y += (opponent_speed *1.4)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed *1.4)
            
    #FASTEST DIFFICULTY
    if (diff_level_lo == 0) and (diff_level_md == 0) and (diff_level_hi <= 0.6):
        print("fastest")
        if (dist_level_lo != 0) and (dist_level_md == 0) and (dist_level_hi == 0): #close
            print("fastest close")
            if opponent.top < ball.y:
                opponent.y += (opponent_speed *1.5)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed *1.5)
        if (dist_level_lo == 0) and (dist_level_md != 0) and (dist_level_hi == 0): #mid range
            print("fastest mid")
            if opponent.top < ball.y:
                opponent.y += (opponent_speed *1.6)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed *1.6)
        if (dist_level_lo == 0) and (dist_level_md == 0) and (dist_level_hi != 0): #further away
            print("fastest far")
            if opponent.top < ball.y:
                opponent.y += (opponent_speed *1.7)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed *1.7)
        else: #failsafe condition
            if opponent.top < ball.y:
                opponent.y += (opponent_speed *1.6)
            if opponent.bottom > ball.y:
                opponent.y -= (opponent_speed *1.6)
 

def opponent_ai():
    global player_score, opponent_score   
    
    difficulty_set()   
    opponent_difficulty_set()
    
    #Boundary check
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= HEIGHT:
        opponent.bottom = HEIGHT

        
def ball_start():
    global ball_speed_x, ball_speed_y, ball_moving, score_time

    ball.center = (WIDTH/2, HEIGHT/2)
    current_time = pygame.time.get_ticks()
    
    #Start countdown sequence
    if current_time - score_time < 700:
        no_3 = font.render("3",False,light_gray)
        Screen.blit(no_3,(WIDTH/2 - 10, HEIGHT/2 + 20))
    if 700 < current_time - score_time < 1400:
        no_2 = font.render("2",False,light_gray)
        Screen.blit(no_2,(WIDTH/2 - 10, HEIGHT/2 + 20))
    if 1400 < current_time - score_time < 2100:
        no_1 = font.render("1",False,light_gray)
        Screen.blit(no_1,(WIDTH/2 - 10, HEIGHT/2 + 20))
    
    #Check if the start sequence is currently executing
    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0,0
    else:
        ball_speed_y = 3 * random.choice((1,-1))
        ball_speed_x = 3 * random.choice((1,-1))
        score_time = None
    
def reset():
    global player_score, opponent_score, score_time
    
    player_score = 0
    opponent_score = 0
    score_time = pygame.time.get_ticks()

def main():
    global player_speed
    
    run = True
    while run:
        for event in pygame.event.get():
             if event.type == pygame.QUIT: #exit application
                 run = False
             if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_UP: #move player up
                     player_speed = -7
                 if event.key == pygame.K_DOWN: #move player down
                     player_speed = 7 
                 if event.key == pygame.K_SPACE: #reset game
                     reset()
             if event.type == pygame.KEYUP:
                 if event.key == pygame.K_UP: #stops players upward movement when releasing key
                     player_speed = 0
                 if event.key == pygame.K_DOWN: #stops players downward movement when releasing key
                     player_speed = 0
                     
        
        ball_properties()
        player_properties()
        opponent_ai()
        
        #Draw Objects
        Screen.fill(Background)
        pygame.draw.rect(Screen, light_gray, player)
        pygame.draw.rect(Screen, light_gray, opponent)
        pygame.draw.ellipse(Screen, light_gray, ball)
        pygame.draw.aaline(Screen, light_gray, (WIDTH/2, 0), (WIDTH/2, HEIGHT))
        
        if score_time: #Initiate start sequence
            ball_start()
        
        #Text display
        player_text = font.render("Player: " + f'{player_score}',False,light_gray)
        Screen.blit(player_text,(900,10))

        opponent_text = font.render("Opponent: " +f'{opponent_score}',False,light_gray)
        Screen.blit(opponent_text,(220,10))  
              
        pygame.display.flip()
        clock.tick(60) #control speed of loop
            
    pygame.quit()
    sys.exit()
    
main()