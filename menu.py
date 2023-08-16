import pygame
from images import *
from buttons import *

class Menu(pygame.Surface):
    def __init__(
            self,
            position: tuple,
            titleImagePath: FilePath,
            titleSize: tuple,
            titleText: str,
            titleTextColor: tuple,
            titleTextFont: pygame.font.Font,
            titleTextPosition: tuple,

            buttonPanelImagePath: FilePath,
            buttonCount: int,
            buttonSize: tuple,
            buttonColor: tuple,
            buttonSelectedColor,
            buttonTexts : tuple,
            buttonTextColor: tuple,
            buttonSelectedTextColor: tuple,
            buttonsTextPositions: tuple,
            buttonTextFont: pygame.font.Font
            ) -> None:
        

        space = 20 # space between objects
        buttonAdditionalSize = 15
        self.position = Vector2(position)
        
        #-# Title #-#
        self.title = Image(titleImagePath, (0, 0), self.position, titleSize)
        self.titleText = titleTextFont.render(titleText, False, titleTextColor)
        self.title.blit(self.titleText, titleTextPosition)

        #-# Button Panel #-#
        self.buttonPanelSize = [buttonSize[0] + space * 2, buttonSize[1]*buttonCount + (buttonCount + 3)*space]
        self.buttonPanelPosition = 0, titleSize[1] - space/2
        self.buttonPanel = Image(buttonPanelImagePath, self.buttonPanelPosition, None, self.buttonPanelSize)
        
        #-# Buttons #-#
        buttonSelectedSize = buttonSize[0], buttonSize[1] + buttonAdditionalSize
        self.buttons = []
        for i in range(buttonCount):
            buttonPosition = Vector2(space, space*(i+3/2) + buttonSize[1]*i)
            buttonScreenPosition = buttonPosition + self.buttonPanelPosition + self.position
            
            self.buttons.append(Button(buttonColor, buttonSelectedColor, buttonTexts[i], buttonTexts[i], buttonTextColor, buttonSelectedTextColor
                                , buttonsTextPositions[i], (buttonsTextPositions[i][0], buttonsTextPositions[i][1] + buttonAdditionalSize / 2)
                                , buttonTextFont, buttonPosition, buttonScreenPosition, buttonSize, buttonSelectedSize))

        self.size = self.buttonPanelSize[0], self.buttonPanelSize[1] + titleSize[1] - space/2
        super().__init__(self.size, pygame.SRCALPHA)


    def Draw(self, surface: pygame.Surface):

        self.title.Draw(self)
        self.buttonPanel.ReblitImage()

        for button in self.buttons:
            button.Draw(self.buttonPanel)

        self.buttonPanel.Draw(self)

        surface.blit(self, self.position)