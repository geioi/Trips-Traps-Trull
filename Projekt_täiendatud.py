#Arvuti on võitmatu (Sellepärast, et ta ei taha oodata inimese käiku, vaid... 
#...märgib kõik lahtrid korraga ära, seega töötab korralikult ainult...
#...kahe mängijaga versioon :(   )

import pygame
from pygame.locals import *

pygame.init()

#Nupu loomise funktsioonid menüü jaoks on loodud Simon H. Larsen'i poolt, mitte isiklikult välja mõeldud!
class Button:
    def create_button(self, surface, color, x, y, length, height, width, text, text_color):
        surface = self.draw_button(surface, color, length, height, x, y, width)
        surface = self.write_text(surface, text, text_color, length, height, x, y)
        self.rect = pygame.Rect(x,y, length, height)
        return surface

    def write_text(self, surface, text, text_color, length, height, x, y):
        font_size = int(length//len(text))
        myFont = pygame.font.SysFont("Calibri", font_size)
        myText = myFont.render(text, 1, text_color)
        surface.blit(myText, ((x+length/2) - myText.get_width()/2, (y+height/2) - myText.get_height()/2))
        return surface

    def draw_button(self, surface, color, length, height, x, y, width):           
        for i in range(1,10):
            s = pygame.Surface((length+(i*2),height+(i*2)))
            s.fill(color)
            alpha = (255/(i+2))
            if alpha <= 0:
                alpha = 1
            s.set_alpha(alpha)
            pygame.draw.rect(s, color, (x-i,y-i,length+i,height+i), width)
            surface.blit(s, (x-i,y-i))
        pygame.draw.rect(surface, color, (x,y,length,height), 0)
        pygame.draw.rect(surface, (190,190,190), (x,y,length,height), 1)  
        return surface

    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False


võitja = None

XO = 'X' #X alustab

joonestik =  [ [ None, None, None ], #tühjad lahtrid

          [ None, None, None ],

          [ None, None, None ] ]

def loo_tabel(ttt):
    taust = pygame.Surface(ttt.get_size())
    taust = taust.convert()
    taust.fill((250,250,250))
    
    #tõmbame jooned
    
    pygame.draw.line(taust,(0,0,0),(100,0),(100,300),2) #vertikaalsed jooned
    pygame.draw.line(taust,(0,0,0),(200,0),(200,300),2)

    pygame.draw.line(taust,(0,0,0),(0,100),(300,100),2) #horisontaalsed jooned
    pygame.draw.line(taust,(0,0,0),(0,200),(300,200),2)
    return taust


def näita_tabelit(ttt, tabel):
    ttt.blit (tabel, (0,0))
    pygame.display.flip()

def hiire_positsioon_tabelis(Xkoordinaat, Ykoordinaat):
    if (Ykoordinaat < 100): #millisele reale klikib
        rida = 0
    elif (Ykoordinaat < 200):
        rida = 1
    else:
        rida = 2
    if (Xkoordinaat < 100): #millisele veerule klikib
        veerg = 0
    elif (Xkoordinaat < 200):
        veerg = 1
    else:
        veerg = 2
    return (rida, veerg)

def klikk_tabelis(tabel): #teeme kindlaks kuhu klikiti
    global joonestik, XO

    (Xkoordinaat, Ykoordinaat) = pygame.mouse.get_pos()

    (rida, veerg) = hiire_positsioon_tabelis (Xkoordinaat, Ykoordinaat)

    if joonestik[rida][veerg] == 'X' or joonestik[rida][veerg] == 'O': #kontrollime kas lahter on kasutusel
        return #lahter on juba kasutusel

    joonistamine (tabel, rida, veerg, XO) #joonista X või O
    
    if (XO == 'X'):
        XO = 'O' #käigu üleandmine teisele inimesele
    else:
        XO = 'X'


def joonistamine(tabel, tabelirida, tabeliveerg, Tähis):
    Xkeskkoht = tabeliveerg * 100 + 50
                                    #leiame keskkoha
    Ykeskkoht = tabelirida * 100 + 50

    if (Tähis == 'O'): #joonistame O
        pygame.draw.circle (tabel, (0,0,0), (Xkeskkoht, Ykeskkoht), 44, 2)

    else: #joonistame X
        pygame.draw.line (tabel, (0,0,0), (Xkeskkoht - 22, Ykeskkoht - 22), (Xkeskkoht + 22, Ykeskkoht + 22), 2)
        pygame.draw.line (tabel, (0,0,0), (Xkeskkoht + 22, Ykeskkoht - 22), (Xkeskkoht - 22, Ykeskkoht + 22), 2)

    joonestik[tabelirida][tabeliveerg] = Tähis #märgime lahtri kasutatuks


def mängu_võitja(tabel): #kontrollib, kas kumbki võitis
    global joonestik, võitja

    for rida in range (0, 3): #kontrollime ridu
        if joonestik [rida][0] == joonestik[rida][1] == joonestik[rida][2] and joonestik [rida][0] is not None:
            võitja = joonestik[rida][0] #see rida võitis
            pygame.draw.line (tabel, (250,0,0), (0, (rida + 1)*100 - 50), (300, (rida + 1)*100 - 50), 2)
            break

    for veerg in range (0, 3): #kontrollime veerge
        if joonestik[0][veerg] == joonestik[1][veerg] == joonestik[2][veerg] and joonestik[0][veerg] is not None:
            võitja = joonestik[0][veerg] #see veerg võitis
            pygame.draw.line (tabel, (250,0,0), ((veerg + 1)* 100 - 50, 0), ((veerg + 1)* 100 - 50, 300), 2)
            break

    if joonestik[0][0] == joonestik[1][1] == joonestik[2][2] and joonestik[0][0] is not None: #kontrollime diagonaale
        võitja = joonestik[0][0] #vasakult paremale diagonaal võitis
        pygame.draw.line (tabel, (250,0,0), (50, 50), (250, 250), 2)

    if joonestik[0][2] == joonestik[1][1] == joonestik[2][0] and joonestik[0][2] is not None:
        võitja = joonestik[0][2] #paremalt vasakule diagonaal võitis
        pygame.draw.line (tabel, (250,0,0), (250, 50), (50, 250), 2)


def joonistamine_inimene (tabel, tabelirida, tabeliveerg, Tähis):
    Xkeskkoht = tabeliveerg * 100 + 50
                                    #leiame keskkoha
    Ykeskkoht = tabelirida * 100 + 50

    pygame.draw.line (tabel, (0,0,0), (Xkeskkoht - 22, Ykeskkoht - 22), (Xkeskkoht + 22, Ykeskkoht + 22), 2)                                                                                                           #joonistame X
    pygame.draw.line (tabel, (0,0,0), (Xkeskkoht + 22, Ykeskkoht - 22), (Xkeskkoht - 22, Ykeskkoht + 22), 2)

    joonestik[tabelirida][tabeliveerg] = Tähis #märgime lahtri kasutatuks

def joonistamine_arvuti (tabel, tabelirida, tabeliveerg, Tähis):
    Xkeskkoht = tabeliveerg * 100 + 50
                                    #leiame keskkoha
    Ykeskkoht = tabelirida * 100 + 50

    pygame.draw.circle (tabel, (0,0,0), (Xkeskkoht, Ykeskkoht), 44, 2)

    joonestik[tabelirida][tabeliveerg] = Tähis #märgime lahtri kasutatuks

def klikk_inimene (tabel): #teeme kindlaks kuhu klikiti
    global joonestik, XO

    (Xkoordinaat, Ykoordinaat) = pygame.mouse.get_pos()

    (rida, veerg) = hiire_positsioon_tabelis (Xkoordinaat, Ykoordinaat)

    if joonestik[rida][veerg] == 'X' or joonestik[rida][veerg] == 'O': #kontrollime kas lahter on kasutusel
        return #lahter on juba kasutusel

    joonistamine_inimene (tabel, rida, veerg, XO) #joonista X
    
    XO = 'O' #käigu üleandmine arvutile


def klikk_arvuti(tabel):
    global joonestik, XO

    for rida in range(3):
        for veerg in range(3):
            if joonestik[0][0] != 'X' and joonestik[0][0] != 'O': #kontrollime kas lahter on kasutusel
                joonistamine_arvuti (tabel, rida, veerg, XO) #joonista O
            elif joonestik[0][1] != 'X' and joonestik[0][1] != 'O':
                joonistamine_arvuti (tabel, rida, veerg, XO)
            elif joonestik[0][2] != 'X' and joonestik[0][2] != 'O':
                joonistamine_arvuti (tabel, rida, veerg, XO)
            elif joonestik[1][0] != 'X' and joonestik[1][0] != 'O':
                joonistamine_arvuti (tabel, rida, veerg, XO)
            elif joonestik[1][1] != 'X' and joonestik[1][1] != 'O':
                joonistamine_arvuti (tabel, rida, veerg, XO)
            elif joonestik[1][2] != 'X' and joonestik[1][2] != 'O':
                joonistamine_arvuti (tabel, rida, veerg, XO)
            elif joonestik[2][0] != 'X' and joonestik[2][0] != 'O':
                joonistamine_arvuti (tabel, rida, veerg, XO)
            elif joonestik[2][1] != 'X' and joonestik[2][1] != 'O':
                joonistamine_arvuti (tabel, rida, veerg, XO)
            elif joonestik[2][2] != 'X' and joonestik[2][2] != 'O':
                joonistamine_arvuti (tabel, rida, veerg, XO)

    XO = 'X' # käigu üleandmine inimesele

def kaks(): #rakendatakse siis, kui mängija valib 2 mängijaga variandi
    ttt = pygame.display.set_mode((300,325)) #loome mänguakna

    tabel = loo_tabel(ttt)
    mäng_jookseb = 1
    while mäng_jookseb == 1: #mängutsükkel
        for event in pygame.event.get():
            if event.type is QUIT:
                mäng_jookseb  = 0
            elif event.type is MOUSEBUTTONDOWN:
                klikk_tabelis(tabel)

            näita_tabelit(ttt,tabel) #uuendab mängulauda peale igat käiku
            mängu_võitja(tabel) #kontrollib võitjat peale igat käiku
            if võitja is not None:
                break


def arvuti_vastu(): #rakendatakse siis, kui mängija valib 1 mängijaga variandi
    ttt = pygame.display.set_mode((300,325)) #loome mänguakna

    tabel = loo_tabel(ttt)
    mäng_jookseb = 1
    while mäng_jookseb == 1:
        for event in pygame.event.get():
            if event.type is QUIT:
                mäng_jookseb  = 0
            elif event.type is MOUSEBUTTONDOWN:
                klikk_inimene(tabel)
                klikk_arvuti(tabel)

            näita_tabelit(ttt,tabel) #uuendab mängulauda peale igat käiku
            mängu_võitja(tabel) #kontrollib võitjat peale igat käiku
            if võitja is not None:
                break
            

class alusta_mängu:
    def __init__(s):
        s.tsükkel()
    
    def ekraan(s): #loome ekraani
        s.screen = pygame.display.set_mode((300,325))
        pygame.display.set_caption("Trips-Traps-Trull")

    def näita_nuppe(s): #näitame nuppe ekraanil
        s.screen.fill((255,255,255))
        s.Nupp1.create_button(s.screen, (107,142,35), 75, 75, 150, 75, 0, "1 Mängija", (255,255,255))
        s.Nupp2.create_button(s.screen, (107,142,35), 75, 160, 150, 75, 0, "2 Mängijat", (255,255,255))
        pygame.display.flip()

    def tsükkel(s): #programmi ja menüü jooksutamise tsükkel
        s.Nupp1 = Button()
        s.Nupp2 = Button()
        s.ekraan()
        while True:
            s.näita_nuppe()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == MOUSEBUTTONDOWN:
                    if s.Nupp1.pressed(pygame.mouse.get_pos()):
                        arvuti_vastu()
                    if s.Nupp2.pressed(pygame.mouse.get_pos()):
                        kaks()






alusta_mängu()
