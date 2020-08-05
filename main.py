import pygame
import random

# pygame初始化
pygame.init()

# 設定長寬
size = WIDTH,HEIGHT = 640,480

# 設定顏色
Black = (0,0,0)
Red = (255,0,0)
Gray = (127,127,127)

# 開啟一個視窗 #各種設定
display = pygame.display.init()
pygame.display.set_caption("main")
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
ball_speed = [random.uniform(4.0,5.0),random.uniform(4.0,5.0)]
pygame.mouse.set_visible(False)

#載入各種圖片
ball_image = pygame.image.load("Ball.png")
brick1 = pygame.image.load("黃磚塊1.png")

#建立物件的類別
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(ball_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.centery = HEIGHT/2
        self.die = False
        pass
    def update(self):
        pass

    def move_playing(self):
        self.rect = self.rect.move(ball_speed)
        if self.rect.left < 0 or self.rect.right >WIDTH:
            ball_speed[0] = -ball_speed[0]
        if self.rect.top < 10:
            ball_speed[1] = -ball_speed[1]
        if self.rect.bottom > HEIGHT:
            self.die = True

    def move_start(self):
        self.rect = self.rect.move(0,5)
        

class Brick(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(brick1,(80,40))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Board(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # 很重要一定要有，繼承
        self.image = pygame.Surface((100,10))
        self.image.fill(Black)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.centery = HEIGHT-20


#初始化 # Bricks應該設為一個Group
board = Board()
ball = Ball()
bricks = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(board, ball, bricks)



for i in range(6):
    for j in range(3):
        brick = Brick(((160/7)*(i+1)+80*i),(10*(j+1)+40*j))
        bricks.add(brick)

if __name__ == "__main__":
    # 關閉視窗
    runnning = True
    while runnning:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type==pygame.QUIT or ball.die ==True or len(bricks.sprites())==0:
                runnning=False

    # 設定Board的位置
        board.rect.centerx = pygame.mouse.get_pos()[0]

    # 球的移動
        ball.move_playing()
    # 碰撞偵測
        hits = pygame.sprite.spritecollide(ball, bricks, False)
        for hit in hits:
            ball_speed[1] = -ball_speed[1]
            hit.kill()
            
        if pygame.sprite.collide_rect(ball, board):
             ball_speed[1] = -ball_speed[1]

    # 修正會卡在螢幕上方的問題
        List = []
        List.append(ball_speed[1])
        for n in range(len(List)):
            if n>3:
                if List[n] == List[n-2]:
                    ball_speed[1]+=1
        
        screen.fill(Gray)
        all_sprites.draw(screen)
        bricks.draw(screen)
        pygame.display.flip()
pygame.quit()