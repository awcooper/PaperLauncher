###########################################
##Adam Cooper                            ## 
##Section H                              ##
##15-112                                 ##
##Paper Launch!!!!                       ## 
##A 15-112 term project by Adam Cooper   ##
###########################################
import pygame, os, pickle, random, math, time
pygame.init()
pygame.font.init()

global data
class Struct: pass
data = Struct()

black  = (   0,   0,   0)
data.white  = ( 255, 255, 255)
data.green  = (   0, 255,   0)
data.red    = ( 255,   0,   0)
data.yellow = ( 225, 225,   0)

def empty():
    # The uses the Pickle Module to save all of the values that the user needs
    # to remember into a dictionary. The Program can then call upon these values
    # again when the File starts up. If There is not save file the program will
    # attempt to create one. If it fails it will just give an error message
    # this is also where the empty Save File is created.
    data.emptySaveFile = {
               'agility' : 0,
               'fortitude' : 0,
               'iterance' : 0,
               'serendipity' : 0,
               'resistance' : 0,
               'bank' : 500 ,
               'maxHeight' : 0,
               'playTime' : 0,
               'unlockedBoots': 1,
               'unlockedCannons': 1,
               'currentCannon' : 'slingshot',
               'sketchbook' : ['self'],
                'unlockedBoots' : 1,
                'currentBoot' : 'oldBoots',
                'autoSave' : True 
                }

def loadGame():
    try:
        data.save = pickle.load(open('PaperLaunchFiles/PLSaveFile.pkl','rb'))
        data.firstTime = False
    except:
        saveFile = data.emptySaveFile 
        data.firstTime = 'saveMessage'
        try:
            pickle.dump(saveFile ,open('PaperLaunchFiles/PLSaveFile.pkl','wb'))
            data.save =  pickle.load(open('PaperLaunchFiles/PLSaveFile.pkl','rb'))
            data.createdSaveFile = True
        except:
            data.createdSaveFile = False
            data.save = data.emptySaveFile 

empty()
loadGame()

##########################################################################
################### Init Functions #######################################
##########################################################################

def init(constant = False):
    data.ani = 0
    data.startedPlaying = time.time()
    initSound()
    initData()
    initStats()
    initItemInfo()
    data.onScreenIcons = [icon(data.sprites['saveIcon'],0),
                          icon(data.sprites['sketchBookIcon'],0),
                          icon(data.sprites['saveIcon'],0)]
    initExtras()

def initExtras():
    data.sketchbook = data.save['sketchbook']
    data.sketchbookSelect = 0
    data.sketchbookDisplay =['self']
    
def makeSketchbook():
    # This just goes though the sketchbook and collects all of the art work
    # and stores them in a tuple with the designated artist. This is sort of
    # like a credits page for everybody who helped me out and it leads for
    # an interesting challenge to the player 
    display = [(sprite,'Adam Cooper') for sprite in [data.sprites['selfair'],
            data.sprites['selfHurt'],
            data.sprites['oldBoot']] + data.selfFallingSprite] 
    if 'trogdor' in data.sketchbook:
        display += [(sprite,'Internet') for sprite in [data.sprites['trogdor'],
                                                       data.sprites['trogdorEvent']]]
    if 'nyanCat' in data.sketchbook:
        display += [(sprite,'Audrey Wu') for sprite in [data.sprites['nyanCat1'],
                                                        data.sprites['nyanCat'],
                                                        data.sprites['nyanCat3'],
                                                        data.sprites['nyanCat2']]]
    if 'airplane' in data.sketchbook:
        display += [(sprite,'Connie Dai') for sprite in [data.sprites['airplane'],
                                                         data.sprites['airplane1'],
                                                         data.sprites['boom']]]
    if 'shark' in data.sketchbook:
        display += [(data.sprites['shark'],'Dan Cushman')]
    if 'bear' in data.sketchbook:
        display += [(data.sprites['bear'], 'Faith Quist'),(data.sprites['bearSwipe'],
                                                           'Faith Quist')]
    if 'car' in data.sketchbook:
        display += [(data.sprites['car1'], 'Hira Ahmad'), (data.sprites['car12'],
                                                           'Hira Ahmad')]
    if 'carpeDiemMachine' in data.sketchbook:
        display += [(data.sprites['carpeDiemMachine'],'Adam Cooper'),
                                                       (data.sprites['carpeDiem'],
                                                        'Internet')]
    if 'money' in data.sketchbook:
        display += [(data.sprites['money'],'Hira Ahmad')]
    if 'tank' in data.sketchbook:
        display += [(data.sprites['tank'],'Internet')]
    if 'cannon' in data.sketchbook:
        display += [(data.sprites['bigcannon'],'Internet')]
    if 'sunMachine' in data.sketchbook:
        display += [(data.sprites['sunMachine'],'Internet')]
    if 'slingshot' in data.sketchbook:
        display += [(sprite, 'Adam Cooper') for sprite in [data.sprites['slingshot'],
                                                data.sprites['slingshotSwoosh']]]
    if data.unlockedBoots == 3:
        display += [(data.sprites['hermesBoot'],'Faith Quist')]
    if data.unlockedBoots != 1:
        display += [(data.sprites['moonBoot'],'Adam Cooper')]
    return display 
        
    
def initGame():
    if data.firstTime:
        data.instructions = True
    data.gameOver = False
    data.runCash = 0
    data.maxHeight = 0
    initPhysics()
    initObjects()


def initObjects():
    data.onScreen = [cannon()]
    data.launch = 'launchBar'

def initData():
    initImages()
    data.ariel = pygame.font.match_font('timesNewRoman')
    data.debugMode = False
    size = [data.canvasWidth, data.canvasHeight]
    data.screen = pygame.display.set_mode(size)
    background = pygame.Surface(data.screen.get_size())
    pygame.display.set_caption("Paper Launcher")
    data.radius = 30
    data.ground = 100
    data.keyDown = False
    data.currentScreen = 'mainMenu'
    data.gameOverButtonSelect = 0 
    data.buttonSelect = 3
    initStoreMenu()
    initOptionsMenu()
    data.instructions = False
    data.htpi = 0

def initOptionsMenu():
    data.optionsSelect = 'autoSave'
    data.areYouSure = False

    
def initStoreMenu():
    data.storeButtonSelect  = 0
    data.cannonButtonSelect = 0
    data.bootButtonSelect = 0 
    data.costs = [
        [300,600,2500,7500,15000], #agaility
        [300,600,2500,7500,17000], #fortitude
        [100,700,1200,5400,10000], #iterance
        [300,600,2500,7500,20000], #serendipity
        [300,800,5000,7500,17000], #resistance
        [0,7500,20000], #boots
        [0,1000,7500,15000,30000] # cannons
                 ]
    data.allCannons = ['slingshot','cannon','tank','sunMachine','carpeDiemMachine']

