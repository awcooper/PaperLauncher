import pygame
pygame.init()

global data
class Struct: pass
data = Struct()

bg = pygame.image.load('C:/python27/launch/paper.gif')
data.canvasHeight, data.canvasWidth = bg.get_size()

##########################################################################
################### Init Functions #######################################
##########################################################################

def init(constant = False):
    data.gameOver = False
    initPhysics()
    initPressEvents()
    if constant == False:
        try:
            initSound()
        except: pass
        initData()
    initObjects()
    
def initPressEvents():
    data.up = False
    data.down = False
    data.boostCount = 10

def initObjects():
    #spikeBall = physicalObject('spikeBall', [canvas.data.bgx + canvas.data.canvasWidth, canvas.data.bgy -200],0,'C:/python27/launch/spikeBall.gif')
    data.showCannon = True
    data.onScreen = []
    data.launch = 'launchBar'
    data.player = player(canvas.data.selfHeight,30)
    

def initData():
    data.musicNote =  pygame.image.load('C:/python27/launch/musicNote.gif')
    data.highScore = []


def initPhysics():
    paperBg = pygame.image.load('C:/python27/launch/paper.gif')
    data.canvasHeight, data.canvasWidth = paperBg.get_size()
    data.bgx = 0
    data.bgy = canvas.data.canvasHeight 
    data.speed = 0
    data.yVelocity = 0
    data.radius = 26
    data.distance = 0
    data.launchBarLength= 0
    data.xFriction = 1.2
    data.yFriction = -1.2
    data.ground = 100 #how many pixes high the ground is # 140 bg2
    data.selfHeight = canvas.data.ground + 6
    data.theta = math.pi/32
    data.dTheta = math.pi/32

def initSound():
    data.playMusic = True
    data.songs = filePath(['beetovenVirus','levels', 'handguns', 'ghostsnstuff', 'iAmTheBest', 'passionForExploring', 'tetrisTheme', 'marioThemeSong', 'harderBetterFasterStronger', 'getLow'], '.wav')
    data.songSelect = 0

##########################################################################
################### Timer Events #########################################
##########################################################################


##########################################################################
################### Laws of Physics ######################################
##########################################################################

##########################################################################
################### Object and Class Definitions #########################
##########################################################################


##########################################################################
################### Main Loop ############################################
##########################################################################


##########################################################################
################### Helper Functions #####################################
##########################################################################

def filePath( items, extention, folder = '',):
    if len(folder) > 0:
        folder += '/'
    return ["C:/python27/launch/" + folder + item  + extention for item in items ]

def randomHexColor():
    # hex values are written in #rrggaa format in hexidecimal
    hexValue = ''
    for rgb in range(0,3):
        hexDigit = str(hex(random.randint(0, 0xff)))[2:] 
        if len(hexDigit) == 1:
            hexValue += '0' + hexDigit
        else: hexValue += hexDigit 
    return '#' + hexValue 

print data.canvasHeight, data.canvasWidth 