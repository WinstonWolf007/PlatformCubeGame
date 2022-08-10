#############################################################
import pygame
pygame.init()


#############################################################
class Block(pygame.sprite.Sprite):
    def __init__(self, surface: pygame.Surface, size: list, pos: list):
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.surface = surface
        self.color = (50, 52, 57)
        super().__init__()

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect)


#############################################################
class End(pygame.sprite.Sprite):
    def __init__(self, surface: pygame.Surface, pos: list):
        self.surface = surface
        self.rect = pygame.Rect(pos[0], pos[1], 50, 50)
        self.color = (255, 200, 17)
        super().__init__()

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect)


#############################################################
class Player(pygame.sprite.Sprite):
    def __init__(self, surface: pygame.Surface):
        super().__init__()
        self.velocity = 1
        self.surface = surface
        self.size = (50, 99)
        self.position = [0, 0]
        self.body = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        self.feet = pygame.Rect(self.position[0], self.position[1]+self.size[1], self.size[0], 21)
        self.color = (200, 100, 100)
        self.power = 10*20
        self.dftPower = 10*20
        self.gravity = 1
        self.key = {}
        self.isGrounded = False
        self.jumpsActive = False

    def draw(self, block: list):
        for blc in block:
            if self.feet.colliderect(blc):
                self.isGrounded = True
                break
        else:
            self.isGrounded = False

        if not self.isGrounded and not self.jumpsActive:
            self.position[1] += self.gravity

        elif self.jumpsActive:
            if self.power != 0:
                self.power -= 1
                self.position[1] -= 1
            else:
                self.power = self.dftPower
                self.jumpsActive = False
                self.isGrounded = False

        self.setPos()
        pygame.draw.rect(self.surface, self.color, self.feet)
        pygame.draw.rect(self.surface, self.color, self.body)

    def jumps(self):
        if self.isGrounded:
            self.jumpsActive = True

    def move(self, velocity):
        self.position[0] += velocity
        self.setPos()

    def setPos(self):
        self.body.x, self.body.y = self.position
        self.feet.x, self.feet.y = [self.position[0], self.position[1] + self.size[1]]

    def death(self):
        return self.feet.y > self.surface.get_size()[1]

    def win(self, winObj):
        return self.body.colliderect(winObj)


#############################################################
# check if one element is on collision with a set elements
def collide_rect_list(collideRect, collide2: list):
    for col in collide2:
        if collideRect.colliderect(col):
            break
    else:
        return False
    return True


#############################################################
# Init page, playerClass and font
screen = pygame.display.set_mode([949, 887])
pygame.display.set_caption('~ Game ~')
player = Player(screen)
font = pygame.font.SysFont('bold', 50)
font2 = pygame.font.SysFont('bold', 80)


#############################################################
# level sys
level = {
    '0': [
        [200, screen.get_size()[1] - 200],
        End(screen, [750, screen.get_size()[1] - 300]),
        Block(screen, [400, 50], [0, screen.get_size()[1] - 50]),
        Block(screen, [300, 50], [600, screen.get_size()[1] - 200])
    ],
    '1': [
        [50, screen.get_size()[1] - 200],
        End(screen, [750, screen.get_size()[1] - 300]),
        Block(screen, [100, 50], [0, screen.get_size()[1] - 50]),
        Block(screen, [100, 50], [300, screen.get_size()[1] - 50]),
        Block(screen, [100, 50], [500, screen.get_size()[1] - 50]),
    ],
    '2': [
        [200, 200],
        End(screen, [750, screen.get_size()[1] - 300]),
        Block(screen, [50, 50], [400, screen.get_size()[1] - 50])
    ]
}


#############################################################
# Default variable
levIdx = 0
running = True
player.position = level['0'][0]
end_game = False
textEnd = font2.render('End of Game', True, (50, 52, 57))
textRectEnd = textEnd.get_rect()


#############################################################
# Game loop
while running:

    # check quit event and key
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            player.key[event.key] = True
            if event.key == pygame.K_SPACE:
                player.jumps()
        elif event.type == pygame.KEYUP:
            player.key[event.key] = False

    # This loop is used for move player continuous. If a press to Left key, the player move to left to infinite
    for key in player.key:
        if player.key.get(key):
            if key == pygame.K_LEFT and not collide_rect_list(player.body, level[str(levIdx)][2:]):
                player.move(-player.velocity)
            elif key == pygame.K_RIGHT and not collide_rect_list(player.body, level[str(levIdx)][2:]):
                player.move(player.velocity)

    if player.death():
        running = False
        pygame.quit()

    # if player on collision with win block, change level but if do not other level (keyError). Display the end screen
    elif player.win(level[str(levIdx)][1]):
        try:
            player.position = level[str(levIdx+1)][0]
            levIdx += 1
        except KeyError:
            end_game = True

    textLevel = font.render('Level: ' + str(levIdx + 1), True, (50, 52, 57))
    textRect = textLevel.get_rect()

    screen.fill((240, 240, 240))

    # Draw el element to the screen
    if not end_game:
        for f in level[str(levIdx)][1:]:
            f.draw()
        player.draw(level[str(levIdx)][2:])
    else:
        screen.blit(textEnd, ((screen.get_width()-textEnd.get_width())/2, (screen.get_height()-textEnd.get_height())/2))

    screen.blit(textLevel, textRect)

    pygame.display.update()
    pygame.display.flip()


#############################################################
pygame.quit()