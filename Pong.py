import pygame, sys, random, os
# import pyinstaller


def ball_animation():
    global ball_speed_x, ball_speed_y, opponent_score, player_score, score_time

    # screen boundary collision
    if ball.top <= 0 or ball.bottom >= screen_height:
        ball_speed_y *= -1

    # scoring
    if ball.left <= -100:
        player_score += 1
        score_time = pygame.time.get_ticks()

    if ball.right >= screen_width + 100:
        opponent_score += 1
        score_time = pygame.time.get_ticks()

    # paddle collision
    # if ball hits player and is going right
    if ball.colliderect(player) and ball_speed_x > 0:
        if abs(ball.right - player.left) < 20:
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1

    if ball.colliderect(opponent) and ball_speed_x < 0:
        if abs(ball.left - opponent.right) < 20:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1


def player_animation(mode):
    global beatable2

    if mode == 'auto':
        if beatable2:
            if player.top < ball.y:  # opponent.top
                player.top += player_max
            if player.bottom > ball.y:
                player.bottom -= player_max  # opponent.bottom
        elif not beatable2:
            if player.center[1] < ball.y:  # opponent.top
                player.top += player_max
            if player.center[1] > ball.y:
                player.bottom -= player_max  # opponent.bottom

    if player.top <= 0:
        player.top = 0
    if player.bottom >= screen_height:
        player.bottom = screen_height


def opponent_animation():
    if beatable is not None:
        if beatable:
            if opponent.top < ball.y:  # opponent.top
                opponent.top += opponent_speed
            if opponent.bottom > ball.y:
                opponent.bottom -= opponent_speed  # opponent.bottom
        elif not beatable:
            if opponent.center[1] < ball.y:  # opponent.top
                opponent.top += opponent_speed
            if opponent.center[1] > ball.y:
                opponent.bottom -= opponent_speed  # opponent.bottom

    # screen boundaries
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= screen_height:
        opponent.bottom = screen_height


def ball_restart(mode):
    global ball_speed_x, ball_speed_y, score_time, beatable, beatable2, speed_up_timer, player_max, opponent_speed, speed_up

    current_time = pygame.time.get_ticks()
    ball.center = (screen_width / 2, screen_height / 2)

    # shows timer
    if current_time - score_time < 700:
        number_three = game_font_normal.render('3', True, light_grey)
        screen.blit(number_three, (screen_width/2 - 10, screen_height/2 + 20))
    if 700 < current_time - score_time < 1400:
        number_three = game_font_normal.render('2', True, light_grey)
        screen.blit(number_three, (screen_width/2 - 10, screen_height/2 + 20))
    if 1400 < current_time - score_time < 2100:
        number_three = game_font_normal.render('1', True, light_grey)
        screen.blit(number_three, (screen_width/2 - 10, screen_height/2 + 20))

        if mode == 'random':
            # randomly decides if computer is beatable or not
            beat_int = random.randint(0, 1)
            if beat_int == 0:
                beatable = True
            elif beat_int == 1:
                beatable = False
        if mode == 'auto':
            beatable, beatable2 = False, False
            if not auto_infinite:
                while not beatable and not beatable2:
                    rand_int = random.randint(0, 1)
                    if rand_int:
                        beatable = True
                    else:
                        beatable = False
                    rand_int = random.randint(0, 1)
                    if rand_int:
                        beatable2 = True
                    else:
                        beatable2 = False

    if current_time - score_time < 2100:
        ball_speed_x, ball_speed_y = 0, 0
    else:
        ball_speed_y = 7 * random.choice((1, -1))
        ball_speed_x = 7 * random.choice((1, -1))
        score_time = None
        speed_up_timer = 0
        if mode != 'auto':
            speed_up = 0


def reset_game():
    global player_score, opponent_score, score_time, pause, player, opponent, beatable, ball_speed_x, ball_speed_y, player_max, opponent_speed, speed_up_timer, speed_up
    player_score = 0
    opponent_score = 0
    speed_up_timer = 0
    speed_up = 0

    ball_speed_x = 7 * random.choice((1, -1))
    ball_speed_y = 7 * random.choice((1, -1))
    player_max = 7
    opponent_speed = 7

    beatable = True
    player = pygame.Rect(screen_width - 20, screen_height / 2 - 70, 10, 140)
    opponent = pygame.Rect(10, screen_height / 2 - 70, 10, 140)
    score_time = True
    pause = False


