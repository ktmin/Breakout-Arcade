# play.py
# Joon Il Moon jm2239, Kyongtae Min km567
# 12/08/2016
"""Subcontroller module for Breakout

This module contains the subcontroller to manage a single game in the Breakout App. 
Instances of Play represent a single game.  If you want to restart a new game, you are 
expected to make a new instance of Play.

The subcontroller Play manages the paddle, ball, and bricks.  These are model objects.  
Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer."""
from constants import *
from game2d import *
from models import *
import random


# PRIMARY RULE: Play can only access attributes in models.py via getters/setters
# Play is NOT allowed to access anything in breakout.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)

class Play(object):
    """An instance controls a single game of breakout.
    
    This subcontroller has a reference to the ball, paddle, and bricks. It animates the 
    ball, removing any bricks as necessary.  When the game is won, it stops animating.  
    You should create a NEW instance of Play (in Breakout) if you want to make a new game.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 25 for an example.
    
    INSTANCE ATTRIBUTES:
        _paddle [Paddle]: the paddle to play with 
        _bricks [list of Brick]: the list of bricks still remaining 
        _ball   [Ball, or None if waiting for a serve]:  the ball to animate
        _tries  [int >= 0]: the number of tries left 
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Breakout. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Breakout.  Only add the getters and setters that you need for 
    Breakout.
    
    You may change any of the attributes above as you see fit. For example, you may want
    to add new objects on the screen (e.g power-ups).  If you make changes, please list
    the changes with the invariants.
                  
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _lives [list of Balls]: the number balls that player have
        _coll[int>=0]: the number of collision between the paddle and the ball
    """
    
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getbricks(self):
        """Returns: the list of bricks in the game"""
        return self._bricks
    def getballs(self):
        """Returns: the ball in the game"""
        return self._ball
    def gettries(self):
        """Returns: the tries in the game"""
        return self._tries
    def getlives(self):
        """Returns: the list of balls that the player has"""
        return self._lives
    
    
    # INITIALIZER (standard form) TO CREATE PADDLES AND BRICKS
    def __init__(self):
        """Initializer: Creates Game object that does not contain the attribute _ball in order
        to be called later on"""
        a=[]
        for m in range(BRICK_ROWS):
            if m==0 or m==1:
                x=colormodel.RED
            elif m==2 or m==3:
                x=colormodel.ORANGE
            elif m==4 or m==5:
                x=colormodel.YELLOW
            elif m==6 or m==7:
                x=colormodel.GREEN
            elif m==8 or m==9:
                x=colormodel.CYAN
            for t in range(BRICKS_IN_ROW):
                a.append(Brick(x=(BRICK_SEP_H/2.0)+(BRICK_WIDTH/2.0)
                               +t*(BRICK_WIDTH+BRICK_SEP_H),
                               y=546-m*(BRICK_SEP_H+BRICK_HEIGHT),
                               width=BRICK_WIDTH,height=BRICK_HEIGHT,fillcolor=x))
        self._bricks=a
        self._paddle=Paddle(x=GAME_WIDTH/2.0,
                            y=PADDLE_OFFSET,width=PADDLE_WIDTH,
                            height=PADDLE_HEIGHT,fillcolor=colormodel.BLACK)
        self._tries=3
        
        a=Ball(x=GAME_WIDTH/2.0,y=GAME_HEIGHT/2.0,
                        width=BALL_DIAMETER, height=BALL_DIAMETER,
                        fillcolor=colormodel.BLUE)
        b=Ball(x=GAME_WIDTH/2.0,y=GAME_HEIGHT/2.0,
                        width=BALL_DIAMETER, height=BALL_DIAMETER,
                        fillcolor=colormodel.BLUE)
        c=Ball(x=GAME_WIDTH/2.0,y=GAME_HEIGHT/2.0,
                        width=BALL_DIAMETER, height=BALL_DIAMETER,
                        fillcolor=colormodel.BLUE)
        self._lives=[a,b,c]
        self._coll=0
    # UPDATE METHODS TO MOVE PADDLE, SERVE AND MOVE THE BALL
    
    def updatePaddle(self,input):
        """Moves Paddle
        
        Parameter: input is a arrow key pressed
        Precondtion: arrow is a GInput
        """
        ds=0
        if input.is_key_down('left'):
            ds-=4.0
        elif input.is_key_down('right'):
            ds+=4.0
        
        if ds<0:
            self._paddle.x=max(self._paddle.x+ds,PADDLE_WIDTH/2.0)
        elif ds>0:
            self._paddle.x=min(self._paddle.x+ds,GAME_WIDTH-PADDLE_WIDTH/2.0)
    
    def serveBall(self):
        """Makes the ball and serves it, it is
        a initializer for the attribute _ball then cuts the _tries by one
        """    
        self._ball=self._lives.pop(0)
        self._tries=self._tries-1
    
    # DRAW METHOD TO DRAW THE PADDLES, BALL, AND BRICKS
    def draw(self, view):
        """Draws paddles and bricks to the given Window(view)
        
        Parameter: view is window
        Precondition: view is a GView
        """
        for x in self._bricks:
            x.draw(view)
        self._paddle.draw(view)
        
    def drawball(self,view):
        """ Draw ball to the given Window(view)
        
        parameter: view is window
        Precondition: view is a Gview
        """
        if self._paddle.colpaddle(self._ball):
            self.Change_color()
        self._ball.draw(view)
        
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION
    def updateball(self):
        """This method moves, bounces and sets the velocity of the ball accordingly"""
        self._ball.Bounceball()
        self._ball.moveball()
        if self._paddle.colpaddle(self._ball):
            self.bounce_Sound().play()  
            if self._paddle.colLeft(self._ball):
                self._ball.setVy()
                self._ball.setVx()
            elif self._paddle.colRight(self._ball):
                self._ball.setVy()
                self._ball.setVx()
            else:
                self._ball.setVy()
        self.deletebrick()
        
    # ADD ANY ADDITIONAL METHODS (FULLY SPECIFIED) HERE
    def deletebrick(self):
        """Delete a certain brick when it gets hit by a ball
        and set a vertical speed to opposite direction
        """
        
        for x in self._bricks:
            if x.colbrick(self._ball):
                self._bricks.remove(x)
                self._ball.setVy()
                self.break_Sound().play()
                
                
    
    def break_Sound(self):
        """This method randomly generates sound and returns
        that sound
        """
        a1=Sound('cup1.wav')
        a2=Sound('plate1.wav')
        a3=Sound('plate2.wav')
        a4=Sound('saucer1.wav')
        a5=Sound('saucer2.wav')
        s=[a1,a2,a3,a4,a5]
        
        return random.choice(s)
    
    def Change_color(self):
        """This changes the ball color"""
        c1 = colormodel.BLACK
        c2 = colormodel.YELLOW
        c3 = colormodel.BLUE
        c4 = colormodel.GREEN
        c5 = colormodel.RED
        c6 = colormodel.CYAN
        cs = [c1,c2,c3,c4,c5,c6]
        self._ball.fillcolor=(random.choice(cs))
    
    def bounce_Sound(self):
        """This constructs a Sound object that makes the sound when
        the ball hits the paddle"""
        return Sound('bounce.wav')
    
    def countCollision(self):
        """This method counts the number of collision using _coll
        and boosts the speed accordingly as _coll increases"""
        if self._paddle.colpaddle(self._ball):
            self._coll=self._coll+1
        if self._coll==7:
            self._ball.Booster()
            self._coll=self._coll+1
        if self._coll==20:
            self._ball.Booster()
            self._coll=self._coll+1
        if self._coll==40:
            self._ball.Booster()
            self._coll=self._coll+1
      

        
    
        
        
        
        
    
    

    
            
        
        
        
        
        