def initItemInfo():
    data.cannonPower = { 'slingshot' : 20, 'cannon' : 40, 'tank' : 80, 'sunMachine' : 140,   'carpeDiemMachine': 300  }
    data.fortitudePower = { 0:(1.7, -1.85), 1:(1.5, -1.7), 2:(1.4, -1.6),3:(1.3, -1.5), 4:( 1.15, -1.4), 5:(1.1, -1.2) }
    data.serendipityPower = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0 }
    data.speedCap = {0:0,1:0,2:0,3:0,4:0,5:0}
    data.bootForce = {'oldBoots':8, 'hermesBoots':15,'moonBoots':28}
    data.allBoots = ['oldBoots','hermesBoots','moonBoots']
    makeStoreButton()

def initImages():
    # this sets up some general image information that is useful during gameplay 
    data.htpImages = []
    data.sprites = dict()
    imageFinder('PaperLaunchFiles/Images')
    for htpnumber in xrange(1,9):
        data.htpImages += [data.sprites['htp' + str(htpnumber)]]
    data.selfFallingSprite = [data.sprites['selfFalling'],
                              data.sprites['selfFalling2'],
                              data.sprites['selfFalling3']]
    data.canvasHeight, data.canvasWidth = 600, 1000
    if 'userbg' in data.sprites and data.sprites['userbg'].get_size()[0] > 700:
        data.bg = data.sprites['userbg']
    else: data.bg = data.sprites['paperSlice']
    data.sprites['gameOverScreen'] = pygame.transform.scale(data.sprites['gameOverScreen'],
                                        (int(data.canvasWidth*.8),
                                         int(data.canvasHeight*.8)))
    data.bgWidth, data.bgHeight = data.bg.get_size()
    data.menubg = data.sprites['mainMenu']
    data.buttonList = [data.sprites['playButton'],
                       data.sprites['storeButton'],
                       data.sprites['extrasButton'],
                       data.sprites['optionsButton']]
    data.buttonWidth, data.buttonHeight = data.sprites['playButton'].get_size()
    data.menubg = pygame.transform.scale(data.menubg, (data.canvasWidth, data.canvasHeight))
    data.playerSprite = data.sprites['selfair']
    data.bootSprites = [data.sprites['oldBoot'],data.sprites['moonBoot'],data.sprites['hermesBoot']]
    data.selfSpriteWidth, data.selfSpriteHeight = data.playerSprite.get_size()
    data.changeAni = 'up'
    data.pad = .2
    data.cannonSprites = [data.sprites['slingshot'],
                          data.sprites['bigcannon'],
                          data.sprites['tank'],
                          data.sprites['sunMachine'],
                          data.sprites['carpeDiem'] ]

def imageFinder(path):
    # This recursive Function goes thought the Paper Launch Folder and then
    # compiles a dictinary of all of the image files in the folder and uses
    # the name of the file as a key. This is useful for organizatonal purpouses 
    for filename in os.listdir(path):
        if os.path.isdir(path + "/" + filename) == False:
            try: data.sprites[filename[0:len(filename)-4]] = pygame.image.load(path + "/" + filename)
            except: pass
        else:
            imageFinder(path + "/" + filename)


def initPhysics():
    data.bgx = 0
    data.bgy = 0
    data.radius = data.sprites['selfair'].get_size()[1]
    data.distance = 0
    data.launchBarLength= 0
    data.xFriction, data.yFriction = data.fortitudePower[data.fortitudeLevel]
    data.ground = 100
    data.selfHeight = 0
    data.theta = math.pi/32
    data.dTheta = math.pi/32
    data.yVelocity = 0
    data.xSpeed = 0
    data.maxBoost = 5 + data.iteranceLevel
    data.boostCount = data.maxBoost
    data.selfHitbox = pygame.Rect([100, data.canvasHeight - int(data.selfHeight + data.selfSpriteHeight*data.pad),
        int(data.selfSpriteWidth *( 1 - data.pad*2)),int(data.selfSpriteHeight *( 1 - data.pad*2))] )

    
def initStats():
    # Gets all of the data from the save file or 
    data.bank = data.save['bank']
    data.serendipityLevel = data.save['serendipity']
    data.resistanceLevel = data.save['resistance']
    data.iteranceLevel = data.save['iterance']
    data.fortitudeLevel = data.save['fortitude']
    data.agilityLevel = data.save['agility']
    data.unlockedCannons = data.save['unlockedCannons']
    data.stats = [data.agilityLevel, data.fortitudeLevel, data.iteranceLevel, data.serendipityLevel, data.resistanceLevel]
    data.currentCannon = data.save['currentCannon']
    data.unlockedBoots = data.save['unlockedBoots']
    data.currentBoot = data.save['currentBoot']
    data.autoSave = data.save['autoSave']
    
def initSound():
    #This Peice of Code has Been Removed Initially the game was Supposed to
    #Make these songs Available But I changed my mind last minute, In a futrue
    #Verstion of this game I might put this feature back in. 
    data.playMusic = True
    #data.songs = filePath(['beetovenVirus','levels', 'handguns', 'ghostsnstuff',
    #'iAmTheBest', 'passionForExploring', 'tetrisTheme', 'marioThemeSong',
    #'harderBetterFasterStronger', 'getLow'], '.wav'])
    data.songSelect = 0

def makeStoreButton():
    #stores the coords for the store button into a dictionary
    data.buttonData = dict()
    for button in range(0,5):
        data.buttonData[button] = [139, button*36 + 135, 125, 31 ]

##########################################################################
################### Timer Events #########################################
##########################################################################

def gamePlay():
    if not(data.instructions) and not(data.gameOver):
        if data.launch == 'launchBar':
            launchBar()
        elif data.launch == 'angle':
            if data.theta > 0 and data.theta < math.pi/2 :
                data.theta += data.dTheta
            else: #Meter bar flips directions when it reaches a bound.
                data.dTheta *= -1
                data.theta += data.dTheta
        movement()
        if data.selfHeight - data.ground + data.bgy > data.maxHeight:
            data.maxHeight = data.selfHeight - data.ground + data.bgy 
        if data.xSpeed > 0:
            monsterFactory()
 
def launchBar():
    if data.launchBarLength > 100:
        data.launchBarLength = 0
    else: data.launchBarLength += 5
 
def monsterFactory():
    select = random.random()
    if len(data.onScreen) < 13: 
        if select > .99:
            data.onScreen += [random.choice([car(),bear(),shark()])]
        if select > .5 and select < .5 + data.serendipityLevel*.005 + .01:
            data.onScreen += [random.choice([trogdor(),airplane(),nyanCat()])]
        if select < .05 + data.serendipityLevel*.03:
            data.onScreen += [money()]

def gameOver():
    if data.autoSave:
        save()
    data.bank += data.distance/100
    data.endTime = time.time()
    

##########################################################################
################### Laws of Physics ######################################
##########################################################################

def movement():
    ###### Speed Cap #######
    if data.yVelocity > 180:
        data.yVelocity = 180
    if data.xSpeed > 50*(data.agilityLevel + 1):
        data.xSpeed = 50*(data.agilityLevel + 1)
    
    ########################    
    if data.xSpeed == 0 and data.launch == False and data.gameOver == False:
        data.gameOver = True
        gameOver()
    data.bgx += data.xSpeed/3
    data.distance += data.xSpeed
    gravity()
    for item in data.onScreen:
        item.moveObject()
    # this mess of a conditional adjusts the Camera to follow the Ball
    moveCamera()
    if data.selfHeight < 0: 
        bounce()

def moveCamera():
    # this is one of the most confusing lines in the code. While it may seem Simple
    # This was actually very hard to Write. So basically if the person is above
    # about 80 percent of the canvas Height the YVelocity is absorbed by the
    # background insead of the character. Othewse it is added to the height
    # of the actual character. The same logic is meshed with this function
    # for the moving down animation
    if data.selfHeight < data.canvasHeight/2 or \
        (data.yVelocity < 0  and data.bgy == 0) or \
        ( data.yVelocity > 0 and  data.bgy == data.bgHeight - data.canvasHeight) or\
        (data.selfHeight + data.ground > data.canvasHeight*.8): 
            data.selfHeight += data.yVelocity 
    else:
        data.bgy += data.yVelocity

def bounce():
    data.selfHeight = 0
    data.bgy = 0
    if data.xSpeed > 0:
        data.yVelocity = int(data.yVelocity/data.yFriction)
    if data.xSpeed == 0: 
        data.yVelocity = 0
    data.xSpeed = int(data.xSpeed/data.xFriction)


def gravity():
    data.yVelocity -= 1

##########################################################################
################### Object and Class Definitions #########################
##########################################################################


class physicalObject(object):
    # every interactable object in the game has this class. The general Object
    # in this game has basically the same formua that goes along with it.
    # the moveObject functon is the only funciton that is called by literraly every
    # interactable object in the game. Basically the objects move along with the
    # background this fuction also checks for collison with self.hitbox
    # and changes the hitbox as the object Moves
    def moveObject(self):
        if self.location[0] < -data.canvasWidth/2 or self.location[0] > data.canvasWidth*1.5:
            data.onScreen.remove(self)
        self.location[0] -= data.xSpeed/3 + self.resistance
        if not(data.selfHeight < data.canvasHeight/2 or (data.yVelocity < 0\
                                                         and data.bgy == 0)\
               or ( data.yVelocity > 0 and  data.bgy == data.bgHeight - data.canvasHeight)\
               or (data.selfHeight + data.ground > data.canvasHeight*.8)):
            self.location[1] += data.yVelocity
        if self.hitbox.colliderect(data.selfHitbox):
            self.event()
    def draw(self):
    # 33.33% of objects in the game actually use this function. This function is
    # really for objects that are not animated. The fucntion uses the same method
    # in order to draw the hitboxes as all of the classes will do
        pad = .2
        self.hitbox = pygame.Rect(int(self.location[0] + self.width*pad),int(self.location[1] + self.height*pad), int(self.width *( 1 - pad*2)),int(self.height *( 1 - pad*2))) 
        data.screen.blit(self.image,self.location)
        if data.debugMode == True:
            pygame.draw.rect(data.screen,data.red, self.hitbox ,4 )
    def event(self):
        # all objects have different event functions. This is just
        # the default if I havent programed one in yet
        # all objects have this as its adds its name into the sketchbook
        # if its name isn't already there
        if not (str(type(self).__name__) in data.sketchbook):
            data.sketchbook += [str(type(self).__name__)]
            data.onScreenIcons[1].killTime = 40
    def __str__(self):
        # This serves a purpuse for Debug Mode
        return str(type(self).__name__)

class cannon(physicalObject):
    def __init__(self):
        if data.currentCannon == 'slingshot': self.image = data.sprites['slingshot']
        if data.currentCannon == 'cannon': self.image = data.sprites['bigcannon']
        if data.currentCannon == 'tank': self.image = data.sprites['tank']
        if data.currentCannon == 'carpeDiemMachine': self.image = data.sprites['carpeDiem']
        if data.currentCannon == 'sunMachine': self.image =  data.sprites['sunMachine']
        self.width, self.height = self.image.get_size()
        self.location = [ 100, data.canvasHeight - data.ground - self.height + data.bgy - 2,]
        self.resistance = 0
    def event(self):
        if data.currentCannon == 'slingshot':
            self.image = data.sprites['slingshotSwoosh']
        if not (data.currentCannon in data.sketchbook):
            data.sketchbook += [data.currentCannon]
            data.onScreenIcons[1].killTime = 40


#data.canvasHeight - data.ground - self.height + data.bgy - 2 this is the ground 
#random.randint( data.canvasHeight - data.bgHeight + self.height + data.bgy,
#  data.canvasHeight - data.ground - self.height + data.bgy - 2) 
 
class bear(physicalObject): 
    def __init__(self):
        self.resistance = 0
        self.image = data.sprites['bear']
        self.encounter = False
        self.width, self.height = self.image.get_size()
        self.location = [ (data.canvasWidth + self.width ), data.canvasHeight - data.ground - self.height + data.bgy - 2,]
    def event(self):
        if self.encounter == False:
            self.encounter = True
            self.image = data.sprites['bearSwipe']
            data.xSpeed = int(data.xSpeed*(.78 + data.resistanceLevel*.03))
            data.yVelocity = -int((abs(data.yVelocity)) - 15)
            # hits you into the ground and slows you down
        if not (str(type(self).__name__) in data.sketchbook):
            data.sketchbook += [str(type(self).__name__)]
            data.onScreenIcons[1].killTime = 40
        

class shark(physicalObject):
    def __init__(self):
        self.resistance = 10
        self.animationCounter = 0 
        self.encounter = False
        self.image = data.sprites['shark']
        self.width, self.height = self.image.get_size()
        self.location = [ (data.canvasWidth + self.width ), random.randint(
            data.canvasHeight - data.bgHeight + self.height + data.bgy,
            data.canvasHeight - data.bgHeight/2 + self.height + data.bgy ) ]
    def event(self):
        if self.encounter == False:
            self.encounter = True
            data.xSpeed = int(data.xSpeed*(.4 + data.resistanceLevel*.1))
            data.yVelocity = -int((abs(data.yVelocity))) - 12
            # hits you down fast and slows you down 
        if not (str(type(self).__name__) in data.sketchbook):
            data.sketchbook += [str(type(self).__name__)]
            data.onScreenIcons[1].killTime = 40

