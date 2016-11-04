#!/usr/bin/env python

import pygame
import pygame.locals

class Game:
    def __init__(self, name, width, height, frames_per_second):
        self.width = width
        self.height = height
        self.frames_per_second = frames_per_second
        self.on = True

        self.screen = pygame.display.set_mode(
                # set the size
                (width, height),

                # use double-buffering for smooth animation
                pygame.locals.DOUBLEBUF |

                # apply alpha blending
                pygame.locals.SRCALPHA)

        # set the title of the window
        pygame.display.set_caption(name)

    def game_logic(self, keys, newkeys, buttons, newbuttons, mouse_position):
        raise NotImplementedError()

    def paint(self, surface):
        raise NotImplementedError()

    def main_loop(self):
        clock = pygame.time.Clock()
        keys = set()
        buttons = set()
        mouse_position = (1,1)

        while True:
            clock.tick(self.frames_per_second)

            newkeys = set()
            newbuttons = set()
            for e in pygame.event.get():
                # did the user try to close the window?
                if e.type == pygame.QUIT:
                    pygame.quit()
                    return

                # did the user just press the escape key?
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

                # track which mouse buttons are currently pressed
                if e.type == pygame.MOUSEBUTTONDOWN:
                    buttons.add(e.button)
                    newbuttons.add(e.button)
                    mouse_position = e.pos

                if e.type == pygame.MOUSEBUTTONUP:
                    buttons.discard(e.button)
                    mouse_position = e.pos

                if e.type == pygame.MOUSEMOTION:
                    mouse_position = e.pos
                
                # track which keys are currently set
                if e.type == pygame.KEYDOWN:
                    keys.add(e.key)
                    newkeys.add(e.key)
                if e.type == pygame.KEYUP:
                    keys.discard(e.key)

            if self.on:
                self.game_logic(keys, newkeys, buttons, newbuttons, mouse_position)
                self.paint(self.screen)

            pygame.display.flip()

STATE_1   = 1
STATE_2   = 2
STATE_3   = 3
STATE_QUIT  = 4

ACTION_SHOW_1   = 10
ACTION_SHOW_2   = 11
ACTION_SHOW_3   = 12
ACTION_QUIT     = 13

def createButton(x, y, w, h, text, action):
    button = [ x, y, w, h, text, action ]
    return button

def createButtons(width, height):
    button_1    = createButton( 10, 420, 130, 60, "Show 1", ACTION_SHOW_1)
    button_2    = createButton(160, 420, 130, 60, "Show 2", ACTION_SHOW_2)
    button_3    = createButton(310, 420, 130, 60, "Show 3", ACTION_SHOW_3)
    button_quit = createButton(460, 420, 130, 60, "Quit",   ACTION_QUIT)
    buttons = [ button_1, button_2, button_3, button_quit ]
    return buttons

def processClick(data, click_x, click_y):
    for b in getButtons(data):
        x, y, w, h, text, baction = b
        if(click_x >= x and click_x <= x + w and
           click_y >= y and click_y <= y + h):
            applyAction(data, baction)
    return

def applyAction(data, action):
    if action == ACTION_SHOW_1:
        setState(data, STATE_1)
    elif action == ACTION_SHOW_2:
        setState(data, STATE_2)
    elif action == ACTION_SHOW_3:
        setState(data, STATE_3)
    elif action == ACTION_QUIT:
        setState(data, STATE_QUIT)
    return

def getState(data):
    return data[0]

def setState(data, state):
    data[0] = state
    return

def getButtons(data):
    return data[1]

def createData(width, height):
    buttons = createButtons(width, height)
    
    data = []
    data.append( STATE_1 )
    data.append( buttons )
    return data
#
# Websites that might be useful
# http://pygame.org/download.shtml
# http://www.pygame.org/docs/ref/draw.html
# http://www.colorpicker.com/
#

import pygame
import math
import random

BACKGROUND_COLOR        = (  0,   0,   0)
TEXT_COLOR              = (255, 255, 255)
BUTTON_OUTLINE_COLOR    = (255, 255,   0)
BUTTON_BACKGROUND_COLOR = (  0,   0,   0)
COLOR1                  = (200,   0,   0)
COLOR2                  = ( 95, 170, 217)
COLOR3                  = (115, 190, 237)

