import pygame
import random

framePerSec = 27
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
pygame.init()


# Classes
class Player(object):
    # Images
    walkLeft = [pygame.image.load('Chicken_Sprite/L1.png'), pygame.image.load('Chicken_Sprite/L2.png'),
                pygame.image.load('Chicken_Sprite/L3.png'), pygame.image.load('Chicken_Sprite/L4.png'),
                pygame.image.load('Chicken_Sprite/L5.png'), pygame.image.load('Chicken_Sprite/L6.png'),
                pygame.image.load('Chicken_Sprite/L7.png'), pygame.image.load('Chicken_Sprite/L8.png'),
                pygame.image.load('Chicken_Sprite/L9.png')]
    walkRight = [pygame.image.load('Chicken_Sprite/R1.png'), pygame.image.load('Chicken_Sprite/R2.png'),
                 pygame.image.load('Chicken_Sprite/R3.png'), pygame.image.load('Chicken_Sprite/R4.png'),
                 pygame.image.load('Chicken_Sprite/R5.png'), pygame.image.load('Chicken_Sprite/R6.png'),
                 pygame.image.load('Chicken_Sprite/R7.png'), pygame.image.load('Chicken_Sprite/R8.png'),
                 pygame.image.load('Chicken_Sprite/R9.png')]
    jetLeft = [pygame.image.load('Chicken_Sprite/LJet.png'),
               pygame.image.load('Chicken_Sprite/Shooting/LJS1.png')]
    jetRight = [pygame.image.load('Chicken_Sprite/RJet.png'),
                pygame.image.load('Chicken_Sprite/Shooting/RJS1.png')]
    shootLeft = [pygame.image.load('Chicken_Sprite/Shooting/LS1.png'),
                 pygame.image.load('Chicken_Sprite/Shooting/LS2.png'),
                 pygame.image.load('Chicken_Sprite/Shooting/LS3.png'),
                 pygame.image.load('Chicken_Sprite/Shooting/LS4.png'),
                 pygame.image.load('Chicken_Sprite/Shooting/LS5.png'),
                 pygame.image.load('Chicken_Sprite/Shooting/LS6.png'),
                 pygame.image.load('Chicken_Sprite/Shooting/LS7.png'),
                 pygame.image.load('Chicken_Sprite/Shooting/LS8.png'),
                 pygame.image.load('Chicken_Sprite/Shooting/LS9.png'), ]
    shootRight = [pygame.image.load('Chicken_Sprite/Shooting/RS1.png'),
                  pygame.image.load('Chicken_Sprite/Shooting/RS2.png'),
                  pygame.image.load('Chicken_Sprite/Shooting/RS3.png'),
                  pygame.image.load('Chicken_Sprite/Shooting/RS4.png'),
                  pygame.image.load('Chicken_Sprite/Shooting/RS5.png'),
                  pygame.image.load('Chicken_Sprite/Shooting/RS6.png'),
                  pygame.image.load('Chicken_Sprite/Shooting/RS7.png'),
                  pygame.image.load('Chicken_Sprite/Shooting/RS8.png'),
                  pygame.image.load('Chicken_Sprite/Shooting/RS9.png'), ]
    projectile = [pygame.image.load('Chicken_Sprite/Shooting/Drum-projectile-right.png'),
                  pygame.image.load('Chicken_Sprite/Shooting/Drum-projectile-left.png')]
    icons = [pygame.image.load('Icons/Heart.png'),
             pygame.image.load('Icons/LightningBolt.png'),
             pygame.image.load('Icons/GasCan.png'),
             pygame.image.load('Icons/Dead.png')]

    # Attributes
    healthMAX = 100
    energyMAX = 100
    fuelMAX = 80
    health = healthMAX
    energy = energyMAX
    fuel = fuelMAX
    regenableMultiplier = .3
    exhaustionMultiplier = .6
    fuelBufferMultiplier = .8
    maxHealthRegenerated = round(healthMAX * regenableMultiplier)
    energyCoolDownBuffer = round(energyMAX * exhaustionMultiplier)
    fuelCoolDownBuffer = round(fuelMAX * fuelBufferMultiplier)
    energyRecoveryRate = 1
    fuelRecoveryRate = 1
    shotSpeed = 8
    fireRateMultiplier = 1
    shootInt = framePerSec / 1.5 / fireRateMultiplier
    velX = 0
    velY = 0
    initVel = 5
    accX = 0
    accY = 0
    score = 0
    # Conditions
    alive = True
    healthRegen = False
    shot = False
    stunned = False
    sprinted = False
    isSprinting = False
    fuelCoolDown = False
    energyCoolDown = False
    isFly = False
    isJump = False
    collide = True
    isGrounded = False
    isShopping = False
    left = False
    right = True
    stuck = False
    stuckDelay = 0
    walkCount = 0
    stun = 0
    healthRegenDelay = 0

    def __init__(self, x, y, width, height):
        # Coordinates
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.lowerBound = SCREEN_HEIGHT
        self.hitBox = (self.x, self.y, width, height)

    def display_stats(self, window):
        pygame.draw.rect(window, (127, 127, 127), (0, 0, 100, 100))
        font = pygame.font.SysFont('Lucida Console', 15, True)
        text1 = font.render('Health', 1, (255, 0, 0))
        text2 = font.render('Energy', 1, (255, 255, 0))
        text3 = font.render('Fuel', 1, (0, 0, 255))
        if self.health < 0: self.health = 0
        if self.energy < 0: self.energy = 0
        if self.fuel < 0: self.fuel = 0

        # Health bar
        window.blit(text1, (10, 10))
        window.blit(self.icons[0], (14 + text1.get_width(), 12))
        pygame.draw.rect(window, (255, 0, 0), (10, 25, self.healthMAX // 2, 10))  # Red bar
        if self.health > 0:
            pygame.draw.rect(window, (0, 255, 0),
                             (10, 25, round(self.healthMAX / 2 * (self.health / self.healthMAX)), 10))  # Green bar
        pygame.draw.rect(window, (255, 25, 25), (10 + self.maxHealthRegenerated // 2, 55, 1, 10))  # Regen buffer bar

        # Energy bar
        window.blit(text2, (10, 40))
        window.blit(self.icons[1], (14 + text2.get_width(), 40))
        pygame.draw.rect(window, (255, 0, 0), (10, 55, self.energyMAX // 2, 10))  # Red bar
        if self.energy > 0:
            pygame.draw.rect(window, (0, 255, 0),
                             (10, 55, round(self.energyMAX / 2 * (self.energy / self.energyMAX)), 10))  # Green bar
        pygame.draw.rect(window, (0, 0, 255), (10 + self.energyCoolDownBuffer // 2, 55, 1, 10))  # Blue buffer bar

        # Fuel bar (no not the protein bar)
        window.blit(text3, (10, 70))
        window.blit(self.icons[2], (14 + text3.get_width(), 70))
        pygame.draw.rect(window, (255, 0, 0), (10, 85, self.fuelMAX // 2, 10))  # Red bar
        if self.fuel > 0:
            pygame.draw.rect(window, (0, 255, 0),
                             (10, 85, round(self.fuelMAX / 2 * (self.fuel / self.fuelMAX)), 10))  # Green bar
        pygame.draw.rect(window, (0, 0, 255), (10 + self.fuelCoolDownBuffer // 2, 85, 1, 10))  # Blue buffer bar

    def draw(self, window):
        if self.walkCount + 1 >= 27 or self.isShopping or self.isJump or self.isFly or not self.isGrounded:
            self.walkCount = 0
        if self.alive:
            if not self.shot:
                if self.isFly:
                    if self.left:
                        window.blit(self.jetLeft[0], (self.x, self.y))
                    elif self.right:
                        window.blit(self.jetRight[0], (self.x, self.y))
                elif self.left:
                    window.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                    if self.isSprinting:
                        self.walkCount += 2
                    else:
                        self.walkCount += 1
                elif self.right:
                    window.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                    if self.isSprinting:
                        self.walkCount += 2
                    else:
                        self.walkCount += 1
            else:
                if self.isFly:
                    if self.left:
                        window.blit(self.jetLeft[1], (self.x, self.y))
                    elif self.right:
                        window.blit(self.jetRight[1], (self.x, self.y))
                elif self.left:
                    window.blit(self.shootLeft[self.walkCount // 3], (self.x, self.y))
                    if self.isSprinting:
                        self.walkCount += 2
                    else:
                        self.walkCount += 1
                elif self.right:
                    window.blit(self.shootRight[self.walkCount // 3], (self.x, self.y))
                    if self.isSprinting:
                        self.walkCount += 2
                    else:
                        self.walkCount += 1
            # (hitbox) pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.height), 2)
        else:
            window.blit(self.icons[3], (self.x, self.y))

    def hit(self, num):
        if not self.stunned:
            self.health -= num
            self.stunned = True
            self.shot = True
            self.shootInt = framePerSec / 1.5 / self.fireRateMultiplier
            self.healthRegenDelay = framePerSec * 3
            if self.health <= 0:
                self.alive = False

    def check_movement(self, projectiles, keys):
        self.check_status()
        # Gravity
        if self.y < self.lowerBound - self.height:
            self.accY = .9
        else:
            self.accY = 0
            self.velY = 0
        # Determining moving left and right
        if keys[pygame.K_LEFT] and self.x > 0:
            self.velX = -self.initVel
            self.left = True
            self.right = False
        elif keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.velX = self.initVel
            self.right = True
            self.left = False
        else:
            self.walkCount = 0
            self.velX = 0
        # Move down a platform by turning off collision
        if keys[pygame.K_DOWN]:
            self.collide = False
        else:
            self.collide = True

        # Using the jetPack
        fuelDec = 2.8
        if keys[pygame.K_UP] and self.fuel > 0 and not self.fuelCoolDown:
            self.fuel -= fuelDec
            self.velY = -self.initVel
            self.accY = 0
            self.isFly = True
            self.isGrounded = False
        else:
            self.isFly = False
            if self.fuel < self.fuelMAX:
                self.fuel += 1 * self.fuelRecoveryRate
                if self.fuel >= self.fuelCoolDownBuffer:
                    self.fuelCoolDown = False

        # Jumping
        if keys[pygame.K_SPACE] and not self.isJump and self.energy > 0 \
                and not self.energyCoolDown and not self.isFly and self.isGrounded and self.velY == 0:
            self.isJump = True
            self.energy -= 10
            self.velY -= 10
        if self.isJump and not self.isFly:
            self.walkCount = 0
            if self.velY == 0 and self.isGrounded:
                self.isJump = False

        # Sprinting
        if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) and self.energy > 0 and not self.energyCoolDown:
            self.isSprinting = True
            if self.left and self.initVel * -2 <= self.velX <= -self.initVel:
                self.accX = -2
            elif self.right and self.initVel * 2 >= self.velX >= self.initVel:
                self.accX = 2
            self.energy -= 2
        else:
            self.accX = 0
            self.isSprinting = False
            if self.energy < self.energyMAX:
                self.energy += 1 * self.energyRecoveryRate

        # Shooting
        if keys[pygame.K_f] and not self.shot:
            self.shoot(projectiles)

        # Movement
        if (self.x < 0 or self.x + self.width > SCREEN_WIDTH) and self.stuckDelay <= 0:
            self.accX = 0
            self.velX = 0
            self.stuckDelay = 5
        if self.stuckDelay > 0:
            self.stuckDelay -= 1

        if self.isGrounded:
            if self.velX >= 12:
                self.accY = 0
            elif self.velX <= -self.initVel - 1:
                self.velX += 1

        if self.velY >= self.initVel + .1:
            self.velY -= .3
        elif self.velY <= -self.initVel * 3 - .1:
            self.velY += .1

        self.velX += self.accX
        self.velY += self.accY
        self.x += self.velX
        self.y += self.velY

    def check_status(self):
        # Shooting
        if self.shot:
            if self.shootInt > 0:
                self.shootInt -= 1
            else:
                self.shootInt = (framePerSec / 1.5) / self.fireRateMultiplier
                self.shot = False
        if self.stun > 0:
            self.stun -= 1
        else:
            self.stunned = False
            self.stun = 20

        # Health and Regen
        if self.alive and self.health < self.maxHealthRegenerated and self.healthRegenDelay <= 0:
            self.health += 1
        elif not self.stunned:
            self.healthRegenDelay -= 1
        if self.health <= 0:
            self.alive = False
        # Energy
        if self.energy <= 0:
            self.energyCoolDown = True
        elif self.energy >= self.energyCoolDownBuffer:
            self.energyCoolDown = False
        # Fuel
        if self.fuel <= 0:
            self.fuelCoolDown = True

    def shoot(self, projectiles):
        self.shot = True
        if self.left:
            projectiles.append(
                Projectile(self.x, self.y + 20, 20, 10, self.projectile[1], self.shotSpeed, -1))
        elif self.right:
            projectiles.append(
                Projectile(self.x + self.width - 8, self.y + 20, 20, 10, self.projectile[0], self.shotSpeed, 1))

    def recover_health(self):
        self.health = self.healthMAX

    def change_health_max(self, num):
        self.healthMAX += num
        self.health += num
        self.change_max_health_regenerated(0)

    def change_max_health_regenerated(self, num):
        self.regenableMultiplier += num
        if self.regenableMultiplier > 1:
            self.regenableMultiplier = 1
        self.maxHealthRegenerated = round(self.healthMAX * self.regenableMultiplier)

    def change_max_energy(self, num):
        self.energyMAX += num
        self.change_energy_cool_down_buffer(0)

    def change_energy_recovery(self, num):
        self.energyRecoveryRate += num

    def change_energy_cool_down_buffer(self, num):
        self.exhaustionMultiplier += num
        if self.exhaustionMultiplier < 0:
            self.exhaustionMultiplier = 0
        elif self.exhaustionMultiplier > 1:
            self.exhaustionMultiplier = 1
        self.energyCoolDownBuffer = round(self.energyMAX * self.exhaustionMultiplier)

    def change_fuel_capacity(self, num):
        self.fuelMAX += num
        self.change_fuel_cool_down_buffer(0)

    def change_fuel_recovery(self, num):
        self.fuelRecoveryRate += num

    def change_fuel_cool_down_buffer(self, num):
        self.fuelBufferMultiplier += num
        if self.fuelBufferMultiplier < 0:
            self.fuelBufferMultiplier = 0
        elif self.fuelBufferMultiplier > 1:
            self.fuelBufferMultiplier = 1
        self.fuelCoolDownBuffer = round(self.fuelMAX * self.fuelBufferMultiplier)

    def change_movement_speed(self, num):
        self.initVel += num

    def change_shot_speed(self, num):
        self.shotSpeed += num

    def change_fire_rate(self, num):
        self.fireRateMultiplier += num
        self.shootInt = (framePerSec // 2) / self.fireRateMultiplier

    def change_score(self, num):
        self.score += num

    def dead_grav(self):
        # Gravity
        if self.y < self.lowerBound - self.height:
            self.accY = .9
        else:
            self.accY = 0
            self.velY = 0
        if (self.x < 0 or self.x + self.width > SCREEN_WIDTH) and self.stuckDelay <= 0:
            self.accX = 0
            self.velX = 0
            self.stuckDelay = 5
        if self.stuckDelay > 0:
            self.stuckDelay -= 1

        if self.isGrounded:
            if self.velX >= 12:
                self.accY = 0
            elif self.velX <= -self.initVel - 1:
                self.velX += 1

        if self.velY >= self.initVel + .1:
            self.velY -= .3
        elif self.velY <= -self.initVel * 3 - .1:
            self.velY += .1

        self.velX += self.accX
        self.velY += self.accY
        self.x += self.velX
        self.y += self.velY


class Enemy(object):
    walkLeft = [pygame.image.load('Wolf_Sprite/WL1.png'), pygame.image.load('Wolf_Sprite/WL2.png'),
                pygame.image.load('Wolf_Sprite/WL3.png'), pygame.image.load('Wolf_Sprite/WL4.png'),
                pygame.image.load('Wolf_Sprite/WL5.png'), pygame.image.load('Wolf_Sprite/WL6.png'),
                pygame.image.load('Wolf_Sprite/WL7.png'), pygame.image.load('Wolf_Sprite/WL8.png'),
                pygame.image.load('Wolf_Sprite/WL9.png')]
    walkRight = [pygame.image.load('Wolf_Sprite/WR1.png'), pygame.image.load('Wolf_Sprite/WR2.png'),
                 pygame.image.load('Wolf_Sprite/WR3.png'), pygame.image.load('Wolf_Sprite/WR4.png'),
                 pygame.image.load('Wolf_Sprite/WR5.png'), pygame.image.load('Wolf_Sprite/WR6.png'),
                 pygame.image.load('Wolf_Sprite/WR7.png'), pygame.image.load('Wolf_Sprite/WR8.png'),
                 pygame.image.load('Wolf_Sprite/WR9.png')]
    projectile = [pygame.image.load('Wolf_Sprite/Fork-Projectile-Left.png'),
                  pygame.image.load('Wolf_Sprite/Fork-Projectile-Right.png')]

    width = 75
    height = 100
    shot = False
    shootInt = 0
    vel = 3
    walkCount = 0
    healthMAX = 100
    health = healthMAX
    delay = round(30 * random.random() + 20)
    shootStopDelay = 0

    def __init__(self, x, y, *path):
        self.x = x
        self.y = y
        self.hitBox = (self.x, self.y, self.x + self.width, self.y + self.height)
        if len(path) == 1:
            path = (self.x, path[0])
        self.path = path

    def draw(self, window):
        self.move()
        if self.walkCount + 1 >= 27:
            self.walkCount = 0
        if self.vel > 0:
            window.blit(self.walkRight[round(self.walkCount) // 3], (self.x, self.y))
        elif self.vel < 0:
            window.blit(self.walkLeft[round(self.walkCount) // 3], (self.x, self.y))
        pygame.draw.rect(window, (255, 0, 0), (
            self.x + (self.width - self.healthMAX // 2) // 2, self.y - 10, self.healthMAX // 2, 7))  # Red bar
        pygame.draw.rect(window, (0, 255, 0),
                         (self.x + (self.width - self.healthMAX // 2) // 2, self.y - 10,
                          round(self.healthMAX / 2 * (self.health / self.healthMAX)),
                          7))  # Green bar

    def move(self):
        if self.shot:
            self.walkCount = 0
            self.shootStopDelay = 45
        if self.vel > 0 >= self.shootStopDelay:
            if self.x + self.vel < max(self.path):
                self.x += self.vel
                self.walkCount += 1
            else:
                if self.delay > 0:
                    self.delay -= 1
                    self.walkCount = 0
                else:
                    self.vel *= -1
                    self.walkCount = 0
                    self.delay = round(30 * random.random() + 20)
        elif self.vel < 0 and self.shootStopDelay <= 0:
            if self.x - self.vel > min(self.path):
                self.x += self.vel
                self.walkCount += 1
            else:
                if self.delay > 0:
                    self.delay -= 1
                    self.walkCount = 0
                else:
                    self.vel *= -1
                    self.walkCount = 0
                    self.delay = round(30 * random.random() + 20)
        if self.shootStopDelay > 0:
            self.shootStopDelay -= 1

    def hit(self):
        self.health -= 10

    def shoot(self, projectiles):
        if self.vel > 0:
            projectiles.append(Projectile(self.x + self.width, self.y + 33, 35, 10, self.projectile[1], 8, 1))
        elif self.vel < 0:
            projectiles.append(Projectile(self.x, self.y + 33, 35, 10, self.projectile[0], 8, -1))
        self.shot = True
        self.shootInt = 20


class Boss(Enemy):
    walkLeft = [pygame.image.load('Boss_Sprite/BL1.png'), pygame.image.load('Boss_Sprite/BL2.png'),
                pygame.image.load('Boss_Sprite/BL3.png'), pygame.image.load('Boss_Sprite/BL4.png'),
                pygame.image.load('Boss_Sprite/BL5.png'), pygame.image.load('Boss_Sprite/BL6.png'),
                pygame.image.load('Boss_Sprite/BL7.png'), pygame.image.load('Boss_Sprite/BL8.png'),
                pygame.image.load('Boss_Sprite/BL9.png')]
    walkRight = [pygame.image.load('Boss_Sprite/BR1.png'), pygame.image.load('Boss_Sprite/BR2.png'),
                 pygame.image.load('Boss_Sprite/BR3.png'), pygame.image.load('Boss_Sprite/BR4.png'),
                 pygame.image.load('Boss_Sprite/BR5.png'), pygame.image.load('Boss_Sprite/BR6.png'),
                 pygame.image.load('Boss_Sprite/BR7.png'), pygame.image.load('Boss_Sprite/BR8.png'),
                 pygame.image.load('Boss_Sprite/BR9.png')]
    projectile = [pygame.image.load('Boss_Sprite/Knife-projectile-left.png'),
                  pygame.image.load('Boss_Sprite/Knife-projectile-right.png')]

    width = 120
    height = 160
    healthMAX = 150
    health = healthMAX
    vel = 2

    def __init__(self, x, y, *path):
        super()
        self.x = x
        self.y = y
        self.hitBox = (self.x, self.y, self.x + self.width, self.y + self.height)
        if len(path) == 1:
            path = (self.x, path[0])
        self.path = path

    def shoot(self, projectiles):
        if self.vel > 0:
            projectiles.append(Projectile(self.x + self.width, self.y + self.height//2, 35, 10, self.projectile[1], 8, 1))
        elif self.vel < 0:
            projectiles.append(Projectile(self.x, self.y + self.height//2, 35, 10, self.projectile[0], 8, -1))
        self.shot = True
        self.shootInt = 15

    def move(self):
        if self.shot:
            self.walkCount = 0
            self.shootStopDelay = 45
        if self.vel > 0 >= self.shootStopDelay:
            if self.x + self.vel < max(self.path):
                self.x += self.vel
                self.walkCount += .66
            else:
                if self.delay > 0:
                    self.delay -= 1
                    self.walkCount = 0
                else:
                    self.vel *= -1
                    self.walkCount = 0
                    self.delay = round(30 * random.random() + 20)
        elif self.vel < 0 and self.shootStopDelay <= 0:
            if self.x - self.vel > min(self.path):
                self.x += self.vel
                self.walkCount += .66
            else:
                if self.delay > 0:
                    self.delay -= 1
                    self.walkCount = 0
                else:
                    self.vel *= -1
                    self.walkCount = 0
                    self.delay = round(30 * random.random() + 20)
        if self.shootStopDelay > 0:
            self.shootStopDelay -= 1
    def hit(self):
        self.health -= 5
        if self.shootStopDelay <= 0:
            self.vel *= -1


class Platform(object):
    platform = pygame.image.load("Background/platform.png")
    height = 20

    def __init__(self, x, y, width):
        self.x = x
        self.y = y
        self.width = width
        self.hitBox = (self.x, self.y, width, self.height)

    def draw(self, window):
        x = 0
        while x < self.width:
            window.blit(self.platform, (self.x + x, self.y, 10, 20))
            x += 10
        # For seeing location
        # font = pygame.font.SysFont('Lucida Console', 10, True)
        # text1 = font.render('(' + str(round(self.x)) + ', ', 1, (0, 0, 0))
        # text2 = font.render(str(self.y) + ')', 1, (0, 0, 0))
        # text3 = font.render(str(self.width), 1, (0, 0, 0))
        # window.blit(text1, (round(self.x), self.y - 10))
        # window.blit(text2, (self.x + text1.get_width(), self.y - 10))
        # window.blit(text3, (self.x + self.width - text3.get_width(), self.y - 10))


class Projectile(object):
    velY = 0
    accY = 0

    def __init__(self, x, y, width, height, picture, vel, facing):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.picture = picture
        self.facing = facing
        self.vel = vel * facing

    def draw(self, window, projectiles, *playerCords):
        self.move(projectiles, playerCords)
        window.blit(self.picture, (self.x, self.y))

    def move(self, projectiles, *playerCords):
        if self.picture == Boss.projectile[0] or self.picture == Boss.projectile[1]:
            if playerCords[0][1] + 30 < self.y and playerCords[0][0] < self.x:
                self.accY = -.12
            elif playerCords[0][1] + 30 > self.y and playerCords[0][0] < self.x:
                self.accY = .12
            elif playerCords[0][1] + 30 < self.y and playerCords[0][0] + 20 > self.x:
                self.accY = -.12
            elif playerCords[0][1] + 30 > self.y and playerCords[0][0] + 20 > self.x:
                self.accY = .12
            if playerCords[0][1] + 40 >= self.y and playerCords[0][1] + 20 <= self.y + self.height:
                if self.vel > 0 and self.x <= playerCords[0][0] or self.vel < 0 and self.x >= playerCords[0][0] + 40:
                    self.velY = self.accY
            self.velY += self.accY
            self.y += self.velY
        if self.x + self.width <= 0 or self.x >= SCREEN_WIDTH:
            projectiles.remove(self)
        self.x += self.vel


class Shop(object):
    pics = [pygame.image.load('Shop_Sprite/B_Shop.png'),
            pygame.image.load('Shop_Sprite/P_Shop.png')]
    menu = [pygame.image.load('Shop_Sprite/Main_Menu.png'),
            pygame.image.load('Shop_Sprite/Health_Menu.png'),
            pygame.image.load('Shop_Sprite/Energy_Menu.png'),
            pygame.image.load('Shop_Sprite/Fuel_Menu.png'),
            pygame.image.load('Shop_Sprite/Other_Menu.png'),
            pygame.image.load('Shop_Sprite/Health_Menu_Advanced.png'),
            pygame.image.load('Shop_Sprite/Energy_Menu_Advanced.png'),
            pygame.image.load('Shop_Sprite/Fuel_Menu_Advanced.png'),
            pygame.image.load('Shop_Sprite/Other_Menu_Advanced.png')]

    isVisible = False
    inRange = False
    advanced = False
    health = False
    energy = False
    fuel = False
    other = False
    buttonDelay = 0

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, window, player):
        if self.isVisible:
            if self.inRange and not player.isShopping:
                window.blit(self.pics[1], (self.x, self.y))
            else:
                window.blit(self.pics[0], (self.x, self.y))

    def display_menu(self, window, player):
        font = pygame.font.SysFont('Lucida Console', 20, )
        if player.isShopping:
            if self.health:
                if self.advanced:
                    window.blit(self.menu[5], (150, 50))
                    window.blit(font.render(str(player.health), 1, (0, 0, 0)), (267, 363))
                    window.blit(font.render(str(player.healthMAX), 1, (0, 0, 0)), (318, 363))
                    window.blit(font.render(str(player.healthMAX), 1, (0, 0, 0)), (290, 465))
                    window.blit(font.render(str(round(player.regenableMultiplier * 100)) + '%', 1, (0, 0, 0)),
                                (290, 587))
                else:
                    window.blit(self.menu[1], (150, 50))
            elif self.energy:
                if self.advanced:
                    window.blit(self.menu[6], (150, 50))
                    window.blit(font.render(str(player.energyMAX), 1, (0, 0, 0)), (290, 363))
                    window.blit(font.render(str(round(player.energyRecoveryRate * 100)) + '%', 1, (0, 0, 0)),
                                (289, 478))
                    window.blit(font.render(str(round(player.exhaustionMultiplier * 100)) + '%', 1, (0, 0, 0)),
                                (292, 587))
                else:
                    window.blit(self.menu[2], (150, 50))
            elif self.fuel:
                if self.advanced:
                    window.blit(self.menu[7], (150, 50))
                    window.blit(font.render(str(player.fuelMAX), 1, (0, 0, 0)), (294, 361))
                    window.blit(font.render(str(round(player.fuelRecoveryRate * 100)) + '%', 1, (0, 0, 0)),
                                (290, 470))
                    window.blit(font.render(str(round(player.fuelBufferMultiplier * 100)) + '%', 1, (0, 0, 0)),
                                (292, 583))
                else:
                    window.blit(self.menu[3], (150, 50))
            elif self.other:
                if self.advanced:
                    window.blit(self.menu[8], (150, 50))
                    window.blit(font.render(str(round(player.fireRateMultiplier * 100)) + '%', 1, (0, 0, 0)),
                                (290, 363))
                    window.blit(font.render(str(player.initVel), 1, (0, 0, 0)),
                                (295, 467))
                    window.blit(font.render(str(player.shotSpeed), 1, (0, 0, 0)),
                                (295, 582))
                else:
                    window.blit(self.menu[4], (150, 50))
            else:
                window.blit(self.menu[0], (150, 50))

    def calculate_menu(self, player, keys):
        if self.health:
            if keys[pygame.K_a] and self.buttonDelay <= 0:
                self.advanced = not self.advanced
                self.buttonDelay = framePerSec // 2
            if keys[pygame.K_h] and self.buttonDelay <= 0:
                self.health = False
                player.isShopping = False
                self.buttonDelay = framePerSec // 2
                player.recover_health()
                print("health recovered")
                return 1
            elif keys[pygame.K_j] and self.buttonDelay <= 0:
                self.health = False
                player.isShopping = False
                self.buttonDelay = framePerSec // 2
                player.change_health_max(10)
                print("increased max health")
                return 1
            elif keys[pygame.K_k] and self.buttonDelay <= 0:
                self.health = False
                player.isShopping = False
                self.buttonDelay = framePerSec // 2
                player.change_max_health_regenerated(.05)
                print('increased healthRegenBuffer')
                return 1
            elif keys[pygame.K_b] and self.buttonDelay <= 0:
                self.health = False
                self.buttonDelay = framePerSec // 2
        elif (keys[pygame.K_h]) and not (self.energy or self.fuel or self.other) and self.buttonDelay <= 0:
            self.buttonDelay = framePerSec // 2
            self.health = True
            print('choose health')

        if self.energy:
            if keys[pygame.K_a] and self.buttonDelay <= 0:
                self.advanced = not self.advanced
                self.buttonDelay = framePerSec // 2
            if keys[pygame.K_h] and self.buttonDelay <= 0:
                self.energy = False
                player.isShopping = False
                self.buttonDelay = framePerSec // 2
                player.change_max_energy(10)
                print('increased max energy')
                return 1
            elif keys[pygame.K_j] and self.buttonDelay <= 0:
                self.energy = False
                player.isShopping = False
                self.buttonDelay = framePerSec // 2
                player.change_energy_recovery(.2)
                print('increased energy recovery rate')
                return 1
            elif keys[pygame.K_k] and self.buttonDelay <= 0:
                self.energy = False
                player.isShopping = False
                self.buttonDelay = framePerSec // 2
                player.change_energy_cool_down_buffer(-.15)
                print('increased energy exhaustion buffer')
                return 1
            elif keys[pygame.K_b] and self.buttonDelay <= 0:
                self.energy = False
                self.buttonDelay = framePerSec // 2
        elif (keys[pygame.K_j]) and not (self.health or self.fuel or self.other) and self.buttonDelay <= 0:
            self.energy = True
            self.buttonDelay = framePerSec // 2
            print('choose energy')

        if self.fuel:
            if keys[pygame.K_a] and self.buttonDelay <= 0:
                self.advanced = not self.advanced
                self.buttonDelay = framePerSec // 2
            if keys[pygame.K_h] and self.buttonDelay <= 0:
                self.fuel = False
                player.isShopping = False
                self.buttonDelay = framePerSec // 2
                player.change_fuel_capacity(10)
                print('increased max fuel')
                return 1
            elif keys[pygame.K_j] and self.buttonDelay <= 0:
                self.fuel = False
                player.isShopping = False
                self.buttonDelay = framePerSec // 2
                player.change_fuel_recovery(.2)
                print('increased fuel recovery rate')
                return 1
            elif keys[pygame.K_k] and self.buttonDelay <= 0:
                self.fuel = False
                player.isShopping = False
                self.buttonDelay = framePerSec // 2
                player.change_fuel_cool_down_buffer(-.15)
                print('increased fuel exhaustion buffer')
                return 1
            elif keys[pygame.K_b] and self.buttonDelay <= 0:
                self.fuel = False
                self.buttonDelay = framePerSec // 2
        elif keys[pygame.K_k] and not (self.energy or self.health or self.other) and self.buttonDelay <= 0:
            self.fuel = True
            self.buttonDelay = framePerSec // 2
            print('choose fuel')

        if self.other:
            if keys[pygame.K_a] and self.buttonDelay <= 0:
                self.advanced = not self.advanced
                self.buttonDelay = framePerSec // 2
            if keys[pygame.K_h] and self.buttonDelay <= 0:
                self.other = False
                player.isShopping = False
                self.buttonDelay = framePerSec // 2
                player.change_fire_rate(.15)
                print('decreased shot cool down')
                return 1
            elif keys[pygame.K_j] and self.buttonDelay <= 0:
                self.other = False
                player.isShopping = False
                self.buttonDelay = framePerSec // 2
                player.change_movement_speed(1)
                print('increase movement speed')
                return 1
            elif keys[pygame.K_k] and self.buttonDelay <= 0:
                self.other = False
                player.isShopping = False
                self.buttonDelay = framePerSec // 2
                player.change_shot_speed(2)
                print('increase bullet speed')
                return 1
            elif keys[pygame.K_b] and self.buttonDelay <= 0:
                self.other = False
                self.buttonDelay = framePerSec // 2
        if (keys[pygame.K_l]) and not (self.energy or self.fuel or self.health) and self.buttonDelay <= 0:
            self.other = True
            self.buttonDelay = framePerSec // 2
            print('choose other')

        elif keys[pygame.K_b] and self.buttonDelay <= 0:
            player.isShopping = False
            player.change_score(30)
            return 1
        if self.buttonDelay > 0:
            self.buttonDelay -= 1
        return 0