class car(physicalObject):
    def __init__(self):
        self.resistance = 20
        self.animationCounter = 0 
        self.encounter = False
        self.image = data.sprites['car1']
        self.width, self.height = self.image.get_size()
        self.location = [ (data.canvasWidth + self.width ),
            data.canvasHeight - data.ground - self.height + data.bgy - 2,]
    def draw(self):
        pad = .2
        # This is the first exaple of an animation counter It keeps track of
        # its own animation counter and uses it to animate iteself by moding
        # itself with different numbers 
        self.animationCounter = (self.animationCounter + 1)%10
        self.hitbox = pygame.Rect(int(self.location[0] + self.width*pad),
                                  int(self.location[1] + self.height*pad),
                                  int(self.width *( 1 - pad*2)),
                                  int(self.height *( 1 - pad*2))) 
        if self.animationCounter%9 < 5:
            self.image = data.sprites['car1']
        else: self.image = data.sprites['car12']
        data.screen.blit(self.image,self.location)
        if data.debugMode == True:
            pygame.draw.rect(data.screen,data.red,self.hitbox,4)
    def event(self):
        if self.encounter == False:
            data.xSpeed = int(data.xSpeed/(2 - data.resistanceLevel*.15))
            data.yVelocity = (10 + abs(data.yVelocity))
            self.encounter = True
            # hits you up but slows you down 
        if not (str(type(self).__name__) in data.sketchbook):
            data.sketchbook += [str(type(self).__name__)]
            data.onScreenIcons[1].killTime = 40


class nyanCat(physicalObject):
    def __init__(self):
        self.animationCounter = 0
        self.encounter = False 
        self.resistance = -20
        self.image = data.sprites['nyanCat']
        self.width, self.height = self.image.get_size()
        self.location = [ (data.canvasWidth + self.width ),
            random.randint( data.canvasHeight - data.bgHeight + self.height + data.bgy,
                           data.canvasHeight - data.bgHeight/2 + self.height + data.bgy ) ]
    def draw(self):
        pad = .2
        # for more explanations look at car
        self.animationCounter = (self.animationCounter + 1 )% 12
        self.hitbox = pygame.Rect(int(self.location[0] + self.width*pad),
                                  int(self.location[1] + self.height*pad),
                                  int(self.width *( 1 - pad*2)),
                                  int(self.height *( 1 - pad*2))) 
        if (self.animationCounter/3) % 4 == 0:
            self.image = data.sprites['nyanCat']
        if (self.animationCounter/3) % 4 == 1:
            self.image = data.sprites['nyanCat1']
        if (self.animationCounter/3) % 4 == 2:
            self.image = data.sprites['nyanCat2']           
        else: self.image = data.sprites['nyanCat3']
        data.screen.blit(self.image,self.location)
        if data.debugMode == True:
             pygame.draw.rect(data.screen,data.red,self.hitbox,4)
    def event(self):
        if data.boostCount < data.maxBoost and self.encounter == False:
            data.boostCount += 1
            self.encounter = True
        if not (str(type(self).__name__) in data.sketchbook):
            data.sketchbook += [str(type(self).__name__)]
            data.onScreenIcons[1].killTime = 40


class money(physicalObject):
    def __init__(self):
        self.resistance = 0
        self.image = data.sprites['money']
        self.width, self.height = self.image.get_size()
        self.location = [ (data.canvasWidth + self.width ),
            random.randint( data.canvasHeight - data.bgHeight + self.height + data.bgy,
                           data.canvasHeight - data.ground - self.height + data.bgy - 2) ]
    def event(self):
        data.onScreen.remove(self)
        value = 100
        data.runCash += value
        data.bank += value
        if not (str(type(self).__name__) in data.sketchbook):
            data.sketchbook += [str(type(self).__name__)]
            data.onScreenIcons[1].killTime = 40

class airplane(physicalObject):
    def __init__(self):
        self.animationCounter = True
        self.encounter = False
        self.resistance = -23
        self.image = data.sprites['airplane']
        self.width, self.height = self.image.get_size()
        self.location = [ (data.canvasWidth + self.width ),
            random.randint( data.canvasHeight - data.bgHeight + self.height + data.bgy,
                           data.canvasHeight - data.bgHeight/2 + self.height + data.bgy ) ]
    def draw(self):
        # look at car for more Explanation 
        pad = .2
        self.animationCounter = not(self.animationCounter)
        self.hitbox = pygame.Rect(int(self.location[0] + self.width*pad),
                                  int(self.location[1] + self.height*pad),
                                  int(self.width *( 1 - pad*2)),int(self.height *( 1 - pad*2))) 
        data.screen.blit(self.image,self.location)
        if self.encounter == False:
            if self.animationCounter == True:
                self.image = data.sprites['airplane1']
            else: self.image = data.sprites['airplane']
    def event(self):
        if self.encounter == False:
            self.image = data.sprites['boom']
            self.width, self.height = self.image.get_size()
            self.encounter = True
            self.resistance = 0
            data.yVelocity = abs(data.yVelocity) + 20
            data.xSpeed += 70
            #Hits you up and makes you go faster 
        if not (str(type(self).__name__) in data.sketchbook):
            data.sketchbook += [str(type(self).__name__)]
            data.onScreenIcons[1].killTime = 40

class trogdor(physicalObject):
    def __init__(self):
        self.encounter = False
        self.resistance = 0
        self.image = data.sprites['trogdor']
        self.width, self.height = self.image.get_size()
        self.location = [ (data.canvasWidth + self.width ),
            data.canvasHeight - data.ground - self.height + data.bgy - 2,]
    def event(self):
        if self.encounter == False:
            self.image = data.sprites['trogdorEvent']
            self.width, self.height = self.image.get_size()
            self.encounter = True 
            data.yVelocity = abs(data.yVelocity) + 17
            data.xSpeed += 50
            # same deal as the plane but less
        if not (str(type(self).__name__) in data.sketchbook):
            data.sketchbook += [str(type(self).__name__)]
            data.onScreenIcons[1].killTime = 40
  
class icon(object):
    # This is just convient for displaying icons to have each icon have its
    # own Killtime 
    def __init__(self,image,killTime =-1,location=-1):
        self.image = image
        self.width, self.height = self.image.get_size()
        self.killTime = killTime
        if location == -1:
            self.location = [data.canvasWidth - self.width,0]
        else: self.location = location
    def animate(self):
        if self.killTime == -1: pass
        elif self.killTime == 0: pass
        else: self.killTime -= 1
    def draw(self):
            if self.killTime != 0:
                data.screen.blit(self.image,self.location)

