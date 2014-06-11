###########################################
##Adam Cooper                            ## 
##Section H                              ##
##15-112                                 ##
##Toss The Ball!!!!                      ## 
##A 15-112 term project by Adam Cooper   ##
###########################################

import winsound 
from Tkinter import *
from winsound import *
import math
import copy 
import string

##########################################################################
################### Controller Events ####################################
##########################################################################

def mousePressed(event):
    try:
        clickMusicButton(event)
    except: pass
    
def clickMusicButton(event):
    musicButtonX = canvas.data.canvasWidth -30
    musicButtonY = canvas.data.canvasHeight - 30
    #its on the edge of the screeen so we don't need to
    #worry of the other sides of the box. The music note
    #is 30x30 pixels
    if event.x > musicButtonX and event.y > musicButtonY:
        if canvas.data.playMusic == True:
            winsound.PlaySound(None, 1)
            canvas.data.musicNote =  PhotoImage(file = 'C:/python27/launch/musicNoteX.gif')
        else:
            winsound.PlaySound(canvas.data.songs[canvas.data.songSelect],SND_FILENAME|SND_ASYNC|SND_LOOP)
            canvas.data.musicNote =  PhotoImage(file = 'C:/python27/launch/musicNote.gif')
        canvas.data.playMusic = not(canvas.data.playMusic)

def keyPressed(event):
    global canvas
    if event.keysym.isdigit() and canvas.data.playMusic and int(event.keysym) < len(canvas.data.songs) and int(event.keysym) >= 0:
        songSelect(event)
    elif event.keysym == 'space':
        launchMode(event)
    elif event.keysym =='k':
        canvas.data.yVelocity += 15
        canvas.data.speed += 15
    elif event.keysym == 'r':
        init(True)

def songSelect(event):
    canvas.data.songSelect = int(event.keysym)
    winsound.PlaySound(canvas.data.songs[canvas.data.songSelect],SND_FILENAME|SND_ASYNC|SND_LOOP)

def launchMode(event):
    if canvas.data.launch == 'launchBar':
        canvas.data.launch = 'angle'
    elif canvas.data.launch == 'angle':
        canvas.data.launch = False
        launchSelf(canvas.data.theta, canvas.data.launchBarLength)



##########################################################################
################### Init Functions #######################################
##########################################################################
    
def init(constant = False):
    canvas.data.gameOver = False
    initPhysics()
    if constant == False:
        try:
            initSound()
        except: pass
        initData()
    initObjects()
    
    
def initObjects():
    #spikeBall = physicalObject('spikeBall', [canvas.data.bgx + canvas.data.canvasWidth, canvas.data.bgy -200],0,'C:/python27/launch/spikeBall.gif')
    canvas.data.showCannon = True
    canvas.data.onScreen = []
    canvas.data.launch = 'launchBar'

def initData():
    canvas.data.bg = PhotoImage(file = 'C:/python27/launch/background.gif')
    canvas.data.musicNote =  PhotoImage(file = 'C:/python27/launch/musicNote.gif')
    canvas.data.highScore = []


def initPhysics():
    canvas.data.bgx = 0
    canvas.data.bgy = canvas.data.canvasHeight 
    canvas.data.speed = 0
    canvas.data.yVelocity = 0
    canvas.data.bgHeight = 1600 #bg2 1872
    canvas.data.bgWidth = 1600 #bg2 1872
    canvas.data.radius = 26
    canvas.data.distance = 0
    canvas.data.launchBarLength= 0
    canvas.data.xFriction = 1.2
    canvas.data.yFriction = -1.2
    canvas.data.ground = 140 #how many pixes high the ground is # 120 bg2
    canvas.data.selfHeight = canvas.data.ground + 6
    canvas.data.theta = math.pi/32
    canvas.data.dTheta = math.pi/32

def initSound():
    canvas.data.playMusic = True
    canvas.data.songs = filePath(['tossThemeSong','throughTheFireAndTheFlames', 'handguns', 'ghostsnstuff', 'iAmTheBest', 'passionForExploring', 'tetrisTheme', 'marioThemeSong', 'harderBetterFasterStronger', 'getLow'], '.wav')
    canvas.data.songSelect = 0
    winsound.PlaySound(canvas.data.songs[canvas.data.songSelect],SND_FILENAME|SND_ASYNC|SND_LOOP)

##########################################################################
################### Timer Events #########################################
##########################################################################

def timerFired():
    redrawAll()
    delay = 20 # milliseconds
    if canvas.data.gameOver == False:
        if canvas.data.showCannon == True:
            launchBar()
        adjustSpeed()
        if canvas.data.launch == False: #and canvas.data.yVelocity > -canvas.data.canvasHeight/3:
            canvas.data.yVelocity -= 1 #gravity
            if canvas.data.speed == 0 and canvas.data.selfHeight == canvas.data.ground:
                canvas.data.gameOver = True
                highScore()
    canvas.after(delay, timerFired) # pause, then call timerFired again

def launchBar():
    if canvas.data.launch:
        drawFireBar()
        if canvas.data.launch == 'launchBar':
        #Launch bar goes up utnil it reach the max
        #and then starts over.
            if canvas.data.launchBarLength > 100:
                canvas.data.launchBarLength = 0
            else: canvas.data.launchBarLength += 5
        elif canvas.data.launch == 'angle':
            drawAngleMeter()
            if canvas.data.theta > 0 and canvas.data.theta < math.pi/2 :
                canvas.data.theta += canvas.data.dTheta
            else:
                #Meter bar flips directions when it reaches a bound.
                canvas.data.dTheta *= -1
                canvas.data.theta += canvas.data.dTheta
 
def highScore():
    highScore = copy.deepcopy(canvas.data.highScore)
    highScore += [int(canvas.data.distance)/100]
    highScore = sorted(highScore)[::-1]
    canvas.data.highScore = highScore[0:5]  
    
##########################################################################
################### Laws of Physics ######################################
##########################################################################


def launchSelf(theta , force):
    canvas.data.speed = round(  math.cos(theta) * force )
    canvas.data.yVelocity = round(  math.sin(theta) * ( force)/3) 

def adjustSpeed():
    canvas.data.bgx -= canvas.data.speed #Adjusts the speed that the backgroud
    canvas.data.distance += canvas.data.speed
    #is scrolling
    if canvas.data.bgy <  canvas.data.bgHeight - canvas.data.canvasHeight:
        canvas.data.bgy += canvas.data.yVelocity
    if canvas.data.bgy >  canvas.data.bgHeight - canvas.data.canvasHeight and canvas.data.yVelocity < 0 and canvas.data.selfHeight  < canvas.data.canvasHeight/2 :
        canvas.data.bgy += canvas.data.yVelocity
    elif canvas.data.selfHeight  > canvas.data.canvasHeight/2 and \
    canvas.data.bgy <  canvas.data.bgHeight and canvas.data.bgy <= canvas.data.canvasHeight:
        canvas.data.bgy += canvas.data.yVelocity
    else:
        canvas.data.selfHeight += canvas.data.yVelocity
    if canvas.data.selfHeight < canvas.data.ground:
        canvas.data.selfHeight = canvas.data.ground 
        canvas.data.bgy = canvas.data.canvasHeight - 2
        canvas.data.yVelocity = int(canvas.data.yVelocity/canvas.data.yFriction)
        canvas.data.speed = int(canvas.data.speed/canvas.data.xFriction)
    for item in canvas.data.onScreen:
        item.moveObject((canvas.data.yVelocity, canvas.data.speed))

##########################################################################
################### Drawing Fucntions ####################################
##########################################################################

def redrawAll():
    canvas.delete(ALL)
    scrollBackground()
    drawSelf()
    for item in canvas.data.onScreen:
        item.draw()
    drawCannon()
    drawOutOfRange()
    drawInfo()
    if canvas.data.gameOver == True:
        drawHighScore()

def drawHighScore():
    cx = canvas.data.canvasWidth/2
    cy = canvas.data.canvasHeight/2
    canvas.create_rectangle(cx - cx/2, cy - cy/2, cx + cx/2,\
                   cy + cy/1.5, fill = 'yellow', width = 2)
    canvas.create_text(cx, cy - 20, text="Game Over!",\
                   font=("Helvetica", 32, "bold"))
    canvas.create_text(cx, cy + 20, text= '1st: ' +\
        str(canvas.data.highScore[0]) + ' m', font=("Helvetica", 18))
    if len(canvas.data.highScore) > 1:
        canvas.create_text(cx, cy + 44, text= '2nd: ' + \
            str(canvas.data.highScore[1]) + ' m', font=("Helvetica", 18))
    if len(canvas.data.highScore) > 2:
        canvas.create_text(cx, cy + 68, text='3rd: ' +
        str(canvas.data.highScore[2]) + ' m', font=("Helvetica", 18))
    if len(canvas.data.highScore) > 3:
        canvas.create_text(cx, cy + 92, text='4th: ' +
        str(canvas.data.highScore[3]) + ' m', font=("Helvetica", 18))
    if len(canvas.data.highScore) > 4:
        canvas.create_text(cx, cy + 116, text='5th: ' +
        str(canvas.data.highScore[4]) + ' m', font=("Helvetica", 18))
        

