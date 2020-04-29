from Classes import *
from Menus import *

# Set Up
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fried Chicken")
clock = pygame.time.Clock()
run: bool
if __name__ == '__main__':
    run = True

# Global variables
bg = pygame.image.load("Background/Jungle.png")
framePerSec = 27
paused = False
won = False
level = 0
buttonDelay = 0
attempt = 1
# Initializations
chick = Player(150, 400, 40, 60)
shop = Shop(870, 549, 115, 155)
platforms = []
wolves = []
wolfProjectiles = []
chickProjectiles = []


def check_collisions():
    # Player connecting with platforms
    if chick.collide:
        for plat in platforms:
            if plat.y + 5 < chick.y + chick.height < plat.y + 20:
                if chick.x + chick.width - 10 > plat.x and chick.x + 10 < plat.x + plat.width:
                    chick.lowerBound = plat.y + 11
                    chick.isGrounded = True
                    chick.accY = 0
                    chick.velY = 0
                    if not chick.stuck and chick.stuckDelay <= 0:
                        chick.y = chick.lowerBound - chick.height
                        chick.stuck = True
                    elif chick.isJump or chick.isFly or chick.collide:
                        chick.stuck = False
                else:
                    chick.lowerBound = SCREEN_HEIGHT + 20
                    chick.isGrounded = False
    else:
        chick.lowerBound = SCREEN_HEIGHT
        chick.isGrounded = False
        if chick.isGrounded and not chick.isJump and not chick.isFly and chick.stuckDelay <= 0:
            chick.velY = 5
            chick.stuckDelay = 5
    # Player being hit
    for projectile in wolfProjectiles:
        if chick.y + chick.height >= projectile.y and chick.y <= projectile.y + projectile.height:
            if chick.x + chick.width >= projectile.x and chick.x <= projectile.x + projectile.width:
                if projectile.picture == Boss.projectile[0] or projectile.picture == Boss.projectile[1]:
                    chick.hit(15)
                    if chick.alive:
                        chick.change_score(-10)
                else:
                    chick.hit(10)
                    if chick.alive:
                        chick.change_score(-10)
                wolfProjectiles.remove(projectile)
    for wolf in wolves:
        # Wolf being hit
        for projectile in chickProjectiles:
            if wolf.y + wolf.height >= projectile.y and wolf.y <= projectile.y + projectile.height:
                if wolf.x + wolf.width >= projectile.x and wolf.x <= projectile.x + projectile.width:
                    wolf.hit()
                    chickProjectiles.remove(projectile)
        # Wolf dying
        if wolf.health <= 0:
            wolves.remove(wolf)
            chick.change_score(25)
        # Wolf hitting
        if chick.y + chick.height >= wolf.y and chick.y <= wolf.y + wolf.height:
            if chick.x + chick.width >= wolf.x and chick.x <= wolf.x + wolf.width and chick.alive:
                chick.hit(10)
        # Wolf Shooting
        if wolf.shot:
            wolf.shootInt -= 1
            if wolf.shootInt <= 0:
                wolf.shot = False
                wolf.shootInt = 20
        elif chick.y + chick.height > wolf.y and chick.y < wolf.y + wolf.height:
            if wolf.vel > 0 and chick.x > wolf.x + wolf.width:
                wolf.shoot(wolfProjectiles)
            elif wolf.vel < 0 and chick.x + chick.width < wolf.x:
                wolf.shoot(wolfProjectiles)
    # Checking shop range
    if chick.y + chick.height >= shop.y and chick.y <= shop.y + shop.height:
        if chick.x + chick.width + 100 >= shop.x and chick.x - 100 <= shop.x + shop.width:
            shop.inRange = True
        else:
            shop.inRange = False
    else:
        shop.inRange = False


controls = False
helping = False
naming = True
RUSure = False


def reset():
    global chick, paused, shop, level, naming, attempt
    chick = Player(150, 400, 40, 60)
    shop = Shop(870, 549, 115, 155)
    level = 0
    attempt += 1
    pygame.draw.rect(win, (0, 0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    paused = False


def pause():
    global paused, buttonDelay, controls, helping, naming, RUSure, attempt
    paused = True
    while paused:
        keys = pygame.key.get_pressed()
        if naming:
            name_screen(win, None)
        elif not chick.alive:
            lose_menu(win, chick.score, attempt)
            if attempt > 1:
                attempt -= 1
            if (keys[pygame.K_h] or keys[pygame.K_ESCAPE]) and buttonDelay <= 0 and not helping and not controls:
                reset()
                buttonDelay = 2
            elif (keys[pygame.K_l] and buttonDelay <= 0) or RUSure:
                RUSure = True
                r_u_sure(win, "to quit?")
                if keys[pygame.K_y] and buttonDelay <= 0:
                    pygame.quit()
                elif keys[pygame.K_n] and buttonDelay <= 0:
                    RUSure = False
                    buttonDelay = 2
        elif won:
            win_menu(win, chick.score, attempt)
            if attempt > 1:
                attempt -= 1
            if (keys[pygame.K_h] or keys[pygame.K_ESCAPE]) and buttonDelay <= 0 and not helping and not controls:
                reset()
                buttonDelay = 2
            elif keys[pygame.K_l] or RUSure:
                RUSure = True
                r_u_sure(win, "to quit?")

                if keys[pygame.K_y] and buttonDelay <= 0:
                    pygame.quit()
                elif keys[pygame.K_n] and buttonDelay <= 0:
                    RUSure = False
                    buttonDelay = 2
        else:
            if level == 0:
                start_menu(win)
            else:
                pause_menu(win)
            if (keys[pygame.K_h] or keys[pygame.K_ESCAPE]) and buttonDelay <= 0 and not helping and not controls:
                paused = False
                buttonDelay = 2
            elif (keys[pygame.K_j] and buttonDelay <= 0 and not helping) or controls:
                controls = True
                controls_menu(win)
                if keys[pygame.K_b] and buttonDelay <= 0:
                    controls = False
                    buttonDelay = 2
            elif (keys[pygame.K_k] and buttonDelay <= 0 and not controls) or helping:
                helping = True
                help_menu(win)
                if keys[pygame.K_b] and buttonDelay <= 0:
                    helping = False
                    buttonDelay = 2
            elif (keys[pygame.K_l] and not helping and not controls) or RUSure:
                RUSure = True
                r_u_sure(win, "to quit?")
                if keys[pygame.K_y] and buttonDelay <= 0:
                    pygame.quit()
                elif keys[pygame.K_n] and buttonDelay <= 0:
                    RUSure = False
                    buttonDelay = 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if naming:
                naming = name_screen(win, event)
        if buttonDelay > 0:
            buttonDelay -= 1
        pygame.display.update()
        clock.tick(framePerSec)


def level1():
    global platforms, wolves, chickProjectiles, wolfProjectiles
    platforms = [  # Highest to lowest
        Platform(400, 90, 230),
        Platform(750, 170, 150),
        Platform(0, 200, 80),
        Platform(420, 230, 100),
        Platform(580, 295, 140),
        Platform(100, 330, 180),
        Platform(800, 385, 200),
        Platform(390, 400, 150),
        Platform(50, 480, 230),
        Platform(600, 510, 230),
        Platform(300, 580, 200),
        Platform(100, 720, 200),

        Platform(550, 670, 450),  # Shop platform
        Platform(0, SCREEN_HEIGHT, SCREEN_WIDTH)  # Bottom of screen

    ]
    wolves = [  # the path should be 25 left of the ends of the chosen platforms and 90 above.
        Enemy(78, 240, 78, 230)
    ]
    chickProjectiles = []
    wolfProjectiles = []


def level2():
    global platforms, wolves, chickProjectiles, wolfProjectiles
    platforms = [
        Platform(400, 90, 230),
        Platform(800, 180, 230),
        Platform(150, 250, 200),
        Platform(580, 295, 240),
        Platform(910, 380, 90),
        Platform(390, 410, 150),
        Platform(50, 480, 230),
        Platform(650, 530, 200),
        Platform(240, 580, 250),
        Platform(100, 720, 200),

        Platform(550, 670, 450),
        Platform(0, SCREEN_HEIGHT, SCREEN_WIDTH)
    ]

    wolves = [
        Enemy(900, 90, 778, 925),
        Enemy(100, 390, 28, 240)
    ]
    chickProjectiles = []
    wolfProjectiles = []


def level3():
    global platforms, wolves, chickProjectiles, wolfProjectiles
    platforms = [
        Platform(310, 130, 180),
        Platform(700, 170, 200),
        Platform(150, 230, 200),
        Platform(580, 295, 240),
        Platform(280, 400, 250),
        Platform(600, 510, 230),
        Platform(0, 570, 180),
        Platform(300, 620, 160),
        Platform(100, 720, 200),

        Platform(550, 670, 450),
        Platform(0, SCREEN_HEIGHT, SCREEN_WIDTH)
    ]

    wolves = [
        Enemy(600, 420, 577, 782),
        Enemy(350, 310, 255, 485),
        Enemy(750, 80, 675, 855)
    ]
    chickProjectiles = []
    wolfProjectiles = []


def level4():
    global platforms, wolves, chickProjectiles, wolfProjectiles
    platforms = [
        Platform(325, 100, 200),
        Platform(610, 150, 100),
        Platform(175, 200, 100),
        Platform(760, 250, 240),
        Platform(580, 305, 140),
        Platform(50, 330, 200),
        Platform(350, 380, 200),
        Platform(130, 450, 100),
        Platform(670, 460, 330),
        Platform(0, 560, 120),
        Platform(300, 620, 160),
        Platform(100, 720, 200),

        Platform(550, 670, 450),
        Platform(0, SCREEN_HEIGHT, SCREEN_WIDTH)
    ]

    wolves = [
        Enemy(800, 160, 735, 925),
        Enemy(700, 370, 645, 925),
        Enemy(150, 240, 25, 200),
        Enemy(400, 10, 300, 475)
    ]
    chickProjectiles = []
    wolfProjectiles = []


def level_boss1():
    global platforms, wolves, chickProjectiles, wolfProjectiles
    platforms = [
        Platform(325, 200, 250),
        Platform(700, 240, 100),
        Platform(150, 280, 100),
        Platform(750, 340, 100),
        Platform(375, 400, 250),
        Platform(100, 440, 100),
        Platform(725, 500, 100),
        Platform(200, 540, 100),
        Platform(350, 600, 300),

        Platform(700, 670, 350),
        Platform(0, SCREEN_HEIGHT, SCREEN_WIDTH)
    ]

    wolves = [
        Boss(500, 250, 330, 550)
    ]
    chickProjectiles = []
    wolfProjectiles = []


def redraw():
    # Background
    win.blit(bg, (0, 0))
    # Status box
    pygame.draw.rect(win, (127, 127, 127), (SCREEN_WIDTH - 120, 0, 120, 80))
    font = pygame.font.SysFont('Lucida Console', 15, True)
    text1 = font.render('Level: ' + str(level), 1, (0, 0, 0))
    text2 = font.render('Enemies: ' + str(len(wolves)), 1, (0, 0, 0))
    text3 = font.render('Score: ' + str(chick.score), 1, (0, 0, 0))
    win.blit(text1, ((SCREEN_WIDTH - 120) + 10, 10))
    win.blit(text2, ((SCREEN_WIDTH - 120) + 10, 35))
    win.blit(text3, ((SCREEN_WIDTH - 120) + 10, 60))
    # Drawing everything
    chick.display_stats(win)
    for plat in platforms:
        plat.draw(win)
    for w in wolves:
        w.draw(win)
    for projectile in wolfProjectiles:
        projectile.draw(win, wolfProjectiles, chick.x, chick.y)
    for projectile in chickProjectiles:
        projectile.draw(win, chickProjectiles)
    shop.draw(win, chick)
    chick.draw(win)
    shop.display_menu(win, chick)
    pygame.display.update()


# Main Loop
while run:
    if not paused:
        clock.tick(framePerSec)
    lvl = level
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    check_collisions()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE] and buttonDelay <= 0:
        paused = True
        buttonDelay = 10
    if buttonDelay > 0:
        buttonDelay -= 1
    if len(wolves) == 0 and level != 0:
        shop.isVisible = True
        if level == 5:
            won = True
            paused = True
    if keys[pygame.K_e] and shop.isVisible and shop.inRange:
        chick.isShopping = True
    if chick.isShopping:
        level += shop.calculate_menu(chick, keys)
    elif level == 0:
        paused = True
        pause()
        level += 1
    if chick.alive and not chick.isShopping:
        chick.check_movement(chickProjectiles, keys)
    elif not chick.alive:
        chick.dead_grav()
        if chick.isGrounded:
            paused = True
    if level > lvl:
        if level == 1:
            level1()
            chick.change_score(-50)
        if level == 2:
            level2()
        if level == 3:
            level3()
        if level == 4:
            level4()
        if level == 5:
            level_boss1()
        if level == 6:
            chick.change_score(1000)
            won = True
            if chick.isGrounded:
                pause = True
        chick.change_score(50)
        shop.isVisible = False
    redraw()
    if paused:
        pause()

pygame.quit()
