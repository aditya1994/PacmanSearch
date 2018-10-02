# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        score = successorGameState.getScore()

        food = newFood.asList()

        # If all the food is eater return high score
        if(len(food) == 0):
            return 100000

        #Finding closest food dot
        foodDis = 10000
        for dot in food:
            if util.manhattanDistance(dot, newPos) < foodDis:
                foodDis = util.manhattanDistance(dot, newPos)

        # Get distance from nearest Ghost
        ghostPos = successorGameState.getGhostPosition(1)
        disFromGhost = util.manhattanDistance(newPos, ghostPos)

        if disFromGhost <=2:
            # If near Ghost, run away
            score = score - 3*(10 - disFromGhost)
        else:
            # Plus points for eating food
            score  = score + (100 - foodDis)/2

        return score



def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        # Pacman position is 0

        #First call to min function
        act = self.max_func(gameState, 1, 0)
        return act

    def max_func(self, gameState, depth, agent_num):

        if gameState.isWin() or gameState.isLose():
            return gameState.getScore()

        Best_score = -100000000
        Best_action = ' '
        # Checking all the min states

        for action in gameState.getLegalActions(agent_num):
            child = gameState.generateSuccessor(agent_num, action)

            score = self.min_func(child, depth, agent_num + 1)
            if score > Best_score:
                Best_score = score
                Best_action = action
        if depth == 1:
            return Best_action
        else:
            return Best_score

    def min_func(self, gameState, depth, agent_num):
        if gameState.isWin() or gameState.isLose():
            return gameState.getScore()

        Best_score = 100000000


        for action in gameState.getLegalActions(agent_num):
            child = gameState.generateSuccessor(agent_num, action)
            if agent_num == gameState.getNumAgents() -1:
                if depth == self.depth:
                    score = self.evaluationFunction(child)
                else:
                    score = self.max_func(child, depth+1, 0)

            else:
                score =  self.min_func(child, depth, agent_num + 1)
            if score < Best_score:
                Best_score = score

        return Best_score





class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        act = self.max_func(gameState, 1, 0, -10000000, 10000000)
        return act

    def max_func(self, gameState, depth, agent_num, alpha , beta):

        if gameState.isWin() or gameState.isLose():
            return gameState.getScore()

        Best_score = -100000000
        Best_action = ' '
        # Checking all the min states

        for action in gameState.getLegalActions(agent_num):
            child = gameState.generateSuccessor(agent_num, action)

            score = self.min_func(child, depth, agent_num + 1, alpha, beta)
            if score > Best_score:
                Best_score = score
                Best_action = action
            if alpha < Best_score:
                alpha = Best_score
            if Best_score > beta:
                return Best_score

        if depth == 1:
            return Best_action
        else:
            return Best_score

    def min_func(self, gameState, depth, agent_num, alpha , beta):
        if gameState.isWin() or gameState.isLose():
            return gameState.getScore()

        Best_score = 100000000

        for action in gameState.getLegalActions(agent_num):
            child = gameState.generateSuccessor(agent_num, action)
            if agent_num == gameState.getNumAgents() - 1:
                if depth == self.depth:
                    score = self.evaluationFunction(child)
                else:
                    score = self.max_func(child, depth + 1, 0, alpha , beta)

            else:
                score = self.min_func(child, depth, agent_num + 1, alpha, beta)
            if score < Best_score:
                Best_score = score
            if beta > Best_score:
                beta = Best_score
            if Best_score < alpha:
                return Best_score

        return Best_score

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        act = self.max_func(gameState, 1, 0)
        return act

    def max_func(self, gameState, depth, agent_num):

        if gameState.isWin() or gameState.isLose():
            return gameState.getScore()

        Best_score = -100000000
        Best_action = ' '
        # Checking all the expected states

        for action in gameState.getLegalActions(agent_num):
            child = gameState.generateSuccessor(agent_num, action)

            score = self.exp_func(child, depth, agent_num + 1)
            if score > Best_score:
                Best_score = score
                Best_action = action
        if depth == 1:
            return Best_action
        else:
            return Best_score

    def exp_func(self, gameState, depth, agent_num):
        if gameState.isWin() or gameState.isLose():
            return gameState.getScore()

        Best_score = 0
        prob = 1.0 / len(gameState.getLegalActions(agent_num))

        for action in gameState.getLegalActions(agent_num):

            child = gameState.generateSuccessor(agent_num, action)
            if agent_num == gameState.getNumAgents() - 1:
                if depth == self.depth:
                    score = self.evaluationFunction(child)
                else:
                    score = self.max_func(child, depth + 1, 0)

            else:
                score = self.exp_func(child, depth, agent_num + 1)
            Best_score += score*prob

        return Best_score


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    score = currentGameState.getScore()

    food = newFood.asList()

    # If all the food is eater return high score
    if (len(food) == 0):
        return 100000
    if currentGameState.isWin():
        return 1000000
    if currentGameState.isLose():
        return -1000000

    # Finding closest food dot
    foodDis = 100000
    for dot in food:
        Disfood = util.manhattanDistance(dot, newPos)
        if  Disfood< foodDis:
            foodDis = Disfood

    # Get distance from nearest Ghost

    capPos = currentGameState.getCapsules()
    nearestCap = 100000
    for cap in capPos:
        nearCap = util.manhattanDistance(cap, newPos)
        if  nearCap< nearestCap:
            nearestCap = nearCap


    ghostPos = currentGameState.getGhostPosition(1)
    disFromGhost = util.manhattanDistance(newPos, ghostPos)
    score = score + 5*sum(newScaredTimes)



    if sum(newScaredTimes) == 0:
        if disFromGhost <= 1:
             # If near Ghost, run away
             score = score - 10 * (5 - disFromGhost)
        else:
            # Plus points for eating food
            score = score + (100- foodDis)/2
            score = score + 40 * (1 / nearestCap)
    else:
        score = score + (100 - foodDis)/1.5
        score = score + 50 * (1 / nearestCap)



    return score




better = betterEvaluationFunction