def auto_speed(speed_up, mode):
    global player_max, opponent_speed, ball_speed_x, ball_speed_y, game_speed, speed_up_allowed
    ball_x_negative = False
    ball_y_negative = False

    if ball_speed_x < 0:
        ball_x_negative = True

    if ball_speed_y < 0:
        ball_y_negative = True

    if mode == 'auto':
        if speed_up == 0:
            player_max = 7
            opponent_speed = 7
            ball_speed_x = 7
            ball_speed_y = 7
        if speed_up == 1:
            player_max = 9
            opponent_speed = 9
            ball_speed_x = 9
            ball_speed_y = 9
        elif speed_up == 2:
            player_max = 14
            opponent_speed = 14
            ball_speed_x = 14
            ball_speed_y = 14
        elif speed_up == 3:
            player_max = 20
            opponent_speed = 20
            ball_speed_x = 20
            ball_speed_y = 20
        if ball_x_negative:
            ball_speed_x *= -1
        if ball_y_negative:
            ball_speed_y *= -1
    elif speed_up_allowed:
        if speed_up == 0:
            ball_speed_x = 7
            ball_speed_y = 7
            opponent_speed = 7
        if speed_up == 1:
            ball_speed_x = 9
            ball_speed_y = 9
            opponent_speed = 9
        elif speed_up == 2:
            ball_speed_x = 14
            ball_speed_y = 14
            opponent_speed = 14
        elif speed_up == 3:
            ball_speed_x = 20
            ball_speed_y = 20
            opponent_speed = 20
        if ball_x_negative:
            ball_speed_x *= -1
        if ball_y_negative:
            ball_speed_y *= -1


# General Setup
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
game_speed = 60
click = False
beatable = True
beatable2 = True
freesansbold_path = '/Users/towella/Documents/programming/python/Pong/freesansbold.ttf'

# settings
pause = False
options = False
show_debug = False
auto_infinite = False
speed_up_allowed = True
speed_up = 0

# Screen Setup
screen_width = 1000  # 980
screen_height = 680
screen = pygame.display.set_mode((screen_width, screen_height), pygame.SCALED | pygame.RESIZABLE, vsync=True)
pygame.display.set_caption('Pong -- Main Menu -- Andrew Towell')

# Game Rectangles
ball = pygame.Rect(screen_width/2 - 15, screen_height/2 - 15, 30, 30)
player = pygame.Rect(screen_width - 20, screen_height/2 - 70, 10, 140)
opponent = pygame.Rect(10, screen_height/2 - 70, 10, 140)

# Colours
bg_colour = pygame.Color('grey12')
light_grey = (200, 200, 200)

# Speeds
ball_speed_x = 7 * random.choice((1, -1))
ball_speed_y = 7 * random.choice((1, -1))
player_speed = 0
player_speed2 = 0
player_max = 7
opponent_speed = 7

# Score Counter
player_score = 0
opponent_score = 0
game_font_large = pygame.font.Font(freesansbold_path, 52)  # pygame.font.get_default_font()
game_font_normal = pygame.font.Font(freesansbold_path, 32)
game_font_small = pygame.font.Font(freesansbold_path, 22)

# Timer
score_time = True
speed_up_timer = 0
time_increase = 0.1


