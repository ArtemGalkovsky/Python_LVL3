from mcpi.minecraft import Minecraft
mc=Minecraft.create()
import time
pos=mc.player.getTilePos()
x=pos.x
y=pos.y
z=pos.z



def floor(x1, y1, z1, d, h, w):
    x2=x1+d-1
    y2=y1+h-1
    z2=z1+w-1
    mc.setBlocks(x1, y1, z1, x2, y2, z2, 159,8)
    mc.setBlocks(x1+1, y1+1, z1, x2-1, y2-1, z1, 102)
    mc.setBlocks(x1+1, y1+1, z2, x2-1, y2-1, z2, 102)
    mc.setBlocks(x1+1, y1+1, z1+1, x2-1, y2-1, z2-1, 0)

def fillFloor(f, x, y, z):
    floor = {
        "num": f,
        "xyz": (x, y, z)
    }
    if f == 1:
        #divan 1
        mc.setBlocks(x+5,y,z,x+12,y,z,35,15)
        mc.setBlock(x+5,y,z+1,35,15)
        mc.setBlock(x+12,y,z+1,35,15)
        #divan 2
        mc.setBlocks(x+1,y,z+2,x+1,y,z+5,35,15)
        mc.setBlocks(x+2,y,z+2,35,15)
        mc.setBlocks(x+2,y,z+4,35,15)
        # divan 3
        mc.setBlock(x+15,y,z+2,35,15)
        mc.setBlock(x+15,y,z+5,35,15)
        mc.setBlocks(x+16,y,z+2,x+16,y,z+5,35,15)
        #knizhnaya polka
        mc.setBlocks(x,y,z+12,x,y+8,z+16,47)
        mc.setBlocks(x+17,y,z+12,x+17,y+8,z+16,47)
        mc.setBlocks(x+2,y-1,z+13,x+15,y-1,z+15,35,8)
        mc.setBlocks(x+4,y-1,z+3,x+13,y-1,z+5,35,8)
        mc.setBlocks(x+14,y,z+10,x+14,y,z+11,35,15)
        mc.setBlocks(x+3,y,z+8,x+15,y,z+11,35,15)
        mc.setBlocks(x+4,y,z+17,x+13,y+8,z+17,35,15)
        mc.setBlocks(x+2,y,z+17,x+3,y+8,z+17,18,1)
        mc.setBlocks(x+13,y,z+17,x+15,y+8,z+17,18,1)
        mc.setBlocks(x,y+5,z,x,y+5,z+17,89)######1
        mc.setBlocks(x+17,y+5,z,x+17,y+5,z+17,89)
        #mc.player.setPos(x,y+8,z)
        #dinamit
        dinamit = (x, y-1, z+17, 46)
        mc.setBlock(*dinamit)
        floor["dinamit"] = dinamit
        
    elif f == 2:
        #kover
        mc.setBlocks(x,y-1,z,x+11,y-1,z+17,35,8)
        #cvet
        mc.setBlocks(x,y,z,x,y+8,z+17,89)
        #rasteniya
        mc.setBlocks(x,y,z+2,x,y+5,z+5,18)
        mc.setBlocks(x,y,z+12,x,y+5,z+15,18)
        #knizhnie polki
        mc.setBlocks(x+17,y,z,x+17,y+5,z+3,47)
        mc.setBlocks(x+17,y,z+14,x+17,y+5,z+17,47)
        # krovat
        mc.setBlocks(x+12,y,z+4,x+17,y,z+4,5,5)
        mc.setBlocks(x+12,y,z+4,x+12,y,z+13,5,5)
        mc.setBlocks(x+12,y,z+13,x+17,y,z+13,5,5)
        mc.setBlocks(x+17,y,z+5,x+17,y,z+12,35)
        mc.setBlocks(x+13,y,z+5,x+16,y,z+12,35,14)
        #cvet
        mc.setBlocks(x+17,y+5,z,x+17,y+5,z+17,89)
    elif f == 3:
        #knizhnie polki
        mc.setBlocks(x,y,z+1,x,y+5,z+16,47)
        #cvet
        mc.setBlocks(x,y+5,z,x+17,y+5,z,89)
        mc.setBlocks(x,y+5,z,x,y+5,z+17,89)
        mc.setBlocks(x,y+5,z+17,x+17,y+5,z+17,89)
        #rasteniya
        mc.setBlocks(x+17,y+4,z,x+17,y+4,z+1,18)
        mc.setBlocks(x+17,y+4,z+16,x+17,y+5,z+17,18)
        #doska
        mc.setBlocks(x+17,y,z+2,x+17,y+5,z+15,35,13)
        #stol uchitelya
        mc.setBlocks(x+14,y,z,x+14,y,z+3,5,2)
        mc.setBlock(x+15,y,z+4,5,2)
        #stoli uchenikov
        mc.setBlocks(x+12,y,z+3,x+12,y,z+5,5,2)
        mc.setBlocks(x+12,y,z+8,x+12,y,z+10,5,2)
        mc.setBlocks(x+12,y,z+13,x+12,y,z+15,5,2)
        mc.setBlocks(x+9,y,z+3,x+9,y,z+5,5,2)
        mc.setBlocks(x+9,y,z+8,x+9,y,z+10,5,2)
        mc.setBlocks(x+9,y,z+13,x+9,y,z+15,5,2)
        mc.setBlocks(x+6,y,z+3,x+6,y,z+5,5,2)
        mc.setBlocks(x+6,y,z+8,x+6,y,z+10,5,2)
        mc.setBlocks(x+6,y,z+13,x+6,y,z+15,5,2)
        mc.setBlocks(x+3,y,z+3,x+3,y,z+5,5,2)
        mc.setBlocks(x+3,y,z+8,x+3,y,z+10,5,2)
        mc.setBlocks(x+3,y,z+13,x+3,y,z+15,5,2)
    elif f == 4:
        #tratuar
        #mc.setBlocks(x,y-1,z+2,x+1,y-1,z+15,98)
        #mc.setBlocks(x+2,y-1,z+1,x+15,y-1,z,98)
        #mc.setBlocks(x+16,y-1,z+2,x+17,y-1,z+15,98)
        #mc.setBlocks(x+15,y-1,z+16,x+2,y-1,z+17,98)
        #proezzhaya chast
        #mc.setBlocks(x+2,y-1,z+2,x+15,y-1,z+15,4)
        #peshexodni ostrovok
        #mc.setBlocks(x+6,y-1,z+6,x+11,y-1,z+11,98)
        #mc.setBlocks(x+7,y-1,z+7,x+10,y-1,z+10,98)
        #svetofor

        ramka = (x+17, y, z+8, x+17, y+4, z+12)
        pole = (x+17, y+1, z+9, x+17, y+3, z+11)
        floor["pole"] = pole
        mc.setBlocks(*ramka, 89)
        mc.setBlocks(*pole, 5, 5)
        
        
    #elif f == 5:
    return floor
    