##########################################################################
################### Drawing Function #####################################
##########################################################################

def redrawAll():
    #Self Documenting 
    if data.currentScreen == 'mainMenu': drawMainMenu()
    elif data.currentScreen == 'store': drawStore()
    elif data.currentScreen == 'options': drawOptions()
    elif data.currentScreen == 'game':
        scrollBackground()
        if data.launch == False: drawSelf()
        for item in data.onScreen: item.draw()
        drawInfo()
        drawBoosts()
        lol()
        if data.launch != False:
            drawLaunchBar()
            if data.launch == 'angle': drawAngle()
        if data.gameOver == True: drawGameOver()
        if data.debugMode == True: drawDebugMode()
    elif data.currentScreen == 'extras': drawSketchBook()
    for icon in data.onScreenIcons: icon.draw()
    if data.instructions: drawInstructions()
    if data.firstTime == 'saveMessage': drawSaveMessage()

def drawOptions():
    data.screen.blit(data.sprites['tealPaperBg'],(0,0))
    font = pygame.font.Font(data.ariel, 30)
    if data.autoSave == True:
        ext = 'ON'
    else: ext = 'OFF'
    erase = font.render('Delete File', 1, (10, 12, 10))
    autoSaveInfo = font.render('AutoSave: ' + ext , 1, (10, 12, 10))
    saveGame = font.render('Save Game' , 1, (10, 12, 10))
    width,height = autoSaveInfo.get_size()
    data.screen.blit(autoSaveInfo,(100,150))
    data.screen.blit(saveGame,(100,150 + height) )
    data.screen.blit(erase,(100,150 + height*2) )
    if data.optionsSelect == 'autoSave':
        start = 0
    elif data.optionsSelect == 'save':
        start = 1
    else: start = 2
    pygame.draw.rect(data.screen,[225,0,0],[100,150 + height*start ,width,height], 2)
    if data.areYouSure == True:
        data.screen.blit(data.sprites['htpBg'],(0,0))
        data.screen.blit(data.sprites['areYouSure'],(300,220))
    

def drawSaveMessage():
    data.screen.blit(data.sprites['htpBg'],(0,0))
    if data.createdSaveFile == True:
        data.screen.blit(data.sprites['saveFileYes'],(300,220))
    if data.createdSaveFile == False:
        data.screen.blit(data.sprites['saveFileNo'],(300,220))

def drawSketchBook():
    #in the works 
    data.screen.blit(data.sprites['sketchbookBg'],(0,0))
    data.sketchbookDisplay = makeSketchbook() 
    width, height = data.sketchbookDisplay[data.sketchbookSelect][0].get_size()
    data.screen.blit(data.sketchbookDisplay[data.sketchbookSelect][0],
                     (data.canvasWidth/2 - width/2, data.canvasHeight/2 - height/2))
    font = pygame.font.Font(data.ariel, 40)
    name = font.render( data.sketchbookDisplay[data.sketchbookSelect][1] , 1, (10, 12, 10))
    width, height = name.get_size()
    data.screen.blit(name,[data.canvasWidth/2 - width/2,
                           data.canvasHeight - 50 - height/2])
    
def drawInstructions():
    data.screen.blit(data.sprites['htpBg'],(0,0))
    data.screen.blit(data.htpImages[data.htpi],(50,50))

def lol():
    if len(data.onScreen) and data.launch == False and str(data.onScreen[0]) == 'cannon' \
            and data.currentCannon == 'carpeDiemMachine' and data.xSpeed > 70:
            data.screen.blit(data.sprites['kosbie'],(0,0))

def drawAngle():
    bottom = data.canvasHeight - data.ground - 10 
    pygame.draw.line( data.screen, data.red, (110, bottom),
                     ( int(110 + 100*math.cos(data.theta)),
                      int( bottom +(100)*math.sin( -data.theta))),5)

def drawLaunchBar():
    if data.launchBarLength > 95:
        color = data.yellow
    else: color = data.red
    pygame.draw.rect(data.screen,[0,0,0],[75,
        data.canvasHeight -data.ground - 100,20,100])
    pygame.draw.rect(data.screen,color,[75,
        data.canvasHeight - data.ground - data.launchBarLength, 20, data.launchBarLength])

def drawDebugMode():
    font = pygame.font.Font(data.ariel, 20)
    onScreenList = [str(item) for item in data.onScreen]
    yVelocity = font.render('yVelcoity = ' + str(data.yVelocity), 1, (10, 12, 10))
    xSpeed = font.render('xSpeed = ' + str(data.xSpeed), 1, (10, 12, 10))
    onScreen = font.render(str(onScreenList), 1, (10, 12, 10))
    data.screen.blit(onScreen,(0,0))
    data.screen.blit(xSpeed,(0,20))
    data.screen.blit(yVelocity,(0,40))

def drawGameOver():
    data.screen.blit(data.sprites['gameOverScreen'],
                     [data.canvasWidth*.1, data.canvasHeight*.1])
    font = pygame.font.Font(data.ariel, 20)
    bank = text = font.render(str(data.bank), 1, (10, 12, 10))
    runCash = font.render(str(data.runCash), 1, (10, 12, 10))
    distance = font.render(str(data.distance/100), 1, (10, 12, 10))
    runTime = data.endTime - data.startTime 
    runTime = ('%.1fs') % (runTime)
    runTime = font.render(runTime, 1, (10, 12, 10))
    maxHeight = font.render(str(data.maxHeight) + 'cm',1, (10, 12, 10)) 
    data.screen.blit(maxHeight,[403,202])
    data.screen.blit(runTime,[368,230])
    data.screen.blit(distance,[466,174])
    data.screen.blit(runCash,[397,284])
    data.screen.blit(bank,[392,313])
    pygame.draw.rect( data.screen,
        [0xff,0,0],[572, 175 + data.gameOverButtonSelect*152, 212, 136],4)


def drawMainMenu():
    middle = data.canvasWidth/2 - data.buttonWidth/2
    data.screen.blit(data.menubg,(0,0))
    buffer = 60
    down = 120
    scale = 1.4
    for button in range(0,3):
        image = data.buttonList[(button + data.buttonSelect)%4]
        if button == 1:
            image = pygame.transform.scale(image, (int(data.buttonWidth*scale),
                    int(data.buttonHeight*scale) +down))
            position = (data.canvasWidth/2 - int(data.buttonWidth*scale)/2 ,
                    data.canvasHeight/2 - int(data.buttonHeight*scale) +down)
        else: position = (middle - data.buttonWidth - buffer,
                    data.canvasHeight/2 - data.buttonHeight + down)
        data.screen.blit(image,position)
        middle += data.buttonWidth + buffer