def clearBackground(surface, width, height):
    rect = pygame.Rect(0, 0, width, height)
    surface.fill( BACKGROUND_COLOR, rect)
    return

def drawButton(surface, font, button, state):
    x, y, w, h, text, baction = button
    outline = pygame.Rect(x, y, w, h)
    pygame.draw.rect(surface, BUTTON_OUTLINE_COLOR, outline, 1)
    drawTextCenter(surface, text, x + w/2, y + h/2, font, TEXT_COLOR)
    return

#
# accomplish:
# polygon
#

def drawPicture1(surface, width, height, font):
    text = "Welcome to Code Camp!"
    drawTextCenter(surface, text, width/2, height/2, font, TEXT_COLOR)

    # pygame.draw.circle(surface, COLOR1, (250, 250), 50)

    # points = [ (400, 400), (450, 400), (400, 450) ]
    # pygame.draw.polygon(surface, COLOR1, points)
    
    return

def drawPicture2(surface, width, height, font):
    text = "The Rookie Kit will be released soon."
    drawTextCenter(surface, text, width/2, height/2, font, TEXT_COLOR)
    
    # rectangle = pygame.Rect(200, 100, 50, 75)
    # pygame.draw.rect(surface, COLOR2, rectangle, 1)
    
    # rectangle = pygame.Rect(300, 200, 50, 75)
    # pygame.draw.rect(surface, COLOR2, rectangle)
    
    return

def drawPicture3(surface, width, height, font):
    text = "Checkin begins at 7:00 am, coding starts at 8:00."
    drawTextCenter(surface, text, width/2, height/2, font, TEXT_COLOR)

    # pygame.draw.line(surface, COLOR3, (50, 75), (100, 150))
    return

def drawWindow(surface, width, height, font, data):
    
    clearBackground(surface, width, height)
    
    state = getState(data)
    if state == STATE_1:
        drawPicture1(surface, width, height, font)
    elif state == STATE_2:
        drawPicture2(surface, width, height, font)
    elif state == STATE_3:
        drawPicture3(surface, width, height, font)
    else:
        # draw nothing
        pass
    
    buttons = getButtons(data)
    for b in buttons:
        drawButton(surface, font, b, state)
        
    return

# Draws text left justified at "x".
# The bottom of the text is displayed at "y".
def drawTextLeft(surface, text, x, y, font, color):
    text_object  = font.render(text, False, color)
    text_rect    = text_object.get_rect()
    text_rect.bottomleft = (x, y)
    surface.blit(text_object, text_rect)
    return
    
# Draws text right justified at "x".
# The bottom of the text is displayed at "y".
def drawTextRight(surface, text, x, y, font, color):
    text_object = font.render(text, False, color)
    text_rect = text_object.get_rect()
    text_rect.bottomright = (x, y)
    surface.blit(text_object, text_rect)
    return

# Draws text centered at "x".
# The middle of the text is displayed at "y".
def drawTextCenter(surface, text, x, y, font, color):
    text_object = font.render(text, False, color)
    text_rect = text_object.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_object, text_rect)
    return
#
# Draw several pictures
# Use a mouse clickable button for selection
#

import pygame
import math

class PygameStarter(Game):

    def __init__(self, width, height):

        Game.__init__(self, "Pygame Check",
                      width,
                      height,
                      10)
        
        self.font_height = 12
        self.font = pygame.font.SysFont("Courier New", self.font_height)
        self.data = createData(self.width, self.height)
        return
        
        
    def game_logic(self, keys, newkeys, buttons, newbuttons, mouse_position):
        x = mouse_position[0]
        y = mouse_position[1]

        if 1 in newbuttons:
            processClick(self.data, x, y)

        state = getState(self.data)
        if state == STATE_QUIT:
            e = pygame.event.Event(pygame.QUIT, {})
            pygame.event.post(e)
            
        return
    
    def paint(self, surface):
        drawWindow(surface, self.width, self.height, self.font, self.data)
        return

def main():
    pygame.font.init()
    game = PygameStarter(600, 500)
    game.main_loop()
    
if __name__ == "__main__":
    main()
