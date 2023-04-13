import random
import pickle
import gzip
import os

class Board():
  def __init__(self):
    self.board = [0, 0, 0,
                  0, 0, 0,
                  0, 0, 0]

  def player1Move(self, tile):
    self.board[tile] = 1
  
  def player2Move(self, tile):
    self.board[tile] = 2
  

  def checkWin(self):
    b = [[self.board[0], self.board[1], self.board[2]],
         [self.board[3], self.board[4], self.board[5]],
         [self.board[6], self.board[7], self.board[8]]]

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

  def resetBoard(self):
      self.board = [0, 0, 0,
                  0, 0, 0,
                  0, 0, 0]
  
  def printBoard(self):
    pBoard = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    i = 0
    for t in self.board:
      if t == 0:
        pBoard[i] = ' '
      if t == 1:
        pBoard[i] = 'O'
      if t == 2:
        pBoard[i] = 'X'
      i += 1
    print(pBoard[0] + ' | ' + pBoard[1] + ' | ' + pBoard[2])
    print('---------')
    print(pBoard[3] + ' | ' + pBoard[4] + ' | ' + pBoard[5])
    print('---------')
    print(pBoard[6] + ' | ' + pBoard[7] + ' | ' + pBoard[8])

def playerMove(Game, player):
    tile = -1
    while not (Game.board[tile] == 0 and tile >= 0 and tile < 9):
        try:
            tile = int(input("Space: "))-1
            s = Game.board[tile]
        except:
            print("Enter a number 1-9")
            tile = -1
      
    if player == 1: Game.player1Move(tile)
    if player == 2: Game.player2Move(tile)
    Game.printBoard()

