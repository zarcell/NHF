# A BEKERETEZETT DOLGOK DIREKT VANNAK BEKERETEZVE, DO NOT TOUCH

from pyconio import gotoxy, flush
from PIL import Image
import cursor
import keyboard
import time
import math
import os
import random

from osztalyok import menupontok, szilard, szilard_ellenfelnek, szilard_jatekosnak, uzenetek_halott_ellenfel
from osztalyok import Timer, Coord, Palya, Kamera, Jatekos, Ellenfel, Fegyver

def tavolsag(c1, c2):
    return math.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2)

def uzenet(szoveg, lesz_e_kerdes=False):
    pont = ((40-30)//2, (20-12)//2)
    gotoxy(pont[0], pont[1])
    print('▓'*30, end='')
    for y in range(10):
        gotoxy(pont[0], pont[1]+1+y)
        print('▓' + ' '*28 + '▓', end='')
    gotoxy(pont[0], pont[1]+11)
    print('▓'*30, end='')

    szoveg = szoveg.split(' ')
    sor = 0
    sor_hoszz = 0
    for szo in szoveg:
        if len(szo) + sor_hoszz > 26:
            sor += 1
            if sor > 5:
                sor = 0
                gotoxy(pont[0]+2, pont[1]+2+7)
                print('{:^26}'.format('<ENTER>'))
                while not keyboard.is_pressed('enter'):
                    pass
                for y in range(8):
                    gotoxy(pont[0]+2, pont[1]+2+y)
                    print(' '*26, end='')
            sor_hoszz = 0
        gotoxy(pont[0]+2+sor_hoszz, pont[1]+2+sor)
        print(szo, end=' ')
        sor_hoszz += len(szo) + 1
        time.sleep(0.05)

    time.sleep(0.5)
    
    if not lesz_e_kerdes:
        gotoxy(pont[0]+2, pont[1]+8)
        print('{:^26}'.format('[ENTER]'))

        while not keyboard.is_pressed('enter'):
            pass

def kerdes(szoveg):
    uzenet(szoveg, True)

    pont = ((40-30)//2, (20-12)//2)
    gotoxy(pont[0]+2, pont[1]+8)
    print('{:^26}'.format('[SPACE]      [BACKSPACE]'))
                
    while True:
        if keyboard.is_pressed('backspace'):
            return False
        if keyboard.is_pressed('space'):
            return True

def tutorial(fegyver):
    gotoxy(42, 2)
    print(' '*20)
    if kerdes('Do you need a short tutorial?'):
        uzenet('Alright! Let me tell you...')
        uzenet('☺ <-this is you.')
        uzenet('☻ <-and this is an enemy.')
        if not kerdes('So far it\'s simple. Right?'):
            uzenet('Come on, it\'s not that hard...')
        uzenet('You can move with the <WASD> keys.')
        uzenet('You are on a big island, if you want to see how big it is just press <M>.')
        uzenet('Not now... When you will be on the field!')
        gotoxy(42, 0)
        print('STA' + '▓'*10)
        uzenet('If you want to go faster, just hold <SHIFT>. Although, you have a stamina (shown top right) which you need for running faster.')
        gotoxy(42, 2)
        print('WEAPON: {}'.format(fegyver))
        uzenet('Another thing you can find in your way are weapons.')
        uzenet('☼ <-this is a weapon!')
        uzenet('If you find one, step on it and press <F>.')
        uzenet('Not for respect this time...')
        uzenet('You can inspect anything by stepping on it and pressing <F>.')
        uzenet('I think I told you everything you need for now.')
        uzenet('Oh, yes, one more thing!')
        uzenet('░ <- this is water, you can\'t swim.')
        uzenet('▒ <- and this is solid rock, also you can\'t swim in it.')
        uzenet('Now let\'s go and explore!')
        uzenet('and don\'t forget to press <M> sometimes!')
    else:
        gotoxy(42, 0)
        print('STA' + '▓'*10)
        gotoxy(42, 2)
        print('WEAPON: {}'.format(fegyver))

def csata(j, e):
    kep_file = os.path.join(os.path.dirname(__file__), 'csata.png')
    try:
        im = Image.open(kep_file)
        pixels = im.load()
    except:
        raise FileNotFoundError('PNG nem található: {}'.format(kep_file))

    kep = [[' ' for _ in range(40)] for _ in range(20)]
    for y in range(20):
        for x in range(40):
            gotoxy(x, y)
            c = pixels[x, y]
            if c == (170, 170, 170): #szürke
                kep[y][x] = '░'
            elif c == (255, 255, 255): #fehér
                kep[y][x] = ' '
            elif c == (0, 0, 0): #fekete
                kep[y][x] = '▒'

    lovedek = '•'
    e_tav = 25
    celzas = j.fegyver.acc *100
    jatekos_halott = False
    vege = False
    elfutas = False
    
    def kep_kirajzol():
        for y in range(20):
            for x in range(40):
                gotoxy(x, y)
                print(kep[y][x], end='')
        gotoxy(7, 14)
        print(j.skin)
        gotoxy(7+e_tav, 14)
        print(e.skin)
        gotoxy(5, 16)
        print('◄A▒D►')

    kep_kirajzol()
    time.sleep(0.5)
    while not vege:
        kep_kirajzol()

        while not (keyboard.is_pressed('d') or keyboard.is_pressed('a')):
            pass
        
        if keyboard.is_pressed('a') and not keyboard.is_pressed('d'): #menekules
            uzenet('You are trying to run away...')
            if random.randint(1, 6) > 4:
                elfutas = True
                vege = True
                uzenet('...and you managed to run away!')
            else:
                uzenet('...but you can\'t, keep fighting!')
                e_tav -= 24//6
                celzas *= 1.1
        
        if keyboard.is_pressed('d') and not keyboard.is_pressed('a'): #loves
            gotoxy(8, 14)
            print(lovedek, end='')
            for i in range(1, 40-8):
                gotoxy(7+i, 14)
                if i != e_tav:
                    print(' ', end='')
                    if i+1 != e_tav:
                        gotoxy(7+i+1, 14)
                        print(lovedek, end='')
                    time.sleep(0.014)
                elif random.randint(0, 100) <= celzas:
                    vege = True
                    print('X', end='')
                    time.sleep(0.7)
                    break
                else:
                    e_tav -= 24//6
                    celzas *= 1.1
            gotoxy(39, 14)
            print(' ', end='')
            
        if e_tav <= 1:
            e_tav = 1
            jatekos_halott = True
            vege = True
            uzenet('Too late, the enemy catched you...')
    
    if elfutas:
        e.state = 1
    else:
        if jatekos_halott:
            uzenet('You died...')
            return False
        else:
            e.state = -1
    return True

class Menu:
    def __init__(self, mp):
        self.menupontok = mp
        self.menu_index = 0

    def kirajzol(self):
        gotoxy(0, 0)
        for _ in range(20):
            print(' '*80)
        
        yy = (20-len(self.menupontok))//2
        n = 0
        for sor in self.menupontok:
            n = len(sor) if len(sor) > n else n
        xx = (40-n)//2

        for y in range(len(self.menupontok)):
            gotoxy(xx, yy+y)
            print(self.menupontok[y])

        while True:
            for i in range(len(self.menupontok)):
                gotoxy(xx-2, yy+i)
                if i == self.menu_index:
                    print('☺', end='')
                else:
                    print(' ', end='')
            if keyboard.is_pressed('w') or keyboard.is_pressed('up'):
                self.menu_index -= 1
                if self.menu_index < 0:
                    self.menu_index = len(self.menupontok)-1
            
            if keyboard.is_pressed('s') or keyboard.is_pressed('down'):
                self.menu_index += 1
                if self.menu_index > len(self.menupontok)-1:
                    self.menu_index = 0
            
            if keyboard.is_pressed('enter'):
                break

            time.sleep(0.05)
            
class DolgokPalyan:
    def __init__(self, p):
        self.p = p
        self.adat = {}
    
    def at(self, hol):
        return self.adat[hol]

    def hozza_ad(self, mit, hova):
        if self.p.adat[mit.y][mit.x] not in szilard_ellenfelnek:
            self.p.adat[mit.y][mit.x] = mit.skin
            self.adat[hova] = mit
    
    def benne_van(self, hol):
        return hol in self.adat
    
    def kivesz(self, honnan):
        del self.adat[honnan]

class Game:
    def __init__(self):
        self.fut = True
        self.gameState = 0
        self.p = Palya()
        gotoxy(0, 9)
        print('{:^40}'.format('Loading map...'))
        self.p.beolvas(os.path.join(os.path.dirname(__file__), 'sziget.png'))

        self.k = Kamera(self.p)
        self.k.kirajzol()

        self.j = Jatekos(self.p, self.k, 476, 178)

        self.enemies = []
        self.enemies.append(Ellenfel(self.p, self.j, self.j.x+10, self.j.y-10))
        for _ in range(1000):
            while True:
                r_x = random.randint(0, 1023)
                r_y = random.randint(0, 1023)
                if str(self.p.adat[r_y][r_x]) not in szilard_ellenfelnek and tavolsag((self.j.x, self.j.y), (r_x, r_y)) >= 15:
                    self.enemies.append(Ellenfel(self.p, self.j, r_x, r_y))
                    break

        self.dolgok = DolgokPalyan(self.p)
        fegyo = Fegyver('sling-shot', 0.35, round(self.j.x+3), round(self.j.y))
        self.dolgok.hozza_ad(fegyo, (fegyo.x, fegyo.y))

        self.timers = []
        self.timers.append(Timer(20))

        tutorial(self.j.fegyver)
    
    def run(self):
        if self.gameState == 0:
            self.j.mozgat()

            for e in self.enemies:
                tav_jatekostol = tavolsag( (self.j.x, self.j.y), (e.x, e.y) )
                if e.state == 1:
                    if tav_jatekostol >= 10:
                        e.state = 0
                else:
                    if tav_jatekostol <= 2.2:
                        self.fut = csata(self.j, e)
                        self.k.kirajzol()
                        if not self.fut:
                            break
                    elif tav_jatekostol <= 8:
                        e.target = Coord(self.j.x, self.j.y)
                    if e.state == -1:
                        e.meghal()
                        self.enemies.remove(e)
                        self.k.kirajzol()
                    elif e.state == 0:
                        e.mozgat()
            
            self.k.render()

            if keyboard.is_pressed('f'):
                if self.j.amin_all == '☼':
                    valasz = kerdes('You have found {}! Do you want to change your {}?'.format(self.dolgok.at((round(self.j.x), round(self.j.y))), self.j.fegyver))
                    if valasz:
                        self.j.fegyver = self.dolgok.at((round(self.j.x), round(self.j.y)))
                        self.dolgok.kivesz((round(self.j.x), round(self.j.y)))
                    self.j.amin_all = ' '
                    self.k.kirajzol()
                    self.j.statok()
                elif self.j.amin_all == 'X':
                    r = random.randint(0, len(uzenetek_halott_ellenfel)-1)
                    uzenet(uzenetek_halott_ellenfel[r])
                    self.k.kirajzol()
            
            if keyboard.is_pressed('m'):
                self.gameState = 1
                self.k.terkep_kirajzol(11, 1, self.j, True)

        elif self.gameState == 1:
            self.timers[0].tick()
            if self.timers[0].value == self.timers[0].max -1:
                if self.timers[0].bool:
                    self.k.terkep_kirajzol(11, 1, self.j, False)
                else:
                    self.k.terkep_kirajzol(11, 1, self.j, True)
            if keyboard.is_pressed('backspace'):
                self.k.kirajzol()
                self.gameState = 0
            

        if keyboard.is_pressed('escape'):
            valasz = kerdes('You sure you want to quit the game? You can\'t save progress yet!')
            if valasz:
                self.fut = False
            else:
                self.k.kirajzol()

        flush()

def main():
    cursor.hide()

    ################################
    fps = float(40)                #
    frameDelay = float(1000 / fps) #
    ################################

    menu = Menu(menupontok)
    menu.kirajzol()
    game = Game()

    run = True
    while run:
    #################################################
        starting_time = float(time.time() * 1000)   #
    #################################################

        game.run()
        
        if not game.fut:
            run = False

    #############################################################
        taken_time = float(time.time() * 1000) - starting_time  #
        if frameDelay > taken_time:                             #
            time.sleep(float((frameDelay - taken_time) / 1000)) #
    #############################################################

main()