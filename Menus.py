import pygame
from Classes import SCREEN_WIDTH
import gspread
from oauth2client.service_account import ServiceAccountCredentials

name = ""
named = False
# Google sheet info
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("Fried Chicken Scores").sheet1

data = sheet.get_all_records()
print(data)


# I got this class from Stackoverflow user skrx, I modified the class to my needs but I do not take full credit for
# the Input Box class
class InputBox:
    COLOR_INACTIVE = (190, 190, 190)
    COLOR_ACTIVE = (0, 0, 0)
    FONT = pygame.font.SysFont('Lucida Console', 15, True)

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = self.COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                txt = self.text
                print(self.text)
                self.text = ''
                return txt
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            # Re-render the text.
            self.txt_surface = self.FONT.render(self.text, True, self.color)
            return ""

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface,
                    (self.rect.x + self.rect.width // 2 - self.txt_surface.get_width() // 2, self.rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


nameBox = InputBox(400, 420, 200, 20, '')


def name_screen(win, event):
    global name, hasName

    pygame.draw.rect(win, (100, 100, 100), (300, 150, 400, 500))
    pygame.draw.rect(win, (0, 0, 0), (300, 150, 400, 500), 1)
    pygame.draw.rect(win, (0, 0, 0), (300, 150, 400, 180), 1)
    font1 = pygame.font.SysFont('showcardgothic', 70, True)
    font2 = pygame.font.SysFont('Lucida Console', 20, True)
    text1 = font1.render('FRIED', 1, (255, 255, 255))
    text2 = font1.render('CHICKEN', 1, (255, 255, 255))
    text3 = font2.render('Please enter your first', 1, (255, 255, 255))
    text4 = font2.render('name and last initial,', 1, (255, 255, 255))
    text5 = font2.render('then hit ENTER.', 1, (255, 255, 255))
    win.blit(text1, (SCREEN_WIDTH // 2 - text1.get_width() // 2, 180))
    win.blit(text2, (SCREEN_WIDTH // 2 - text2.get_width() // 2, 250))
    win.blit(text3, (SCREEN_WIDTH // 2 - text3.get_width() // 2, 350))
    win.blit(text4, (SCREEN_WIDTH // 2 - text4.get_width() // 2, 370))
    win.blit(text5, (SCREEN_WIDTH // 2 - text5.get_width() // 2, 390))
    if event is not None:
        name = nameBox.handle_event(event)
    nameBox.update()
    nameBox.draw(win)
    if name:
        return False
    else:
        return True


def start_menu(win):
    pygame.draw.rect(win, (100, 100, 100), (300, 150, 400, 500))
    pygame.draw.rect(win, (0, 0, 0), (300, 150, 400, 500), 1)
    font1 = pygame.font.SysFont('showcardgothic', 70, True)
    font2 = pygame.font.SysFont('Lucida Console', 20, True)
    text1 = font1.render('FRIED', 1, (255, 255, 255))
    text6 = font1.render('CHICKEN', 1, (255, 255, 255))
    text2 = font2.render('Press \'H\' to PLAY.', 1, (255, 255, 255))
    text4 = font2.render('Press \'K\' for HELP.', 1, (255, 255, 255))
    text3 = font2.render('Press \'J\' for CONTROLS.', 1, (255, 255, 255))
    text5 = font2.render('Press \'L\' to QUIT.', 1, (255, 255, 255))
    win.blit(text1, (SCREEN_WIDTH // 2 - text1.get_width() // 2, 180))
    win.blit(text6, (SCREEN_WIDTH // 2 - text6.get_width() // 2, 250))
    win.blit(text2, (SCREEN_WIDTH // 2 - text2.get_width() // 2, 350))
    win.blit(text3, (SCREEN_WIDTH // 2 - text3.get_width() // 2, 425))
    win.blit(text4, (SCREEN_WIDTH // 2 - text4.get_width() // 2, 500))
    win.blit(text5, (SCREEN_WIDTH // 2 - text5.get_width() // 2, 575))
    pygame.draw.rect(win, (0, 0, 0), (300, 325, 400, 76), 1)
    pygame.draw.rect(win, (0, 0, 0), (300, 400, 400, 76), 1)
    pygame.draw.rect(win, (0, 0, 0), (300, 475, 400, 76), 1)
    pygame.draw.rect(win, (0, 0, 0), (300, 550, 400, 76), 1)


def pause_menu(win):
    pygame.draw.rect(win, (100, 100, 100), (300, 150, 400, 500))
    pygame.draw.rect(win, (0, 0, 0), (300, 150, 400, 500), 1)
    font1 = pygame.font.SysFont('showcardgothic', 75, True)
    font2 = pygame.font.SysFont('Lucida Console', 20, True)
    text1 = font1.render('PAUSED', 1, (255, 255, 255))
    text2 = font2.render('Press \'H\' to RESUME.', 1, (255, 255, 255))
    text4 = font2.render('Press  \'K\' for HELP.', 1, (255, 255, 255))
    text3 = font2.render('Press \'J\' for CONTROLS.', 1, (255, 255, 255))
    text5 = font2.render('Press \'L\' to QUIT.', 1, (255, 255, 255))
    win.blit(text1, (SCREEN_WIDTH // 2 - text1.get_width() // 2, 200))
    win.blit(text2, (SCREEN_WIDTH // 2 - text2.get_width() // 2, 350))
    win.blit(text3, (SCREEN_WIDTH // 2 - text3.get_width() // 2, 425))
    win.blit(text4, (SCREEN_WIDTH // 2 - text4.get_width() // 2, 500))
    win.blit(text5, (SCREEN_WIDTH // 2 - text5.get_width() // 2, 575))
    pygame.draw.rect(win, (0, 0, 0), (300, 325, 400, 76), 1)
    pygame.draw.rect(win, (0, 0, 0), (300, 400, 400, 76), 1)
    pygame.draw.rect(win, (0, 0, 0), (300, 475, 400, 76), 1)
    pygame.draw.rect(win, (0, 0, 0), (300, 550, 400, 76), 1)


def controls_menu(win):
    pygame.draw.rect(win, (100, 100, 100), (300, 150, 400, 500))
    pygame.draw.rect(win, (0, 0, 0), (300, 150, 400, 500), 1)
    pygame.draw.rect(win, (0, 0, 0), (300, 150, 400, 90), 1)
    pygame.draw.rect(win, (0, 0, 0), (300, 600, 400, 50), 1)
    font1 = pygame.font.SysFont('showcardgothic', 50, True)
    font2 = pygame.font.SysFont('Lucida Console', 20, True)

    texts = [
        font1.render('Controls', 1, (255, 255, 255)),
        font2.render('    →     to move RIGHT   ', 1, (255, 255, 255)),
        font2.render('    ←     to move LEFT    ', 1, (255, 255, 255)),
        font2.render('    ↑     to use JET PACK ', 1, (255, 255, 255)),
        font2.render('    ↓     to jump DOWN    ', 1, (255, 255, 255)),
        font2.render(' \'SPACE\'  to JUMP         ', 1, (255, 255, 255)),
        font2.render(' \'SHIFT\'  to SPRINT       ', 1, (255, 255, 255)),
        font2.render('   \'F\'    to SHOOT        ', 1, (255, 255, 255)),
        font2.render('  \'ESC\'   to PAUSE        ', 1, (255, 255, 255)),
        font2.render('Press \'B\' to RETURN.', 1, (255, 255, 255))
    ]
    win.blit(texts[0], (SCREEN_WIDTH // 2 - texts[0].get_width() // 2, 175))
    win.blit(texts[len(texts) - 1], (SCREEN_WIDTH // 2 - texts[len(texts) - 1].get_width() // 2, 615))
    y = 260
    for i in range(1, len(texts) - 1):
        win.blit(texts[i], (SCREEN_WIDTH // 2 - texts[i].get_width() // 2, y))
        y += 42


def help_menu(win):
    pygame.draw.rect(win, (100, 100, 100), (300, 150, 400, 500))
    pygame.draw.rect(win, (0, 0, 0), (300, 150, 400, 500), 1)
    pygame.draw.rect(win, (0, 0, 0), (300, 150, 400, 90), 1)
    pygame.draw.rect(win, (0, 0, 0), (300, 600, 400, 50), 1)
    font1 = pygame.font.SysFont('showcardgothic', 50, True)
    font2 = pygame.font.SysFont('Lucida Console', 15, True)
    texts = [font1.render('Help', 1, (255, 255, 255)),
             font2.render('The goal is to get past all of', 1, (255, 255, 255)),
             font2.render('the wolves by shooting all of them.', 1, (255, 255, 255)),
             font2.render('You can move up either by jumping or', 1, (255, 255, 255)),
             font2.render('using your jet pack or move down to', 1, (255, 255, 255)),
             font2.render('drop off platforms. After each level', 1, (255, 255, 255)),
             font2.render('you can get upgrades or refill your', 1, (255, 255, 255)),
             font2.render('health, however if you pass the', 1, (255, 255, 255)),
             font2.render('opportunity you get a bonus to your', 1, (255, 255, 255)),
             font2.render('score. Once you beat the final boss,', 1, (255, 255, 255)),
             font2.render('check and compare your final score', 1, (255, 255, 255)),
             font2.render('with everyone else on the google sheet.', 1, (255, 255, 255)),
             font2.render('Press \'B\' to RETURN.', 1, (255, 255, 255))]

    win.blit(texts[0], (SCREEN_WIDTH // 2 - texts[0].get_width() // 2, 175))
    win.blit(texts[len(texts) - 1], (SCREEN_WIDTH // 2 - texts[len(texts) - 1].get_width() // 2, 615))
    y = 260
    for i in range(1, len(texts) - 1):
        win.blit(texts[i], (SCREEN_WIDTH // 2 - texts[i].get_width() // 2, y))
        y += 30


def win_menu(win, score, attempt):
    global name, found, named
    pygame.draw.rect(win, (100, 100, 100), (300, 150, 400, 500))
    pygame.draw.rect(win, (0, 0, 0), (300, 150, 400, 500), 1)
    pygame.draw.rect(win, (0, 0, 0), (300, 150, 400, 90), 1)
    font1 = pygame.font.SysFont('showcardgothic', 50, True)
    font2 = pygame.font.SysFont('Lucida Console', 20, True)
    texts = [
        font1.render('You Win!', 1, (255, 255, 255)),
        font2.render('Final Score: ' + str(score), 1, (255, 255, 255)),
        font2.render('Thanks for playing!', 1, (255, 255, 255)),
        font2.render('Now go to the google sheet', 1, (255, 255, 255)),
        font2.render('to see others\' score.', 1, (255, 255, 255)),
        font2.render('Press \'H\' to PLAY again.', 1, (255, 255, 255)),
        font2.render('Press \'L\' to QUIT.', 1, (255, 255, 255))
    ]

    win.blit(texts[0], (SCREEN_WIDTH // 2 - texts[0].get_width() // 2, 175))
    win.blit(texts[-2], (SCREEN_WIDTH // 2 - texts[-2].get_width() // 2, 420))
    win.blit(texts[-1], (SCREEN_WIDTH // 2 - texts[-1].get_width() // 2, 450))
    y = 260
    for i in range(1, len(texts) - 2):
        win.blit(texts[i], (SCREEN_WIDTH // 2 - texts[i].get_width() // 2, y))
        y += 30
    if attempt > 1:
        named = False
    if not named:
        update_sheet(name, score, True)


def lose_menu(win, score, attempt):
    global name, found, named
    pygame.draw.rect(win, (100, 100, 100), (300, 150, 400, 500))
    pygame.draw.rect(win, (0, 0, 0), (300, 150, 400, 500), 1)
    pygame.draw.rect(win, (0, 0, 0), (300, 150, 400, 90), 1)
    font1 = pygame.font.SysFont('showcardgothic', 50, True)
    font2 = pygame.font.SysFont('Lucida Console', 20, True)
    texts = [
        font1.render('You Lost!', 1, (255, 255, 255)),
        font2.render('Final Score: ' + str(score), 1, (255, 255, 255)),
        font2.render('Thanks for playing!', 1, (255, 255, 255)),
        font2.render('You now can either retry or', 1, (255, 255, 255)),
        font2.render('go to the google sheet', 1, (255, 255, 255)),
        font2.render('to see others\' score.', 1, (255, 255, 255)),
        font2.render('Press \'H\' to PLAY again.', 1, (255, 255, 255)),
        font2.render('Press \'L\' to QUIT.', 1, (255, 255, 255))
    ]

    win.blit(texts[0], (SCREEN_WIDTH // 2 - texts[0].get_width() // 2, 175))
    win.blit(texts[-2], (SCREEN_WIDTH // 2 - texts[-2].get_width() // 2, 450))
    win.blit(texts[-1], (SCREEN_WIDTH // 2 - texts[-1].get_width() // 2, 480))
    y = 260
    for i in range(1, len(texts) - 2):
        win.blit(texts[i], (SCREEN_WIDTH // 2 - texts[i].get_width() // 2, y))
        y += 30
    if attempt > 1:
        named = False
    if not named:
        found = False
        update_sheet(name, score)


def r_u_sure(win, action):
    pygame.draw.rect(win, (100, 100, 100), (325, 250, 350, 114))
    pygame.draw.rect(win, (0, 0, 0), (325, 250, 350, 114), 1)
    font2 = pygame.font.SysFont('Lucida Console', 16, True)
    texts = [
        font2.render('Are you sure you want', 1, (255, 255, 255)),
        font2.render(str(action), 1, (255, 255, 255)),
        font2.render('Press \'Y\' or \'N\'', 1, (255, 255, 255)),
    ]
    y = 270
    for i in range(0, len(texts)):
        win.blit(texts[i], (SCREEN_WIDTH // 2 - texts[i].get_width() // 2, y))
        y += 30


found = False


def update_sheet(name, score, won=False):
    global data, found, named
    i = 2
    while i <= len(data) + 1:
        if name == sheet.cell(i, 1).value:
            if int(sheet.cell(i, 2).value) < score:
                sheet.update_cell(i, 2, score)
            sheet.update_cell(i, 3, int(int(sheet.cell(i, 3).value) + 1))
            if won:
                sheet.update_cell(i, 4, int(int(sheet.cell(i, 4).value) + 1))
            found = True
        i += 1
    if not found:
        if won:
            sheet.append_row([name, score, 1, 1])
        else:
            sheet.append_row([name, score, 1, 0])
        found = True
    named = True


print(name)
