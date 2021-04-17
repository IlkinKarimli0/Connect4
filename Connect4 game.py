import time
import pygame
import sys
import random
import math
import copy

UP_rect_color = (221,210,197)
GRAY = (149,169,193)
empty_circle = (229,234,240)
RED=(225,26,0)
BLUE = (0,0,255)

board =[[' ','1','2','3','4','5','6','7',' '],
        ['6',' ',' ',' ',' ',' ',' ',' ','6'],
        ['5',' ',' ',' ',' ',' ',' ',' ','5'],
        ['4',' ',' ',' ',' ',' ',' ',' ','4'],
        ['3',' ',' ',' ',' ',' ',' ',' ','3'],
        ['2',' ',' ',' ',' ',' ',' ',' ','2'],
        ['1',' ',' ',' ',' ',' ',' ',' ','1'],
        [   ,'1','2','3','4','5','6','7',  ]] 

def disc_adder(column,player_sign,f_board):
    for row in range(6,0,-1):
        if f_board[row][column] == ' ':
            f_board[row][column] = player_sign
            break
    return f_board
        
def board_printer(board):
    for i in range(8):
        print(' '.join(board[i]))

def exist_move(board,column): 
    if 1<=column<=7:
        return 1 if board[1][column] == ' ' else 0
    else:
        return 0

def valid_locations(board):
    valid_locations = []
    for i in range(1,8):
        if board[1][i] ==  ' ':
            valid_locations.append(i)
    return valid_locations
        

def clean_board(board):
    for row in range(1,7):
        for column in range(1,8):
            board[row][column] = ' '

def winning_check(board,player_sign):
    for row in range(6,0,-1):
        for column in range(1,5): 
            if(board[row][column] == player_sign and board[row][column] == board[row][column+1] and board[row][column+1] == board[row][column+2] and  board[row][column+2] == board[row][column+3]):
                return 1
    for column in range(1,8):
        for row in range(6,3,-1):
            if(board[row][column] == player_sign and board[row][column]==board[row-1][column] and board[row-1][column]==board[row-2][column] and board[row-2][column]==board[row-3][column]):
                return 1
    for row in range(6,3,-1):
        for column in range(1,5):
            if(board[row][column] == player_sign and board[row][column]==board[row-1][column+1] and board[row-1][column+1]==board[row-2][column+2] and board[row-2][column+2]==board[row-3][column+3]):
                return 1
    for row in range(6,3,-1):
        for column in range(7,3,-1):
            if(board[row][column] == player_sign and board[row][column]==board[row-1][column-1] and board[row-1][column-1]==board[row-2][column-2] and board[row-2][column-2]==board[row-3][column-3]):
                return 1
    return 0

def terminal_node(board):
    if winning_check(board,'0') == 1 or winning_check(board,'*') == 1 or len(valid_locations(board))==0 :
        return True
    else:
        False

def minimax(min_board,depth,alpha,beta,maximizingPlayer):
    validLocations = valid_locations(min_board)
    terminalNode = terminal_node(min_board)
    if depth==0 or terminalNode:
        if terminalNode == True:
            if winning_check(min_board,'0') == 1:
                return (None,10000000)
            elif winning_check(min_board,'*') == 1:
                return (None,-100000000)
            else:
                return (None,0)
        else:
            return (None,best_move_calculator(min_board,'0')[1])
    if maximizingPlayer:
        column = random.choice(validLocations)
        value = -math.inf
        for columns in validLocations:
            boardCopy = copy.deepcopy(min_board)
            boardCopy = disc_adder(columns,'0',boardCopy)
            new_score = minimax(boardCopy,depth-1,alpha,beta,False)[1]
            if new_score > value:
                value = new_score
                column = columns
            alpha = max(value,alpha)
            if alpha >= beta:
                break
        return column,value
    else:#minimizing
        column = random.choice(validLocations)
        value = math.inf
        for columns in validLocations:
            boardCopy = copy.deepcopy(min_board)
            boardCopy = disc_adder(columns,'*',boardCopy)  
            new_score = minimax(boardCopy,depth-1,alpha,beta,True)[1]
            if new_score < value:
                value = new_score
                column = columns
            beta = min(beta,value)
            if alpha >= beta:
                break
        return column,value  



