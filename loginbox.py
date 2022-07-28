import pygame

pygame.init()
#COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_INACTIVE = pygame.Color(255, 255, 255, 255)
#COLOR_ACTIVE = pygame.Color('dodgerblue2')
COLOR_ACTIVE = pygame.Color(200, 200, 200, 255)
COLOR_FONT = pygame.Color(0, 0, 0, 255)
FONT = pygame.font.Font(None,32)

class InputBox:
    
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, COLOR_FONT)

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.rect.w, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect)
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        
        


class button:
    def __init__(self, position, size, clr=[100, 100, 100], cngclr=None, func=None, text='', font="Segoe Print", font_size=16, font_clr=[0, 0, 0], visible = True):
        self.clr    = clr
        self.size   = size
        self.func   = func
        self.surf   = pygame.Surface(size)
        self.rect   = self.surf.get_rect(center=position)
        self.visible = visible

        if cngclr:
            self.cngclr = cngclr
        else:
            self.cngclr = clr

        if len(clr) == 4:
            self.surf.set_alpha(clr[3])


        self.font = pygame.font.SysFont(font, font_size)
        self.txt = text
        self.font_clr = font_clr
        self.txt_surf = self.font.render(self.txt, 1, self.font_clr)
        self.txt_rect = self.txt_surf.get_rect(center=[wh//2 for wh in self.size])

    def draw(self, screen):
        self.mouseover()
        if self.visible == True:
            self.surf.fill(self.curclr)
            self.surf.blit(self.txt_surf, self.txt_rect)
            screen.blit(self.surf, self.rect)

    def mouseover(self):
        self.curclr = self.clr
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.curclr = self.cngclr

    def call_back(self, *args):
        if self.func:
            return self.func(*args)

class text:
    def __init__(self, msg, position, clr=[100, 100, 100], font="Segoe Print", font_size=15, mid=False):
        self.position = position
        self.font = pygame.font.SysFont(font, font_size)
        self.txt_surf = self.font.render(msg, 1, clr)

        if len(clr) == 4:
            self.txt_surf.set_alpha(clr[3])

        if mid:
            self.position = self.txt_surf.get_rect(center=position)


    def draw(self, screen):
        screen.blit(self.txt_surf, self.position)
    
#버튼 함수 기능들 모아놓은 부분
def fn_login(username, password, server): #button1이 눌렸을 때 실제로 일어나는 작업
    print('button1')
    data = "login " + username + " " + password # login username password 꼴로 줘서 split할 예정
    currentid = server.login(data)
    return currentid
def fn_register(username, password, nickname, server): #button2가 눌렸을 때 실제로 일어나는 작업
    print('button2')
    data = "register " + username + " " + password + " " + nickname
    currentid = server.login(data)
    return currentid
def fn_create(server):
    data = "create"
    roomnum = server.send(data)
    print(roomnum)
    return roomnum
def fn_enter(server, roomcode):
    print("button2")
    data = "enter " + roomcode
    roomnum = server.send(data)
    print(roomnum)
    return roomnum
def fn_loginmod() :
    return 1
def fn_regmod():
    return 2
def fn_qmod():
    return 3

def fn_ready(server):
    data = "ready"

    return server.send(data)


if __name__ == '__main__':
    pygame.init()
    screen_size = (300, 200)
    size        = 10
    clr         = [255, 0, 255]
    bg          = (255, 255, 0)
    font_size   = 15
    font        = pygame.font.Font(None, font_size)
    clock       = pygame.time.Clock()

    screen    = pygame.display.set_mode(screen_size)
    screen.fill(bg)

    button1 = button(position=(80, 100), size=(100, 50), clr=(220, 220, 220), cngclr=(255, 0, 0), func=fn1, text='button1')
    button2 = button((220, 100), (100, 50), (220, 220, 220), (255, 0, 0), fn2, 'button2')

    button_list = [button1, button2]

    crash = True
    while crash:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crash = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    crash = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    for b in button_list:
                        if b.rect.collidepoint(pos):
                            b.call_back()

        for b in button_list:
            b.draw(screen)

        pygame.display.update()
        clock.tick(60)