def drawOutOfRange():
    if canvas.data.selfHeight > canvas.data.canvasHeight:
        canvas.create_rectangle(170, 10,210,50, fill = 'orange')
        canvas.create_text(190, 30, text = str(int(canvas.data.selfHeight)))

def drawCannon():
    if canvas.data.showCannon == True and canvas.data.bgx > -canvas.data.canvasWidth/2:
        canvas.create_rectangle( 20 + canvas.data.bgx, canvas.data.bgy - canvas.data.ground,
            190 + canvas.data.bgx, canvas.data.bgy - canvas.data.ground - 120, fill = 'orange')
    else: canvas.data.showCannon = False

def drawInfo():
    canvas.create_rectangle(4, canvas.data.canvasHeight - 34, canvas.data.canvasWidth, canvas.data.canvasHeight, fill = 'white', width = 2 )
    canvas.create_text(canvas.data.canvasWidth/2, canvas.data.canvasHeight - 15, text = 'Distance: ' + str(int(canvas.data.distance)/100) + 'm')
    canvas.create_image(canvas.data.canvasWidth - 31, canvas.data.canvasHeight - 1, image = canvas.data.musicNote, anchor = SW)

def drawSelf():
    radius = canvas.data.radius 
    drawCircle( 190 - radius, canvas.data.canvasHeight - canvas.data.selfHeight - radius, radius)

def scrollBackground():
    bg = canvas.data.bg
    bgWidth = canvas.data.bgWidth
    if canvas.data.bgx < -bgWidth:
        canvas.data.bgx = 0 
    canvas.create_image(canvas.data.bgx, canvas.data.bgy, image = bg, anchor = SW)
    canvas.create_image(canvas.data.bgx + bgWidth, canvas.data.bgy, image = bg, anchor = SW)

def drawFireBar():
    canvas.create_rectangle(220, canvas.data.canvasHeight - canvas.data.ground - 10, 200, canvas.data.canvasHeight - canvas.data.ground - 10 - canvas.data.launchBarLength, fill = 'red')

def drawAngleMeter():
    bottom = canvas.data.canvasHeight - canvas.data.ground - 10
    canvas.create_line(224, bottom, 224 + 100*math.cos(canvas.data.theta), bottom +(100)*math.sin( - canvas.data.theta), fill="red", width=5)


##########################################################################
################### Object and Class Definitions #########################
##########################################################################


class physicalObject(object):
    def __init__(self, type, location, hitbox, photo):
        self.type = type
        self.location = location
        self.hitbox = hitbox
        self.photo = PhotoImage(file = photo)
        self.kill = False
        
    def moveObject(self,movement):
        self.location = [canvas.data.bgx + canvas.data.canvasWidth, canvas.data.bgy -200]
    
    def draw(self):
        canvas.create_image(self.location, image = self.photo, anchor = SW)


class enemy(physicalObject):
    pass
    
class player(physicalObject):
    pass

class gun():
    pass

##########################################################################
################### Helper Functions #####################################
##########################################################################

def filePath( items, extention, folder = '',):
    if len(folder) > 0:
        folder += '/'
    return ["C:/python27/launch/" + folder + item  + extention for item in items ]

def drawCircle(x,y,rad):
    canvas.create_oval(x-rad,y-rad,x+rad,y+rad,width=4,fill='cyan')

def distance(x1,x2,y1,y2):
    return ((x2-x1)**2 + (y2-y1)**2  )**.5
    

##########################################################################
################### Run Function and Execute##############################
##########################################################################


def run():
    # create the root and the canvas
    global canvas
    root = Tk()
    canvasWidth = 1000
    canvasHeight = 600
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    root.resizable(width=0, height=0)
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.canvasWidth  = canvasWidth
    canvas.data.canvasHeight = canvasHeight
    init()
    root.bind("<Button-1>", mousePressed)
    root.bind("<Key>", keyPressed)
    # set up events
    timerFired()
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run()