import pygame as pg
import os,time
from pygame.locals import *
import sudoku_generator as generator
import sudoku_checker 
import sudoku_ai as ai
import win32gui,win32api,win32con


FPS = 30
Pre = None
Blank = None
BlankInfo = None


os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" %(0,0)
Pre_Color = (100,100,100)
Hover_Color = (200,200,200)
Blank_Color = (180,180,180)
Danger_Color = (200,100,100)
Number_Color = (255,255,255)
Background_Color = (0,0,0)
Row_Count = 9
Column_Count = 9

WINDOW_W = 900
WINDOW_H = 900


PILE_GAP = 5
PILE_W = (WINDOW_W - (Row_Count + 2) * PILE_GAP - ((Row_Count//3)-1) *0.5* PILE_GAP)/Row_Count
PILE_H = PILE_W


Ai = False
Ai_Inteval = 0.4



pg.init()
pg.font.init()
WINDOW = pg.display.set_mode((WINDOW_W,WINDOW_H))
pg.display.set_caption("美丽的数独")

WINDOW.fill(Background_Color)

NUMBER_FONT = pg.font.Font("C:\Windows\Fonts\STXIHEI.TTF",60)

FILL_SOUND = pg.mixer.Sound("./audios/fill.wav")


def update_fun(index):
    y = index//9
    x = index%9
    drawBoard([x,y])
    pg.mixer.Sound.play(FILL_SOUND)
    move_cursor(index)
    pg.display.update()


def move_cursor(index):
    y = index//9
    x = index%9
    left,top = getLeftTopOfPile(x,y)
    win32api.SetCursorPos((int(left+PILE_W/2),int(top+PILE_H/2)))



def main():
    global Pre,Blank,BlankInfo
    clock = pg.time.Clock()
    mouse_pos = None
    Pre,Blank,BlankInfo = initBoard()
    active_pile = None


    ll =0
    my_str = ["这","次","一","定"]


    if(Ai):
        ai.solve(Blank,update_fun,Ai_Inteval)


    while True:
        clock.tick(FPS)

        mouse_right = False
        mouse_left = False
        


        for event in pg.event.get(): 
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pg.quit()
                quit()
                break
            elif event.type == MOUSEMOTION:
                mouse_pos = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                #left click
                if(event.button==1):
                    mouse_left = True
                #right click
                elif(event.button==3):
                    mouse_right = True
            elif event.type == pg.KEYDOWN:
                if(active_pile!=None):
                    if(event.key == pg.K_1):

                        fillBlank(my_str[ll],active_pile)
                        ll+=1
                    # if(event.key == pg.K_2):
                    #     fillBlank(12,active_pile)
                    # if(event.key == pg.K_3):
                    #     fillBlank(13,active_pile)
                    # if(event.key == pg.K_4):
                    #     fillBlank(14,active_pile)
                    # if(event.key == pg.K_5):
                    #     fillBlank(15,active_pile)
                    # if(event.key == pg.K_6):
                    #     fillBlank(16,active_pile)
                    # if(event.key == pg.K_7):
                    #     fillBlank(17,active_pile)
                    # if(event.key == pg.K_8):
                    #     fillBlank(18,active_pile)
                    # if(event.key == pg.K_9):
                    #     fillBlank(19,active_pile)
                  

                    sudoku_checker.check_valid(Blank,BlankInfo)
                    
                    

            

        #if mouse left click 

        pileHover = getPileFromPoint(mouse_pos)
        if(pileHover!=None):
            if(Pre[pileHover[1]][pileHover[0]]==0):
                active_pile = pileHover
                # if(mouse_left):
                #     awakePile(pileHover[0],pileHover[1])
                # else:
        else:
            active_pile = None
        

        drawBoard(active_pile)
        pg.display.update()




def hoverPile(x,y):
    left,top = getLeftTopOfPile(x,y)
    pg.draw.rect(WINDOW,Hover_Color,(left,top,PILE_W,PILE_H))



def awakePile(x,y):
    pass


def fillBlank(number,active_pile):
    Blank[active_pile[1]][active_pile[0]] = number
    pg.mixer.Sound.play(FILL_SOUND)

    
    


def getPileFromPoint(mouse_pos):
    mousex = mouse_pos[0]
    mousey = mouse_pos[1]

    for y in range(Row_Count):
        for x in range(Column_Count):
            left,top = getLeftTopOfPile(x,y)
            rect = pg.Rect((left,top,PILE_W,PILE_H))

            if rect.collidepoint(mousex,mousey):
                return x,y
    
    return None



def getLeftTopOfPile(x,y):
    xGapCount = x//3
    yGapCount = y//3
    left = x*(PILE_W+PILE_GAP) + PILE_GAP + xGapCount * 0.5*PILE_GAP
    top = y*(PILE_H+PILE_GAP) + PILE_GAP + yGapCount * 0.5* PILE_GAP
    return left,top




def drawBoard(active_pile):
    for y in range(Row_Count):
        for x in range(Column_Count):
            xGapCount = x//3
            yGapCount = y//3
            left = x*(PILE_W+PILE_GAP) + PILE_GAP + xGapCount * 0.5*PILE_GAP
            top = y*(PILE_H+PILE_GAP) + PILE_GAP + yGapCount * 0.5* PILE_GAP
            pg.draw.rect(WINDOW,Pre_Color,(left,top,PILE_W,PILE_H))



            if active_pile != None and x == active_pile[0] and y == active_pile[1]:
                if(Pre[y][x]==0):
                    pg.draw.rect(WINDOW,Hover_Color,(left,top,PILE_W,PILE_H))


            if(Pre[y][x]!=0):
                drawText(str(Pre[y][x]),left+PILE_W/2,top+PILE_W/2,NUMBER_FONT,Number_Color)
            else:
                if(BlankInfo[y][x]==False):
                    pg.draw.rect(WINDOW,Danger_Color,(left,top,PILE_W,PILE_H))
                if(Blank[y][x]!=0):
                    drawText(str(Blank[y][x]),left+PILE_W/2,top+PILE_W/2,NUMBER_FONT,(0,200,0))

    

def drawText(text,x,y,font,color):
    text = font.render(text,True,color)
    rect = text.get_rect()
    rect.centerx = x
    rect.centery = y
    WINDOW.blit(text,rect)

def initBoard():
    pre = generator.main("Medium")
    blank = []
    info = []



    for y in range(len(pre)):
        blank.append([])
        info.append([])
        for x in range(len(pre[y])):
            blank[y].append(pre[y][x])
            info[y].append(True)


    return pre,blank,info
    


if __name__ == "__main__":
    main()