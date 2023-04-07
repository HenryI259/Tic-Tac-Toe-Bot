class Board():
  def __init__(self):
    self.board = [[0, 0, 0],
                  [0, 0, 0],
                  [0, 0, 0]]

  def player1Move(self, x, y):
    self.board[y][x] = 1
  
  def player2Move(self, x, y):
    self.board[y][x] = 2
  

  def checkWin(self):
    b = self.board
    for y in b:
      if y[0] == 1 and y[1] == 1 and y[2] == 1:
        return 1
      elif y[0] == 2 and y[1] == 2 and y[2] == 2:
        return 2
    for x in range(3):
      if b[0][x] == 1 and b[1][x] == 1 and b[2][x] == 1:
        return 1
      elif b[0][x] == 2 and b[1][x] == 2 and b[2][x] == 2:
        return 2
    if b[0][0] == 1 and b[1][1] == 1 and b[2][2] == 1:
      return 1
    elif b[0][0] == 2 and b[1][1] == 2 and b[2][2] == 2:
      return 2
    elif b[0][2] == 1 and b[1][1] == 1 and b[2][0] == 1:
      return 1
    elif b[0][2] == 2 and b[1][1] == 2 and b[2][0] == 2:
      return 2
    else:
      return 0
  
  def printBoard(self):
    pBoard = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    i = 0
    for y in self.board:
      for x in y:
        if x == 0:
          pBoard[i] = ' '
        if x == 1:
          pBoard[i] = 'O'
        if x == 2:
          pBoard[i] = 'X'
        i += 1
    print(pBoard[0] + ' | ' + pBoard[1] + ' | ' + pBoard[2])
    print('---------')
    print(pBoard[3] + ' | ' + pBoard[4] + ' | ' + pBoard[5])
    print('---------')
    print(pBoard[6] + ' | ' + pBoard[7] + ' | ' + pBoard[8])

Game = Board()
while Game.checkWin() == 0:
  print("Player 1")
  x = -1
  y = -1
  while not (Game.board[y][x] == 0 and (x == 0 or x == 1 or x == 2) and (y == 0 or y == 1 or y == 2)):
    try:
      x = int(input("x: "))-1
      y = int(input("y: "))-1
      s = Game.board[y][x]
    except:
      print("Enter a number 1-3")
      
  board.player2Move(x, y)
  board.printBoard()
  
  print("Player 2")
  x = -1
  y = -1
  while not (Game.board[y][x] == 0 and (x == 0 or x == 1 or x == 2) and (y == 0 or y == 1 or y == 2)):
    try:
      x = int(input("x: "))-1
      y = int(input("y: "))-1
      s = Game.board[y][x]
    except:
      print("Enter a number 1-3")
      
  board.player2Move(x, y)
  board.printBoard()