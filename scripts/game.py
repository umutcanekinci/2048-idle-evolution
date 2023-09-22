#-# Import Packages #-#
import pygame
from random import choice

from scripts.default.application import *
from scripts.default.menu_button import *
from scripts.default.color import *
from scripts.default.object import *
from scripts.default.path import *
from scripts.default.text import *
from scripts.building import *
from scripts.cloud import *
from scripts.menu import *
from scripts.tile import *

#-# Game Class #-#
class Game(Application):

	def __init__(self) -> None:

		#-# Window Settings #-#
		super().__init__("2048 Game", (1440, 900), None, 165)

		#-# Game Settings #-#
		self.cursorSize = 25, 25
		self.gameBackgorundColor = CustomBlue
		self.menuBackgroundColor = Yellow
		self.cloudCount = 10
		self.rowCount = self.columnCount = 2
		self.maxRowCount, self.maxColumnCount = 7, 7
		self.maxBuildingLevel = 6
		self.money = 10000
		self.isInfoPanelOpen = False
		self.infoMode = False

		#-# Costs #-#
		self.buildCost = lambda age: (age+1)*100
		self.ageCost = lambda age: (age+1)*1000
		self.expandCost = lambda x: (x+1)*100

		#region Paths

		#-# Font Paths #-#
		self.fontPath = FontPath("kenvector_future")
		self.fontPathThin = FontPath("kenvector_future_thin")

		#-# Sound Paths #-#
		self.clickSoundPath = SoundPath("click")
		self.goBackSoundPath = SoundPath("back")

		#endregion
		
		#-# Start The Application #-#
		self.SetCursorVisible(False)
		self.SetCursorImage(Object((0, 0), self.cursorSize, {"Normal" : ImagePath("cursor")}))
		self.SetFonts()

		#-# Main Menu #-# 
		self.menuWidth, self.menuHeight = (440, 315)
		menuPosition = (self.width - self.menuWidth) / 2, (self.height - self.menuHeight) / 2
		self.mainMenu = Menu(menuPosition, ImagePath("blue_button03", "gui"), (440, 70), self.title, White, self.buttonFont, (118, 15), ImagePath("grey_panel", "gui"), 3, (400, 60), "blue", "yellow", ["Start", "Settings", "Exit"], 30, Gray, White, self.fontPath)
		
		#-# Settings Menu #-#
		self.menuWidth, self.menuHeight = (440, 315)
		menuPosition = (self.width - self.menuWidth) / 2, (self.height - self.menuHeight) / 2
		self.settingsMenu = Menu(menuPosition, ImagePath("blue_button03", "gui"), (440, 70), "Settings", White, self.buttonFont, (128, 15), ImagePath("grey_panel", "gui"), 0, (400, 60), "blue", "yellow", [], 30, Gray, White, self.fontPath)

		#-# Game #-#
		self.buildings = Buildings()
		self.tiles = Tiles([self.rowCount, self.columnCount], [self.maxRowCount, self.maxColumnCount])

		self.gamePanelSize = self.gamePanelWidth, self.gamePanelHeight = (1400, 100)
		self.gamePanelPosition = self.gamePanelX, self.gamePanelY = (20, self.height - self.gamePanelHeight - 20)
		
		#region #-# Adding Objects #-#

		self.AddObject("menu", "main menu", self.mainMenu)
		self.AddObject("menu", "cloud animation", CloudAnimation(self.size))
		self.AddObject("settings", "settings menu", self.settingsMenu)
		self.AddObject("settings", "cloud animation", CloudAnimation(self.size))
		self.AddObject("game", "clouds", GameClouds(self.cloudCount, self.size))
		self.AddObject("game", "game panel", Object(self.gamePanelPosition, self.gamePanelSize, {"Normal" : ImagePath("grey_panel", "gui")}))
		self.AddObject("game", "info mode button", Button((100, 800), (60, 60),  {"On" : ImagePath("green", "gui"), "Off" : ImagePath("red", "gui")}))
		self.AddObject("game", "info mode button image", Object((105, 805), (50, 50), {"Normal" : ImagePath("info", "gui")}))
		self.AddObject("game", "expand button", Button((320, 800), (200, 60), {"Normal" : ImagePath("green", "gui"), "Mouse Over" : ImagePath("red", "gui")}, "EXPAND", str(self.expandCost(self.tiles.rowCount)) + "$", 27, textFontPath=self.fontPath))
		self.AddObject("game", "build button", Button((620, 800), (200, 60), {"Normal" : ImagePath("green", "gui"), "Mouse Over" : ImagePath("red", "gui")}, "BUILD", str(self.buildCost(0)) + "$", 27, textFontPath=self.fontPath))
		self.AddObject("game", "next age button", Button((920, 800), (200, 60), {"Normal" : ImagePath("green", "gui"), "Mouse Over" : ImagePath("red", "gui")}, "NEXT AGE", str(self.ageCost(0)) + "$", 27, textFontPath=self.fontPath))
		self.AddObject("game", "money text", Text((1180, 810), "", 55, color=Green, backgorundColor=Black, isCentered=False))
		self.AddObject("game", "tiles", self.tiles)
		self.AddObject("game", "buildings", self.buildings)
		self.AddObject("game", "cloud animation", CloudAnimation(self.size))
		
		#endregion
		
		self.objects["game"]["info mode button"].SetStatus("Off")

		self.SetAge(0)

	def SetFonts(self) -> None:

		self.buttonFont = pygame.font.Font(self.fontPath, 30)
		self.infoPanelTextFont = pygame.font.Font(self.fontPathThin, 15)
		self.infoPanelButtonFont = pygame.font.Font(self.fontPathThin, 24)

	def Run(self) -> None:

		#-# Open first tab #-#
		self.OpenTab("menu")

		super().Run()

	def ControlSelectingTile(self) -> None:

		isThereAnySelectedTile = self.tiles.isThereSelectedTile()

		for row in self.tiles:

			for tile in row:
				
				isMouseOver = tile.isMouseOver(self.mousePosition)

				if isMouseOver:

					if not isThereAnySelectedTile:
						
						tile.selected = True
						
						if self.infoMode:
							tile.rect = tile.selectedRect
						
				else:

					tile.selected = False
					tile.rect = tile.unselectedRect

	def Expand(self) -> None:
		
		if self.money >= self.expandCost(self.tiles.rowCount):

			self.money -= self.expandCost(self.tiles.rowCount)
			self.tiles.Expand()

			self.objects[self.tab]["expand button"].text.Update("Mouse Over", str(self.expandCost(self.tiles.rowCount)) + "$")
	
	def SetAge(self, ageNumber) -> None:
			
		self.buildings.SetAge(ageNumber)
		
		self.objects["game"]["build button"].text.Update("Mouse Over", str(self.buildCost(ageNumber)) + "$")
		self.objects["game"]["next age button"].text.Update("Mouse Over", str(self.ageCost(ageNumber)) + "$")

	def NextAge(self) -> None:

		if self.buildings.ageNumber + 1 < len(ages) and self.money >= self.ageCost(self.buildings.ageNumber):
			
			self.SetAge(self.buildings.ageNumber + 1)
			self.money -= self.ageCost(self.buildings.ageNumber)

	def HandleExitEvents(self, event) -> None:
		
		#-# Quit when trying to close window #-#
		if event.type == pygame.QUIT:

			self.Exit()

		#-# Go back if escape button pressed #-#
		elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
				
			self.PlaySound(self.goBackSoundPath)

			if self.tab == "menu":

				self.Exit()

			elif self.tab == "settings":

				self.OpenTab("menu")

			elif self.tab == "game":

				if self.isInfoPanelOpen:

					self.isInfoPanelOpen = False

				else:

					self.OpenTab("menu")

	def HandleEvents(self, event) -> None:

		super().HandleEvents(event)

		if self.tab == "menu":
			
			#-# Control click button events with space button #-#
			if event.type == pygame.KEYUP:

				if event.key == pygame.K_SPACE:

					if self.mainMenu.buttons[0].status == "Selected":

						self.PlaySound(self.clickSoundPath)
						self.OpenTab("game")

					elif self.mainMenu.buttons[1].status == "Selected":

						self.PlaySound(self.clickSoundPath)
						self.OpenTab("settings")

					elif self.mainMenu.buttons[2].status == "Selected":

						self.PlaySound(self.clickSoundPath)
						self.Exit()

			#-# Control click button events with mouse #-#
			elif event.type == pygame.MOUSEBUTTONUP:
				
				if self.mainMenu.buttons[0].isMouseOver(self.mousePosition):

					self.PlaySound(self.clickSoundPath)
					self.OpenTab("game")

				elif self.mainMenu.buttons[1].isMouseOver(self.mousePosition):

					self.PlaySound(self.clickSoundPath)
					self.OpenTab("settings")

				elif self.mainMenu.buttons[2].isMouseOver(self.mousePosition):
					self.PlaySound(self.goBackSoundPath)
					self.Exit()

		elif self.tab == "game":

			if event.type == pygame.MOUSEMOTION:
					
				if self.isInfoPanelOpen:

					#-# Select info panel buttons if mouse over #-#
					self.infoPanelSellButton.selected = self.infoPanelSellButton.isMouseOver(self.mousePosition)
					self.closeInfoButtonCross.selected = self.closeInfoButton.selected = self.closeInfoButton.isMouseOver(self.mousePosition)

				else:
				
					#-# Select tile if mouse over it #-#
					self.ControlSelectingTile()

			elif event.type == pygame.MOUSEBUTTONUP:

				if self.isInfoPanelOpen:
				
					#-# sell building #-#
					if self.infoPanelSellButton.selected:
						
						self.buildings.remove(self.infoBuilding)
						self.money += self.infoBuilding.sellPrice
						self.isInfoPanelOpen = False
						self.PlaySound(self.goBackSoundPath)
					
					#-# close info panel #-#
					elif self.closeInfoButton.selected:

						self.isInfoPanelOpen = False
						self.PlaySound(self.goBackSoundPath)
				
				else:

					#-# On/off info mode with clicking info mode button #-#
					if self.objects[self.tab]["info mode button"].isMouseOver(self.mousePosition):
						
						self.infoMode = not self.infoMode
						
						if self.infoMode:

							self.objects[self.tab]["info mode button"].SetStatus("On")

						else:

							self.objects[self.tab]["info mode button"].SetStatus("Off")
						
						self.PlaySound(self.clickSoundPath)

					#-# Open building info if tile is clicked #-#
					if self.infoMode:

						for row in self.tiles:

							for tile in row:

								if tile.selected:

									for building in self.buildings:

										if building.tile == tile:

											self.OpenBuildingInfo(building)
											self.PlaySound(self.clickSoundPath)

											break
									break

					#-# expand #-#
					elif self.objects[self.tab]["expand button"].isMouseOver(self.mousePosition):

						self.PlaySound(self.clickSoundPath)
						self.Expand()

					#-# Create building if build button clicked #-#
					elif self.objects[self.tab]["build button"].isMouseOver(self.mousePosition):

						self.PlaySound(self.clickSoundPath)
						self.CreateBuilding()

					#-# Go next age #-#
					elif self.objects[self.tab]["next age button"].isMouseOver(self.mousePosition):

						self.PlaySound(self.clickSoundPath)
						self.NextAge()

			elif event.type == pygame.KEYUP:

				#-# Create/Move buildings with keys #-#
				if not self.isInfoPanelOpen:

					if event.key == pygame.K_SPACE and not self.infoMode:
						
						self.PlaySound(self.clickSoundPath)
						self.CreateBuilding()
					
					elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					
						self.MoveBuildings("right")
					
					elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
					
						self.MoveBuildings("left")
					
					elif event.key == pygame.K_UP or event.key == pygame.K_w:
					
						self.MoveBuildings("up")
					
					elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
					
						self.MoveBuildings("down")

	def OpenBuildingInfo(self, building: Building) -> None:

		self.closeInfoButton = MenuButton("red_circle", ((self.width - 250)/2 + 250 - 20, (self.height - 400)/2 - 12), selectedColor="yellow_circle")
		self.closeInfoButtonCross = MenuButton("grey_crossWhite", (9, 9), ((self.width - 250)/2 + 250 - 20 + 9, (self.height - 400)/2 - 12 + 9), "grey_crossGrey")
		
		self.infoBuilding = building

		self.infoPanel = Object(((self.width - 250)/2, (self.height - 400)/2), (250, 400), {"Normal" : ImagePath("grey_panel", "gui")})

		self.infoPanelTopSide = pygame.Surface((250, 300), pygame.SRCALPHA)

		buildingImage = Object((20, 20), (65, 89), {"Normal" : building.GetImagePath()})
		levelText = self.infoPanelTextFont.render("Level: " + str(building.level), True, Gray)
		speedText = self.infoPanelTextFont.render("Speed: " + str(building.speed) + " $/sec", True, Gray)
		cooldownText = self.infoPanelTextFont.render("Cooldown: " + str(building.cooldown) + " sec", True, Gray)
		sellPriceText = self.infoPanelTextFont.render("Sell Price: " + str(building.sellPrice), True, Gray)
		
		self.infoPanelTopSide.blit(levelText, (90, 35))
		self.infoPanelTopSide.blit(speedText, (90, 50))
		self.infoPanelTopSide.blit(cooldownText, (90, 65))
		self.infoPanelTopSide.blit(sellPriceText, (90, 80))
		buildingImage.Draw(self.infoPanelTopSide)

		self.infoPanelSellButton = MenuButton("red", (20, 325), ((self.width - 250)/2 + 20, (self.height - 400)/2 + 325), "yellow", "SELL", "+" + str(building.sellPrice) + "$", White, Gray, None, None, (75, 10), (73, 15), 35, self.fontPath, (210, 50), (210, 60))
		self.infoPanelSellButton = Button(((self.width - 250)/2 + 20, (self.height - 400)/2 + 325), (210, 50), {"Normal" : ImagePath("green", "gui"), "Mouse Over" : ImagePath("red", "gui")}, "SELL", str(building.sellPrice) + "$", 25)
		self.isInfoPanelOpen = True

		#self.infoPanel.ReblitImage()
		self.infoPanel.surfaces["Normal"].blit(self.infoPanelTopSide, (0, 0))
		self.AddObject("game", "info panel sell button", self.infoPanelSellButton)

		self.infoPanel.Draw(self.window)
		self.AddObject("game", "info panel", self.infoPanel)

		#self.closeInfoButtonCross.Draw(self.closeInfoButton.surfaces["Normal"])
		#self.closeInfoButtonCross.Draw(self.closeInfoButton.surfaces["Normal"])

		self.closeInfoButton.Draw(self.window)
		self.AddObject("game", "close info button", self.closeInfoButton)

	def MoveBuildings(self, rotation: str) -> None:

		isBuildingsMoving = False

		for building in self.buildings:
			if not building.velocity == Vector2(0, 0):
				isBuildingsMoving = True
				break

		if not self.infoMode and not isBuildingsMoving:

			if rotation == "up" or rotation == "down":
                
				for columnNumber in range(self.tiles.columnCount):
					
					buildingCountInThisColumn = 0
					buildingsInThisColumn = []

					for building in self.buildings:
						if building.tile.columnNumber == columnNumber + 1:
							buildingCountInThisColumn += 1
							buildingsInThisColumn.append(building)
			
					if buildingCountInThisColumn > 0:

						if rotation == "up":

							buildingsInThisColumn.sort(key=lambda building: building.tile.rowNumber)
							
							previousBuilding = None
							targetRow = 0
							for building in buildingsInThisColumn:

								if not previousBuilding:
									if not building.tile.rowNumber == targetRow + 1:
										building.SetTargetTile(self.tiles[targetRow][columnNumber])
									previousBuilding = building
									targetRow += 1
								elif previousBuilding.level == building.level and self.maxBuildingLevel > building.level:
									previousBuilding.LevelUp(building)
									previousBuilding = None
								else:
									if not building.tile.rowNumber == targetRow + 1:
										building.SetTargetTile(self.tiles[targetRow][columnNumber])
									previousBuilding = building
									targetRow += 1

						else:

							buildingsInThisColumn.sort(key=lambda building: building.tile.rowNumber, reverse=True)
							
							previousBuilding = None
							targetRow = 0
							for building in buildingsInThisColumn:

								if not previousBuilding:
									if not building.tile.rowNumber == self.tiles.rowCount - targetRow:
										building.SetTargetTile(self.tiles[self.tiles.rowCount - targetRow - 1][columnNumber])
									previousBuilding = building
									targetRow += 1
								elif previousBuilding.level == building.level and self.maxBuildingLevel > building.level:
									previousBuilding.LevelUp(building)
									previousBuilding = None
								else:
									if not building.tile.rowNumber == self.tiles.rowCount - targetRow:
										building.SetTargetTile(self.tiles[self.tiles.rowCount - targetRow - 1][columnNumber])
									previousBuilding = building
									targetRow += 1

			elif rotation == "right" or rotation == "left":

				for rowNumber in range(self.tiles.rowCount):
					
					buildingCountInThisRow = 0
					buildingsInThisRow = []

					for building in self.buildings:
						if building.tile.rowNumber == rowNumber + 1:
							buildingCountInThisRow += 1
							buildingsInThisRow.append(building)
				
					if  buildingCountInThisRow > 0:

						if rotation == "left":

							buildingsInThisRow.sort(key=lambda building: building.tile.columnNumber)

							previousBuilding = None
							targetColumn = 0
							for building in buildingsInThisRow:
								
								if not previousBuilding:
									if not building.tile.columnNumber == targetColumn + 1:
										building.SetTargetTile(self.tiles[rowNumber][targetColumn])
									previousBuilding = building
									targetColumn += 1
								elif previousBuilding.level == building.level and self.maxBuildingLevel > building.level:
									previousBuilding.LevelUp(building)
									previousBuilding = None
								else:
									if not building.tile.columnNumber == targetColumn + 1:
										building.SetTargetTile(self.tiles[rowNumber][targetColumn])
									previousBuilding = building
									targetColumn += 1

						else:

							buildingsInThisRow.sort(key=lambda building: building.tile.columnNumber, reverse=True)

							previousBuilding =  None
							targetColumn = 0
							for building in buildingsInThisRow:

								if not previousBuilding:
									if not building.tile.columnNumber == self.tiles.columnCount - targetColumn:
										building.SetTargetTile(self.tiles[rowNumber][self.tiles.columnCount - targetColumn - 1])
									previousBuilding = building
									targetColumn += 1
								elif previousBuilding.level == building.level and self.maxBuildingLevel > building.level:
									previousBuilding.LevelUp(building)
									previousBuilding = None
								else:
									if not building.tile.columnNumber == self.tiles.columnCount - targetColumn:
										building.SetTargetTile(self.tiles[rowNumber][self.tiles.columnCount - targetColumn - 1])
									previousBuilding = building
									targetColumn += 1

			self.buildings.sort(key=lambda building: building.tile.columnNumber)

	def CreateBuilding(self) -> None:

		isBuildingsMoving = False

		for building in self.buildings:
			if not building.velocity == Vector2(0, 0):
				isBuildingsMoving = True
				break

		if not isBuildingsMoving and self.money >= self.buildCost(self.buildings.ageNumber): #and not self.infoMode

			try:
				
				emptyTiles = []
				
				for rowNumber in range(self.tiles.rowCount):
					for columnNumber in range(self.tiles.columnCount):
						emptyTiles.append((rowNumber + 1, columnNumber + 1))


				for building in self.buildings:
					emptyTiles.remove((building.tile.rowNumber, building.tile.columnNumber))


				if len(emptyTiles) > 0:
					
					rowNumber, columnNumber = choice(emptyTiles)

					newBuilding = Building(1, self.buildings.ageNumber, self.tiles[rowNumber - 1][columnNumber - 1])
					self.buildings.append(newBuilding)
					self.buildings.sort(key=lambda building: building.tile.columnNumber)
					self.money -= self.buildCost(self.buildings.ageNumber)
					
				else:
					pass # not enough space error

			except NameError as error:

				print("You need to create tiles before creating new building! lol")
	
	def OpenTab(self, tab: str) -> None:

		super().OpenTab(tab)
	
		if tab == "menu":

			self.SetBackgorundColor(self.menuBackgroundColor)

		elif tab == "settings":

			self.SetBackgorundColor(self.menuBackgroundColor)

		elif tab == "game":

			self.SetBackgorundColor(self.gameBackgorundColor)

		if self.tab in self.objects:
			
			if "cloud animation" in self.objects[self.tab]:

				self.objects[self.tab]["cloud animation"].CreateClouds()

	def UpdateMoney(self) -> None:

		time = pygame.time.get_ticks()

		for building in self.buildings:
			
			if not building.lastTime: building.lastTime = time
			
			if time - building.lastTime > (building.cooldown)*1000:
				
				self.money += building.cooldown*building.speed
				building.lastTime = pygame.time.get_ticks()

		#-# Money Text #-#
		self.objects[self.tab]["money text"].Update("Normal", str(self.money) + "$")

	def Draw(self) -> None:
		
		if self.tab == "game":

			self.UpdateMoney()

		super().Draw()