def main_menu():
    global click, options

    while True:
        screen.fill(bg_colour)
        # titles and general text
        main_menu_title = game_font_large.render(f'Pong -- Main Menu', True, light_grey)
        screen.blit(main_menu_title, (100, 100))
        controls_text = game_font_small.render(f'Controls: up = w/arrow up, down = s/arrow down, pause = p, exit/quit = ,/esc ', True, light_grey)
        screen.blit(controls_text, (30, 630))

        # x and y mouse pos
        mx, my = pygame.mouse.get_pos()

        # button rect and draw
        button_1 = pygame.Rect(100, 200, 400, 50)
        button_2 = pygame.Rect(100, 300, 400, 50)
        button_3 = pygame.Rect(100, 400, 400, 50)
        button_4 = pygame.Rect(100, 500, 400, 50)
        button_5 = pygame.Rect(850, 25, 120, 60)
        button_6 = pygame.Rect(850, 105, 120, 60)
        button_options = pygame.Rect(820, 185, 150, 60)
        pygame.draw.rect(screen, light_grey, button_1)
        pygame.draw.rect(screen, light_grey, button_2)
        pygame.draw.rect(screen, light_grey, button_3)
        pygame.draw.rect(screen, light_grey, button_4)
        pygame.draw.rect(screen, light_grey, button_5)
        pygame.draw.rect(screen, light_grey, button_6)
        pygame.draw.rect(screen, light_grey, button_options)
        # button text and draw
        b1_text = game_font_normal.render(f'Pong - Beatable', True, bg_colour)
        screen.blit(b1_text, (120, 210))
        b2_text = game_font_normal.render(f'Pong - Unbeatable', True, bg_colour)
        screen.blit(b2_text, (120, 310))
        b3_text = game_font_normal.render(f'Pong - Random', True, bg_colour)
        screen.blit(b3_text, (120, 410))
        b4_text = game_font_normal.render(f'Pong - Multiplayer', True, bg_colour)
        screen.blit(b4_text, (120, 510))
        b5_text = game_font_normal.render(f'Quit', True, bg_colour)
        screen.blit(b5_text, (873, 40))
        b6_text = game_font_normal.render(f'Auto', True, bg_colour)
        screen.blit(b6_text, (873, 120))
        boption_text = game_font_normal.render(f'Options', True, bg_colour)
        screen.blit(boption_text, (832, 200))

        # if mouse touches buttons
        if button_1.collidepoint((mx, my)):
            if click:
                reset_game()
                pygame.display.set_caption('Pong -- Beatable -- Andrew Towell')
                game('beatable')
        elif button_2.collidepoint((mx, my)):
            if click:
                reset_game()
                pygame.display.set_caption('Pong -- Unbeatable -- Andrew Towell')
                game('unbeatable')
        elif button_3.collidepoint((mx, my)):
            if click:
                reset_game()
                pygame.display.set_caption('Pong -- Random -- Andrew Towell')
                game('random')
        elif button_4.collidepoint((mx, my)):
            if click:
                reset_game()
                pygame.display.set_caption('Pong -- Multiplayer -- Andrew Towell')
                game('multi')
        elif button_5.collidepoint((mx, my)):
            if click:
                pygame.quit()
                sys.exit()
        elif button_6.collidepoint((mx, my)):
            if click:
                reset_game()
                if auto_infinite:
                    pygame.display.set_caption('Pong -- Auto(Infinite) -- Andrew Towell')
                else:
                    pygame.display.set_caption('Pong -- Auto(Random) -- Andrew Towell')
                game('auto')
        elif button_options.collidepoint((mx, my)):
            if click:
                pygame.display.set_caption('Pong -- Options -- Andrew Towell')
                options = True

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_COMMA or event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if options:
            options_screen()
        pygame.display.update()
        clock.tick(game_speed)


