import os
import random
import math
import keyboard
from pyconio import gotoxy
from PIL import Image

szilard = {'█', '░', '▒'}
szilard_jatekosnak = szilard | {'☻'}
szilard_ellenfelnek = szilard | {'☺', '☻'}

menupontok = [
    'START GAME',
    'LOAD GAME',
    'EXIT'
]

uzenetek_halott_ellenfel = [
    'This is a corpse of a once moving enemy.',
    'This thing is dead...',
    'I think it\'s dead.',
    'Smells bad...',
    'There\'s nothing just a corpse.'
]

class Timer:
    def __init__(self, max, on=True):
        self.max = max
        self.on = on
        self.value = 0
        self.bool = False

    def reset(self):
        self.value = 0

    def tick(self):
        if self.on:
            if self.value <= self.max:
                self.value += 1
            else:
                self.reset()
                self.bool = not self.bool

class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return '({}, {})'.format(self.x, self.y)

class Palya:
    def __init__(self, szel=40, mag=20):
        self.szel = szel
        self.mag = mag
        self.adat = [[' ' for x in range(szel)] for y in range(mag)]
    
    def beolvas(self, file='sziget.txt'):
        # BEOLVASÁS TXT-BŐL
        if file.split('.')[1] == 'txt':
            sziget = []
            with open(file, 'rt') as f:
                for sor in f:
                    try:
                        sziget.append(float(sor))
                    except:
                        raise ValueError('Nem sikerült floattá alakítani: {}'.format(sor))
            self.mag = int(math.sqrt(len(sziget)))
            self.szel = self.mag
            self.adat = [[' ' for x in range(self.szel)] for y in range(self.mag)]

            for y in range(0, self.mag):
                for x in range(0, self.szel):
                    tmp = float(sziget[(y*self.szel)+x])
                    if tmp > 0.85: #hegy
                        self.adat[y][x] = '▒'
                    elif tmp > 0.50: #tenger
                        if random.randint(0, 100) > 1:
                            self.adat[y][x] = ' '
                        else:
                            self.adat[y][x] = ','
                    else:
                        self.adat[y][x] = '░'

        # BEOLVASÁS PNG-BŐL
        elif file.split('.')[1] == 'png':
            zold = (50, 255, 50)
            kek = (50, 50, 255)
            szurke = (170, 170, 170)
            try:
                im = Image.open(file)
                pixels = im.load()
                self.szel = im.width
                self.mag = im.height
                self.adat = [[' ' for _ in range(self.szel)] for _ in range(self.mag)]
                for y in range(self.mag):
                    for x in range(self.szel):
                        if pixels[x, y] == zold:
                            if random.randint(0, 500) > 1:
                                self.adat[y][x] = ' '
                            else:
                                self.adat[y][x] = ','
                        elif pixels[x, y] == kek:
                            self.adat[y][x] = '░'
                        elif pixels[x, y] == szurke:
                            self.adat[y][x] = '▒'
                        else:
                            self.adat[y][x] = 'E' # debug ha nincs ilyen
            except:
                raise FileNotFoundError('PNG megnyitása nem sikerült!')
        
        # 16x16-OS TÉRKÉP RAJZOLÁS
        self.terkep = [[' ' for _ in range(16)] for _ in range(16)]
        chunk = self.szel // 16
        for y in range(16):
            for x in range(16):
                tmp = self.adat[y*chunk + (chunk//2)][x*chunk + (chunk//2)]
                if tmp == ',':
                    tmp = ' '
                self.terkep[y][x] = tmp

    def kirajzol(self, x=0, y=0):
        for yy in range(0, self.mag):
            for xx in range(0, self.szel):
                gotoxy(x+xx, y+yy)
                print(self.adat[yy][xx], end='')

class Kamera:
    SZEL = 40
    MAG = 20

    def __init__(self, palya=Palya(), shift_x=0, shift_y=0):
        self.palya = palya
        self.shift_x = shift_x
        self.shift_y = shift_y
        self.adat = [[' ' for x in range(self.SZEL)] for y in range(self.MAG)]
        for y in range(0, self.MAG):
            for x in range(0, self.SZEL):
                if self.adat[y][x] != palya.adat[y+shift_y][x+shift_x]:
                    self.adat[y][x] = palya.adat[y+shift_y][x+shift_x]

    def kirajzol(self, x=0, y=0):
        for yy in range(0, self.MAG):
            for xx in range(0, self.SZEL):
                gotoxy(xx+x, yy+y)
                print(self.adat[yy][xx], end='')
    
    def terkep_kirajzol(self, x, y, j, bool):
        gotoxy(x, y)
        print('{:▓>17}▓'.format('BACKSPACE'), end='')
        for yy in range(16):
            gotoxy(x, y+yy+1)
            print('▓', end='')
            gotoxy(x+17, y+yy+1)
            print('▓', end='')
        gotoxy(x, y+17)
        print('▓'*18, end='')
        for yy in range(16):
            for xx in range(16):
                gotoxy(xx+x+1, yy+y+1)
                print(self.palya.terkep[yy][xx], end='')
        if bool:
            gotoxy(x+1+(int(j.x)//64), y+1+(int(j.y)//64))
            print(j.skin, end='')

    def render(self):
        if self.shift_x > self.palya.szel-self.SZEL:
            self.shift_x = self.palya.szel-self.SZEL
        if self.shift_x < 0:
            self.shift_x = 0
        if self.shift_y > self.palya.mag-self.MAG:
            self.shift_y = self.palya.mag-self.MAG
        if self.shift_y < 0:
            self.shift_y = 0

        for y in range(0, self.MAG):
            for x in range(0, self.SZEL):
                if self.adat[y][x] != self.palya.adat[y+self.shift_y][x+self.shift_x]:
                    self.adat[y][x] = self.palya.adat[y+self.shift_y][x+self.shift_x]
                    gotoxy(x, y)
                    print(self.adat[y][x])

class Fegyver:
    def __init__(self, name, acc, x=0, y=0):
        self.name = name
        self.skin = '☼'
        self.acc = acc
        self.x = x
        self.y = y
        self.image_fn = os.path.join(os.path.dirname(__file__), 'weapons/{}.png'.format(self.name))
        self.image = [[' ' for _ in range(40)] for _ in range(20)]
        self.image_upload(self.image_fn)

    def __str__(self):
        return '{} [{}]'.format(self.name, self.acc * 10)

    def image_upload(self, file):
        try:
            im = Image.open(file)
        except:
            raise FileNotFoundError('Fegyver PNG nem található:', file)

        pixels = im.load()
        if im.width != 40 or im.height != 20:
            raise ValueError('Képméret nem stimmel!')
        for y in range(20):
            for x in range(40):
                if pixels[x, y] == (0, 0, 0):
                    self.image[y][x] = '▒'
                elif pixels[x, y] == (170, 170, 170):
                    self.image[y][x] = '░'
                elif pixels[x, y] != (255, 255, 255):
                    self.image[y][x] = 'E'
    
    def image_draw(self):
        for y in range(20):
            for x in range(40):
                gotoxy(x, y)
                print(self.image[y][x], end='')
        gotoxy(0, 0)
        print(self.name.upper())

class Jatekos:
    skin = '☺'
    stamina = 1000
    mozog = False
    fegyver = Fegyver('stone', 0.2)

    '''
    Állapotok:
        0 = szabad/mozog
        1 = harc mással
    '''

    def __init__(self, palya=Palya(), kam=Kamera(), x=0, y=0):
        self.palya = palya
        self.kam = kam
        self.x = x
        self.y = y
        self.alap_seb = 0.2
        self.amin_all = self.palya.adat[y][x]
        self.palya.adat[y][x] = self.skin

        self.state = 0

        self.statok()

    def mozgat(self):
        ##SZABAD ÁLLAPOT
        if self.state == 0:
            elozo_x = self.x
            elozo_y = self.y

            ##SEBESSEG KEZELES
            if keyboard.is_pressed('left shift') and self.stamina > 5 and self.mozog:
                speed_x = self.alap_seb * 1.25
                self.stamina -= 5
            else:
                speed_x = self.alap_seb
                if self.stamina < 1000:
                    self.stamina += 1
                if self.stamina > 1000:
                    self.stamina = 1000
            speed_y = speed_x * 0.75

            # BILLENTYŰK
            if keyboard.is_pressed('d'):
                self.x += speed_x
            if keyboard.is_pressed('a'):
                self.x -= speed_x
            if keyboard.is_pressed('s'):
                self.y += speed_y
            if keyboard.is_pressed('w'):
                self.y -= speed_y

            ##MAS DOLGOKKAL VALO INTERAKCIO
            if round(elozo_x) != round(self.x):
                if self.palya.adat[round(self.y)][round(self.x)] in szilard_jatekosnak:
                    self.x = elozo_x
                    self.speed_x = self.speed_y = 0
            if round(elozo_y) != round(self.y):
                if self.palya.adat[round(self.y)][round(self.x)] in szilard_jatekosnak:
                    self.y = elozo_y
                    self.speed_x = self.speed_y = 0

            ##PALYAN MOZGATAS
            self.palya.adat[round(elozo_y)][round(elozo_x)] = self.amin_all
            self.amin_all = self.palya.adat[round(self.y)][round(self.x)]
            self.palya.adat[round(self.y)][round(self.x)] = self.skin

            ##KAMERA MOZGATAS
            if round(self.x) > round(self.kam.SZEL/2-1) and round(self.x) < round(self.palya.szel - self.kam.SZEL/2 + 1):
                self.kam.shift_x = round(self.x - self.kam.SZEL/2)
            if round(self.y) > round(self.kam.MAG/2-1) and round(self.y) < round(self.palya.mag - self.kam.MAG/2 + 1):
                self.kam.shift_y = round(self.y - self.kam.MAG/2)
        else:
            gotoxy(0, 0)
            print('HIBA: NINCS ILYEN ÁLLAPOT')
            input()

        ##ALLAPOTTOL FUGGETLEN DOLGOK
        #STAMINA RAJZOLAS
        gotoxy(self.kam.SZEL + 2, 0)
        print('STA' + '▓'*(self.stamina//100) + '░'*(10-self.stamina//100), end='')

        #MOZGAS KEZELES
        if elozo_x == self.x and elozo_y == self.y:
            self.mozog = False
        else:
            self.mozog = True

    def statok(self):
        gotoxy(42, 2)
        print('WEAPON: {}      '.format(self.fegyver))

class Ellenfel:
    speed_x = 0.0
    speed_y = 0.0
    state = 0
    target = None

    def __init__(self, palya, jatekos, x=0, y=0, skin='☻'):
            self.palya = palya
            self.jatekos = jatekos
            self.x = x
            self.start_x = x
            self.start_y = y
            self.y = y
            self.skin = skin
            self.amin_all = self.palya.adat[y][x]
            self.palya.adat[y][x] = self.skin

    def mozgat(self):
        elozo_x = self.x
        elozo_y = self.y
        
        if self.speed_x == 0 and self.speed_y == 0:
            self.start_x = round(self.x)
            self.start_y = round(self.y)
            self.target = Coord(
                random.randint(self.start_x-10, self.start_x+10),
                random.randint(self.start_y-10, self.start_y+10))
        
        a = self.target.x - self.x
        b = self.target.y - self.y
        #0-val való osztás korrigálás
        if a == 0:
            a = 0.00001
        alpha = math.atan(b/a)
        self.speed_x = abs(math.cos(alpha) * 0.1)
        self.speed_y = abs(math.sin(alpha) * 0.1)
        if self.target.x < self.x:
            self.speed_x = -self.speed_x
        if self.target.y < self.y:
            self.speed_y = -self.speed_y
        
        if abs(int(self.x) - (self.target.x)) < 2:
            self.speed_x = 0
        if abs(int(self.y) - int(self.target.y)) < 2:
            self.speed_y = 0
        
        self.x += self.speed_x
        self.y += self.speed_y

        if round(elozo_x) != round(self.x):
            if self.palya.adat[round(self.y)][round(self.x)] in szilard_ellenfelnek:
                self.x = elozo_x
                self.speed_x = 0
        if round(elozo_y) != round(self.y):
            if self.palya.adat[round(self.y)][round(self.x)] in szilard_ellenfelnek:
                self.y = elozo_y
                self.speed_y = 0
        
        self.palya.adat[round(elozo_y)][round(elozo_x)] = self.amin_all
        self.amin_all = self.palya.adat[round(self.y)][round(self.x)]
        self.palya.adat[round(self.y)][round(self.x)] = self.skin
    
    def meghal(self):
        self.palya.adat[round(self.y)][round(self.x)] = 'X'