def neboskreb(x, y, z, floorsCount):
    neboskrebObj = {
        "xyz": (x, y, z)
    }
    floors = {}
    f=0
    while (f < floorsCount):
        floor(x, y+f*8, z, 20, 8, 20)
        floorObj = fillFloor(f+1, x+1, y+f*8+1, z+1)
        f+=1
        floors[f] = floorObj
        
    neboskrebObj["floors"] = floors
    return neboskrebObj

def hitInPole(event, pole):
    return (event.pos.x >= pole[0] and event.pos.x <= pole[3] and
            event.pos.y >= pole[1] and event.pos.y <= pole[4] and
            event.pos.z >= pole[2] and event.pos.z <= pole[5])

def xyzToXY(event, pole):
    return (event.pos.z - min(pole[2], pole[5]), event.pos.y - min(pole[1], pole[4]))

def gameHit(xy, game, t):
    print(xy, t, game)
    if game[xy[0]][xy[1]] == 0:
        game[xy[0]][xy[1]] = t
        return True
    return False

def setGameBlock(xy, pole, t):
    if t == 1:
        mc.setBlock(pole[0], xy[1] + min(pole[1], pole[4]), xy[0] + min(pole[2], pole[5]), 35, 5)
    else:
        mc.setBlock(pole[0], xy[1] + min(pole[1], pole[4]), xy[0] + min(pole[2], pole[5]), 35)

def hitComp(game, pole):
    if game[1][1] == 0:
        gameHit((1, 1), game, 2)
        setGameBlock((1, 1), pole, 2)
    else:
        x = 0
        for yl in game:
            y = 0
            for d in yl:
                print('test ', x, y, d, game)
                if (d == 0):
                    gameHit((x, y), game, 2)
                    setGameBlock((x, y), pole, 2)
                    return
                y += 1
            x += 1

