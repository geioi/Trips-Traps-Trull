import pygame

from pygame.locals import *

pygame.init()
ttt = pygame.display.set_mode((300,325)) #loome mänguakna
pygame.display.set_caption = ("Trips-Traps-Trull")

võitja = None



def init_tabel(ttt):
    taust = pygame.Surface(ttt.get_size())
    taust = taust.convert()
    taust.fill((250,250,250))
    
    #tõmbame jooned
    
    pygame.draw.line (taust, (0,0,0), (100,0), (100,300), 2) #vertikaalsed jooned
    pygame.draw.line (taust, (0,0,0), (200,0), (200,300), 2)

    pygame.draw.line (taust, (0,0,0), (0,100), (300,100), 2) #horisontaalsed jooned
    pygame.draw.line (taust, (0,0,0), (0,200), (300,200), 2)
    return taust


def näita_tabelit (ttt, tabel):
    hetkeseis(tabel)
    ttt.blit (tabel, (0,0))
    pygame.display.flip()

def hiire_positsioon_tabelis (Xkoordinaat, Ykoordinaat):
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

def klikk_tabelis (tabel): #teeme kindlaks kuhu klikiti
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


def joonistamine (tabel, tabelirida, tabeliveerg, Tähis):
    Xkeskkoht = tabeliveerg * 100 + 50
                                    #leiame keskkoha
    Ykeskkoht = tabelirida * 100 + 50

    if (Tähis == 'O'): #joonistame O
        pygame.draw.circle (tabel, (0,0,0), (Xkeskkoht, Ykeskkoht), 44, 2)

    else:
        pygame.draw.line (tabel, (0,0,0), (Xkeskkoht - 22, Ykeskkoht - 22), (Xkeskkoht + 22, Ykeskkoht + 22), 2)
                                                                                                            #joonistame X
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


def hetkeseis (tabel): #kuva hetkeseis(kelle käik/kes võitis)
    global XO, võitja
    if võitja is None:
        sõnum = XO + " käib"
    else:
        sõnum = võitja + " võitis!"
    font = pygame.font.Font(None, 24)
    tekst = font.render(sõnum, 1, (0,0,0))
#kopeerime sõnumi mänguaknas
    tabel.fill ((250, 250, 250), (0, 300, 300, 25))
    tabel.blit (tekst, (10, 300))


XO = 'X' #X alustab

joonestik =  [ [ None, None, None ], #tühjad lahtrid

          [ None, None, None ],

          [ None, None, None ] ]

tabel = init_tabel(ttt)
jooksutab = 1
while jooksutab == 1:
    for event in pygame.event.get():
        if event.type is QUIT:
            jooksutab  = 0
        elif event.type is MOUSEBUTTONDOWN:
            klikk_tabelis(tabel)

        mängu_võitja(tabel) #kontrollib võitjat peale igat käiku

        näita_tabelit(ttt,tabel) #uuendab mängulauda
        if võitja is not None:
            break
