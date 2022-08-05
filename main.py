import pygame
import random


# window settings :
screen_width, screen_height = 960, 540
screen_color = (255, 255, 255)
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("pygame exercise")


def is_on_ground(rect, obst):
    return (rect.colliderect(obst) and abs(obst.top - rect.bottom) <= 20) or rect.bottom >= screen_height


def main():
    # rect settings :
    rect_color = (255, 15, 15)
    prev_color = (100, 100, 100)
    width, height = 50, 50
    x, y = round(screen_width / 2 - width), screen_height - height
    rect = pygame.Rect(x, y, width, height)

    # rectangle's x movement parameters :
    x_velocity = 0

    # rectangle's y movement parameters :
    y_velocity = 0

    # obstacle settings :
    obst_color = (20, 20, 20)
    obst_width, obst_height = 200, 50
    obst_x, obst_y = 500, 400
    obst = pygame.Rect(obst_x, obst_y, obst_width, obst_height)

    # game loop :
    clock = pygame.time.Clock()
    running = True
    flag = True
    frame = 0
    rnd_x, rnd_y = 0, 0
    while running:
        clock.tick(60)  # sets fps
        for event in pygame.event.get():  # checks if user quit the window
            if event.type == pygame.QUIT:
                running = False

        # drawing :
        win.fill(screen_color)  # paints the background
        if frame >= 90:
            if flag:
                try:
                    rnd_x = random.randint(30, obst.left - obst.width - 30)
                except:
                    rnd_x = random.randint(obst.right + 30, screen_width - obst_width - 30)
                try:
                    rnd_y = random.randint(60, obst.top - obst.height)
                except:
                    rnd_y = random.randint(obst.bottom + 30, 400)
                flag = False
            pygame.draw.rect(win, prev_color, (rnd_x, rnd_y, obst_width, obst_height))
        pygame.draw.rect(win, rect_color, rect)
        pygame.draw.rect(win, obst_color, obst)

        # movement :
        keys = pygame.key.get_pressed()  # checks for button presses

        # x axis :
        if keys[pygame.K_RIGHT] and x_velocity < 9:
            x_velocity += 0.3
        elif keys[pygame.K_LEFT] and x_velocity > -9:
            x_velocity -= 0.3
        elif x_velocity > 0:
            x_velocity -= 0.15
        elif x_velocity < 0:
            x_velocity += 0.15
        if abs(x_velocity) < 0.2:
            x_velocity = 0

        # y axis :
        if keys[pygame.K_UP] and is_on_ground(rect, obst):
            y_velocity = 10
        elif keys[pygame.K_DOWN]:
            y_velocity -= 9.8 / 30
        else:
            y_velocity -= 9.8 / 60

        # collision :
        if is_on_ground(rect, obst) and y_velocity < 0:
            y_velocity *= -1
        if rect.colliderect(obst):
            if abs(obst.bottom - rect.top) <= 10 and y_velocity > 0:
                y_velocity *= -0.5
            elif abs(obst.right - rect.left) <= 10 and x_velocity < 0:
                x_velocity *= -0.5
            elif abs(obst.left - rect.right) <= 10 and x_velocity > 0:
                x_velocity *= -0.5

        if x_velocity != 0:
            if (x_velocity > 0 and rect.right >= screen_width) or (x_velocity < 0 and rect.left <= 0):
                x_velocity *= -0.5
            else:
                rect.x += x_velocity
        if y_velocity != 0:
            rect.y -= y_velocity

        rect.x = round(rect.x)
        rect.y = round(rect.y)

        # misc :
        frame += 1
        if frame >= 180:
            obst.x = rnd_x
            obst.y = rnd_y
            frame = 0
            flag = True

        pygame.display.update()  # update window

    pygame.quit()


if __name__ == '__main__':
    main()