def isGameFinishedBy(g, t):
    tt = (t, t, t)
    return (
        (g[0][0], g[0][1], g[0][2]) == tt or
        (g[1][0], g[1][1], g[1][2]) == tt or
        (g[2][0], g[2][1], g[2][2]) == tt or
        (g[0][0], g[1][0], g[2][0]) == tt or
        (g[0][1], g[1][1], g[2][1]) == tt or
        (g[0][2], g[1][2], g[2][2]) == tt or
        (g[0][0], g[1][1], g[2][2]) == tt or
        (g[0][2], g[1][1], g[2][0]) == tt
    )

def isGameNichya(g):
    for yl in game:
        for d in yl:
            if d == 0:
                return False
    return True
    

pos=mc.player.getTilePos()
x=pos.x
z=pos.z
y=pos.y

#platform
mc.setBlocks(x,y-1,z+1,x+50,y-1,z+50,2)
neboskrebObj = neboskreb(x,y-1,z+1,5)

time.sleep(5)

floors = neboskrebObj["floors"]
#1 itazh
floor1 = floors[1]
dinamit = floor1["dinamit"]
dinamitPos = dinamit[0:3]
playerPos = (0,0,0)

(fx, fy, fz) = floor1["xyz"]
mc.player.setPos(fx+1, fy, fz+1)
while playerPos != dinamitPos:
    time.sleep(0.5)
    pos = mc.player.getTilePos()
    playerPos = (pos.x, pos.y-1, pos.z)
    

print(' УРА, ты нашел динамит! Ты прошел первый уровень, поздравляю!')

#2 itazh
floor2 = floors[2]
(fx, fy, fz) = floor2["xyz"]
mc.player.setPos(fx+3, fy, fz+5)
temp=float(input('Какая у тебя температура '))
while temp<36 or temp>36.6:
    print('О нет, как жаль. Ты не можешь идти сегодня в школу!')
    time.sleep(5)
    temp=float(input('Какая у тебя температура '))
print('У тебя хорошая температура, иди в школу')


#3 itazh
floor3 = floors[3]
(fx, fy, fz) = floor3["xyz"]
mc.player.setPos(fx, fy, fz)

voprosi=[
    ('Какого газа в атмосфере Земли больше всего?\nа) кислород   б)углекислай газ   в)азот   г)водород','в'),
    ('Какой римской цифры не существует?\nа) 1000   б)0   в)10000   г)100000', 'б'),
    ('Планета Венера названа в честь человека?\n а)правда  б)ложь', 'б)'),
    ('Какой продукт никогда не портится?\nа) мед   б)оливковое  масло   в)черный перец  г)сушеные овощи', 'а'),
    ('Какое единственное млекопитающие не способно прыгать?\nа) слон   б)жираф   в)волк   г)носорог', 'а'),
    ('В какой стране появились Олимпийские игры?\nа)Россия   б)Испания   в)Италия   г)Греция', 'г'),
    ('Сколько океанов на нашей планете?\nа)4   б)6   в)5   г)7', 'в'),
    ('Какая самая длинная река в мире?\nа)Амазонка   б)Нил   в)Янцзы', 'а'),
    ('Сколько спутников у Земли?\nа)4   б)2   в)1   г)0', 'в')
]
otveti=[]

for vopr in voprosi:
    otvet=input('\n' + vopr[0] + '\n')
    otveti.append(otvet==vopr[1])

result=0
index=1
for otvet in otveti:
    if otvet:
        print(index, '. Верно')
        result += 1
    else:
        print(index, '. Неверно')
    index+=1

print('Количество набраных баллов: ', result)

#4 itazh
mc.events.clearAll()
(fx, fy, fz) = floors[4]["xyz"]
pole = floors[4]["pole"]
mc.player.setPos(fx+1, fy, fz+1)

game = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
finished = False
win = 0
while not finished:
    time.sleep(0.5)
    hits = mc.events.pollBlockHits()
    if len(hits) > 0:
        hit = hits[0]
        if hitInPole(hit, pole):
            hitXY = xyzToXY(hit, pole)
            if gameHit(hitXY, game, 1):
                setGameBlock(hitXY, pole, 1)
                if (isGameFinishedBy(game, 1)):
                    finished = True
                    win = 1
                else:
                    hitComp(game, pole)
                    if (isGameFinishedBy(game, 2)):
                        finished = True
                        win = 2
    if isGameNichya(game):
        finished = True

if win == 1:
    print('Вы выиграли')
elif win == 0
    print('Ничья')
else:
    print('Вы проиграли')