def game(mode):
    global player_speed, beatable, pause, running, player_speed2, show_debug, beatable2, click, speed_up, speed_up_timer, speed_up_allowed

    if mode == 'beatable':
        beatable = True
    elif mode == 'unbeatable':
        beatable = False
    elif mode == 'multi':
        beatable = None
    elif mode == 'auto':
        beatable, beatable2 = False, False
        if not auto_infinite:
            while not beatable and not beatable2:
                rand_int = random.randint(0, 1)
                if rand_int:
                    beatable = True
                else:
                    beatable = False
                rand_int = random.randint(0, 1)
                if rand_int:
                    beatable2 = True
                else:
                    beatable2 = False

    running = True
    while running:

        # x and y mouse pos
        mx, my = pygame.mouse.get_pos()

        click = False
        # Event Checks
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # player input
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_DOWN and mode != 'auto':
                    player_speed = player_max
                elif event.key == pygame.K_s and mode != 'auto':
                    if beatable is not None:
                        player_speed = player_max
                    else:
                        player_speed2 = player_max
                elif event.key == pygame.K_UP and mode != 'auto':
                    player_speed = -player_max
                elif event.key == pygame.K_w and mode != 'auto':
                    if beatable is not None:
                        player_speed = -player_max
                    else:
                        player_speed2 = -player_max

                # debug keys
                elif event.key == pygame.K_SLASH and mode == 'random':
                    beatable = not beatable
                elif event.key == pygame.K_PERIOD:
                    show_debug = not show_debug
                elif event.key == pygame.K_p:
                    pause = True
                elif event.key == pygame.K_COMMA or event.key == pygame.K_ESCAPE:
                    running = False
                    pygame.display.set_caption('Pong -- Main Menu -- Andrew Towell')
                elif event.key == pygame.K_u:
                    speed_up_allowed = not speed_up_allowed

            # reset player speed
            elif event.type == pygame.KEYUP and mode != 'auto':
                # if down arrow pressed
                if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    player_speed = 0
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    if mode != 'multi':
                        player_speed = 0
                    else:
                        player_speed2 = 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if not pause:
            # Ball Logic
            ball.x += ball_speed_x
            ball.y += ball_speed_y
            ball_animation()
            player.y += player_speed
            if mode == 'multi':
                opponent.y += player_speed2

            # Player Logic
            player_animation(mode)

            # Opponent Logic
            opponent_animation()

            # Visuals
            screen.fill(bg_colour)
            pygame.draw.rect(screen, light_grey, player)
            pygame.draw.rect(screen, light_grey, opponent)
            pygame.draw.ellipse(screen, light_grey, ball)
            pygame.draw.aaline(screen, light_grey, (screen_width/2, 0), (screen_width/2, screen_height))

            if score_time:
                ball_restart(mode)

            player_text = game_font_normal.render(f'{player_score}', True, light_grey)
            opponent_text = game_font_normal.render(f'{opponent_score}', True, light_grey)
            beattext = game_font_small.render(f'(p1:{player_speed} p2:{player_speed2} b1:{beatable} b2:{beatable2} m:{mode} s:{speed_up_allowed} i:{auto_infinite})', True, light_grey)
            screen.blit(player_text, (523, 333))
            screen.blit(opponent_text, (462, 333))
            if show_debug:
                screen.blit(beattext, (0, 0))

            # buttons
            button_1 = pygame.Rect(870, 25, 100, 50)
            pygame.draw.rect(screen, light_grey, button_1)
            b1_text = game_font_small.render(f'Pause', True, bg_colour)
            screen.blit(b1_text, (887, 40))

            # if mouse touches buttons
            if button_1.collidepoint((mx, my)):
                if click:
                    pause = True

            if mode == 'auto':
                button_2 = pygame.Rect(760, 25, 100, 50)
                pygame.draw.rect(screen, light_grey, button_2)
                b2_text = game_font_small.render('>' * (speed_up + 1), True, bg_colour)
                screen.blit(b2_text, (783, 40))

                # if mouse touches buttons
                if button_2.collidepoint((mx, my)):
                    if click:
                        speed_up += 1
                        if speed_up > 3:
                            speed_up = 0

            # speed
            else:
                speed_up_timer += time_increase
                if speed_up_timer >= 50:
                    speed_up += 1
                    speed_up_timer = 0
                    if speed_up > 3:
                        speed_up = 3

            auto_speed(speed_up, mode)

            # Update
            pygame.display.flip()
            clock.tick(game_speed)
        else:
            pause_game()


