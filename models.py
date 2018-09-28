# models.py
# Joon Il Moon jm2239, Kyongtae Min km567
# 12/08/2016
"""Models module for Breakout

This module contains the model classes for the Breakout game. That is anything that you
interact with on the screen is model: the paddle, the ball, and any of the bricks.

Technically, just because something is a model does not mean there has to be a special 
class for it.  Unless you need something special, both paddle and individual bricks could
just be instances of GRectangle.  However, we do need something special: collision 
detection.  That is why we have custom classes.

You are free to add new models to this module.  You may wish to do this when you add
new features to your game.  If you are unsure about whether to make a new class or 
not, please ask on Piazza."""
import random # To randomly generate the ball velocity
from constants import *
from game2d import *


# PRIMARY RULE: Models are not allowed to access anything except the module constants.py.
# If you need extra information from Play, then it should be a parameter in your method, 
# and Play should pass it as a argument when it calls the method.


class Paddle(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball, as well as move it
    left and right.  You may wish to add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    
    # INITIALIZER TO CREATE A NEW PADDLE
    def __init__(self,**keywords):
        """This initializer creates a paddle instance"""
        GRectangle.__init__(self,**keywords)
    # METHODS TO MOVE THE PADDLE AND CHECK FOR COLLISIONS
    def colpaddle(self,ball):
        """Returns: True if the ball collides with this paddle
        
        Adjustment has been made in order to solve the problem when the ball goes to the side
        and it starts to bounce and back and fourth inside the paddle.
        
        Parameter ball: The ball to check
        Precondition: ball is of class ball
        """
        if self.contains(ball.left, ball.bottom) and self.contains(ball.left, ball.bottom + BALL_DIAMETER/3.0):
            return False
        elif self.contains(ball.right, ball.bottom) and self.contains(ball.right, ball.bottom + BALL_DIAMETER/3.0):
            return False
        elif self.contains(ball.left,ball.bottom):
            return True
        elif self.contains(ball.right,ball.bottom):
            return True
        else:
            return False
        
    
       
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    
    def colLeft(self,ball):
        """Returns: True if the ball collides with the first one-fourth part
        of the paddle
        
        Parameter ball: The ball to check
        Precondition: ball is of class ball
        """
        
        
        if (self.left<ball.right<(self.left+0.25*PADDLE_WIDTH)) and self.contains(ball.right,ball.bottom):
           return True
        elif (self.left<(ball.left+ball.right)/2.0<(self.left+0.25*PADDLE_WIDTH)) and self.contains((ball.left+ball.right/2.0),ball.bottom):
       #((self.top-1)<ball.bottom<self.top+1):
            return True
        else:
            return False
        
        
    def colRight(self,ball):
        """Returns: True if the ball collides with the last one-fourth part
        of the paddle
        
        Parameter ball: The ball to check
        Precondition: ball is of class ball
        """
        if ((self.right-0.25*PADDLE_WIDTH)<ball.left<self.right) and self.contains(ball.left,ball.bottom):
            return True
        elif (self.right-0.25*PADDLE_WIDTH)<(ball.right+ball.left)/2.0<self.right and self.contains((ball.left+ball.right)/2.0,ball.bottom):
            return True
        else:
            return False

class Brick(GRectangle):
    """An instance is the game paddle.
    
    This class contains a method to detect collision with the ball.  You may wish to 
    add more features to this class.
    
    The attributes of this class are those inherited from GRectangle.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE A BRICK
    def __init__(self,**keywords):
        """This initializer creates a brick instance"""
        GRectangle.__init__(self,**keywords)
    # METHOD TO CHECK FOR COLLISION
    def colbrick(self,ball):
        """Returns: True if the ball collides with this brick
        
        Parameter ball: The ball to check
        Precondition: ball is of class ball
        """
        if self.contains(ball.left,ball.top):
            return True
        elif self.contains(ball.left,ball.bottom):
            return True
        elif self.contains(ball.right,ball.top):
            return True
        elif self.contains(ball.right,ball.bottom):
            return True
        else:
            return False
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Ball(GEllipse):
    """Instance is a game ball.
    
    We extend GEllipse because a ball must have additional attributes for velocity.
    This class adds this attributes and manages them.
    
    INSTANCE ATTRIBUTES:
        _vx [int or float]: Velocity in x direction 
        _vy [int or float]: Velocity in y direction 
    
    The class Play will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with no
    setters for the velocities.
    
    How? The only time the ball can change velocities is if it hits an obstacle
    (paddle or brick) or if it hits a wall.  Why not just write methods for these
    instead of using setters?  This cuts down on the amount of code in Gameplay.
    
    NOTE: The ball does not have to be a GEllipse. It could be an instance
    of GImage (why?). This change is allowed, but you must modify the class
    header up above.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def setVy(self):
        """set _vy to -self._vy"""
        self._vy=-self._vy
    def setVx(self):
        """set _vx to -self._vx"""
        self._vx=-self._vx
    
    def getBottom(self):
        """Returns: the bottom of the ball"""
        return self.bottom
    
    # INITIALIZER TO SET RANDOM VELOCITY
    def __init__(self,**keywords):
        """This initializer creates a new ball, it is a subclass of GEllipse
        
           :param keywords: dictionary of keyword arguments
        
        This class supports all the same keywords as 'GEllipse',"""
        GEllipse.__init__(self,**keywords)
        self._vx=random.uniform(2.0,3.5)
        self._vx=self._vx * random.choice([-1, 1])
        self._vy=random.uniform(2.0,3.5)
        
    # METHODS TO MOVE AND/OR BOUNCE THE BALL
    def moveball(self):
        """This method moves the ball using the attribut _vx and _vy
        that indicates the ball's velocity"""
        self.y=self.y+self._vy
        self.x=self._vx+self.x
    
    def Bounceball(self):
        """This method bounces the ball when it hits the wall"""
        if self.top >=GAME_HEIGHT:
            self._vy=-self._vy
        elif self.bottom <=0:
            self._vy = -self._vy
        elif self.right>= GAME_WIDTH:
            self._vx=-self._vx
        elif self.left<=0:
            self._vx = -self._vx
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def Booster(self):
        """This doubles the horizontal speed of the ball"""
        self._vy=self._vy*1.5


# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE