print('CMPT103F19_X01L_MS3_CM.py  3.00  2019/12/03  Courtney McNeilly')
'''***********************************************************************
Icebreaker Game:
- Two players alternate turns; each player gets a turn to:
  (1) move to a valid adjacent square, where there is solid ice, 
      and other player not there
  (2) break a solid piece of ice which is no longer able to be moved to
- Game ends when there is no more valid moves to make

Game Logic:
- game variables:
  - player = 0 or 1, identifies current player
  - players = list of 2 lists of; { row, col, visual image }
    ex. { r, c, reddot.gif }
  - board: list of NR lists of NC Rectangles; fill color = SOLID (white) ice or
    BROKEN (purple)
  - r, c: (row, col) coordinates of mouse, realtive to the game board (getMouse
    return the x and y coordinates of mouse and is then calculated with GAP)
  - NR: number of rows
  - NC: number of columns
- GUI variables: main game window, Quit and Reset buttons, info msg displays
  current player and coordinates on board, mouse msg changes according to who's 
  turn it is and which move it is (move or break ice) and "NOT VALID" 
  when appropriate
- Reset button: re-position players to original positions, and restore all ice
  to solid
- Quit button: quits the game when clicked

***********************************************************************'''

from graphics import *
from time import sleep

#=========================================================================
# PROGRAM PARAMETERS & CONSTANTS

WIN_TITLE = "Icebreaker v3.0 2019 Courtney McNeilly"
WIN1_TITLE = "ARE YOU READY?!"                      # window for splash screen
WIN2_TITLE = "CONTINUE?"                            # window for continue screen
NR, NC = 10, 10                                     # # of rows, cols on board
p1_img = Image(Point(0,0), "Dot_Red.gif")           # player 1
p2_img = Image(Point(0,0), "Dot_Blue.gif")          # player 2
SQ_SZ = p1_img.getWidth()                           # size of squares
GAP = 10                                            # pixels between squares
BOTTOM = 100                                        # size of bottom of win
# win window width and height dynamic sizing
WIN_W, WIN_H = NC * (SQ_SZ + GAP) + GAP, NR * (SQ_SZ + GAP) + GAP + BOTTOM
SOLID, BROKEN = 'white', 'purple'                   # colours for ice

#=========================================================================
# GLOBAL VARIABLES

# Declare program variables:

# GUI Variables
win        = None                             # Main app GraphWin
win1       = None
win2       = None                             # End of game prompt window
info_msg   = None                             # Informative text: Text 
btn_Quit   = None                             # Quit button in win
btn_Reset  = None                             # reset button in win
mouse_msg  = None                             # To display mouse coordinates
splash_msg = None                             # msg on splash screen
winner     = None                             # holds winner var for functions

