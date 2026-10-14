from pygame import *
from random import *
import sounddevice as sd
import numpy as np

sr = 16000
block = 256
mic_level = 0.0


def audio_cb(indata, frames, time, status):
    global mic_level
    if status:
        return
    rms = float(np.sqrt(np.mean(indata ** 2)))
    mic_level = 0.85 * mic_level + 0.15 * rms


init()

window_size = (800, 600)
window = display.set_mode(window_size)
clock = time.Clock()
display.set_caption("flappy Bird")

player_rect = Rect(150, 250, 90, 90)

background = image.load("night sky.webp")
background = transform.scale(background, window_size)

bird = image.load("bird2-removebg-preview.png")
bird = transform.scale(bird, (90, 90))

tube_top = image.load("pipe_flappy_bird_new-removebg-preview.png")
tube_bottom = transform.rotate(tube_top, 180)


def generate_tubes(
    count,
    tube_width=140,
    gap=280,
    min_height=50,
    max_height=300,
    distance=650
):
    tubes = []
    start_x = window_size[0] + 200
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
gravity = 0.3
y_vel = 0.0
THRESH = 0.001
IMPULSE = -7.0 

flet = False 


#!! Затримка між голосовими стрибками пташки
voice_cooldown = 0

with sd.InputStream(
    samplerate=sr,
    channels=1,
    blocksize=block,
    callback=audio_cb
):
    while 1:
        for e in event.get():
            if e.type == QUIT:
                quit()
        #!!! Перевіряємо, чи залишилася затримка після попереднього стрибка
        if voice_cooldown > 0:
            voice_cooldown -= 1
        #!!! Якщо мікрофон почув звук і затримка закінчилася — пташка стрибає
        if mic_level > THRESH and not lose and voice_cooldown == 0:
            y_vel = IMPULSE 
            flet = False 
            #!!! Після стрибка чекаємо 12 кадрів перед наступним стрибком
            voice_cooldown = 7

        if not flet and not lose:     
            y_vel += gravity
            player_rect.y += int(y_vel) 
        elif flet and not lose: 
            player_rect.x += 2

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
            player_rect.x = 150 
            y_vel = 2
            #!!! Після рестарту прибираємо затримку голосового стрибка
            voice_cooldown = 0 
            flet = False

        if lose:
            player_rect.y += y_vel
            y_vel *= 1.1
            if player_rect.bottom >= window_size[1]:
                player_rect.bottom = window_size[1]
                y_vel = 0


        if player_rect.bottom >= window_size[1]:
            player_rect.bottom = window_size[1] 
            flet = True 
            y_vel = 0 
        if player_rect.y <= 0:
            lose = True 
            

        window.blit(background, (0, 0))
        for tube in tubes[:]:
            if not lose:
                tube.x -= 5
            if tube.x < -100:
                tubes.remove(tube)
                score += 0.5
                continue
            if tube.y == 0:
                pipe = transform.scale(
                    tube_top,
                    (tube.width, tube.height)
                )
            else:
                pipe = transform.scale(
                    tube_bottom,
                    (tube.width, tube.height)
                )

            window.blit(pipe, tube)

            if player_rect.colliderect(tube):
                lose = True 
                y_vel = 0 

        if len(tubes) < 8:
            tubes += generate_tubes(150)

        window.blit(bird, player_rect)

        score_text = my_font.render(
            f"score: {int(score)}",
            True,
            "white"
        )

        window.blit(score_text, (20, 20))
        display.update()
        clock.tick(60)