def drawInfo():
    font = pygame.font.Font(data.ariel, 20)
    pygame.draw.rect( data.screen,[0xff,0xff,0xff],
                [4, data.canvasHeight - 34, data.canvasWidth - 6, 30])
    data.screen.blit(data.sprites['musicNote'],
                [data.canvasWidth - 34, data.canvasHeight - 34] )
    if data.selfHeight + data.ground > data.canvasHeight:
        pygame.draw.rect( data.screen,[0xff,0,0],[ 70, 4, 100, 35])
        pygame.draw.rect( data.screen,[0,0,0],[ 70, 4, 100, 35], 2)
        height = font.render(str(data.selfHeight) + 'm',  1, (10, 12, 10))
        data.screen.blit(height, [72,6])
    text = font.render("Distance: " + str(data.distance/100) + 'm', 1, (10, 12, 10))
    textpos = text.get_rect(centerx=data.canvasWidth/2, centery=data.canvasHeight - 20)
    data.screen.blit(text, [data.canvasWidth/2 - 80, data.canvasHeight - 30 ] )
    pygame.draw.rect( data.screen,[0,0,0],[4, data.canvasHeight - 36, data.canvasWidth-6, 30],2)

def drawStore():
    data.screen.blit(data.sprites['store'], (0,0))
    drawPurchaseInfo()
    drawBuyButton()
    drawCannonStore()
    drawBootStore()
    drawLevelBars()

def drawBootStore():
    iconHeight = 80
    iconWidth = 100
    start = 323
    pos = 0
    tall = 170  + iconHeight + 15
    for boot in xrange(len(data.bootSprites)):
        bootIcon = pygame.transform.scale(data.bootSprites[boot],(iconWidth,iconHeight))
        if data.unlockedBoots <= boot:
            bootIcon = bootIcon.convert()
            bootIcon.set_alpha(100)
        data.screen.blit(bootIcon, [start + pos, data.canvasHeight - tall, ] )
        pos += 150
    if data.storeButtonSelect == 5:
        pygame.draw.rect( data.screen,[255,0,0],[start + 150*data.bootButtonSelect,
            data.canvasHeight - tall,iconWidth,iconHeight] ,6)
    if data.unlockedBoots == 1:
        pygame.draw.rect( data.screen,
            [0,0,0],[start + 150*2, data.canvasHeight - tall,iconWidth,iconHeight])
    pygame.draw.rect( data.screen,[0,0,0],
            [start + 150*data.allBoots.index(data.currentBoot),
            data.canvasHeight - tall,iconWidth,iconHeight] ,4)

    
def drawCannonStore():
    pos = 0
    iconHeight = 80
    iconWidth = 100
    data.allCannons
    for cannon in xrange(len(data.cannonSprites)):
        cannonIcon = pygame.transform.scale(data.cannonSprites[cannon],(iconWidth,iconHeight))
        if data.unlockedCannons <= cannon:
            cannonIcon = cannonIcon.convert()
            cannonIcon.set_alpha(100)
        data.screen.blit(cannonIcon, [230 + pos, data.canvasHeight - 170, ] )
        pos += 150
    if data.storeButtonSelect == 6:
        pygame.draw.rect( data.screen,[255,0,0],[230 + 150*data.cannonButtonSelect,
            data.canvasHeight - 170,iconWidth,iconHeight] ,6)
    pygame.draw.rect( data.screen,[0,0,0],[230 + 150*data.allCannons.index(data.currentCannon),
            data.canvasHeight - 170,iconWidth,iconHeight] ,4)
    pos = 150*2
    for shadeIn in range(data.unlockedCannons+1,5):
        pygame.draw.rect( data.screen,[0,0,0],[230 + 150*shadeIn,
            data.canvasHeight - 170,iconWidth,iconHeight])

        
def drawLevelBars():
    for bar in xrange(0,5):
        barWidth = data.stats[bar]
        barHeight = 40
        pygame.draw.rect( data.screen,[255,0,0],
            [284, 130 + barHeight*bar , 100*barWidth, barHeight - 2])

    
def drawBuyButton():
    font = pygame.font.Font(data.ariel, 20)
    if data.storeButtonSelect < 5 and data.stats[data.storeButtonSelect] < 5 and\
    data.costs[data.storeButtonSelect][data.stats[data.storeButtonSelect]] != 0:
        cost = 'Cost: $' + str(data.costs[data.storeButtonSelect][data.stats[data.storeButtonSelect]])
    elif data.storeButtonSelect == 6 and data.cannonButtonSelect == data.unlockedCannons:
        cost = 'Cost: $' +  str( data.costs[6][data.unlockedCannons])
    elif data.storeButtonSelect == 5 and data.bootButtonSelect == data.unlockedBoots:
        cost = 'Cost: $' +  str( data.costs[5][data.unlockedBoots])
    else: cost = ''
    cost = font.render(cost, 1, (10, 12, 10))
    data.screen.blit(cost, [150, data.canvasHeight - 30])

def drawPurchaseInfo():
    # This is the text that comes up When you are going to make a purchace at
    # The Store
    font = pygame.font.Font(data.ariel, 20)
    if data.storeButtonSelect == 0:
        text = 'Agilitiy lv' + str(data.agilityLevel + 1) + ': Increase Your Maximum Speed'
        if data.agilityLevel == 5: text = 'Maxed!!!'
    elif data.storeButtonSelect == 1:
        text = 'Fortitude lv' + str(data.fortitudeLevel + 1 ) + ': Lose less speed when you hit the ground'
        if data.fortitudeLevel == 5: text = 'Maxed!!!'
    elif data.storeButtonSelect == 2:
        text = 'Iterance lv' + str(data.iteranceLevel + 1) + ': Increase the Number of times you can boost'
        if data.iteranceLevel == 5: text = 'Maxed!!!'
    elif data.storeButtonSelect == 3:
        text = 'Serendipity lv' + str(data.serendipityLevel + 1) + ': Increace your chances of seeing money and helpful Doodles'
        if data.serendipityLevel == 5: text = 'Maxed!!!'
    elif data.storeButtonSelect == 4:
        text = 'Resistance lv' + str(data.resistanceLevel + 1) + ': lose less speed when hitting enimies'
        if data.resistanceLevel == 5: text = 'Maxed!!!'
    elif data.storeButtonSelect == 6:
        if data.cannonButtonSelect == 0:
            text = 'Slingshot: Good for propelling you forward.'
        if data.cannonButtonSelect == 1:
            text = 'Cannon: Perfect for recreational launching.'
        if data.cannonButtonSelect == 2:
            text = 'Tank: If the military comes asking for some Top Secret schematics we don\'t know nothin.'
        if data.cannonButtonSelect == 3:
            text = 'Sun Machine: For launching with a bit more elegance.'
        if data.cannonButtonSelect == 4:
            text = 'Capre Diem Machine: Seize the Day, Soar to the Heavens.'
    elif data.storeButtonSelect == 5:
        if data.bootButtonSelect == 0:
            text = 'Old Boots: Old yet reliable.'
        if data.bootButtonSelect == 1:
            text =  'Moon Boots: Get to the Moon and Back.'
        if data.bootButtonSelect == 2:
            text = 'Hermes Boots: The boots of the gods.'
    else: text = ''
    if data.storeButtonSelect < 5:
        pygame.draw.rect(data.screen, data.red,data.buttonData[data.storeButtonSelect],2)
    text = font.render(text, 1, (10, 12, 10))
    data.screen.blit(text, [150,543 ] )
    money = font.render( 'Money: ' + str(data.bank),1, (10, 12, 10))
    data.screen.blit(money, [10, data.canvasHeight - 30])
    
    