# Game Variables
player    = 0                                 # Whose turn it is
players   = [ [NR//2, 0   , p1_img],          # Basic info of each player
              [NR//2, NC-1, p2_img] ]         # [row, column, visible info]

board     = []                                # NR x NC Squares
x = 0                                         # x coordinate of the click
y = 0                                         # y coordinate of the click
r = None                                      # Current row
c = None                                      # Current column

#==============================================================================
# Creates a button given window, coordinates, width/height, and text parameters
# -----------------------------------------------------------------------------
def btn_create(win, x1, y1, w, h, txt):
    r = Rectangle(Point(x1, y1), Point(x1+w, y1+h))
    r.draw(win)                                         # draw rectangle in win
    t = Text(r.getCenter(), txt)
    t.draw(win)
    return [r, t]

# -----------------------------------------------------------------------------
# Detects if a button has been clicked. Board is a list [ Rectangle, Text ]
#------------------------------------------------------------------------------
def btn_clicked(pt, btn):  
    x1, y1 = btn[0].getP1().getX(), btn[0].getP1().getY()
    x2, y2 = btn[0].getP2().getX(), btn[0].getP2().getY()
      
    return x1 < pt.x < x2 and y1 < pt.y < y2

# -----------------------------------------------------------------------------
# Creates the game board based on the NR, NC, and GAP parameters
#------------------------------------------------------------------------------
def board_create():     # board consists of a list with lists for each row
    global win, board, GAP, row, col, btn_Quit, btn_Reset
    for row in range(NR):  
        board.append([])
        for col in range(NC):
            board[row].append(Rectangle(Point( GAP + col * (SQ_SZ + GAP),
                                               GAP + row * (SQ_SZ + GAP) ),
                                        Point( SQ_SZ + GAP + col *(SQ_SZ+GAP), 
                                               SQ_SZ + GAP + row *(SQ_SZ+GAP))))
            board[row][col].setFill(SOLID)
            board[row][col].draw(win)
            
    # get row and column of players
    r0, c0, r1, c1 = players[0][:2] + players[1][:2]
    
    # move both players into starting positions and draw images
    p1_img.move((GAP+(SQ_SZ+GAP)*c0+(SQ_SZ)//2), (GAP+(SQ_SZ+GAP)*r0+SQ_SZ//2))
    p1_img.draw(win)
    p2_img.move((GAP+(SQ_SZ+GAP)*c1+SQ_SZ//2), (GAP+(SQ_SZ+GAP)*r1+SQ_SZ//2))
    p2_img.draw(win)
    
# -----------------------------------------------------------------------------
# Resets the board and game variables when called, moves players back to 
# original positions
# -----------------------------------------------------------------------------
def reset_game():
    global player, players, x, y, r, c, board, NR, NC, p1_img, p2_img
    
    # Get player positions
    rp0, cp0 = players[0][:2]          # Player 0 position
    rp1, cp1 = players[1][:2]          # Player 1 position
        
    # Calculate difference in row and col, move players back to starting point
    p1_img.move( -(SQ_SZ+GAP)*cp0          , NR//2*(SQ_SZ+GAP)-(SQ_SZ+GAP)*rp0 )
    p2_img.move( (SQ_SZ+GAP)*((NC-1)-cp1)  , NR//2*(SQ_SZ+GAP)-(SQ_SZ+GAP)*rp1 )
    
    # Reset players' positions and turn in variables
    player    = 0                                # Reset turn to player 0
    players   = [ [NR//2, 0   , p1_img],         # Basic info of each player
                  [NR//2, NC-1, p2_img] ]
    
    # Reset the ice to SOLID
    for row in range(NR):  
        for col in range(NC):
            board[row][col].setFill(SOLID)
    
# ----------------------------------------------------------------------------
# SYNTAX: bool = prompt_window(string_yes, string_no, initial_msg)
# Returns True if user selects "Yes" button and returns false if user selects
# "No" button.
# ----------------------------------------------------------------------------
def prompt_window(string_yes="WOOHOO!\nResetting Game...",\
                  string_no="FINE THEN!\nQuitter...", \
                  initial_msg=f"Congrats!! \nPlay Again?"):
    global players, player
    
    win2 = GraphWin(WIN2_TITLE, 300, 300)               # New window
    
    # Create and draw message    
    won_msg = Text(Point(150, 100), initial_msg)
    won_msg.draw(win2)
    won_msg.setSize(20)
    
    # Create buttons to quit and continue
    btn_Continue = btn_create(win2, 120, 165, 60, 20, "Yes")
    btn_Quit2 = btn_create(win2, 120, 200, 60, 20, "No")
    
    while True:
        # Get click coordinates
        pt = win2.getMouse()                 # Wait for get mouse click
        x, y = pt.getX(), pt.getY()  
        
        # If button clicked, write enthusiastic message and restart game
        if btn_clicked(pt, btn_Continue):
            won_msg.setText(string_yes)
            sleep(1.5)
            win2.close()
            reset_game()
            return True
        
        # If clicked, pout and quit the game
        if btn_clicked(pt, btn_Quit2):
            won_msg.setText(string_no)
            sleep(2)
            win2.close()
            return False
# ----------------------------------------------------------------------------
# SYNTAX: bool = splash_screen()
# Returns True and only True when button clicked because who doesn't want to
# play this game?
# ----------------------------------------------------------------------------

def splash_screen():
    global win1, splash_msg, btn_Start
    
    win1 = GraphWin(WIN1_TITLE, 500, 250)               # New window
    
    # Set up welcome message
    splash_msg = Text(Point(250, 100), "Welcome to ICEBREAKER!")
    splash_msg.draw(win1)
    splash_msg.setSize(30)
    
    # Add start button
    btn_Start = btn_create(win1, 200, 165, 100, 40, "Start")
    
    while True:
        # Get click coordinates
        pt = win1.getMouse()                 # Wait for get mouse click
        x, y = pt.getX(), pt.getY()
        
        # wait until button clicked, breaks when button is clicked
        if btn_clicked(pt, btn_Start):
            break
        
    win1.close()
    return True

# -----------------------------------------------------------------------------
# Returns True if current player has somewhere to move, i.e. there is an
# adjacent square available to move to, i.e. there is a square on the board
# with solid ice, and the other player is not occupying
# -----------------------------------------------------------------------------
def can_move():
    # Relative coordinates of squares adjacent to current player's location
    adjacent = [ (-1, -1), (-1, 0), (-1, 1),
                 ( 0, -1), ( 0, 1),
                 ( 1, -1), ( 1, 0), ( 1, 1) ]
    
    rp, cp = players[player][:2]          # Current player's row and column
    for ra, ca in adjacent:
        r, c = rp+ra , cp+ca              # Coordinates of adjacent square
        if r < 0 or r >= NR or c < 0 or c >= NC:
            continue
        other_player_not_there = players[1-player][:2] != [ r, c ]
        if solid_ice(r, c) and other_player_not_there:
            return True
    return False

# -----------------------------------------------------------------------------
# Returns True if (r, c) is adjacent to current player's coord's, and solid ice
# and other player not there
# -----------------------------------------------------------------------------
def valid_move(r, c):
    rp, cp = players[player][:2]
    opnt = players[1-player][:2] != [ r, c ]
    return abs(r-rp) <= 1 and abs(c-cp) <= 1 and (rp, cp) != (r, c) \
            and solid_ice(r, c) and opnt

# -----------------------------------------------------------------------------
# SYNTAX: bool = solid_ice()
# Returns True if the color of the ice in r, c is SOLID. Used to determine
# valid move for ice clicked.
# -----------------------------------------------------------------------------
def solid_ice(r, c):
    # Determine color of square: white = solid ice, else = broken
    return board[r][c].config['fill'] == SOLID

# =============================================================================

def main():
    global win, info_msg, btn_Quit, btn_Reset, board, row, col, player, \
           players, r, c, x, y, win2, won_msg, splash_msg, winner
    
    # Start with splash screen
    splash_screen()
    
    # Set up window, messages, board, and buttons
    win = GraphWin(WIN_TITLE, WIN_W, WIN_H)
    info_msg = Text(Point(130, WIN_H - BOTTOM//2), "ICE BREAKER")
    info_msg.draw(win)
    info_msg.setSize(13)
    board_create()
    
    btn_Quit = btn_create(win, WIN_W -80, 
                          WIN_H-BOTTOM+20, 60, 20, 'QUIT')
    btn_Reset = btn_create(win, WIN_W -80, 
                           WIN_H-BOTTOM+45, 60, 20, 'RESET')    
    
    mouse_msg = Text(Point(130, WIN_H-30), "Move Piece")
    mouse_msg.draw(win)
    mouse_msg.setSize(13)

    #--------------------------------------------------------------------------
    # MAIN GUI LOOP
    while True:
        
        info_msg.setText(f"PLAYER: {player}: "
                         f"[{players[player][1]}, {players[player][0]}]")        
        
        pt = win.getMouse()                         # Wait for get mouse click
        x, y = pt.getX(), pt.getY()                  
        
        # If button Quit clicked, sets msg to 'Bye Bye!'
        if btn_clicked(pt, btn_Quit):
            info_msg.setText("Bye Bye!")            
            mouse_msg.setText("")
            # sleep for pause before win.close(), better UX
            sleep(1)
            break
        
        # If button Reset clicked, sets msg to 'Reset' and resets game board
        if btn_clicked(pt, btn_Reset):
            info_msg.setText("Resetting...")
            reset_game()    
            info_msg.setText("Reset")
            #sleep before continuing to next turn
            sleep(1)
            continue
        
        # Get the coordinates of the mouse click
        c, r = int((pt.x // (SQ_SZ+GAP))) , int((pt.y // (SQ_SZ+GAP)))
        #mouse_msg.setText(f"{int(pt.x), int(pt.y)} = {c, r}")    # Dev check
        
        
        # Current player moves and breaks ice
        if valid_move(r, c):
            
            rp, cp = players[player][:2]          # current player's position
            # Move player's image
            players[player][2].move( (SQ_SZ+GAP)*(c-cp), (SQ_SZ+GAP)*(r-rp) ) 
            players[player][:2] = [ r, c ]        # update player coordinates
            mouse_msg.setText('Break Ice')        # indicates break ice turn
            
            # Break Ice
            pt = win.getMouse()
            c, r = int(pt.x // (SQ_SZ+GAP)), int(pt.y // (SQ_SZ+GAP))
            board[r][c].setFill(BROKEN)           # set ice fill to broken
            winner = player                         
            player = 1 - player                   # switch to other player
            mouse_msg.setText('Move Piece')       # indicates player to move
            continue
        else:
            mouse_msg.setText("NOT VALID")
        
        # If player cannot move, indicate the other player has won
        if not can_move():
            
            # set message to winning player
            info_msg.setText(f"GAME OVER\nPlayer {1-player} HAS WON\n")
                             #f"(Player {players[player][:2]})"  # Dev Check
            mouse_msg.setText('')
            # sleep before opening prompt window
            sleep(.5)
            
            # open prompt window and ask if players want to play again
            if prompt_window("WOOHOO!\nResetting Game...",\
                             "FINE THEN!\nQuitter...", \
                             f"Congrats, Player {winner}!! \nPlay Again?"):
                # if True then reset game and continue playing
                reset_game()
                continue
            
            # if False, quit and close all windows
            else:
                break
            
        # -----------------------------------------------------------------
            
    # =========================================================================
    
    # Removed get mouse for UX. Should close quicker when Quit Btns clicked
    win.close()
  
# Runs the main function    
main()