def best_move_calculator(best_board,player_sign):
    scores = list()
    if player_sign == '0':
        enemy = '*'
    elif player_sign == '*':
        enemy = '0'
    for columns in range(1,8):
        score = Three_alligned(best_board,player_sign,columns) + center_score(best_board,player_sign)+two_alligned_horizontal(best_board,player_sign,columns)#+blocker(best_board,enemy,columns) #last_move(best_board,player_sign,columns)
        score +=  - Three_alligned(best_board,enemy,columns) - two_alligned_horizontal(best_board,enemy,columns) 
        scores.append(score)
    return (scores.index(max(scores))+1 , max(scores))

def AI(board):
    #disc_adder(best_move_calculator(board,'0')[0],'0',board,) 
    column,score = minimax(board,6,-math.inf,math.inf,True)
    print(column,score)
    disc_adder(column,'0',board)

def Three_alligned(best_board,player_sign,column):
    score=0
    if exist_move(best_board,column) == 0:
        return -100 
    fake_board = best_board
    #horizontal 
    for row in range(6,0,-1):
        for column in range(1,5):
            if(fake_board[row][column] == player_sign and fake_board[row][column] == fake_board[row][column+1] and fake_board[row][column+1] == fake_board[row][column+3] and fake_board[row][column+2] == ' '):
                score+=3
            if(fake_board[row][column] == player_sign and fake_board[row][column] == fake_board[row][column+2] and fake_board[row][column+2] == fake_board[row][column+3] and fake_board[row][column+1] == ' '):
                score+=3
        for column in range(1,6):
            if(fake_board[row][column] == player_sign and fake_board[row][column] == fake_board[row][column+1] and fake_board[row][column+1] == fake_board[row][column+2]):
                if fake_board[row][column+3] == ' ':
                    score+=3
                if fake_board[row][column-1] == ' ':
                    score +=3
    #vertical checking
    for row in range(6,3,-1):
        for column_add in range(1,8):
            if(fake_board[row][column_add] == player_sign and fake_board[row][column_add]==fake_board[row-1][column_add] and fake_board[row-1][column_add]==fake_board[row-2][column_add]):
                score+=3
    #dioganal checking
    for row in range(6,3,-1):
        for column in range(1,5):
            if(fake_board[row][column] == player_sign and fake_board[row][column]==fake_board[row-1][column+1] and fake_board[row-1][column+1]== fake_board[row-3][column+3]) and fake_board[row-2][column+2] == ' ':
                if fake_board[row-1][column+2] != ' ':
                    score +=3
            if(fake_board[row][column] == player_sign and fake_board[row][column]==fake_board[row-2][column+2] and fake_board[row-2][column+2]== fake_board[row-3][column+3]) and fake_board[row-1][column+1] == ' ':
                if fake_board[row][column+1] != ' ':
                    score +=3
            
    for row in range(6,3,-1):
        for column in range(7,3,-1):
            if(board[row][column] == player_sign and board[row][column]==board[row-1][column-1] and board[row-1][column-1]==board[row-2][column-2] and board[row-2][column-2]==board[row-3][column-3]):
                return 1
    return score


#def predicter(player_sign,column,enemy):

def center_score(best_board,player_sign):
    for row in range(6,0,-1):
        if best_board[row][4] == player_sign:
            return 4
        else:
            return 0