def pause_game():
    global pause, game_speed, click, running

    while pause:
        pause_screen = pygame.Rect(screen_width / 4, screen_height / 4, screen_width / 2, screen_height / 2)
        pygame.draw.rect(screen, light_grey, pause_screen)
        pause_text = game_font_normal.render(f'PAUSED', True, bg_colour)
        screen.blit(pause_text, (screen_width / 2 - 65, screen_height / 2 - 100))

        button_1 = pygame.Rect(screen_width / 2 - 220, screen_height / 2, 200, 100)
        button_2 = pygame.Rect(screen_width / 2 + 20, screen_height / 2, 200, 100)
        button_3 = pygame.Rect(870, 25, 100, 50)
        pygame.draw.rect(screen, bg_colour, button_1)
        pygame.draw.rect(screen, bg_colour, button_2)
        pygame.draw.rect(screen, light_grey, button_3)

        b1_text = game_font_normal.render(f'Menu', True, light_grey)
        b2_text = game_font_normal.render(f'Resume', True, light_grey)
        b3_text = game_font_small.render(f'Resume', True, bg_colour)
        screen.blit(b1_text, (screen_width / 2 - 165, screen_height / 2 + 35))
        screen.blit(b2_text, (screen_width / 2 + 55, screen_height / 2 + 35))
        screen.blit(b3_text, (877, 40))

        # x and y mouse pos
        mx, my = pygame.mouse.get_pos()

        if button_1.collidepoint((mx, my)):
            if click:
                pause = False
                running = False
                pygame.display.set_caption('Pong -- Main Menu -- Andrew Towell')
        elif button_2.collidepoint((mx, my)) or button_3.collidepoint((mx, my)):
            if click:
                pause = False

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_COMMA or event.key == pygame.K_ESCAPE:
                    pause = False
                    running = False
                    pygame.display.set_caption('Pong -- Main Menu -- Andrew Towell')
                elif event.key == pygame.K_p:
                    pause = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(game_speed)


def options_screen():
    global options, click, speed_up_allowed, show_debug, auto_infinite

    while options:
        options_window = pygame.Rect(40, 40, screen_width / 1.09, screen_height / 1.14)
        pygame.draw.rect(screen, light_grey, options_window)
        options_text = game_font_large.render(f'OPTIONS', True, bg_colour)
        speedup_text = game_font_normal.render(f'Speed Up During Game --------', True, bg_colour)
        debug_text = game_font_normal.render(f'Allow Debug Title ---------------', True, bg_colour)
        infinite_text = game_font_normal.render(f'Infinite Auto Mode ---------------', True, bg_colour)
        screen.blit(options_text, (screen_width / 2 - 120, 80))
        screen.blit(speedup_text, (150, 200))
        screen.blit(debug_text, (150, 320))
        screen.blit(infinite_text, (150, 440))

        button_close = pygame.Rect(40, 40, 50, 50)
        button_speedup = pygame.Rect(630, 170, 200, 100)
        button_debug = pygame.Rect(630, 290, 200, 100)
        button_infinite = pygame.Rect(630, 410, 200, 100)
        pygame.draw.rect(screen, light_grey, button_close)
        pygame.draw.rect(screen, bg_colour, button_speedup)
        pygame.draw.rect(screen, bg_colour, button_debug)
        pygame.draw.rect(screen, bg_colour, button_infinite)

        bclose_text = game_font_normal.render(f'X', True, bg_colour)
        bspeedup_text = game_font_normal.render(f'{speed_up_allowed}', True, light_grey)
        bdebug_text = game_font_normal.render(f'{show_debug}', True, light_grey)
        binfinite_text = game_font_normal.render(f'{auto_infinite}', True, light_grey)
        screen.blit(bclose_text, (50, 50))
        screen.blit(bspeedup_text, (690, 205))
        screen.blit(bdebug_text, (690, 325))
        screen.blit(binfinite_text, (690, 445))

        # x and y mouse pos
        mx, my = pygame.mouse.get_pos()

        if button_close.collidepoint((mx, my)):
            if click:
                options = False
                pygame.display.set_caption('Pong -- Main Menu -- Andrew Towell')
        elif button_speedup.collidepoint((mx, my)):
            if click:
                speed_up_allowed = not speed_up_allowed
        elif button_debug.collidepoint((mx, my)):
            if click:
                show_debug = not show_debug
        elif button_infinite.collidepoint((mx, my)):
            if click:
                auto_infinite = not auto_infinite

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_COMMA or event.key == pygame.K_ESCAPE:
                    options = False
                    pygame.display.set_caption('Pong -- Main Menu -- Andrew Towell')
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(game_speed)


main_menu()