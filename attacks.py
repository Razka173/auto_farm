import func as f
import time as t
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

p = os.getenv("BOT_PORT", '5555') # port

def Position(n):
    if n == 1:
        f.tap(261.2, 341.3, p)
    if n == 2:
        f.tap(529.4, 173, p)
    if n == 3:
        f.tap(676.9, 70.8, p)
    if n == 4:
        f.tap(992, 87, p)
    if n == 5:
        f.tap(1195, 224.5, p)
    if n == 6:
        f.tap(1406.9, 424.7, p)
    if n == 7:
        f.tap(311.1, 572.5, p)
    if n == 8:
        f.tap(468.1, 680.7, p)
    if n == 9:
        f.tap(1266.1, 635.7, p)
    if n == 10:
        f.tap(1144.5, 698.9, p)
    if n == 'c1':
        f.tap(715, 420, p)
    if n == 'c2':
        f.tap(800, 400, p)
    if n == 'c3':
        f.tap(870, 420, p)

def Slot(n):  # tap on slot n
    xccord = 175-130
    for x in range(0,n):
        xccord += 130
    f.tap(xccord, 800, p) # y is fixed at 800

# attack types
def TapTap(params = {}):
    troop_slots = params.get("troop_slots", 0)
    workshop_slots = params.get("workshop_slots", 1)
    hero_slots = params.get("heroes_slots", 0)

    spell_slot_position = troop_slots + workshop_slots + hero_slots + 1
    hero_slot_1_position = troop_slots + workshop_slots + 1
    hero_slot_2_position = troop_slots + workshop_slots + 2
    hero_slot_3_position = troop_slots + workshop_slots + 3
    hero_slot_4_position = troop_slots + workshop_slots + 4

    if workshop_slots >= 1:
        # workshop
        Slot(2) 
        Position(10)
        t.sleep(1)

    if hero_slots >= 1:
        # heroes 1
        Slot(hero_slot_1_position) 
        Position(10)
        t.sleep(1)
    
    if hero_slots >= 2:
        # heroes 2
        Slot(hero_slot_2_position) 
        Position(10)
        t.sleep(1)
    
    if hero_slots >= 3:
        # heroes 3
        Slot(hero_slot_3_position) 
        Position(10)
        t.sleep(1)
    
    if hero_slots >= 4:
        # heroes 4
        Slot(hero_slot_4_position) 
        Position(10)
        t.sleep(1)

    # spell
    Slot(spell_slot_position) 
    for p in ['c1','c2','c3']:
        for x in range(4):
            Position(p)
            t.sleep(0.75)
    t.sleep(1)

    # troops
    Slot(1)
    for i in range (4):
        # 3 tap per position
        for pos in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
            for i in range(3):
                Position(pos)
                t.sleep(0.1)
        t.sleep(2)

def Sdrag():
    f.swipe(p)
    Slot(1)
    for x in range(1,5): #Super drag
        Position(x)
        Position(x)
        
  
    Slot(2) #clanC
    Position("c")
    
    for x in range(0,4): #heros
        Slot(x+3) 
        Position("c")
        
    Slot(3) #Royal champ ability
    Slot(4) #Archer queen ability
    
    Slot(7)
    for x in range(0,11): # batspell
        Position("c")

    Slot(5) #warden ability
    Slot(6) #king

def MEKKA():
    f.swipe(p)
    Slot(1)
    for x in range(1,5): #MEKKA
        for y in range(0,8):
            Position(x)
        
  
    Slot(2) #clanC
    Position("c")
    
    for x in range(0,4): #heros
        Slot(x+3) 
        Position("c")
        
    Slot(3) #Royal champ ability
    Slot(4) #Archer queen ability
    
    Slot(7)
    for x in range(0,11): # batspell
        Position("c")

    Slot(5) #warden ability
    Slot(6) #king

def BB():
    f.swipe2(p)
    Slot(1)
    f.tap(1535,585,p)
    t.sleep(0.5)

    Slot(2)
    for x in range(6):
        f.tap(1535,585,p)
    for x in range(2,8):
        Slot(x)
    
def BB2():
    f.swipe2(p)
    Slot(1)
    f.tap(1535,585,p)
    Slot(9)
    for x in range(8):
        f.tap(1535,585,p)
    for x in range(2,10):
        Slot(x)
    