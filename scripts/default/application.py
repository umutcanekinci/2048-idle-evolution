#-# Import Packages #-#
import pygame, sys, os
from pygame import mixer

from scripts.default.button import *
from scripts.default.color import *
from scripts.default.text import *
from scripts.default.object import *

#-# Application Class #-#
class Application():
    
    def __init__(self, title: str = "Game", size: tuple = (640, 480), backgroundColor: tuple = None, FPS: int = 60) -> None:
        
        self.InitPygame()
        self.InitClock()
        self.InitMixer()
        self.SetTitle(title)
        self.SetSize(size)
        self.OpenWindow()
        self.SetFPS(FPS)
        self.SetBackgorundColor(backgroundColor)
        self.objects = {}
        self.tab = ""

    def Run(self) -> None:
        
        #-# Starting App #-#
        self.isRunning = True

        #-# Main Loop #-#
        while self.isRunning:

            #-# FPS #-#
            self.clock.tick(self.FPS)

            #-# Getting Mouse Position #-#
            self.mousePosition = pygame.mouse.get_pos()

            #-# Getting Pressed Keys #-#
            self.keys = pygame.key.get_pressed()

            #-# Handling Events #-#
            for event in pygame.event.get():

                self.HandleEvents(event)

            #-# Set Cursor Position #-#
            if hasattr(self, "cursor"):

                self.cursor.SetPosition(self.mousePosition)    
            
            #-# Draw Objects #-#
            self.Draw()

    def HandleEvents(self, event: pygame.event.Event) -> None:

        if self.tab in self.objects:
                        
            for object in self.objects[self.tab].values():
                
                object.HandleEvents(event, self.mousePosition)

        self.HandleExitEvents(event)

    def HandleExitEvents(self, event: pygame.event.Event) -> None:

        if event.type == pygame.QUIT:

            self.Exit()

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:

                self.Exit()

    def InitPygame(self) -> None:
        
        pygame.init()

    def InitMixer(self) -> None:

        pygame.mixer.init()

    def InitClock(self) -> None:

        self.clock = pygame.time.Clock()

    @staticmethod
    def PlaySound(soundPath: SoundPath) -> None:

        mixer.music.load(soundPath)
        mixer.music.play()

    def OpenWindow(self) -> None:

        self.window = pygame.display.set_mode(self.size)

    def CenterWindow(self) -> None:

        os.environ['SDL_VIDEO_CENTERED'] = '1'

    def SetFPS(self, FPS: int) -> None:
        
        self.FPS = FPS

    def SetTitle(self, title: str) -> None:
        
        self.title = title
        pygame.display.set_caption(self.title)

    def SetSize(self, size: tuple) -> None:

        self.size = self.width, self.height = size

    def SetBackgorundColor(self, color: tuple) -> None:

        self.backgroundColor = color

    def CreateObject(self, tab: str, name: str, *args) -> None:
        
        newObject = Object(*args)
        self.AddObject(tab, name, newObject)

    def AddObject(self, tab: str, name: str, object: Object) -> None:
        
        #-# Create Tab If not exist #-#
        self.AddTab(tab)

        self.objects[tab][name] = object

    def CreateButton(self, tab: str, name: str, *args, **kwargs) -> None:
        
        #-# Creat Tab If not exist #-#
        self.AddTab(tab)
        
        #-# Adding button to tab #-#
        newButton = Buttonxx(name, *args, **kwargs)
        self.objects[tab][name] = newButton

    def CreateText(self, tab: str, name: str, position, text, textSize, antialias=True, color=White, backgorundColor=None, fontPath=None, isCentered=False, status="Normal") -> None:
        
        #-# Creat Tab If not exist #-#
        self.AddTab(tab)
        
        #-# Adding button to tab #-#
        newText = Text(position, text, textSize, antialias, color, backgorundColor, fontPath, isCentered, status)
        self.objects[tab][name] = newText

    def AddTab(self, name: str) -> None:

        #-# Creat Tab If not exist #-#
        if not name in self.objects:

            self.objects[name] = {}

    def OpenTab(self, tab: str) -> None:

        self.tab = tab

    def Exit(self) -> None:

        self.isRunning = False
        pygame.quit()
        sys.exit()

    def SetCursorVisible(self, value=True) -> None:

        pygame.mouse.set_visible(value)

    def SetCursorImage(self, image: Object) -> None:

        self.cursor = image

    def Draw(self) -> None:

        #-# Fill Background #-#
        if self.backgroundColor:

            self.window.fill(self.backgroundColor)

        #-# Draw Objects #-#
        if self.tab in self.objects:

            for object in self.objects[self.tab].values():
                    
                object.Draw(self.window)

        #-# Draw Cursor #-#
        if hasattr(self, "cursor"):

            self.cursor.Draw(self.window)    

        pygame.display.update()
