import math
import turtle
import random
from datetime import datetime
import argparse
from PIL import Image
from fractions import gcd

#draw the circle using turtle



def drawCircleTurtle(x, y, r):
    #move to the start of circle

    turtle.up()
    turtle.setpos(x+r, y)
    turtle.down()

    #draw the circle
    for i in range(0, 365):
        a = math.radians(i)
        turtle.setpos(x + r*math.cos(a), y + r*math.sin(a))



class Spiro:
    def __init__(self, xc, yc, col, R, r, l):

        #create turtle
        self.t = turtle.Turtle()

        #set cursor shape
        self.t.shape('turtle')

        #set the step in degree
        self.step = 5

        #set drawing complete flag
        self.drawingComplete = False

        #set parameters
        self.setparams(xc, yc, col, R, r, l)

        # initalize the drawing
        self.restart()

    def setparams(self, xc, yc, col, R, r, l):
        self.xc = xc
        self.yc = yc
        self.R = int(R)
        self.r = int(r)
        self.l = l
        self.col = col

        # reduce r/R to its smallest form by dividing with the Greatest Commen Divider
        gcdVal = math.gcd(int(self.r), int(self.R))
        self.nRot = self.r // gcdVal

        # get ratio of radii
        self.k = r / float(R)

        # set the color
        self.t.color(*col)

        # store the current angle
        self.a = 0

    # restart the drawing
    def restart(self):
        # set the Flag
        self.drawingComplete = False

        # show the turtle
        self.t.showturtle()

        # go to the first point
        self.t.up()
        R, k, l = self.R, self.k, self.l
        a = 0.0
        x = R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
        y = R * ((1 - k) * math.sin(a) + l * k * math.sin((1 - k) * a / k))

        self.t.setpos(self.xc + x, self.yc + y)
        self.t.down()

    # update by one step
    def update(self):

        # skip the rest of the steps if done
        if self.drawingComplete:
            return

        # increment the angle
        self.a += self.step

        # draw a stp
        R, k, l = self.R, self.k, self.l

        # set a angle
        a = math.radians(self.a)

        x = R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
        y = R * ((1 - k) * math.sin(a) + l * k * math.sin((1 - k) * a / k))

        self.t.setpos(self.xc + x, self.yc + y)

        # if drawing is complete set the flag
        if self.a >= 360 * self.nRot:
            self.drawingComplete = True
            self.t.hideturtle()

class SpiroAnimator:

    def __init__(self, N):

        #set timeer value
        self.deltaT = 10

        #get window dimensions
        self.width = turtle.window_width()
        self.height = turtle.window_height()

        #create Spiro objects
        self.spiros = []
        for i in range(N):

            #generate random param
            rparams = self.genRandomParams()

            #set spiro parameters
            spiro = Spiro(*rparams)
            self.spiros.append(spiro)

            #call timer
            turtle.ontimer(self.update, self.deltaT)

    def update(self):

        #update all spiros
        nComplete = 0

        for spiro in self.spiros:

            #update
            spiro.update()

            #count complete spiros
            if spiro.drawingComplete:
                nComplete +=1

        #restart if all spiros are complete
        if nComplete == len(self.spiros):
            self.restart()

        #call the timer
        turtle.ontimer(self.update, self.deltaT)

    def toggleTurtles(self):
        for spiro in self.spiros:
            if spiro.t.isvisible():
                spiro.t.hideturtle()
            else:
                spiro.t.showturtle()


    def genRandomParams(self):
        width, height= self.width, self.height

        R = random.randint(50, min(width, height)//2)
        r = random.randint(10, 9*R//10)
        l = random.uniform(0.1, 0.9)
        xc = random.randint(-width//2, width//2)
        yc = random.randint(-height//2, height//2)

        col = (random.random(),
               random.random(),
               random.random())

        return(xc, yc, col, R, r, l)

    # restart spiro drawing
    def restart(self):
        for spiro in self.spiros:
            # clear
            spiro.clear()

            # generate random parameters
            rparams = self.genRandomParams()

            # set spiro parameters
            spiro.setparams(*rparams)

            # restart drawing
            spiro.restart()

#draw the whole hing
def draw(self):

    #draw the rest of the points
    R, k, l = self.R, self.k, self.l

    for i in range(0, 360*self.nRot + 1, self.step):
        a = math.radians(i)
        x = R * ((1 - k) * math.cos(a) + l * k * math.cos((1 - k) * a / k))
        y = R * ((1 - k) * math.sin(a) + l * k * math.sin((1 - k) * a / k))

        self.t.setpos(self.xc + x, self.yc + y)

        #drwaing done hide turtle
        self.t.hideturtle()

def saveDrawing():
    #hide turtle cursor
    turtle.hideturtle()

    #generate unique file names
    dateStr= (datetime.now()).strftime("%d%b%Y-%H%M%S")
    fileName= 'spiro-' + dateStr
    print('saving drawing to %s.eps/png' % fileName)

    #get tkinter canvas
    canvas = turtle.getcanvas()

    #save the drawing as a postscript image
    canvas.postscript(file=fileName + 'eps')

    #use pillow module to convert the postscript image file to PNG
    img = Image.open(fileName + '.eps')
    img.save(fileName + '.png', 'png')

    #show turtle cursor
    turtle.showturtle()


def main():
    # use sys.argv if needed
    print('generating spirograph...')
    # create parser
    descStr = """This program draws Spirographs using the Turtle module. 
     When run with no arguments, this program draws random Spirographs.

     Terminology:
     R: radius of outer circle
     r: radius of inner circle
     l: ratio of hole distance to r"""

    parser = argparse.ArgumentParser(description=descStr)

    #add expectet arguments
    parser.add_argument('--sparams', nargs=3, dest='sparams', required=False,
                        help="The three arguments in sparams: R, r, l")

    #parse args
    args = parser.parse_args()

    #set the width of drawing window to 80%
    turtle.setup(width=0.8)

    #set cursor shape
    turtle.shape('turtle')

    #set title
    turtle.title("Spirograph")

    #add key handler
    turtle.onkey(saveDrawing, "s")

    #start listening
    turtle.listen()

    #hide turtle cursor
    turtle.hideturtle()

    if args.sparams:
        params = [float(x) for x in args.sparams]

        #draw the spirograp with th given parameters
        col = (0.0, 0.0, 0.0,)
        spiro = Spiro(0, 0, col, *params)
        spiro.draw()

    else:
        #create the animator object
        spiroAnim = SpiroAnimator(4)

        #add a key handler to toggle the turtle cursor
        turtle.onkey(spiroAnim.toggleTurtles, "t")

        #add a key handler to restart the animation
        turtle.onkey(spiroAnim.restart, "space")

    #start the turtle loop
    turtle.mainloop()

#call main
if __name__ == '__main__':
    main()






