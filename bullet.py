import pygame
from pygame.sprite import Sprite
from random import randint
from pygame.locals import K_SPACE

class Bullet(Sprite):
    """docstring for Bullet"""
    def __init__(self,rect):
        super ().__init__()
        self.image = pygame.image.load('res/images/bullet1.png')
        self.rect = self.image.get_rect()
        self.rect.centerx = rect.centerx
        self.rect.centery = rect.centery
        self.speed = 10 
        

    def draw(self,surface):
        surface.blit(self.image,self.rect)

    def move(self):
        if self.rect.y <0 -10:
            self.kill()
            del self
        else :              
            self.rect.y -= self.speed
    def update(self,surface):
        self.move()
        self.draw(surface)

class Boom(Sprite):
    """docstring for Boom"""
    def __init__(self,w,h):
        super (Boom, self).__init__()
        self.image = pygame.image.load('res/images/bomb_supply.png')
        self.rect = self.image.get_rect()
        self.rect.x=randint(-10,w)
        self.rect.y=randint(-h,5)
        self.speed=5
        self.active_flag=True
        self.w=w
        self.h=h
        self.mask=pygame.mask.from_surface(self.image)



    def draw(self,surface):
        surface.blit(self.image,self.rect)

    def move(self):
        if self.rect.y +self.speed < self.h:
            self.rect.y += self.speed
        else:
            self.reset()

    def update(self,surface):
        self.move()
        self.draw(surface)

    def reset(self):
        self.rect.x=randint(0,self.w)
        self.rect.y=randint(-self.h,0)  
        self.active_flag =True

    # def useboom(self):
    #     key = pygame.key.get_pressed()
    #     if key:
    #         if boom_num>0:
    #             pygame.sprite.enemy_group.empty()
    #             enemy_group.update(screen)
    #             boom_num-=1


    

