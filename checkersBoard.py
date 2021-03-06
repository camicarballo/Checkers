#!~pbui/pub/anaconda2-4.1.1/bin
#CHECKERSBOARD

import pygame
import findCell
import classes
import gameplay
import screens1
import functions
import compMove

def boardC(screen, board):
   #quit button
   pygame.draw.rect(screen,(255,255,255),pygame.Rect(730,740,50,20))
   font = pygame.font.Font(None, 24)
   text = font.render("Quit",True,(0,0,0))
   screen.blit(text, (737,743))

   #board of squares
   colorAlt = 0
   for x in range (80,720,80): 
      colorAlt+=1
      for y in range (80,720,80):
         if (colorAlt % 2 == 0): color = (255,255,255)
	 else: color = (128,128,128)
         pygame.draw.rect(screen,color,pygame.Rect(x,y,80,80))
	 colorAlt+=1

def pieces(screen, board):
    for block in board.b:
	for key, value in findCell.cells.items():
            if value == block.cell:
                x, y = key
                if block.type == 'r':
                    pygame.draw.circle(screen, (250, 0, 0), (x+40, y+40), 30)
                if block.type == 'rk':
                    pygame.draw.circle(screen,(250,0,0),(x+40, y+40), 30, 10)
                if block.type == 'b':
                    pygame.draw.circle(screen, (0, 0, 0), (x+40, y+40), 30)
                if block.type == 'bk': 
                    pygame.draw.circle(screen,(0, 0, 0),(x+40, y+40), 30, 10)

def playGame(multiplayer):

	#initialize pygame
	pygame.init()
	screen = pygame.display.set_mode((800,800))
	play = True #continue game play until play == False
	clock = pygame.time.Clock()
	player = 0 #start game with player 0 (red) and alternate turns with player 1
	moveSelect = True #will determine whether a chosen cell is the source or destination
	play = True
	
	#instantiate board object and draw screen
	gameBoard = classes.board()
	boardC(screen, gameBoard)
	pieces(screen, gameBoard)

	#font initializations for player updates
	font = "forque"
	font1 = pygame.font.SysFont(font, 70)
	redText = font1.render("Red's Turn", True, (255, 255, 255))
	blackText = font1.render("Black's Turn", True, (255, 255, 255))
	yourText = font1.render("Your Turn", True, (255, 255, 255))
	compText = font1.render("Computer's Turn", True, (255, 255, 255))
	
	#start screen with first player update
	if multiplayer:
		screen.blit(redText, (275, 20))
	else:
		screen.blit(yourText, (275, 20))

	while (play):
		if player == 0: #player 1
			check_type = 'r'
		elif player == 1: #player 2 or AI
			check_type = 'b'

		#AI's turn
		if not multiplayer and player == 1: #single player mode
			(piece1, piece2) = compMove.makeMove(gameBoard)

			#highlighting/selectpiece
			type1 = gameBoard.b[piece1].getType()
			type2 = gameBoard.b[piece2].getType()
			p = gameplay.validMove(gameBoard.b[piece1], gameBoard.b[piece2], gameBoard)
			if p > 1:
				type2 = gameBoard.b[p].getType()
			functions.selectpiece(piece1, gameBoard, check_type, screen)
			pygame.time.delay(500)

			#move piece
			pygame.time.wait(500)
			functions.makemove(piece1, piece2, p, gameBoard)

			#update screen
			screen.fill((0,0,0))
			boardC(screen, gameBoard)
			pieces(screen, gameBoard)
			screen.blit(yourText, (275, 20))
			pygame.display.flip()

			#check if there is a winner
			winner = functions.iswinner(piece2, type2, type1, gameBoard)
			if winner != 0:
				return winner

			#update player
			player = (player + 1) % 2
			continue

		#HUMANS' TURNS
		for event in pygame.event.get(): #multiplayer mode

			#quit the game
			if functions.quit(event.type) == 0:
				return 0

			#highlighting/select piece
			if event.type==pygame.MOUSEBUTTONUP and moveSelect:
				(x,y) = pygame.mouse.get_pos()
				cell = findCell.checkCell(x,y) #get cell number based on mouse position
				if cell == -1:
					continue
				type1 = gameBoard.b[cell].getType()
				#checks to make sure that the chosen piece is the current player's piece
				if functions.selectpiece(cell, gameBoard, check_type, screen) == 0:
					moveSelect = False
					continue

			#move the checker
			if event.type==pygame.MOUSEBUTTONUP and not moveSelect:
				(x,y) = pygame.mouse.get_pos()
				cell2 = findCell.checkCell(x,y) #get board square number
				if cell2 == -1:
					continue
				#checks if the move is valid
				p = gameplay.validMove(gameBoard.b[cell], gameBoard.b[cell2], gameBoard)
				type2 = gameBoard.b[p].getType()
				moveSelect = True

				#move the selected piece if the move is valid
				functions.makemove(cell, cell2, p, gameBoard)

				#update screen
				screen.fill((0,0,0))
  				boardC(screen, gameBoard)
				pieces(screen, gameBoard)

				#display player update on whose turn it is
				if multiplayer:
					if player == 0:
						screen.blit(blackText, (275, 20))
					else:
						screen.blit(redText, (275, 20))
				else:
					screen.blit(compText, (200, 20))

				#check if there is a winner
				winner = functions.iswinner(cell2, type2, type1, gameBoard)
				if winner != 0:
					return winner

				#next player's turn
				if p!= 1:
					player = (player + 1) % 2

		clock.tick(5)
		pygame.display.flip()
