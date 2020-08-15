import pygame
import data
import sys
import traceback
from pygame.locals import *
import myPlane
import enemy
import bullet
import supply
import random



pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700  # 根据bg尺寸
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption(data.GameTitle)

background = pygame.image.load("./images/background.png").convert()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

#载入游戏音乐
pygame.mixer.music.load("./sound/game_music.wav")
pygame.mixer.music.set_volume(data.GameVolume)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(data.GameVolume)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(data.GameVolume)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(data.GameVolume)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(data.GameVolume)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(data.GameVolume)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(data.GameVolume)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(data.GameVolume)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.5)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.5)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(data.GameVolume)






def main():
    is_double_bullet = False
    pygame.mixer_music.play(-1)

    # create myPlane
    my_plane = myPlane.MyPlane(bg_size)

    # create enemy plane
    enemies = pygame.sprite.Group()

    #  小型敌方飞机
    smallEnemies = pygame.sprite.Group()
    addSmallEnemies(smallEnemies, enemies, data.BigEnemiesNum)
    #  中型敌方飞机
    midEnemies = pygame.sprite.Group()
    addMidEnemies(midEnemies, enemies, data.MidEnemiesNum)
    #  大型敌方飞机
    bigEnemies = pygame.sprite.Group()
    addBigEnemies(bigEnemies, enemies, data.BigEnemiesNum)

    bullets = []
    # 我方子弹 普通
    if True:
        bullet1 = []
        bullet1_index = 0
        bullet1_num = data.SingleBullet
        for i in range(bullet1_num):
            bullet1.append(bullet.Bullet1(my_plane.rect.midtop))

    # 我方子弹 二重
    if True:
        bullet2 = []
        bullet2_index = 0
        bullet2_num = data.DoubleBullet
        for i in range(bullet2_num//2):
            bullet2.append(bullet.Bullet2((my_plane.rect.centerx - 33, my_plane.rect.centery)))
            bullet2.append(bullet.Bullet2((my_plane.rect.centerx + 30, my_plane.rect.centery)))
    # 二重子弹             定时器
    DOUBLE_BULLET_TIME = USEREVENT + 1

    # 飞机破坏图片索引
    if True:
        e1_destroy_index = 0
        e2_destroy_index = 0
        e3_destroy_index = 0
        me_destroy_index = 0

    # 统计得分
    score = 0
    score_font = pygame.font.Font("font/font.ttf", 36)

    # 暂停游戏
    if True:
        paused = False
        pause_nor_image = pygame.image.load("./images/pause_nor.png").convert_alpha()
        pause_pressed_image = pygame.image.load("./images/pause_pressed.png").convert_alpha()
        resume_nor_image = pygame.image.load("./images/resume_nor.png").convert_alpha()
        resume_pressed_image = pygame.image.load("./images/resume_pressed.png").convert_alpha()
        pause_rect = pause_nor_image.get_rect()
        pause_rect.left, pause_rect.top = width - pause_rect.width - 10, 10
        pause_image = pause_nor_image

    # 游戏难度
    level = data.GameLevel

    # 全屏炸弹
    if True:
        bomb_image = pygame.image.load("./images/bomb.png").convert_alpha()
        bomb_rect = bomb_image.get_rect()
        bomb_font = pygame.font.Font("font/font.ttf", 48)
        bomb_num = data.BombNum

    # 每20s触发一次补给
    if True:
        bullet_supply = supply.BulletSupply(bg_size)
        bomb_supply = supply.BombSupply(bg_size)
        SUPPLY_TIME = USEREVENT
        pygame.time.set_timer(SUPPLY_TIME, data.SupplyIntervelTime)

    clock = pygame.time.Clock()

    # 切换我放飞机
    switch_iamge = True

    # 生命数量
    if True:
        life_image = pygame.image.load("./images/life.png").convert_alpha()
        life_rect = life_image.get_rect()
        life_num = data.Life

    # 解除我方复活后的短暂无敌 计时器
    invincible_time = USEREVENT + 2

    # 绘制结束界面
    if True:
        gameover_font = pygame.font.Font("font/font.ttf", 48)
        again_image = pygame.image.load("./images/again.png").convert_alpha()
        again_rect = again_image.get_rect()
        gameover_image = pygame.image.load("./images/gameover.png").convert_alpha()
        gameover_rect = gameover_image.get_rect()

    # 用于阻止重复开关存档文件 save
    saved = False

    # 用于延迟
    delay = 100

    running = True

    while running:
        # 所有事件event
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame, exit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and pause_rect.collidepoint(event.pos):
                    paused = not paused
                    if paused:
                        pause_image = resume_pressed_image
                        pygame.time.set_timer(SUPPLY_TIME, 0)
                        pygame.mixer.music.pause()
                        pygame.mixer.pause()
                    else:
                        pause_image = pause_pressed_image
                        pygame.time.set_timer(SUPPLY_TIME, data.SupplyIntervelTime)
                        pygame.mixer.music.unpause()
                        pygame.mixer.unpause()

            # elif event.type ==MOUSEMOTION:
            #     if pause_rect.collidepoint(event.pos):
            #         if paused:
            #             pause_image = resume_pressed_image
            #         else:
            #             pause_image = pause_pressed_image
            #     else:
            #         if paused:
            #             pause_image = resume_nor_image
            #         else:
            #             pause_image = pause_nor_image

            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    print("按之前还有%d个" % bomb_num)
                    if bomb_num:
                        bomb_num -= 1
                        bomb_sound.play()
                        for each in enemies:
                            if each.rect.bottom > 0:
                                each.alive = False

            elif event.type == SUPPLY_TIME:
                supply_sound.play()
                if random.randint(1, 4) % 4 == 0:
                    bomb_supply.reset()
                else:
                    bullet_supply.reset()

            elif event.type == DOUBLE_BULLET_TIME:
                is_double_bullet = False
                pygame.time.set_timer(DOUBLE_BULLET_TIME, 0)

            elif event.type == invincible_time:
                my_plane.invincible = False
                pygame.time.set_timer(invincible_time, 0)


        # 根据用户的得分来增加难度
        if score >= 5000 * (level ** 2):
            level += 1
            upgrade_sound.play()
            addSmallEnemies(smallEnemies, enemies, 5)
            addMidEnemies(midEnemies, enemies, 3)
            addBigEnemies(bigEnemies, enemies, 1)
            inc_speed(smallEnemies, 1)
            inc_speed(midEnemies, 0.5)
            # inc_speed(bigEnemies, 0.1)
            print("现在的等级是%d级" % level)

        screen.blit(background, (0, 0))

        # 游戏进行时相关 !important
        # 游戏进行时相关 !important
        # 游戏进行时相关 !important
        if life_num and not paused:
            # check keyboard event
            key_pressed = pygame.key.get_pressed()

            if key_pressed[K_w] or key_pressed[K_UP]:
                my_plane.moveUp()

            if key_pressed[K_s] or key_pressed[K_DOWN]:
                my_plane.moveDown()

            if key_pressed[K_a] or key_pressed[K_LEFT]:
                my_plane.moveLeft()

            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                my_plane.moveRight()

            # 绘制大型敌机
            for each in bigEnemies:
                if each.alive:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        if switch_iamge:
                            screen.blit(each.image1, each.rect)
                        else:
                            screen.blit(each.image2, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, BLACK,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5), 2)
                    # 生命大于20%时显示绿色，以下则为红色
                    energy_remain = each.energy / enemy.BigEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5), 2)

                    # 即将出现时，播ngm
                    if each.rect.bottom == -50:

                        enemy3_fly_sound.play(-1)

                        # -1循环播放

                else:
                    # 飞机被破坏
                    if not (delay % 5):
                        if e3_destroy_index == 0:
                            enemy3_down_sound.play()

                        screen.blit(each.destroy_images[e3_destroy_index], each.rect)
                        e3_destroy_index = (e3_destroy_index + 1) % 6
                        if e3_destroy_index == 0:
                            enemy3_fly_sound.stop()
                            score += 5000
                            each.reset()

            # 绘制中型敌机
            for each in midEnemies:
                if each.alive:
                    each.move()
                    if each.hit:
                        screen.blit(each.image_hit, each.rect)
                        each.hit = False
                    else:
                        screen.blit(each.image, each.rect)

                    # 绘制血槽
                    pygame.draw.line(screen, BLACK,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.right, each.rect.top - 5), 2)
                    # 生命大于20%时显示绿色，以下则为红色
                    energy_remain = each.energy / enemy.MidEnemy.energy
                    if energy_remain > 0.2:
                        energy_color = GREEN
                    else:
                        energy_color = RED
                    pygame.draw.line(screen, energy_color,
                                     (each.rect.left, each.rect.top - 5),
                                     (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5), 2)

                else:
                    # 飞机被破坏
                    if not (delay % 5):
                        if e2_destroy_index == 0:

                            enemy2_down_sound.play()
                        screen.blit(each.destroy_images[e2_destroy_index], each.rect)
                        e2_destroy_index = (e2_destroy_index + 1) % 4
                        if e2_destroy_index == 0:
                            score += 1000
                            each.reset()

            # 绘制小型敌机
            for each in smallEnemies:
                if each.alive:
                    each.move()
                    screen.blit(each.image, each.rect)
                else:
                    # 飞机被破坏
                    if not (delay % 5):
                        if e1_destroy_index == 0:
                            enemy1_down_sound.play()
                        screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                        e1_destroy_index = (e1_destroy_index + 1) % 4
                        if e1_destroy_index == 0:
                            score += 100
                            each.reset()

            # 绘制我放飞机
            if my_plane.alive:
                if switch_iamge:
                    screen.blit(my_plane.image1, my_plane.rect)
                    # print(my_plane.rect)
                    # switch_iamge = False
                else:
                    screen.blit(my_plane.image2, my_plane.rect)
                    # switch_iamge = True
            else:
                # 我方飞机被破坏
                if not (delay % 3):
                    if me_destroy_index == 0:

                        me_down_sound.play()
                    screen.blit(my_plane.destroy_images[me_destroy_index], my_plane.rect)
                    e1_destroy_index = (e1_destroy_index + 1) % 4
                    if e1_destroy_index == 0:
                        life_num -= 1
                        # 重生
                        my_plane.reset()
                        pygame.time.set_timer(invincible_time, 3*1000)

            # 检测我方飞机是否被撞
            enemies_down = pygame.sprite.spritecollide(my_plane, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not my_plane.invincible:
                # 这面这个控制我方无敌
                my_plane.alive = False
                for e in enemies_down:
                    e.alive = False

            # 发射我方子弹
            if not (delay % 10):
                bullet_sound.play()
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((my_plane.rect.centerx - 33, my_plane.rect.centery))
                    bullets[bullet2_index+1].reset((my_plane.rect.centerx + 30, my_plane.rect.centery))
                    bullet2_index = (bullet2_index + 2) % bullet2_num
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(my_plane.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % bullet1_num

            # 检测子弹是否击中敌机
            for b in bullets:
                if b.alive:
                    b.move()
                    screen.blit(b.image, b.rect)

                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:
                        bullet.alive = False
                        for e in enemy_hit:
                            # 下面用来判断大中小敌机的不同情况
                            if e in midEnemies or e in bigEnemies:
                                e.hit = True
                                e.energy -= 1
                                if e.energy == 0:
                                    e.alive = False
                            else:
                                e.alive = False

            # 绘制补给炸弹并判断是否获得
            if bomb_supply.alive:
                bomb_supply.move()
                screen.blit(bomb_supply.image, bomb_supply.rect)
                if pygame.sprite.collide_mask(bomb_supply, my_plane):
                    get_bomb_sound .play()
                    bomb_num += 1
                    bomb_supply.alive = False

            # 绘制超级子弹并判断是否获得
            if bullet_supply.alive:
                bullet_supply.move()
                screen.blit(bullet_supply.image, bullet_supply.rect)
                if pygame.sprite.collide_mask(bullet_supply, my_plane):
                    get_bullet_sound.play()
                    # 发射二重子弹
                    is_double_bullet = True
                    pygame.time.set_timer(DOUBLE_BULLET_TIME, data.DoubleBulletTime)
                    bullet_supply.alive = False


            # 绘制剩余生命life数量
            if True:
                if life_num:
                    for i in range(life_num):
                        screen.blit(life_image, (width-10-(i+1)*life_rect.width, height-10-life_rect.height))

            # 绘制剩余炸弹
            if True:
                bomb_text = bomb_font.render("× %d" % bomb_num, True, WHITE)
                text_rect = bomb_text.get_rect()
                screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
                screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))

            # 绘制分数栏
            score_text = score_font.render("LV:%d   Score : %s " % (level, str(score)), True, WHITE)
            screen.blit(score_text, (10, 5))

            # 绘制暂停按钮
            screen.blit(pause_image, pause_rect)

        elif life_num:
            # 绘制分数栏
            score_text = score_font.render("LV:%d   Score : %s " % (level, str(score)), True, WHITE)
            screen.blit(score_text, (10, 5))

            # 绘制暂停按钮
            screen.blit(pause_image, pause_rect)

        # 绘制游戏结束画面
        elif life_num == 0:
            # 背景音乐停止
            pygame.mixer.music.stop()

            # 停止全部音效
            pygame.mixer.stop()

            # 停止补给发放
            pygame.time.set_timer(SUPPLY_TIME, 0)

            # 存档相关
            if not saved:
                # 读取历史最高分
                with open("save.txt", "r") as f:
                    record_score = int(f.read())
                # 如果高于最高分，则存档
                if score > record_score:
                    with open("save.txt", "w") as f:
                        f.write(str(score))

            # 结束界面
            if True:
                record_score_text = score_font.render("Best : %d" % record_score, True, WHITE)
                screen.blit(record_score_text, (50, 50))

                gameover_text1 = gameover_font.render("Your Score: ", True, WHITE)
                gameover_text1_rect = gameover_text1.get_rect()
                gameover_text1_rect.left, gameover_text1_rect.top = \
                    (width - gameover_text1_rect.width) // 2, height // 2
                screen.blit(gameover_text1, gameover_text1_rect)

                gameover_text2 = gameover_font.render(str(score), True, WHITE)
                gameover_text2_rect = gameover_text2.get_rect()
                gameover_text2_rect.left, gameover_text2_rect.top = \
                    (width - gameover_text2_rect.width) // 2, \
                    gameover_text1_rect.bottom + 10
                screen.blit(gameover_text2, gameover_text2_rect)

                again_rect.left, again_rect.top = \
                    (width - again_rect.width) // 2, \
                    gameover_text2_rect.bottom + 50
                screen.blit(again_image, again_rect)

                gameover_rect.left, gameover_rect.top = \
                    (width - again_rect.width) // 2, \
                    again_rect.bottom + 10
                screen.blit(gameover_image, gameover_rect)

                score_text = score_font.render("Score : %s " % str(score), True, WHITE)
                screen.blit(score_text, (10, 5))

            # 检测用户的鼠标操作
            # 如果用户按下鼠标左键
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                if again_rect.left < pos[0] < again_rect.right and \
                        again_rect.top < pos[1] < again_rect.bottom:
                    main()
                elif gameover_rect.left < pos[0] < gameover_rect.right and \
                        gameover_rect.top < pos[1] < gameover_rect.bottom:
                    pygame.quit()
                    sys.exit()



        # mark是否使用超级子弹

        # 切换照片
        if True:
            if not(delay % 5):
                switch_iamge = not switch_iamge
            delay -= 1
            if not delay:
                delay = 100

            pygame.display.flip()
            clock.tick(60)


def addSmallEnemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)


def addMidEnemies(group1, group2, num):
    for i in range(num):
        e2 = enemy.MidEnemy(bg_size)
        group1.add(e2)
        group2.add(e2)


def addBigEnemies(group1, group2, num):
    for i in range(num):
        e3 = enemy.BigEnemy(bg_size)
        group1.add(e3)
        group2.add(e3)


def inc_speed(target, inc):
    for each in target:
        each.speed += inc





if __name__ == "__main__":
    try:
        main()

    except SystemExit:
        pass

    except:
        traceback.print_exc()
        pygame.quit()
        input()
