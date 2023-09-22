#-# Import Packages #-#
import pygame
from images import *
from scripts.default.menu_button import *
from scripts.default.application import Application

#-# Menu Class #-#
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
            buttonTextSize,
            buttonTextColor: tuple,
            buttonSelectedTextColor: tuple,
            buttonTextFontName: str
            ) -> None:
        

        space = 20 # space between objects
        buttonAdditionalSize = 15

        self.position = pygame.math.Vector2(position)
        
        #-# Sound Paths #-#
        self.switchUpSoundPath = SoundPath("switchUp")
        self.switchDownSoundPath = SoundPath("switchDown")

        #-# Title #-#
        self.title = Object((0, 0), titleSize, {"Normal" : titleImagePath}, screenPosition=self.position)
        self.titleText = titleTextFont.render(titleText, False, titleTextColor)
        self.title.surfaces["Normal"].blit(self.titleText, titleTextPosition)

        #-# Button Panel #-#
        self.buttonPanelSize = [buttonSize[0] + space * 2, buttonSize[1]*buttonCount + (buttonCount + 3)*space]
        self.buttonPanelPosition = 0, titleSize[1] - space/2
        self.buttonPanel = Object(self.buttonPanelPosition, self.buttonPanelSize, {"Normal" : buttonPanelImagePath})
        
        #-# Buttons #-#
        buttonSelectedSize = buttonSize[0], buttonSize[1] + buttonAdditionalSize
        self.buttons = []

        for i in range(buttonCount):

            buttonPosition = pygame.math.Vector2(space, space*(i+3/2) + buttonSize[1]*i)
            buttonScreenPosition = buttonPosition + self.buttonPanelPosition + self.position
            
            self.buttons.append(MenuButton(buttonColor, buttonPosition, buttonScreenPosition, buttonSelectedColor, buttonTexts[i], buttonTexts[i], buttonTextColor, buttonSelectedTextColor
                                , buttonTextSize, buttonTextFontName, buttonSize, buttonSelectedSize))


            #self.buttons.append(Button(buttonPosition, buttonSize, {"Selected" : ImagePath("blue", "gui"), "Unselected" : ImagePath("yellow", "gui")}, buttonTexts[i], buttonTexts[i], 25))

        if buttonCount > 0:

            self.buttons[0].SetStatus("Selected")

        self.size = self.buttonPanelSize[0], self.buttonPanelSize[1] + titleSize[1] - space/2

        super().__init__(self.size, pygame.SRCALPHA)

    def HandleEvents(self, event, mousePosition) -> None:

        #-# Change the color of buttons if mouse over it #-#
        if event.type == pygame.MOUSEMOTION:

            for i, button in enumerate(self.buttons):

                if button.isMouseOver(mousePosition) and button.status != "Selected":

                    for j, button2 in enumerate(self.buttons):

                        if button2.status == "Selected":
                            
                            if j > i:

                                Application.PlaySound(self.switchDownSoundPath)

                            else:

                                Application.PlaySound(self.switchUpSoundPath)

                            button.SetStatus("Selected")
                            button2.SetStatus("Unselected")

                            break

        #-# Change the selected button with keys #-#
        elif event.type == pygame.KEYUP:
  
            if event.key == pygame.K_w or event.key == pygame.K_UP:

                for i, button in enumerate(self.buttons):
                            
                    if button.status == "Selected" and i != 0:
                        
                        Application.PlaySound(self.switchUpSoundPath)

                        self.buttons[i-1].SetStatus("Selected")
                        button.SetStatus("Unselected")

                        break

            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:

                for i, button in enumerate(self.buttons):
                            
                    if button.status == "Selected" and i != len(self.buttons) - 1:
                        
                        Application.PlaySound(self.switchDownSoundPath)

                        self.buttons[i+1].SetStatus("Selected")
                        button.SetStatus("Unselected")

                        break

    def Draw(self, surface: pygame.Surface) -> None:

        self.title.Draw(self)
        self.buttonPanel = Object(self.buttonPanel.position, self.buttonPanel.size, self.buttonPanel.imagePaths)

        for button in self.buttons:

            button.Draw(self.buttonPanel.surfaces["Normal"])

        self.buttonPanel.Draw(self)

        surface.blit(self, self.position)