from pygame import * 
from random import * 

init() 

window_size = (800, 600)

window = display.set_mode(window_size) 
clock = time.Clock() 

display.set_caption("flappy Bird") 

player_rect = Rect(150, 250, 100, 100) 

def generate_tubes(count, 
                   tube_width = 140, 
                   gap = 280,
                   min_height = 50, 
                   max_height = 440, 
                   distance = 650
                   ): 
    tubes = [] 
    start_x = window_size[0] 
    for i in range(count): 
        height = randint(min_height, max_height) 
        top_tube = Rect(start_x, 0, tube_width, height) 
        bottom_tube = Rect(
            start_x, 
            height + gap, 
            tube_width, 
            window_size[1] - (height + gap) 
        )
        tubes.extend([top_tube, bottom_tube]) 
        start_x += distance 
    return tubes 

tubes = generate_tubes(150) 

lose = False
score = 0 
my_font = font.Font(None, 100) 
y_vel = 2 


while 1: 
    for e in event.get(): 
        if e.type == QUIT: 
            quit() 

    keys = key.get_pressed() 
    if keys[K_UP] and not lose:
        player_rect.y -= 15 
    if keys[K_DOWN] and not lose: 
        player_rect.y += 15 
    if keys[K_r] and lose:
        lose = False 
        score = 0 
        tubes = generate_tubes(150) 
        player_rect.y = window_size[1] // 2 - 100 
        y_vel = 2              

    

    if lose: 
        player_rect.y += y_vel 
        y_vel *= 1.1  
        if player_rect.bottom >= window_size[1]: 
            player_rect.bottom = window_size[1]

    if player_rect.y >= window_size[1] - player_rect.h: 
        lose = True 
    if player_rect.y <= 0: 
        lose = True 


    window.fill("sky blue") 
    for tube in tubes[:]: 
        if not lose: 
            tube.x -= 10 
        if tube.x < -100: 
            tubes.remove(tube) 
            score += 0.5                                   
        if player_rect.colliderect(tube): 
            lose = True 
        draw.rect(window, "green", tube) 

    if len(tubes) < 8: 
        tubes += generate_tubes(150) 

    draw.rect(window, "yellow", player_rect)
    score_text = my_font.render(f"score: {int(score)}", True, "black") 
    window.blit(score_text, (20, 20))
    display.update() 
    clock.tick(60)  

