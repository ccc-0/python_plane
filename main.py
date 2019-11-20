import pygame
from pygame.locals import *
from sys import exit
from myplane import Myplane,Enemyplane,Enemyplane2,Enemyplane3
from bullet import Bullet,Boom
from pygame.sprite import collide_mask
from pygame.locals import K_SPACE

pygame.init()
# 创建一个窗口
w=480
h=700
screen = pygame.display.set_mode((w,h))

# 修改窗口标题,图标
pygame.display.set_caption("Aircraft Battle!")
icon = pygame.image.load('res/images/plane.ico')
pygame.display.set_icon(icon)

# 加载字体
myfont = pygame.font.Font('res/font/simhei.ttf',30)
#显示分数                 准备字体内容 > 返回surface对象 


# 加载暂停和恢复图片
pause = pygame.image.load('res/images/pause_nor.png')
resume = pygame.image.load('res/images/resume_nor.png')
pause_rect = pause.get_rect() 
pause_rect.x = 400
pause_rect.y = 10
pause_flag = True

'''
# 加载音乐 music 流式音乐，同时只能播放一首
pygame.mixer.music.load('res/sound/game_music.ogg')
# 播放  n 循环n次+1   -1时为无限循环   
pygame.mixer.music.play(-1) 

# 加载音频（可同时播放多个） 
sound = pygame.mixer.Sound('res/sound/enemy1_down.wav')
sound.play()
'''

# 加载资源文件
# 绘制背景
bg = pygame.image.load('res/images/background.png')
bg_rect = bg.get_rect()

again_btn = pygame.image.load('res/images/again.png')
again_btn_rect = again_btn.get_rect()
again_btn_rect.centerx = bg_rect.centerx
again_btn_rect.y =300
gameover_btn = pygame.image.load('res/images/gameover.png')
gameover_btn_rect = gameover_btn.get_rect()
gameover_btn_rect.centerx = bg_rect.centerx
gameover_btn_rect.y=400

life_image = pygame.image.load('res/images/life.png')
life_image_rect = life_image.get_rect()
boom_image= pygame.image.load('res/images/bomb.png')
boom_image_rect = boom_image.get_rect()

# 全局变量声明
run_flag = True
score =0
# life = 3
#pause_flag =True


def mygame():
    # 初始化标记变量
    clock = pygame.time.Clock()
    counter =0
    global score
    score =0
    global life
    life =3
    boom_num=0
    pause_flag =True
    useboom_flag=False
  
    # 创建精灵实体
    plane = Myplane(w,h)
    bullet_group = pygame.sprite.Group(Bullet(plane.rect))
    enemy_group= pygame.sprite.Group(*[Enemyplane(w,h) for x in range(10)])
    enemy2_group= pygame.sprite.Group(*[Enemyplane2(w,h) for x in range(2)])
    enemy3_group= pygame.sprite.Group(*[Enemyplane3(w,h) for x in range(1)])
    boom_group = pygame.sprite.Group(*[Boom(w,h) for x in range(1)])      
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            #鼠标按下和抬起事件                        
            if event.type == MOUSEBUTTONUP:
                if pause_rect.collidepoint(event.pos):
                    pause_flag  =not pause_flag
            #键盘按下事件
            if event.type== KEYDOWN:
                if event.key== K_SPACE:
                    useboom_flag=not useboom_flag
         # 判断pause_flag 绘制暂停 or 恢复
        if pause_flag:
            screen.blit(pause,pause_rect)
        else:
            screen.blit(resume,pause_rect)
        pygame.display.flip()
        if pause_flag:
            pass
        else:
            continue
        
        #滚动的背景
        bg_rect.y +=1
        screen.blit(bg,bg_rect)
        screen.blit(bg,(bg_rect.x,bg_rect.y-h))
        if bg_rect.y >=700:
            bg_rect.y =0

        plane.update(screen)
        bullet_group.update(screen)

        #每n次循环创建一个子弹
        if counter %5==0:
            bullet_group.add(Bullet(plane.rect))
        #每隔n次循环给一个补给
        if counter %200==0:
            boom_group.add(Boom(w,h))

        boom_group.update(screen)
        enemy_group.update(screen)  

        # 碰撞检测
        collide_dict=pygame.sprite.groupcollide(bullet_group,enemy_group,True,False,collide_mask)
        tmp =[]
        for i in collide_dict.values():
            tmp +=i
        for i in tmp :
            i.active_flag=False

        if plane.active_flag:
            collide_dict2= pygame.sprite.spritecollide(plane,enemy_group,False,collide_mask)
            for i in collide_dict2:
                i.active_flag = False 
                plane.active_flag=False
            life -=len(collide_dict2)

        # 绘制我方生命量
        for i in [life]:
            screen.blit(life_image ,(350+i*30,640))


        collide_dict3 = pygame.sprite.spritecollide(plane,boom_group,True,collide_mask)
        if  collide_dict3:
            if boom_num<3:           
                boom_num +=1

        #使用炸弹
        if useboom_flag:
            if boom_num>0:
                temp = pygame.sprite.Group.sprites(enemy_group)
                for i in temp: 
                    i.active_flag = False
                boom_num-=1
                useboom_flag=False
                 

        #显示炸弹数
        myboom = myfont.render('X '+str(boom_num),True,(0,0,0))
        screen.blit(boom_image ,(-4,640))
        screen.blit(myboom ,(65,655))
       

        score += len(tmp)*10
        mytext = myfont.render("分数:"+ str(score),True,(0,0,0))
        screen.blit(mytext,(0,0))
       
        counter+=1

        #增加难度
        if score ==1000:
            if len (enemy_group)<15:
                enemy_group.add(*[Enemyplane(w,h) for i in range(15)])
        if score ==200:
            enemy2_group= pygame.sprite.Group(*[Enemyplane2(w,h) for x in range(2)])
            enemy2_group.update(screen)
        if score ==500:
            enemy3_group= pygame.sprite.Group(*[Enemyplane3(w,h) for x in range(1)])
            enemy3_group.update(screen)
               
        if life <=0 :
            global run_flag
            run_flag=False
            break

        clock.tick(50)        

        # 检测事件      
        # 更新精灵等 状态 比如位置等
        # 碰撞检测
        # 绘制精灵
        # 绘制图片、文字


def gameover():
    # 绘制结束页面
    screen.blit(bg,bg_rect)
    screen.blit(again_btn,again_btn_rect)
    screen.blit(gameover_btn,gameover_btn_rect)
    
    mytext = myfont.render("分数:"+ str(score),True,(0,0,0))
    screen.blit(mytext,(200,200))

    pygame.display.flip()
    while True:
        
        # 事件检测
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == MOUSEBUTTONUP:
                # 判断鼠标弹起位置 是否在 图片区域
                if again_btn_rect.collidepoint(event.pos):
                    global run_flag
                    run_flag = True
                    break
                if gameover_btn_rect.collidepoint(event.pos):
                    exit()
        if run_flag:
            break

        # 事件检测 - 重新开始 or 退出游戏

if __name__ == '__main__' :
    while True:
        if run_flag:
            mygame()
        else:
            gameover()