def drawBoosts():
    start = 6
    width = 25
    for boost in xrange(data.maxBoost ):
        pygame.draw.rect( data.screen,[0,0,0],[start,data.canvasHeight - 34, width-2,28])
        start += width
    start = 6
    width = 25
    for boost in xrange(data.boostCount):
        pygame.draw.rect( data.screen,[0,0,0xff],
            [start,data.canvasHeight - 34, width-2, 28])
        start += width

def drawSelf():
    if (data.changeAni == 'up' and data.yVelocity <= 0) or (data.changeAni == 'down' and data.yVelocity > 0 ):
        changeSprite = True
    else: changeSprite = False
    #This Canges the Animations When the player is falling up down ect
    if changeSprite == True:    
        if data.yVelocity > 0:
            data.playerSprite = data.sprites['selfair']
            data.changeAni = 'up'
        if data.yVelocity <= 0:
            data.playerSprite = random.choice(data.selfFallingSprite)
            data.changeAni = 'down'
    data.selfHitbox = pygame.Rect([100 + 100*data.pad,
        int( data.canvasHeight - data.selfHeight + data.selfSpriteHeight*data.pad - data.radius) - data.ground,
            int(data.selfSpriteWidth *( 1 - data.pad*2)),
            int(data.selfSpriteHeight *( 1 - data.pad*2))] )
    data.screen.blit(data.playerSprite,[100,
        data.canvasHeight - data.radius - data.ground - data.selfHeight])
    if data.debugMode == True:
        pygame.draw.rect(data.screen,data.red,data.selfHitbox,4)
    
def scrollBackground():
    if data.bgy > data.bgHeight - data.canvasHeight:
        data.bgy = data.bgHeight - data.canvasHeight
    if data.bgy < 0:
        data.bgy = 0
    if data.bgx > data.bgWidth:
        data.bgx = 0 
    for tile in xrange(0, abs( -1*data.canvasWidth/data.bgWidth)+1):
        data.screen.blit(data.bg,
            (tile*data.bgWidth - data.bgx,
             data.canvasHeight - data.bgHeight + data.bgy))


##########################################################################
################## Controler Functions ###################################
##########################################################################

def keyPressed():
    if event.type == pygame.MOUSEBUTTONDOWN:
        print pygame.mouse.get_pos()
    if event.type == pygame.KEYDOWN and data.keyDown == False:
        if data.firstTime == 'saveMessage':
            data.firstTime = True
        elif event.key == pygame.K_ESCAPE:
            goBack()
        elif data.instructions:
            if data.htpi == len(data.htpImages) - 1:
                data.instructions = False
                data.firstTime = False
                data.htpi = 0
            else:
                data.htpi += 1
        elif event.key == pygame.K_i:
            data.instructions = True 
        elif data.currentScreen == 'game':
            gameControl()
        elif data.currentScreen == 'mainMenu':
            mainMenuControl()
        elif data.currentScreen == 'store':
            storeControl()
        elif data.currentScreen == 'extras':
            extrasControl()
        elif data.currentScreen == 'options':
            optionsControl()
        data.keyDown = True
    if event.type == pygame.KEYUP:
        data.keyDown = False

def optionsControl():
    if event.key == pygame.K_RETURN:
        if data.optionsSelect == 'autoSave':
            data.autoSave = not(data.autoSave)
        elif data.optionsSelect == 'save':
            save()
        elif data.optionsSelect == 'erase':
            if data.areYouSure == True:
                data.save = data.emptySaveFile
                data.firstTime = True
                initStats()
                data.currentScreen = 'mainMenu'
                data.areYouSure = False
            else: data.areYouSure = True
    elif data.areYouSure == True:
        data.areYouSure = False
    elif event.key == pygame.K_UP:
        if data.optionsSelect == 'save':
            data.optionsSelect = 'autoSave'
        elif data.optionsSelect == 'erase':
            data.optionsSelect = 'save'
    elif event.key == pygame.K_DOWN:
        if data.optionsSelect == 'save':
            data.optionsSelect = 'erase'
        elif data.optionsSelect == 'autoSave':
            data.optionsSelect = 'save'
    
     
    
def extrasControl():
    if event.key == pygame.K_RIGHT:
        data.sketchbookSelect = (data.sketchbookSelect + 1) % len(data.sketchbookDisplay)
    if event.key == pygame.K_LEFT:
        data.sketchbookSelect = (data.sketchbookSelect - 1) % len(data.sketchbookDisplay)



def save():
    try: 
        pickle.dump({
           'agility' : data.agilityLevel,
           'fortitude' : data.fortitudeLevel,
           'iterance' : data.iteranceLevel,
           'serendipity' : data.serendipityLevel,
           'resistance' : data.resistanceLevel,
           'bank' : data.bank ,
           'unlockedCannons' : data.unlockedCannons,
           'maxHeight' : 0,
           'playTime' : 0,
           'currentCannon' : data.currentCannon,
           'sketchbook': data.sketchbook,
           'unlockedBoots' : data.unlockedBoots,
           'currentBoot' : data.currentBoot,
           'autoSave' : data.autoSave
           
            },open('PaperLaunchFiles/PLSaveFile.pkl','wb'))
        data.onScreenIcons[0].killTime = 40
        data.onScreenIcons[2].killTime = 40 
    except: print 'fuck'
    
def moveBootButton():
    if event.key == pygame.K_RIGHT:
        data.bootButtonSelect = (data.bootButtonSelect + 1) % (data.unlockedBoots + 1) % 3
    if event.key == pygame.K_LEFT:
        data.bootButtonSelect = (data.bootButtonSelect - 1) % (data.unlockedBoots + 1) % 3
    
