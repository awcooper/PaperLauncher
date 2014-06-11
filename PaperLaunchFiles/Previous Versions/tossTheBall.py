import winsound 
from Tkinter import *
from winsound import *
import math 


def mousePressed(event):
    if event.x > canvas.data.canvasWidth -30 and event.y > canvas.data.canvasHeight - 30:
        if canvas.data.playMusic == True:
            winsound.PlaySound(None, 1)
        else: winsound.PlaySound(canvas.data.songs[canvas.data.songSelect],SND_FILENAME|SND_ASYNC|SND_LOOP)
        canvas.data.playMusic = not(canvas.data.playMusic)


    
def init():
    #winsound.PlaySound('C:/python27/tossThemeSong.wav', winsound.SND_FILENAME|winsound.SND_LOOP)
    canvas.data.bg = PhotoImage(file = 'C:/python27/background.gif')
    canvas.data.musicNote =  PhotoImage(file = 'C:/python27/musicNote.gif')
    canvas.data.bgx = 0
    canvas.data.playMusic = True
    canvas.data.songs = ["C:/python27/tossThemeSong.wav"]
    canvas.data.songSelect = 0
    winsound.PlaySound(canvas.data.songs[canvas.data.songSelect],SND_FILENAME|SND_ASYNC|SND_LOOP)
    canvas.data.bgy = canvas.data.canvasHeight 
    canvas.data.speed = 0
    canvas.data.yVelocity = 0
    canvas.data.bgHeight = 1600
    canvas.data.radius = 30
    canvas.data.distance = 0
    canvas.data.launchBarLength= 0
    canvas.data.xFriction = 1.2
    canvas.data.yFriction = -1.2
    canvas.data.ground = 140 #ground height in respect to canvas
    canvas.data.theta = math.pi/32
    canvas.data.dTheta = math.pi/32
    canvas.data.showCannon = True
    canvas.data.selfHeight = canvas.data.ground 
    spikeBall = physicalObject('spikeBall', [canvas.data.bgx + canvas.data.canvasWidth, canvas.data.bgy -200],0,'C:/python27/spikeBall.gif')
    canvas.data.onScreen = []
    canvas.data.launch = 'launchBar'
     

def keyPressed(event):
    global canvas
    if event.keysym == 'Up':
        canvas.data.speed += 1
    elif event.keysym == 'Down':
        if canvas.data.speed > 0:
            canvas.data.speed -= 1
    elif event.keysym == 'space':
        if canvas.data.launch == False:
            canvas.data.yVelocity += 15
            canvas.data.speed += 15
        elif canvas.data.launch == 'launchBar':
            canvas.data.launch = 'angle'
        elif canvas.data.launch == 'angle':
            canvas.data.launch = False
            launchSelf(canvas.data.theta, canvas.data.launchBarLength)
    elif event.keysym == 'r':
        init()

def timerFired():
    redrawAll()
    delay = 20 # milliseconds
    if canvas.data.showCannon == True:
        launchBar()
    adjustSpeed()
    if canvas.data.showCannon == False:
        canvas.data.yVelocity -= 1
    canvas.after(delay, timerFired) # pause, then call timerFired again

def launchBar():
    if canvas.data.launch:
        drawFireBar()
        if canvas.data.launch == 'launchBar':
            if canvas.data.launchBarLength > 100:
                canvas.data.launchBarLength = 0
            else: canvas.data.launchBarLength += 5
        elif canvas.data.launch == 'angle':
            drawAngleMeter()
            if canvas.data.theta > 0 and canvas.data.theta < math.pi/2 :
                canvas.data.theta += canvas.data.dTheta
            else:
                canvas.data.dTheta *= -1
                canvas.data.theta += canvas.data.dTheta
    
    
def launchSelf(theta , force):
    canvas.data.speed = round(  math.cos(theta) * force  )
    canvas.data.yVelocity = round( math.sin(theta) * ( force / 2 ) ) 

def drawFireBar():
    canvas.create_rectangle(220, canvas.data.canvasHeight - canvas.data.ground - 10, 200, canvas.data.canvasHeight - canvas.data.ground - 10 - canvas.data.launchBarLength, fill = 'red')

def drawAngleMeter():
    bottom = canvas.data.canvasHeight - canvas.data.ground - 10
    canvas.create_line(224, bottom, 224 + 100*math.cos(canvas.data.theta), bottom +(100)*math.sin( - canvas.data.theta), fill="red", width=5)


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
        canvas.data.selfHeight = canvas.data.canvasHeight/2
        canvas.data.bgy += canvas.data.yVelocity
    else:
        canvas.data.selfHeight += canvas.data.yVelocity
    if canvas.data.selfHeight < canvas.data.ground:
        canvas.data.selfHeight = canvas.data.ground 
        canvas.data.bgy = canvas.data.canvasHeight - 2
        canvas.data.yVelocity /= canvas.data.yFriction
        canvas.data.speed /= canvas.data.xFriction
    for item in canvas.data.onScreen:
        item.moveObject((canvas.data.yVelocity, canvas.data.speed))
    

def redrawAll():
    canvas.delete(ALL)
    scrollBackground()
    adjustHeight()
    drawSelf()
    drawInfo()
    for item in canvas.data.onScreen:
        item.draw()
    if canvas.data.selfHeight > canvas.data.canvasHeight:
        canvas.create_rectangle(170, 10,210,50, fill = 'orange')
        canvas.create_text(190, 30, text = str(int(canvas.data.selfHeight)))
    if canvas.data.showCannon == True and canvas.data.bgx > -300:
        canvas.create_rectangle( 20 + canvas.data.bgx, canvas.data.bgy - canvas.data.ground,
            190 + canvas.data.bgx, canvas.data.bgy - canvas.data.ground - 120, fill = 'yellow')
    else: canvas.data.showCannon = False

def drawInfo():
    canvas.create_rectangle(4, canvas.data.canvasHeight - 34, canvas.data.canvasWidth, canvas.data.canvasHeight, fill = 'white', width = 2 )
    canvas.create_text(canvas.data.canvasWidth/2, canvas.data.canvasHeight - 10, text = 'Distance: ' + str(int(canvas.data.distance)/100) + 'm')
    canvas.create_image(canvas.data.canvasWidth - 31, canvas.data.canvasHeight - 1, image = canvas.data.musicNote, anchor = SW)

def drawSelf():
    radius = canvas.data.radius 
    drawCircle( 190 - radius, canvas.data.canvasHeight - canvas.data.selfHeight - radius, radius)

def drawCircle(x,y,rad):
    canvas.create_oval(x-rad,y-rad,x+rad,y+rad,width=4,fill='cyan')

def scrollBackground():
    bg = canvas.data.bg
    bgWidth = 1600
    if canvas.data.bgx < -bgWidth:
        canvas.data.bgx = 0 
    canvas.create_image(canvas.data.bgx, canvas.data.bgy, image = bg, anchor = SW)
    canvas.create_image(canvas.data.bgx + bgWidth, canvas.data.bgy, image = bg, anchor = SW)
    

def adjustHeight():
    pass


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