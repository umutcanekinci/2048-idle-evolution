#-# Import Packages #-#
import pygame
from random import choice

from scripts.default.application import *
from scripts.default.database import *
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
		self.cloudCount = 30
		self.maxRowCount, self.maxColumnCount = 7, 7
		self.maxBuildingLevel = 6
		self.startingMoney = 10000

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
		self.infoPanelTextFont = pygame.font.Font(self.fontPathThin, 15)

		#-# Main Menu #-# 
		self.menuWidth, self.menuHeight = (440, 315)
		menuPosition = (self.width - self.menuWidth) / 2, (self.height - self.menuHeight) / 2
		self.mainMenu = Menu(menuPosition, ImagePath("blue_button03", "gui"), (440, 70), self.title, 30, White, self.fontPath, (118, 15), ImagePath("grey_panel", "gui"), (400, 60), "blue", "yellow", ["Start", "Settings", "Exit"], 30, Gray, White, self.fontPath)
		
		#-# Settings Menu #-#
		self.menuWidth, self.menuHeight = (440, 315)
		menuPosition = (self.width - self.menuWidth) / 2, (self.height - self.menuHeight) / 2
		self.settingsMenu = Menu(menuPosition, ImagePath("blue_button03", "gui"), (440, 70), "Settings", 30, White, self.fontPath, (128, 15), ImagePath("grey_panel", "gui"), (400, 60), "blue", "yellow", ["Delete Data", "GO BACK"], 30, Gray, White, self.fontPath)

		#-# GamePanel
		self.gamePanelSize = self.gamePanelWidth, self.gamePanelHeight = (1400, 100)
		self.gamePanelPosition = self.gamePanelX, self.gamePanelY = (20, self.height - self.gamePanelHeight - 20)

		self.GetDatasFromDatabase()

		self.AddObjects()

		#-# Info Panel #-#
		self.objects["game"]["info mode button"].SetStatus("Off")
		self.objects["game"]["info panel close button"].surfaces["Normal"].blit(Images(ImagePath("grey_crossWhite", "gui")), (9, 9))
		self.objects["game"]["info panel close button"].surfaces["Normal"].blit(Images(ImagePath("grey_crossGrey", "gui")), (9, 9))
		
		self.SetAge(self.buildings.ageNumber)
		self.UpdateButtonTexts()

	def AddObjects(self):

		self.AddObject("menu", "main menu", self.mainMenu)
		self.AddObject("menu", "cloud animation", CloudAnimation(self.size))
		self.AddObject("settings", "settings menu", self.settingsMenu)
		self.AddObject("settings", "cloud animation", CloudAnimation(self.size))
		self.AddObject("game", "clouds", GameClouds(self.cloudCount, self.size))
		self.AddObject("game", "game panel", Object(self.gamePanelPosition, self.gamePanelSize, {"Normal" : ImagePath("grey_panel", "gui")}))
		self.AddObject("game", "info mode button", Button((100, 800), (60, 60),  {"On" : ImagePath("green", "gui"), "Off" : ImagePath("red", "gui")}))
		self.AddObject("game", "info mode button image", Object((105, 805), (50, 50), {"Normal" : ImagePath("info", "gui")}))
		self.AddObject("game", "expand button", Button((320, 800), (200, 60), {"Normal" : ImagePath("green", "gui"), "Mouse Over" : ImagePath("red", "gui")}, "EXPAND", str(self.tiles.GetExpandCost()) + "$", 27, textFontPath=self.fontPath))
		self.AddObject("game", "build button", Button((620, 800), (200, 60), {"Normal" : ImagePath("green", "gui"), "Mouse Over" : ImagePath("red", "gui")}, "BUILD", str(self.buildings.GetBuildCost()) + "$", 27, textFontPath=self.fontPath))
		self.AddObject("game", "next age button", Button((920, 800), (200, 60), {"Normal" : ImagePath("green", "gui"), "Mouse Over" : ImagePath("red", "gui")}, "NEXT AGE", str(self.buildings.GetAgeCost()) + "$", 27, textFontPath=self.fontPath))
		self.AddObject("game", "money text", Text((1180, 810), "", 55, color=Green, backgroundColor=Black, isCentered=False))
		self.AddObject("game", "tiles", self.tiles)
		self.AddObject("game", "buildings", self.buildings)
		self.AddObject("game", "info panel", Object(((self.width - 250)/2, (self.height - 400)/2), (250, 400), {"Normal" : ImagePath("grey_panel", "gui")}, show=False))
		self.AddObject("game", "info panel top side", Object(((self.width - 250)/2, (self.height - 400)/2), (250, 300), show=False))
		self.AddObject("game", "info panel close button", Button(((self.width - 250)/2 + 250 - 20, (self.height - 400)/2 - 12), None, {"Normal" : ImagePath("red_circle", "gui"), "Mouse Over" : ImagePath("yellow_circle", "gui")}, show=False))
		self.AddObject("game", "cloud animation", CloudAnimation(self.size))
		
	def GetDatasFromDatabase(self):

		self.database = Database("database")
	
		if self.database.Connect():

			sqlCode = "CREATE TABLE IF NOT EXISTS game(age_number INTEGER, size INTEGER, money INTEGER)"
			self.database.Execute(sqlCode)
			self.database.Commit()
			self.database.Disconnect()

			if self.database.Connect():

				sqlCode = "SELECT * FROM game"
				self.database.Execute(sqlCode)
				gameData = self.database.Execute(sqlCode).fetchall()

				if not gameData:

					sqlCode = "INSERT INTO game(age_number, size, money) VALUES(0, 2, "+str(self.startingMoney)+")"
					self.database.Execute(sqlCode)
					self.database.Commit()
					self.database.Disconnect()

					if self.database.Connect():

						sqlCode = "SELECT * FROM game"
						gameData = self.database.Execute(sqlCode).fetchall()

					else:

						self.Exit()

				ageNumber, size, money = gameData[0]

				self.tiles = Tiles([size, size], [self.maxRowCount, self.maxColumnCount])
				self.money = money

				self.database.Execute("CREATE TABLE IF NOT EXISTS buildings(level INTEGER, row INTEGER, column INTEGER)")
				self.database.Commit()
				self.database.Disconnect()

				if self.database.Connect():

					data = self.database.Execute("SELECT * FROM buildings")
					buildings = data.fetchall()

					self.buildings = Buildings()
					self.buildings.ageNumber = ageNumber

					for building in buildings:

						self.AddBuilding(*building)
					
					self.database.Disconnect()
						  
				else:
				
					self.Exit()

			else:

				self.Exit()

		else:

			self.Exit()

	def DeleteData(self):

		if self.database.Connect():

			sqlCode = "DELETE FROM game"
			self.database.Execute(sqlCode)
			self.database.Commit()
			self.database.Disconnect()

			if self.database.Connect():

				sqlCode = "DELETE FROM buildings"
				self.database.Execute(sqlCode)
				self.database.Commit()
				self.database.Disconnect()

			else: 

				self.Exit()

		else: 

			self.Exit()

	def UpdateButtonTexts(self):

		if self.tiles.isMaxSize():

			self.objects["game"]["expand button"].text.UpdateText("Mouse Over", "MAX SIZE")
		
		else:

			self.objects["game"]["expand button"].text.UpdateText("Mouse Over", str(self.tiles.GetExpandCost()) + "$")
		
		if len(self.buildings) == self.tiles.rowCount*self.tiles.columnCount:
			
			self.objects["game"]["build button"].text.UpdateText("Mouse Over", "TILES ARE FULL")
			self.objects["game"]["build button"].text.UpdateSize("Mouse Over", 17)

		else:

			self.objects["game"]["build button"].text.UpdateText("Mouse Over", str(self.buildings.GetBuildCost()) + "$")
			self.objects["game"]["build button"].text.UpdateSize("Mouse Over", 27)

		if self.buildings.ageNumber == self.buildings.maxAgeNumber:
			
			self.objects["game"]["next age button"].text.UpdateText("Mouse Over", "MAX AGE")

		else:

			self.objects["game"]["next age button"].text.UpdateText("Mouse Over", str(self.buildings.GetAgeCost()) + "$")

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
						
						if self.objects["game"]["info mode button"].status == "On":

							tile.rect = tile.selectedRect
						
				else:

					tile.selected = False
					tile.rect = tile.unselectedRect

	def Expand(self) -> None:
		
		if self.money >= self.tiles.GetExpandCost():

			if not self.tiles.isMaxSize():

				self.money -= self.tiles.GetExpandCost()
				self.tiles.Expand()
				self.UpdateButtonTexts()
				self.PlaySound(self.clickSoundPath)
	
	def SetAge(self, ageNumber) -> None:
		
		if ageNumber <= self.buildings.maxAgeNumber:

			self.buildings.SetAge(ageNumber)
			self.UpdateButtonTexts()

	def NextAge(self) -> None:

		if self.buildings.ageNumber < self.buildings.maxAgeNumber and self.money >= self.buildings.GetAgeCost():
			
			self.money -= self.buildings.GetAgeCost()
			self.SetAge(self.buildings.ageNumber + 1)
			self.PlaySound(self.clickSoundPath)

	def HandleExitEvents(self, event) -> None:
		
		#-# Go back if escape button pressed #-#
		if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
				
			self.PlaySound(self.goBackSoundPath)

			if self.tab == "menu":

				self.Exit()

			elif self.tab == "settings":

				self.OpenTab("menu")

			elif self.tab == "game":

				if self.objects["game"]["info panel"].show:

					self.CloseInfoPanel()

				else:
					
					#region #-# Save everything to database #-#

					if self.database.Connect():

						sqlCode = "UPDATE game SET age_number='"+str(self.buildings.ageNumber)+"', size='"+str(self.tiles.rowCount)+"', money='"+str(self.money)+"'"
						self.database.Execute(sqlCode)
						self.database.Commit()
						self.database.Disconnect()

						if self.database.Connect():
							
							sqlCode = "DELETE FROM buildings"
							self.database.Execute(sqlCode)
							self.database.Commit()
							self.database.Disconnect()

							for building in self.buildings:

								if self.database.Connect():
								
									sqlCode = "INSERT INTO buildings(level, row, column) VALUES("+str(building.level)+", "+str(building.tile.rowNumber)+", "+str(building.tile.columnNumber)+")"
									self.database.Execute(sqlCode)
									self.database.Commit()
									self.database.Disconnect()

								else:
									
									self.Exit()

						else:

							self.Exit()

					#endregion

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

		elif self.tab == "settings":

			#-# Control click button events with space button #-#
			if event.type == pygame.KEYUP:

				if event.key == pygame.K_SPACE:

					if self.settingsMenu.buttons[0].status == "Selected":

						self.PlaySound(self.clickSoundPath)
						self.OpenTab("menu")

						self.DeleteData()
						self.GetDatasFromDatabase()
						self.AddObjects()

					elif self.settingsMenu.buttons[1].status == "Selected":

						self.PlaySound(self.clickSoundPath)
						self.OpenTab("menu")

			#-# Control click button events with mouse #-#
			elif event.type == pygame.MOUSEBUTTONUP:
				
				if self.settingsMenu.buttons[0].status == "Selected":

					self.PlaySound(self.clickSoundPath)
					self.OpenTab("menu")

					self.DeleteData()
					self.GetDatasFromDatabase()
					self.AddObjects()
					
				elif self.settingsMenu.buttons[1].status == "Selected":

					self.PlaySound(self.clickSoundPath)
					self.OpenTab("menu")

		elif self.tab == "game":

			#-# sell building #-#
			if self.objects["game"]["info panel"].show:

				if self.infoPanelSellButton.isMouseClick(event, self.mousePosition):
					
					self.buildings.remove(self.infoBuilding)
					self.money += self.infoBuilding.sellPrice
					self.CloseInfoPanel()
					self.PlaySound(self.goBackSoundPath)
					self.UpdateButtonTexts()
				
				#-# close info panel #-#
				elif self.objects["game"]["info panel close button"].isMouseClick(event, self.mousePosition):

					self.CloseInfoPanel()
					self.PlaySound(self.goBackSoundPath)
					self.ControlSelectingTile()
			else:

				#-# Select tile if mouse over it #-#
				self.ControlSelectingTile()

				#-# On/off info mode with clicking info mode button #-#
				if self.objects[self.tab]["info mode button"].isMouseClick(event, self.mousePosition):

					if self.objects["game"]["info mode button"].status == "On":

						self.objects[self.tab]["info mode button"].SetStatus("Off")

					else:

						self.objects[self.tab]["info mode button"].SetStatus("On")
					
					self.PlaySound(self.clickSoundPath)

				#-# Open building info if tile is clicked #-#
				if self.objects["game"]["info mode button"].status == "On" and event.type == pygame.MOUSEBUTTONUP:

					for row in self.tiles:

						for tile in row:

							if tile.selected:

								for building in self.buildings:

									if building.tile == tile:

										self.OpenInfoPanel(building)
										self.PlaySound(self.clickSoundPath)

										break
								break

				#-# expand #-#
				if self.objects[self.tab]["expand button"].isMouseClick(event, self.mousePosition):

					self.Expand()

				#-# Create building if build button clicked #-#
				elif self.objects[self.tab]["build button"].isMouseClick(event, self.mousePosition):

					self.CreateBuilding()

				#-# Go next age #-#
				elif self.objects[self.tab]["next age button"].isMouseClick(event, self.mousePosition):

					self.NextAge()

			if event.type == pygame.KEYUP:

				#-# Create/Move buildings with keys #-#
				if not self.objects["game"]["info panel"].show:

					if event.key == pygame.K_SPACE:
						
						self.CreateBuilding()
					
					elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
					
						self.MoveBuildings("right")
					
					elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
					
						self.MoveBuildings("left")
					
					elif event.key == pygame.K_UP or event.key == pygame.K_w:
					
						self.MoveBuildings("up")
					
					elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
					
						self.MoveBuildings("down")

	def OpenInfoPanel(self, building: Building) -> None:

		self.objects[self.tab]["info panel"].Show()
		self.objects[self.tab]["info panel top side"].Show()
		self.objects[self.tab]["info panel close button"].Show()

		self.infoBuilding = building
		
		levelText = self.infoPanelTextFont.render("Level: " + str(building.level), True, Gray)
		speedText = self.infoPanelTextFont.render("Speed: " + str(building.speed) + " $/sec", True, Gray)
		cooldownText = self.infoPanelTextFont.render("Cooldown: " + str(building.cooldown) + " sec", True, Gray)
		sellPriceText = self.infoPanelTextFont.render("Sell Price: " + str(building.sellPrice), True, Gray)
		
		self.objects["game"]["info panel top side"].AddSurface("Normal", pygame.Surface((250, 300), pygame.SRCALPHA))
		self.objects["game"]["info panel top side"].surfaces["Normal"].blit(levelText, (90, 35))
		self.objects["game"]["info panel top side"].surfaces["Normal"].blit(speedText, (90, 50))
		self.objects["game"]["info panel top side"].surfaces["Normal"].blit(cooldownText, (90, 65))
		self.objects["game"]["info panel top side"].surfaces["Normal"].blit(sellPriceText, (90, 80))
		self.objects["game"]["info panel top side"].surfaces["Normal"].blit(Images(building.GetImagePath(), (65, 89)), (20, 20))

		self.infoPanelSellButton = Button(((self.width - 250)/2 + 20, (self.height - 400)/2 + 325), (210, 50), {"Normal" : ImagePath("green", "gui"), "Mouse Over" : ImagePath("red", "gui")}, "SELL", str(building.sellPrice) + "$", 25)
		self.AddObject("game", "info panel sell button", self.infoPanelSellButton)

	def CloseInfoPanel(self):

		self.objects[self.tab]["info panel"].Hide()
		self.objects[self.tab]["info panel top side"].Hide()
		self.objects[self.tab]["info panel close button"].Hide()
		self.objects[self.tab]["info panel sell button"].Hide()

	def MoveBuildings(self, rotation: str) -> None:

		isBuildingsMoving = False

		for building in self.buildings:
			
			if not building.velocity == Vector2(0, 0):
				isBuildingsMoving = True
				break

		if self.objects["game"]["info mode button"].status == "Off" and not isBuildingsMoving:

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

	def AddBuilding(self, level, rowNumber, columnNumber):

		newBuilding = Building(level, self.buildings.ageNumber, self.tiles[rowNumber - 1][columnNumber - 1])
		self.buildings.append(newBuilding)
		self.buildings.sort(key=lambda building: building.tile.columnNumber)

		if len(self.buildings) == self.tiles.rowCount*self.tiles.columnCount and "game" in self.objects and "build button" in self.objects["game"]:

			self.objects["game"]["build button"].text.UpdateText("Mouse Over", "TILES ARE FULL")
			self.objects["game"]["build button"].text.UpdateSize("Mouse Over", 17)
		
	def CreateBuilding(self) -> None:

		#region Control of buildings are moving

		isBuildingsMoving = False

		for building in self.buildings:

			if not building.velocity == Vector2(0, 0):

				isBuildingsMoving = True

				break

		#endregion

		if not isBuildingsMoving and self.money >= self.buildings.GetBuildCost():

			#region Get Empty Tiles

			emptyTiles = []
			
			for rowNumber in range(self.tiles.rowCount):

				for columnNumber in range(self.tiles.columnCount):

					emptyTiles.append((rowNumber + 1, columnNumber + 1))


			for building in self.buildings:
				emptyTiles.remove((building.tile.rowNumber, building.tile.columnNumber))

			#endregion

			if len(emptyTiles) > 0:
				
				rowNumber, columnNumber = choice(emptyTiles)

				self.AddBuilding(1, rowNumber, columnNumber)
				self.money -= self.buildings.GetBuildCost()
				self.PlaySound(self.clickSoundPath)
				
			else:

				pass # not enough space
	
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
		self.objects[self.tab]["money text"].UpdateText("Normal", str(self.money) + "$")

	def Draw(self) -> None:
		
		if self.tab == "game":

			self.UpdateMoney()

		super().Draw()
