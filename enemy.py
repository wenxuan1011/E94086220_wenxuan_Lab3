import pygame
import math
import os
from settings import PATH
from settings import PATH_BONUS  #匯入由又邊開始的路徑
from settings import RED, GREEN

pygame.init()
ENEMY_IMAGE = pygame.image.load(os.path.join("images", "enemy.png"))

#用來表示按了幾次的'n'鍵
count=0

class Enemy:
    def __init__(self):
        self.width = 40
        self.height = 50
        self.image = pygame.transform.scale(ENEMY_IMAGE, (self.width, self.height))
        self.health = 5
        self.max_health = 10
        global count
        if (count%2==0):  #若為第一次(奇數次),則走由左邊開始的路徑
            self.path = PATH
        else:  #若為第二次(偶數次),則走由右邊開始的路徑
            self.path=PATH_BONUS
        self.path_pos = 0
        self.move_count = 0
        self.stride = 1
        self.x, self.y = self.path[0]  #將一開始的起始點設為path的第一個點

    def draw(self, win):
        # draw enemy
        win.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))
        # draw enemy health bar
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        """
        Draw health bar on an enemy
        :param win: window
        :return: None
        """
        pygame.draw.rect(win,RED,[self.x-22,self.y-35,45,7])  #畫出紅色的血條
        pygame.draw.rect(win,GREEN,[self.x-22,self.y-35,45*self.health/self.max_health,7])  #畫出綠色的血條

    def move(self):
        """
        Enemy move toward path points every frame
        :return: None
        """
        ax, ay=self.path[self.path_pos]  #將目前的點設為A點
        bx, by=self.path[self.path_pos+1]  #將path的下一點設為B點
        distance_A_B=math.sqrt((ax-bx)**2+(ay-by)**2)  #計算出A到B的距離
        max_count=int(distance_A_B/self.stride)  #求出從A到B需要走的最大步數

        if self.move_count<max_count:  #當已走的步數<從A到B需要的最大步數
            unit_vector_x=(bx-ax)/distance_A_B  #X方向的單位向量
            unit_vector_y=(by-ay)/distance_A_B  #Y方向的單位向量
            delta_x=unit_vector_x*self.stride  #求出X方向的變化量
            delta_y=unit_vector_y*self.stride  #求出Y方向的變化量

            #依照X,Y變化量更新座標
            self.x+=delta_x
            self.y+=delta_y
            self.move_count+=1  #已走步數+1
        else:  #當完成A到B後
            self.path_pos+=1  #目前的位子+1(以移動到下一點)
            self.move_count=0  #重置已走的步數


class EnemyGroup:
    def __init__(self):
        self.gen_count = 0  #count period
        self.gen_period = 120   # (unit: frame)
        self.reserved_members = []
        self.expedition = []  # don't change this line until you do the EX.3

    def campaign(self):
        """
        Send an enemy to go on an expedition once 120 frame
        :return: None
        """
        if self.is_empty()==False and self.gen_count==self.gen_period:
            self.expedition.append(self.reserved_members.pop())  #remove self.reserved_members put in to self.expedition
            self.gen_count=0
        elif self.is_empty()==True:  #if self.reserved_members is empty self.gen_count=0
            self.gen_count=0
        else:
            self.gen_count+=1

    def generate(self, num):
        """
        Generate the enemies in this wave
        :param num: enemy number
        :return: None
        """
        for i in range(num):  #傳入"num"個Enemy()到self.reserved_members中
            self.reserved_members.append(Enemy())

        global count  #按下'n'按鍵的次數+1(有新的Enmey即將輸出,代表有按下按鍵)
        count+=1

    def get(self):
        """
        Get the enemy list
        """
        return self.expedition

    def is_empty(self):
        """
        Return whether the enemy is empty (so that we can move on to next wave)
        """
        return False if self.reserved_members else True

    def retreat(self, enemy):
        """
        Remove the enemy from the expedition
        :param enemy: class Enemy()
        :return: None
        """
        self.expedition.remove(enemy)