def storeControl():
    # controls The store. It  workts by using the index of a stat
    # and the using the mod fuction to loop around the stat is a circle like
    # patter and whatnot
    if event.key == pygame.K_p:
        data.currentScreen = 'game'
        initGame()
    elif event.key == pygame.K_UP:
        data.storeButtonSelect = (data.storeButtonSelect - 1)%7
    elif event.key == pygame.K_DOWN:
        data.storeButtonSelect = (data.storeButtonSelect + 1)%7
    if data.storeButtonSelect == 5:
        moveBootButton()
    if data.storeButtonSelect == 6:
        if event.key == pygame.K_RIGHT:
            data.cannonButtonSelect = (data.cannonButtonSelect +1 )% (data.unlockedCannons + 1) % 5
        if event.key == pygame.K_LEFT:   
            data.cannonButtonSelect = (data.cannonButtonSelect -1 )% (data.unlockedCannons + 1) % 5
    if event.key == pygame.K_RETURN:
        if data.storeButtonSelect == 5 and data.bootButtonSelect < data.unlockedBoots:
            setBoot()
        elif data.storeButtonSelect == 5 and data.bootButtonSelect == data.unlockedBoots\
                                     and data.bank >= data.costs[5][data.unlockedBoots]:
            data.bank -= data.costs[5][data.unlockedBoots]
            data.unlockedBoots += 1
            setBoot()
            save()
        elif data.storeButtonSelect == 6 and data.cannonButtonSelect < data.unlockedCannons :
            data.currentCannon = data.allCannons[data.cannonButtonSelect]
        elif data.storeButtonSelect == 6 and data.unlockedCannons < 5:
            if data.costs[6][data.unlockedCannons] <= data.bank:
                data.bank -= data.costs[6][data.unlockedCannons]
                data.unlockedCannons += 1
                data.currentCannon = data.allCannons[data.cannonButtonSelect]
                save()
        elif data.storeButtonSelect < 5 and data.stats[data.storeButtonSelect] < 5 and \
            data.bank >= data.costs[data.storeButtonSelect][data.stats[data.storeButtonSelect]]:
            data.bank -= data.costs[data.storeButtonSelect][data.stats[data.storeButtonSelect]]
            buyShit()
 
def setBoot():
    if  data.bootButtonSelect == 0:
        data.currentBoot = 'oldBoots'
    elif  data.bootButtonSelect == 1:
        data.currentBoot = 'hermesBoots'
    elif  data.bootButtonSelect == 2:
        data.currentBoot = 'moonBoots'
    
def buyShit():
    if data.storeButtonSelect == 0:
                data.agilityLevel += 1
    elif data.storeButtonSelect == 1:
        data.fortitudeLevel += 1
    elif data.storeButtonSelect == 2:
        data.iteranceLevel += 1
    elif data.storeButtonSelect == 3:
        data.serendipityLevel += 1
    elif data.storeButtonSelect == 4:
        data.resistanceLevel += 1
    data.stats = [data.agilityLevel,
                  data.fortitudeLevel,
                  data.iteranceLevel,
                  data.serendipityLevel,
                  data.resistanceLevel]
    if data.autoSave:
        save()

def gameControl():
    if data.launch == 'launchBar':
        data.launch = 'angle'
    elif data.launch == 'angle':
        power = data.cannonPower[data.currentCannon]
        data.xSpeed = int( math.cos(data.theta) * (data.launchBarLength/100.0) * power ) + 20
        data.yVelocity = int( math.sin(data.theta) * (data.launchBarLength/100.0) * power) + 20
        data.launch = False
        data.startTime = time.time()
    elif data.boostCount > 0 and event.key == pygame.K_SPACE:
        boost()
    elif data.debugMode == True:
        if event.key == pygame.K_c:
            data.onScreen += [car()]
        if event.key == pygame.K_b:
            data.onScreen += [bear()]
        if event.key == pygame.K_t:
            data.onScreen += [trogdor()]
        if event.key == pygame.K_n:
            data.onScreen += [nyanCat()]
        if event.key == pygame.K_m:
            data.onScreen += [money()]
        if event.key == pygame.K_s:
            data.onScreen += [shark()]
        if event.key == pygame.K_a:
            data.onScreen += [airplane()]
        if event.key == pygame.K_RETURN:
            boost()
            data.boostCount += 1
    if event.key == pygame.K_d:
        data.debugMode = not(data.debugMode)
    if data.gameOver == True:
        gameOverControl()

def boost():
    data.xSpeed = abs(data.xSpeed) + data.bootForce[data.currentBoot]
    data.yVelocity = abs(data.yVelocity)/2 + data.bootForce[data.currentBoot]
    data.boostCount -= 1

def gameOverControl():
    if event.key == pygame.K_DOWN or event.key == pygame.K_UP:
        data.gameOverButtonSelect = not( data.gameOverButtonSelect)
    if event.key == pygame.K_RETURN:
        if data.gameOverButtonSelect:
            data.currentScreen = 'store'
        else:
            initGame()

def mainMenuControl():
    if event.key == pygame.K_LEFT:
        data.buttonSelect = (data.buttonSelect - 1)%4
    if event.key == pygame.K_RIGHT:
        data.buttonSelect = (data.buttonSelect + 1)%4
    if event.key == pygame.K_RETURN and data.buttonSelect == 2:
        data.currentScreen = 'options'
    if event.key == pygame.K_RETURN and data.buttonSelect == 3:
        data.currentScreen = 'game'
        initGame()
    if event.key == pygame.K_RETURN and data.buttonSelect == 0:
        data.currentScreen = 'store'
    if event.key == pygame.K_RETURN and data.buttonSelect == 1:
        data.currentScreen =  'extras'
  



def goBack():
    if data.currentScreen == 'game' or data.currentScreen == 'store' or 'extras':
        data.currentScreen = 'mainMenu'  

##########################################################################
################### Main Loop ############################################
##########################################################################
clock=pygame.time.Clock()
init()

# -------- Main Program Loop -----------
done = False
while done==False:
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
           done=True # Flag that we are done so we exit this loop
    # Set the screen background
    data.screen.fill(black)
    if data.currentScreen == 'game':
        gamePlay()
    for icon in data.onScreenIcons:
        icon.animate()
    keyPressed()
    redrawAll()
    clock.tick(30)
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()



##########################################################################
################### Helper Functions #####################################
##########################################################################

def filePath( items, extention, folder = '',):
    # I dont really Use this anymore
    if len(folder) > 0:
        folder += '/'
    return ["C:/python27/launch/" + folder + item  + extention for item in items ]

pygame.quit () 