def two_alligned_horizontal(best_board,player_sign,column):
    score = 0
    if exist_move(best_board,column) == 0:
        return -100
    fake_board = best_board
    #horizontal scoring 
    for row_add in range(6,0,-1):
        for column_add in range(1,8):
            if column_add == 1:
                if fake_board[row_add][column_add] == fake_board[row_add][column_add+1]:
                    score+=1
                if fake_board[row_add][column_add] == fake_board[row_add][column_add+2] and fake_board[row_add][column_add+1] == ' ':
                    score+=1
            if column_add == 2:
                if fake_board[row_add][column_add] == fake_board[row_add][column_add+2] and fake_board[row_add][column_add+1] == ' ':
                    score+=1
            if 1<column_add<7:
                if fake_board[row_add][column_add] == fake_board[row_add][column_add-1]:
                    score+=1
                if fake_board[row_add][column_add] == fake_board[row_add][column_add+1]:
                    score+=1
                if 2<column_add<6:
                    if fake_board[row_add][column_add] == fake_board[row_add][column_add-2] and fake_board[row_add][column_add-1] == ' ':
                        score+=1
                    if  fake_board[row_add][column_add] == fake_board[row_add][column_add+2] and fake_board[row_add][column_add+1] == ' ':
                        score+=1
            if column_add == 7:
                if fake_board[row_add][column_add] == fake_board[row_add][column_add-1]:
                    score+=1
                if fake_board[row_add][column_add] == fake_board[row_add][column_add-2] and fake_board[row_add][column_add-1] == ' ':
                    score+=1
            if column_add == 6:
                if fake_board[row_add][column_add] == fake_board[row_add][column_add-2] and fake_board[row_add][column_add-1] == ' ':
                    score+=1
    #vertical scoring
    for row_add in range(6,1,-1):
        if fake_board[row_add][column_add] == fake_board[row_add+1][column_add]:
            score+=1
    #diagonals
    rows = [-1,-2,1,2];columns=[1,2,1,2]
    for i,j in zip(rows,columns):
        if(1<=row_add+i<=6 and 1<=column_add+j <=7):
            if fake_board[row_add+i][column_add+j] == fake_board[row_add][column_add]:
                score+=1
        if(1<=row_add+i<=6 and 1<=column_add-j <=7):
            if fake_board[row_add+i][column_add-j] == fake_board[row_add][column_add]:
                score+=1

    fake_board[row_add][column_add] = ' ';return score
    #check   


########################################################################################################################################################################

# # pygame part
def draw_board(board):
    for col in range(1,8):
        for row in range(1,7):
            pygame.draw.rect(screen,GRAY,((col-1)*SQUARESIZE , (row-1)*SQUARESIZE+SQUARESIZE,SQUARESIZE,SQUARESIZE))
            if board[row][col]== ' ':
                pygame.draw.circle(screen,empty_circle,(int((col-1)*SQUARESIZE+SQUARESIZE/2), int((row-1)*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)),radius)
            elif board[row][col]== '0':
                pygame.draw.circle(screen,RED,(int((col-1)*SQUARESIZE+SQUARESIZE/2), int((row-1)*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)),radius)
            elif board[row][col]== '*':
                pygame.draw.circle(screen,BLUE,(int((col-1)*SQUARESIZE+SQUARESIZE/2), int((row-1)*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)),radius)
            pygame.draw.rect(screen,UP_rect_color,(0,0,width,SQUARESIZE))
    pygame.display.update()

#starting to pygame and display board
pygame.init()
SQUARESIZE = 100
width = 7*SQUARESIZE
height = 7*SQUARESIZE
size = (width,height)
radius = int(SQUARESIZE/2 - 5)
myfont = pygame.font.SysFont("monospace",70,)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
turn = random.randint(1,2)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen,UP_rect_color,(0,0,width,SQUARESIZE))
            posx = event.pos[0]
            if turn == 1:
                pygame.draw.circle(screen,BLUE,(posx,int(SQUARESIZE/2)),radius)
        pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN:
            posx=event.pos[0]
            column = posx//100 +1
            if turn == 1:
                while(exist_move(board,column)==0):
                    column = posx//100 +1
                disc_adder(column,"*",board)
                board_printer(board);draw_board(board)
                turn += 1 #moving ability changing to AI
                if winning_check(board,"*") == 1:
                    message = myfont.render("You WIN :)",1,BLUE)
                    screen.blit(message,(40,10))
                    pygame.display.update()
                    clean_board(board)
                    pygame.time.wait(7000)
                    pygame.display.update()
            if turn == 2:
                time.sleep(1)
                AI(board)
                board_printer(board);draw_board(board)
                turn -= 1
                if winning_check(board,"0") == 1:
                    message = myfont.render("Computer WIN!:)",1,BLUE)
                    screen.blit(message,(40,10))
                    pygame.display.update()
                    clean_board(board)
                    pygame.time.wait(7000)
                    pygame.display.update()

