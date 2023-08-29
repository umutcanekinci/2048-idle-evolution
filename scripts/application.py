#-# Import Packages #-#
import pygame

from random import choice
from sys import exit
from pygame import mixer

from scripts.building import *
from scripts.button import *
from scripts.cloud import *
from scripts.color import *
from scripts.image import *
from scripts.menu import *
from scripts.path import *
from scripts.tile import *

#-# Application Class #-#
class Application():

	def __init__(self) -> None:

		#-# Window Settings #-#
		self.windowTitle = "2048 Game"
		self.windowSize = self.windowWidth, self.windowHeight = 1440, 900
		self.cursorSize = 25, 25

		#-# Game Settings #-#
		self.gameBackgorundColor = CustomBlue
		self.menuBackgroundColor = Yellow
		self.cloudCount = 10
		self.rowCount = self.columnCount = 2
		self.maxSize = 7
		self.maxBuildingLevel = 6
		self.startingMoney = 10000
		
		self.buildCost = lambda age: (age+1)*100
		self.ageCost = lambda age: (age+1)*1000
		self.expandCost = lambda x: (x+1)*1000
		 
		#-# FPS #-#
		self.FPS = 165

		#-# Font Paths #-#
		self.fontPath = FontPath("kenvector_future")
		self.fontPathThin = FontPath("kenvector_future_thin")

		#-# Sound Paths #-#
		self.switchUpSoundPath = SoundPath("switchUp")
		self.switchDownSoundPath = SoundPath("switchDown")
		self.clickSoundPath = SoundPath("click")
		self.goBackSoundPath = SoundPath("back")

	def InitPygame(self) -> None:

		pygame.init()

	def InitMixer(self) -> None:

		mixer.init()

	def OpenWindow(self) -> None:

		self.window = pygame.display.set_mode(self.windowSize, 0, 32)
	
	def SetTitle(self) -> None:

		pygame.display.set_caption(self.windowTitle)

	def SetClock(self) -> None:

		self.clock = pygame.time.Clock()

	def SetCursor(self) -> None:

		pygame.mouse.set_visible(False)
		self.cursor = Image(ImagePath("cursor"), (0, 0), size=self.cursorSize)

	def SetFonts(self) -> None:

		self.buttonFont = pygame.font.Font(self.fontPath, 30)
		self.infoPanelTextFont = pygame.font.Font(self.fontPathThin, 15)
		self.infoPanelButtonFont = pygame.font.Font(self.fontPathThin, 24)

	def PlaySound(self, soundPath: SoundPath) -> None:

		mixer.music.load(soundPath)
		mixer.music.play()

	def isThereSelectedTile(self) -> bool:

		for row in self.tiles:
			for tile in row:

				if tile.selected:

					return True
				
		return False

	def ControlSelectingTile(self) -> None:

		isThereAnySelectedTile = self.isThereSelectedTile()

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
		
		if self.rowCount < self.maxSize and self.columnCount < self.maxSize and self.money >= self.expandCost(self.rowCount):

			self.money -= self.expandCost(self.rowCount)

			self.rowCount = self.columnCount = self.rowCount+1
			self.CreateTiles(self.rowCount, self.columnCount)

			self.expandButton = Button("green", (300, 20), (320, 800), "red", "EXPAND", str(self.expandCost(self.rowCount)) + "$", White, White, (27, 10), (40, 12), self.buttonFont, (200, 60))

	def SetAge(self, ageNumber) -> None:
			
		self.ageNumber = ageNumber
		
		for i in range(len(self.buildings)):
			building = self.buildings[i]
			self.buildings[i] = Building(building.level, self.ageNumber, building.tile)

		self.buildButton = Button("green", (600, 20), (620, 800), "red", "BUILD", str(self.buildCost(self.ageNumber)) + "$", White, White, (50, 10), (60, 12), self.buttonFont, (200, 60))
		self.nextAgeButton = Button("green", (900, 20), (920, 800), "red", "NEXT AGE", str(self.ageCost(self.ageNumber)) + "$", White, White, (12, 10), (45, 12), self.buttonFont, (200, 60))

	def NextAge(self) -> None:

		if self.ageNumber + 1 < len(ages) and self.money >= self.ageCost(self.ageNumber):
			
			self.SetAge(self.ageNumber + 1)
			self.money -= self.ageCost(self.ageNumber)

	def Exit(self) -> None:

		self.run = False
		pygame.quit()
		exit()

	def Run(self) -> None:

		#-# Start The Application #-#
		self.InitPygame()
		self.InitMixer()
		self.OpenWindow()
		self.SetTitle()
		self.SetClock()
		self.SetCursor()
		self.SetFonts()
		self.run = True

		#-# Open first tab #-#
		self.OpenTab("menu")

		#-# Main Loop #-#
		while self.run:

			#-# FPS #-#
			self.clock.tick(self.FPS)
			
			#-# Get Mouse Position #-#
			self.mousePosition = pygame.mouse.get_pos()

			#-# Control Events #-#
			for event in pygame.event.get():

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

				if self.tab == "menu":
					
					#-# Change the color of buttons if mouse over it #-#
					if event.type == pygame.MOUSEMOTION:

						if self.mainMenu.buttons[0].isMouseOver(self.mousePosition):
							
							if not self.mainMenu.buttons[0].selected:

								self.mainMenu.buttons[0].selected = True
								self.mainMenu.buttons[1].selected = False
								self.mainMenu.buttons[2].selected = False
								self.PlaySound(self.switchUpSoundPath)

						elif self.mainMenu.buttons[1].isMouseOver(self.mousePosition):

							if self.mainMenu.buttons[0].selected:

								self.PlaySound(self.switchDownSoundPath)

							elif self.mainMenu.buttons[2].selected:

								self.PlaySound(self.switchUpSoundPath)
							
							self.mainMenu.buttons[1].selected = True
							self.mainMenu.buttons[0].selected = False
							self.mainMenu.buttons[2].selected = False
							
						elif self.mainMenu.buttons[2].isMouseOver(self.mousePosition):

							if not self.mainMenu.buttons[2].selected:

								self.PlaySound(self.switchDownSoundPath)

							self.mainMenu.buttons[2].selected = True
							self.mainMenu.buttons[0].selected = False
							self.mainMenu.buttons[1].selected = False
					
					#-# Control click button events with space button #-#
					elif event.type == pygame.KEYUP:

						if event.key == pygame.K_SPACE:

							if self.mainMenu.buttons[0].selected:

								self.PlaySound(self.clickSoundPath)
								self.OpenTab("game")

							elif self.mainMenu.buttons[1].selected:

								self.PlaySound(self.clickSoundPath)
								self.OpenTab("settings")

							elif self.mainMenu.buttons[2].selected:

								self.PlaySound(self.clickSoundPath)
								self.Exit()

						#-# Change the selected button with keys #-#
						elif event.key == pygame.K_w or event.key == pygame.K_UP:

							if self.mainMenu.buttons[1].selected:

								self.mainMenu.buttons[0].selected = True
								self.mainMenu.buttons[1].selected = False
								self.mainMenu.buttons[2].selected = False
								self.PlaySound(self.switchUpSoundPath)

							elif self.mainMenu.buttons[2].selected:

								self.mainMenu.buttons[1].selected = True
								self.mainMenu.buttons[0].selected = False
								self.mainMenu.buttons[2].selected = False
								self.PlaySound(self.switchUpSoundPath)
								
						elif event.key == pygame.K_s or event.key == pygame.K_DOWN:

							if self.mainMenu.buttons[1].selected:

								self.mainMenu.buttons[0].selected = False
								self.mainMenu.buttons[1].selected = False
								self.mainMenu.buttons[2].selected = True
								self.PlaySound(self.switchDownSoundPath)

							elif self.mainMenu.buttons[0].selected:

								self.mainMenu.buttons[1].selected = True
								self.mainMenu.buttons[0].selected = False
								self.mainMenu.buttons[2].selected = False
								self.PlaySound(self.switchDownSoundPath)

					elif event.type == pygame.MOUSEBUTTONUP:

						#-# Control click button events with mouse #-#
						if self.mainMenu.buttons[0].isMouseOver(self.mousePosition):

							self.PlaySound(self.clickSoundPath)
							self.OpenTab("game")

						elif self.mainMenu.buttons[1].isMouseOver(self.mousePosition):

							self.PlaySound(self.clickSoundPath)
							self.OpenTab("settings")

						elif self.mainMenu.buttons[2].isMouseOver(self.mousePosition):
							self.PlaySound(self.goBackSoundPath)
							self.Exit()

				elif self.tab == "settings":
					pass
 
				elif self.tab == "game":

					if event.type == pygame.MOUSEMOTION:
							
						if self.isInfoPanelOpen:
							#-# Select info panel buttons if mouse over #-#
							self.infoPanelSellButton.selected = self.infoPanelSellButton.isMouseOver(self.mousePosition)
							self.closeInfoButtonCross.selected = self.closeInfoButton.selected = self.closeInfoButton.isMouseOver(self.mousePosition)

						else:
						
							#-# Select tile if mouse over it #-#
							self.ControlSelectingTile()
						
							#-# Select build button if mouse over it #-#
							self.expandButton.selected = self.expandButton.isMouseOver(self.mousePosition)
							self.buildButton.selected = self.buildButton.isMouseOver(self.mousePosition)
							self.nextAgeButton.selected = self.nextAgeButton.isMouseOver(self.mousePosition)

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
							if self.infoModeTrueButton.isMouseOver(self.mousePosition):
								
								self.infoMode = not self.infoMode
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

							elif self.expandButton.isMouseOver(self.mousePosition):
								self.PlaySound(self.clickSoundPath)
								self.Expand()

							#-# Create building if build button clicked #-#
							elif self.buildButton.isMouseOver(self.mousePosition):
								self.PlaySound(self.clickSoundPath)
								self.CreateBuilding()

							elif self.nextAgeButton.isMouseOver(self.mousePosition):
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

			#-# Draw Everything #-#
			self.Draw()

	def OpenBuildingInfo(self, building: Building) -> None:

		self.closeInfoButton = Button("red_circle", ((self.windowWidth - 250)/2 + 250 - 20, (self.windowHeight - 400)/2 - 12), selectedColor="yellow_circle")
		self.closeInfoButtonCross = Button("grey_crossWhite", (9, 9), ((self.windowWidth - 250)/2 + 250 - 20 + 9, (self.windowHeight - 400)/2 - 12 + 9), "grey_crossGrey")
		
		self.infoBuilding = building
		self.infoPanel = Image(ImagePath("grey_panel", "gui"), ((self.windowWidth - 250)/2, (self.windowHeight - 400)/2), size=(250, 400))
		self.infoPanelTopSide = pygame.Surface((250, 300), pygame.SRCALPHA)

		buildingImage = Image(building.GetImagePath(), (20, 20), size=(65, 89))
		levelText = self.infoPanelTextFont.render("Level: " + str(building.level), True, Gray)
		speedText = self.infoPanelTextFont.render("Speed: " + str(building.speed) + " $/sec", True, Gray)
		cooldownText = self.infoPanelTextFont.render("Cooldown: " + str(building.cooldown) + " sec", True, Gray)
		sellPriceText = self.infoPanelTextFont.render("Sell Price: " + str(building.sellPrice), True, Gray)
		
		self.infoPanelTopSide.blit(levelText, (90, 35))
		self.infoPanelTopSide.blit(speedText, (90, 50))
		self.infoPanelTopSide.blit(cooldownText, (90, 65))
		self.infoPanelTopSide.blit(sellPriceText, (90, 80))
		buildingImage.Draw(self.infoPanelTopSide)

		self.infoPanelSellButton = Button("red", (20, 325), ((self.windowWidth - 250)/2 + 20, (self.windowHeight - 400)/2 + 325), "yellow", "SELL", "+" + str(building.sellPrice) + "$", White, Gray, (75, 10), (73, 15), self.infoPanelButtonFont, (210, 50), (210, 60))

		self.isInfoPanelOpen = True

	def MoveBuildings(self, rotation: str) -> None:

		isBuildingsMoving = False

		for building in self.buildings:
			if not building.velocity == Vector2(0, 0):
				isBuildingsMoving = True
				break

		if not self.infoMode and not isBuildingsMoving:

			if rotation == "up" or rotation == "down":
                
				for columnNumber in range(self.columnCount):
					
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
									if not building.tile.rowNumber == self.rowCount - targetRow:
										building.SetTargetTile(self.tiles[self.rowCount - targetRow - 1][columnNumber])
									previousBuilding = building
									targetRow += 1
								elif previousBuilding.level == building.level and self.maxBuildingLevel > building.level:
									previousBuilding.LevelUp(building)
									previousBuilding = None
								else:
									if not building.tile.rowNumber == self.rowCount - targetRow:
										building.SetTargetTile(self.tiles[self.rowCount - targetRow - 1][columnNumber])
									previousBuilding = building
									targetRow += 1

			elif rotation == "right" or rotation == "left":

				for rowNumber in range(self.rowCount):
					
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
									if not building.tile.columnNumber == self.columnCount - targetColumn:
										building.SetTargetTile(self.tiles[rowNumber][self.columnCount - targetColumn - 1])
									previousBuilding = building
									targetColumn += 1
								elif previousBuilding.level == building.level and self.maxBuildingLevel > building.level:
									previousBuilding.LevelUp(building)
									previousBuilding = None
								else:
									if not building.tile.columnNumber == self.columnCount - targetColumn:
										building.SetTargetTile(self.tiles[rowNumber][self.columnCount - targetColumn - 1])
									previousBuilding = building
									targetColumn += 1

			self.buildings.sort(key=lambda building: building.tile.columnNumber)

	def CreateBuilding(self) -> None:

		isBuildingsMoving = False

		for building in self.buildings:
			if not building.velocity == Vector2(0, 0):
				isBuildingsMoving = True
				break

		if not isBuildingsMoving and self.money >= self.buildCost(self.ageNumber): #and not self.infoMode

			try:
				
				emptyTiles = []
				
				for rowNumber in range(self.rowCount):
					for columnNumber in range(self.columnCount):
						emptyTiles.append((rowNumber + 1, columnNumber + 1))


				for building in self.buildings:
					emptyTiles.remove((building.tile.rowNumber, building.tile.columnNumber))


				if len(emptyTiles) > 0:
					
					rowNumber, columnNumber = choice(emptyTiles)

					newBuilding = Building(1, self.ageNumber, self.tiles[rowNumber - 1][columnNumber - 1])
					self.buildings.append(newBuilding)
					self.buildings.sort(key=lambda building: building.tile.columnNumber)
					self.money -= self.buildCost(self.ageNumber)
					
				else:
					pass # not enough space error

			except NameError as error:

				print("You need to create tiles before creating new building! lol")
	
	def OpenTab(self, tab: str) -> None:

		self.PlayCloudAnimation()
		self.tab = tab

		if tab == "menu":
			self.OpenMainMenu()
		elif tab == "settings":
			self.OpenSettings()
		elif tab == "game":
			self.StartGame()

	def PlayCloudAnimation(self) -> None:

		def CreateClouds():
			for i in range(100):

				cloud = Cloud(ImagePath("cloud"), self.windowWidth, self.windowHeight, (200, 200))
				
				#cloud.SetVelocity((random.choice((-4, 4)), 0))
				
				if cloud.position.x <= self.windowWidth/2:
					cloud.SetVelocity((-10, 0))
				else:
					cloud.SetVelocity((10, 0))
				
				self.animationClouds.append(cloud)

		self.animationClouds = []
		CreateClouds()

	def OpenMainMenu(self) -> None:

		buttonSize = (400, 60)
		self.menuWidth, self.menuHeight = (440, 315)
		menuPosition = (self.windowWidth - self.menuWidth) / 2, (self.windowHeight - self.menuHeight) / 2
		buttonTexts = ["Start", "Settings", "Exit"]
		buttonTextPositions = [(140, 10), (110, 10), (160, 10)]
		self.mainMenu = Menu(menuPosition, ImagePath("blue_button03", "gui"), (440, 70), self.windowTitle, White, self.buttonFont, (118, 15), ImagePath("grey_panel", "gui"), 3, buttonSize, "blue", "yellow", buttonTexts, White, Gray, buttonTextPositions, self.buttonFont)

	def OpenSettings(self) -> None:

		buttonSize = (400, 60)
		self.menuWidth, self.menuHeight = (440, 315)
		menuPosition = (self.windowWidth - self.menuWidth) / 2, (self.windowHeight - self.menuHeight) / 2
		buttonTexts = ["Start", "Settings", "Exit"]
		buttonTextPositions = [(140, 10), (110, 10), (160, 10)]
		self.settingsMenu = Menu(menuPosition, ImagePath("blue_button03", "gui"), (440, 70), "Settings", White, self.buttonFont, (128, 15), ImagePath("grey_panel", "gui"), 0, buttonSize, "blue", "yellow", buttonTexts, White, Gray, buttonTextPositions, self.buttonFont)

	def CreateTiles(self, rowCount, columnCount) -> None:

		self.tiles = []

		for rowNumber in range(rowCount):

			row = []

			for columnNumber in range(columnCount):
				row.append(Tile(132, 99, rowNumber + 1, columnNumber + 1))

			self.tiles.append(row)

	def StartGame(self) -> None:
		
		def CreateClouds(count) -> None:

			self.clouds = []
			
			for i in range(count):
				cloud = Cloud(ImagePath("cloud"), self.windowWidth, self.windowHeight)
				self.clouds.append(cloud)

		def CreateGUI() -> None:
			
			self.gamePanelSize = self.gamePanelWidth, self.gamePanelHeight = (1400, 100)
			self.gamePanelPosition = self.gamePanelX, self.gamePanelY = (20, self.windowHeight - self.gamePanelHeight - 20)
			self.gamePanel = Image(ImagePath("grey_panel", "gui"), self.gamePanelPosition, size=self.gamePanelSize)
			
			self.infoModeFalseButton = Button("red", (80, 20), (100, 800), "yellow", size=(60, 60), selectedSize=(200, 30))
			self.infoModeTrueButton = Button("green", (80, 20), (100, 800), "yellow", size=(60, 60), selectedSize=(200, 30))
			self.infoModeButtonImage = Image(ImagePath("info", "gui"), (5, 5), (5, 5), (50, 50))
					
			self.expandButton = Button("green", (300, 20), (320, 800), "red", "EXPAND", str(self.expandCost(self.rowCount)) + "$", White, White, (27, 10), (40, 12), self.buttonFont, (200, 60))
			
			self.SetAge(self.ageNumber)

			self.moneySurface = pygame.Surface((150, 50), pygame.SRCALPHA)

		self.ageNumber = 0
		self.money = self.startingMoney
		self.isInfoPanelOpen = False
		self.infoMode = False
		self.buildings = []
		
		CreateClouds(self.cloudCount)
		self.CreateTiles(self.rowCount, self.columnCount)
		CreateGUI()

	def Draw(self) -> None:

		def FillBackgroundColor(color: tuple) -> None:
			self.window.fill(color)

		def DrawCloudAnimation() -> None:
			for cloud in self.animationClouds:
				cloud.Move()
				cloud.Draw(self.window)
				
				if cloud.position.x >= self.windowWidth or cloud.position.x <= -cloud.width:
					self.animationClouds.remove(cloud)

		def DrawMenuObjects() -> None:
			
			def DrawGUI():
				self.mainMenu.Draw(self.window)
			
			FillBackgroundColor(self.menuBackgroundColor)
			DrawGUI()

		def DrawSettingsObjects() -> None:

			def DrawGUI():
				self.settingsMenu.Draw(self.window)

			FillBackgroundColor(self.menuBackgroundColor)
			DrawGUI()

		def DrawGameObjects() -> None:

			def DrawClouds() -> None:

				for cloud in self.clouds:
					if self.windowWidth - cloud.width + cloud.velocity[0] >= cloud.position.x > self.windowWidth - cloud.width and cloud.velocity[0] > 0:
						newCloud = Cloud(ImagePath("cloud"), self.windowWidth, self.windowHeight)
						newCloud.SetPosition((cloud.position.x - self.windowWidth, cloud.position.y))
						newCloud.velocity = cloud.velocity
						self.clouds.append(newCloud)

					elif cloud.velocity[0] <= cloud.position.x < 0 and cloud.velocity[0] < 0:
						newCloud = Cloud(ImagePath("cloud"), self.windowWidth, self.windowHeight)
						newCloud.SetPosition((cloud.position.x + self.windowWidth, cloud.position.y))
						newCloud.velocity = cloud.velocity
						self.clouds.append(newCloud)

					if cloud.position.x >= self.windowWidth or cloud.position.x < -cloud.width:
						self.clouds.remove(cloud)

					cloud.Move()
					cloud.Draw(self.window)
			
			def DrawTiles() -> None:

				for row in self.tiles:
					for tile in row:
						tile.Draw(self.window)

			def DrawBuildings():

				time = pygame.time.get_ticks()
				for building in self.buildings:
					
					#-# Money #-#
					if not building.lastTime: building.lastTime = time
					
					if time - building.lastTime > (building.cooldown)*1000:
						self.money += building.cooldown*building.speed
						building.lastTime = pygame.time.get_ticks()


					building.Draw(self.window, self.buildings)

			def DrawGUI():

				#self.gamePanel.ReblitImage()
				
				if self.infoMode:
					self.infoModeButtonImage.Draw(self.infoModeTrueButton)
					self.infoModeTrueButton.Draw(self.gamePanel)
				else:
					self.infoModeButtonImage.Draw(self.infoModeFalseButton)
					self.infoModeFalseButton.Draw(self.gamePanel)
				
				self.nextAgeButton.Draw(self.gamePanel)
				self.expandButton.Draw(self.gamePanel)
				self.buildButton.Draw(self.gamePanel)

				if self.isInfoPanelOpen:
					self.infoPanel.ReblitImage()
					self.infoPanel.blit(self.infoPanelTopSide, (0, 0))
					self.infoPanelSellButton.Draw(self.infoPanel)
					self.infoPanel.Draw(self.window)
					self.closeInfoButtonCross.Draw(self.closeInfoButton)
					self.closeInfoButtonCross.Draw(self.closeInfoButton.selectedImage)
					self.closeInfoButton.Draw(self.window)
					
					
				self.window.blit(self.gamePanel, self.gamePanelPosition)

				#-# Money Text #-#
				self.moneySurface.fill(Black)
				self.moneyText = self.buttonFont.render(str(self.money) + "$", False, Yellow)
				self.moneySurface.blit(self.moneyText, (10, 10))
				self.window.blit(self.moneySurface, (0,0))

			FillBackgroundColor(self.gameBackgorundColor)
			DrawClouds()
			DrawTiles()
			DrawBuildings()
			DrawGUI()

		def DrawCursor() -> None:
			self.cursor.SetPosition(self.mousePosition)
			self.cursor.Draw(self.window)

		if self.tab == "menu":

			DrawMenuObjects()

		elif self.tab == "settings":

			DrawSettingsObjects()

		elif self.tab == "game":

			DrawGameObjects()

		if len(self.animationClouds) != 0:

			DrawCloudAnimation()

		DrawCursor()

		pygame.display.update()