class Qagent:
    def __init__(self, Game, alpha, gamma, epsilon, startingQ, name=None):
        self.Game = Game
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.startingQs = [startingQ, startingQ, startingQ, startingQ, startingQ, startingQ, startingQ, startingQ, startingQ]
        self.name = name
        if name and os.path.exists(f"Tables/{name}.pkl.gz"):
            f = gzip.open(f"Tables/{name}.pkl.gz", 'rb')
            self.Q = pickle.load(f, encoding='latin1')
            f.close()
        else:
            self.Q = {}

    def boardToState(self):
        state = 0
        for i in range(9):
            state += self.Game.board[i] * (3 ** i)
        return state;

    def pickA(self, s):
        while True:
            if s in self.Q and random.random()>self.epsilon:
                a = self.Q[s].index(max(self.Q[s]))
            else:
                a = random.randint(0, 8)
            if self.Game.board[a] == 0:
                break
        return a;

    def trainWPlayer(self):
        playerMove(self.Game, 1)
        state = self.boardToState()
        while self.Game.checkWin() == 0:
            action = self.pickA(state)
            self.Game.player2Move(action)
            self.Game.printBoard()

            if self.Game.checkWin() == 2:
                reward = 100
            elif 0 not in self.Game.board:
                reward = 0
            else:
                playerMove(self.Game, 1)

            if self.Game.checkWin() == 1:
                reward = -100
            elif 0 not in self.Game.board:
                reward = 0
            else:
                reward = 1

            newState = self.boardToState()
            if state not in self.Q:
                self.Q[state] = self.startingQs
            if newState not in self.Q:
                self.Q[newState] = self.startingQs
               
            self.Q[state][action] += self.alpha*(reward + self.gamma * max(self.Q[newState]) - self.Q[state][action])

            state = newState
        self.saveQ()
        self.Game.resetBoard()

    def trainWAgent(self, agent, printGame=False):
        looped = False
        while True:
            newState1 = self.boardToState()
            if self.Game.checkWin() == 2:
                if state1 not in agent.Q:
                    agent.Q[state1] = self.startingQs
                if newState1 not in agent.Q:
                    agent.Q[newState1] = self.startingQs
                agent.Q[state1][action1] += agent.alpha*(-100 + agent.gamma * max(agent.Q[newState1]) - agent.Q[state1][action1])

                if state2 not in self.Q:
                    self.Q[state2] = self.startingQs
                if newState2 not in self.Q:
                    self.Q[newState2] = self.startingQs
                self.Q[state2][action2] += self.alpha*(100 + self.gamma * max(self.Q[newState2]) - self.Q[state2][action2])
                break
            elif 0 not in self.Game.board:
                if state1 not in agent.Q:
                    agent.Q[state1] = self.startingQs
                if newState1 not in agent.Q:
                    agent.Q[newState1] = self.startingQs
                agent.Q[state1][action1] += agent.alpha*(agent.gamma * max(agent.Q[newState1]) - agent.Q[state1][action1])

                if state2 not in self.Q:
                    self.Q[state2] = self.startingQs
                if newState2 not in self.Q:
                    self.Q[newState2] = self.startingQs
                self.Q[state2][action2] += self.alpha*(self.gamma * max(self.Q[newState2]) - self.Q[state2][action2])
                break
            else:
                if looped:
                    if state1 not in agent.Q:
                        agent.Q[state1] = self.startingQs
                    if newState1 not in agent.Q:
                        agent.Q[newState1] = self.startingQs
                    agent.Q[state1][action1] += agent.alpha*(1 + agent.gamma * max(agent.Q[newState1]) - agent.Q[state1][action1])

                state1 = newState1
                action1 = agent.pickA(state1)
                self.Game.player1Move(action1)
                if printGame: self.Game.printBoard()
            
            newState2 = self.boardToState()
            if self.Game.checkWin() == 1:
                if state1 not in agent.Q:
                    agent.Q[state1] = self.startingQs
                if newState1 not in agent.Q:
                    agent.Q[newState1] = self.startingQs
                agent.Q[state1][action1] += agent.alpha*(100 + agent.gamma * max(agent.Q[newState1]) - agent.Q[state1][action1])

                if state2 not in self.Q:
                    self.Q[state2] = self.startingQs
                if newState2 not in self.Q:
                    self.Q[newState2] = self.startingQs
                self.Q[state2][action2] += self.alpha*(-100 + self.gamma * max(self.Q[newState2]) - self.Q[state2][action2])
                break
            elif 0 not in self.Game.board:
                if state1 not in agent.Q:
                    agent.Q[state1] = self.startingQs
                if newState1 not in agent.Q:
                    agent.Q[newState1] = self.startingQs
                agent.Q[state1][action1] += agent.alpha*(agent.gamma * max(agent.Q[newState1]) - agent.Q[state1][action1])

                if state2 not in self.Q:
                    self.Q[state2] = self.startingQs
                if newState2 not in self.Q:
                    self.Q[newState2] = self.startingQs
                self.Q[state2][action2] += self.alpha*(self.gamma * max(self.Q[newState2]) - self.Q[state2][action2])
                break
            else:
                if looped:
                    if state2 not in self.Q:
                        self.Q[state2] = self.startingQs
                    if newState2 not in self.Q:
                        self.Q[newState2] = self.startingQs
                    self.Q[state2][action2] += self.alpha*(1 + self.gamma * max(self.Q[newState2]) - self.Q[state2][action2])

                state2 = newState2
                action2 = self.pickA(state2)
                self.Game.player2Move(action2)
                if printGame: self.Game.printBoard()

            
            looped = True
        agent.saveQ()
        self.saveQ()
        Game.resetBoard()



    def saveQ(self):
        f = gzip.open(f'Tables/{self.name}.pkl.gz', 'w')
        pickle.dump(self.Q, f)
        f.close()
        #print('Q Table saved')


def negmax(board):
  if board.board.count(1) == board.board.count(2):
    player = 1
  else:
    player = 2

  board2 = Board()
  for x in range(9):
    board2.board = board.board
    if board2.board[x] == 0:
      board2.board[x] = player


Game = Board()
agent3 = Qagent(Game, 0.9, 0.75, 0.1, 0, "Table 3")
agent4 = Qagent(Game, 0.9, 0.75, 0.1, 0, "Table 4")

for i in range(2000000):
    agent4.trainWAgent(agent3)
    if i % 1000 == 0: print("Training session: " + str(i) + " complete")