import pygame
import sys

#****************************************************functions******************************************************************

def map_mouse_to_board(x, y):
    if x < gameSize / 3:
        column = 0
    elif gameSize / 3 <= x < (gameSize / 3) * 2:
        column = 1
    else:
        column = 2
    if y < gameSize / 3:
        row = 0
    elif gameSize / 3 <= y < (gameSize / 3) * 2:
        row = 1
    else:
        row = 2
    return column, row

def draw_board(board):
    myFont = pygame.font.SysFont('Tahoma', gameSize // 3)
    for y in range(3):
        for x in range(3):
            if board[y][x] == xMark:
                color = xColor
            else:
                color = oColor
            text_surface = myFont.render(board[y][x], False, color)
            screen.blit(text_surface, (y * (gameSize // 3) + margin + (gameSize // 18), x * (gameSize // 3) + margin-20))

def is_full(board):
    return not any(None in sublist for sublist in board)

def get_winner(board):
    # Diagonals
    if ((board[0][0] == board[1][1] and board[1][1] == board[2][2]) \
            or (board[0][2] == board[1][1] and board[1][1] == board[2][0])) and board[1][1] is not None:
        return board[1][1]
    for i in range(3):
        if board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][0] is not None:  # Rows
            return board[i][0]
        if board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[0][i] is not None:  # Columns
            return board[0][i]
    return None

def draw_lines():
    # Vertical lines
    pygame.draw.line(screen, lineColor, (margin + gameSize // 3, margin),
                     (margin + gameSize // 3, screenSize - margin), lineSize)
    pygame.draw.line(screen, lineColor, (margin + (gameSize // 3) * 2, margin),
                     (margin + (gameSize // 3) * 2, screenSize - margin), lineSize)
    # Horizontal lines
    pygame.draw.line(screen, lineColor, (margin, margin + gameSize // 3), (screenSize - margin, margin + gameSize // 3),
                     lineSize)
    pygame.draw.line(screen, lineColor, (margin, margin + (gameSize // 3) * 2),
                     (screenSize - margin, margin + (gameSize // 3) * 2), lineSize)

#************************************************Variables*********************************************************************    
screenSize = 600       
margin = 50    #for avoiding window corners
gameSize = 600 - (2 * margin)   #defining the gaming area into the window
lineSize = 10
backgroundColor = (0, 0, 0)
lineColor = (255, 255, 255)
xColor = (200, 0, 0)         #color of x move
oColor = (0, 0, 200)         #color of o move
xMark = 'X'                  
oMark = 'o'
board = [[None, None, None], [None, None, None], [None, None, None]]    #List in which we store all the moves for drawing
currentMove = 'X'   #Initially x move will be there

#**********************************************Window related things***********************************************************

pygame.init()
screen = pygame.display.set_mode((screenSize, screenSize))
pygame.display.set_caption("Tic Tac Toe")
pygame.font.init()
myFont = pygame.font.SysFont('Tahoma', gameSize // 3)
screen.fill(backgroundColor)
canPlay = True   #variable to control the play 
draw_lines()     #calling function to draw all the line of the game

#**************************************************Main loop*******************************************************************
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:    #for making the cancel button of window work
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN: #when the game overs after that if the user press enter then the game will start again
            if event.key == pygame.K_RETURN:
                board = [[None, None, None], [None, None, None], [None, None, None]]
                screen.fill(backgroundColor)
                draw_lines()
                canPlay = True
                
        if event.type is pygame.MOUSEBUTTONDOWN and canPlay:  #When each and every move is being encountered
            (mouseX, mouseY) = pygame.mouse.get_pos()   
            (column, row) = map_mouse_to_board(mouseX, mouseY)  #calling our function to find row/column at which user hits 
            if board[column][row] is None:   #If the user hitting point is empty then only enter and write the move 
                board[column][row] = currentMove
                if currentMove == xMark:   #if move is x then change the move to o and vice versa
                    currentMove = oMark
                else:
                    currentMove = xMark
                draw_board(board)    #Now draw the updated board
                winner = get_winner(board)  #calling the function to check the winner every time. 
                if winner is not None:   #If anyone win then enter into if block,if draw then move to else block
                    myFont = pygame.font.SysFont('Tahoma', screenSize // 5)
                    text_surface = myFont.render(str(winner) + " has won!", False, lineColor)
                    screen.blit(text_surface, (margin, screenSize // 2 - screenSize // 10))
                    canPlay = False
                else:
                    if is_full(board):
                        myFont = pygame.font.SysFont('Tahoma', screenSize // 5)
                        text_surface = myFont.render("Draw!", False, lineColor)
                        screen.blit(text_surface, (screenSize // 10, screenSize // 2 - screenSize // 10))
    pygame.display.update()
