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
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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
        scoreDistance = 0

        newFood = newFood.asList()
        ghostPositions = currentGameState.getGhostPositions()
        distancesGhost = []

        for index in ghostPositions:
            distancesGhost.append(manhattanDistance(newPos, index))

        if len(distancesGhost) > 0:
            distanceGhost = min(distancesGhost)

        distancesFood = []
        for food in newFood:
            distancesFood.append(manhattanDistance(food, newPos))

        if len(distancesFood) > 0:
            if min(distancesFood) != 0:
                scoreDistance += 1 / (min(distancesFood) * 0.5)

        if distanceGhost < 2:
            scoreDistance = -200
        else:
            scoreDistance += 150

        if action == "stop":
            return successorGameState.getScore()
        return successorGameState.getScore() + scoreDistance


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

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
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

        def max_val(agent, depth, gameState):
            maxVal = float("-inf")
            for newState in gameState.getLegalActions(agent):
                maxVal = max(maxVal, minimax(1, depth, gameState.generateSuccessor(agent, newState)))
            return maxVal

        def min_val(nextAgent, agent, depth, gameState):
            minVal = float("inf")
            for newState in gameState.getLegalActions(agent):
                minVal = min(minVal, minimax(nextAgent, depth, gameState.generateSuccessor(agent, newState)))
            return minVal

        def minimax(agent, depth, gameState):
            if gameState.isLose() or gameState.isWin() or depth == self.depth:
                return self.evaluationFunction(gameState)
            nextAgent = agent + 1

            if nextAgent == gameState.getNumAgents():
                nextAgent = 0

            if nextAgent == 0:
                depth += 1

            if agent == 0:
                return max_val(agent, depth, gameState)
            else:
                return min_val(nextAgent, agent, depth, gameState)

        legalMoves = gameState.getLegalActions(0)
        maxium = float("-inf")
        actionDir = Directions.RIGHT
        for action in legalMoves:
            score = minimax(1, 0, gameState.generateSuccessor(0, action))
            if score > maxium:
                maxium = score
                actionDir = action
        return actionDir


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def max_val(agent, depth, gameState, a, b):
            maxVal = float("-inf")
            for newState in gameState.getLegalActions(agent):
                maxVal = max(maxVal, AlphaBeta(1, depth, gameState.generateSuccessor(agent, newState), a, b))
                if maxVal > b:
                    break
                a = max(a, maxVal)
            return maxVal

        def min_val(nextAgent, agent, depth, gameState, a, b):
            minVal = float("inf")
            for newState in gameState.getLegalActions(agent):
                minVal = min(minVal, AlphaBeta(nextAgent, depth, gameState.generateSuccessor(agent, newState), a, b))
                if minVal < a:
                    break
                b = min(b, minVal)
            return minVal

        def AlphaBeta(agent, depth, gameState, a, b):
            if gameState.isLose() or gameState.isWin() or depth == self.depth:
                return self.evaluationFunction(gameState)
            nextAgent = agent + 1

            if nextAgent == gameState.getNumAgents():
                nextAgent = 0

            if nextAgent == 0:
                depth += 1

            if agent == 0:
                return max_val(agent, depth, gameState, a, b)
            else:
                return min_val(nextAgent, agent, depth, gameState, a, b)

        legalMoves = gameState.getLegalActions(0)
        utility = float("-inf")
        actionDir = Directions.RIGHT
        a = float("-inf")
        b = float("inf")
        for action in legalMoves:
            score = AlphaBeta(1, 0, gameState.generateSuccessor(0, action), a, b)
            if score > utility:
                utility = score
                actionDir = action
            if utility > b:
                return action
            a = max(a, utility)
        return actionDir


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

        def max_val(agent, depth, gameState):
            maxVal = float("-inf")
            for newState in gameState.getLegalActions(agent):
                maxVal = max(maxVal, Expectimax(1, depth, gameState.generateSuccessor(agent, newState)))
            return maxVal

        def exp_val(nextAgent, agent, depth, gameState):
            expVal = 0
            for newState in gameState.getLegalActions(agent):
                expVal += Expectimax(nextAgent, depth, gameState.generateSuccessor(agent, newState))
            return float(expVal) / float(len(gameState.getLegalActions(agent)))

        def Expectimax(agent, depth, gameState):
            if gameState.isLose() or gameState.isWin() or depth == self.depth:
                return self.evaluationFunction(gameState)
            nextAgent = agent + 1

            if nextAgent == gameState.getNumAgents():
                nextAgent = 0

            if nextAgent == 0:
                depth += 1

            if agent == 0:
                return max_val(agent, depth, gameState)
            else:
                return exp_val(nextAgent, agent, depth, gameState)

        legalMoves = gameState.getLegalActions(0)
        maxium = float("-inf")
        actionDir = Directions.RIGHT
        for action in legalMoves:
            score = Expectimax(1, 0, gameState.generateSuccessor(0, action))
            if score > maxium:
                maxium = score
                actionDir = action
        return actionDir


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()

    foodMulti = 12.50
    ghostMulti = -60.00
    capsules = 95
    if currentGameState.isWin():
        return 10000.00
    # if currentGameState.isLose():
    #     return -10000.00
    newFood = newFood.asList()
    foodTarget = []
    for food in newFood:
        foodTarget.append(manhattanDistance(newPos, food))
    foodTarget = min(foodTarget)
    ghostPositions = currentGameState.getGhostPositions()
    distanceGhost = manhattanDistance(newPos, ghostPositions[0])

    if distanceGhost < 3:
        distanceGhost = 1000
    caps = currentGameState.getCapsules()
    capsPoint = 0
    if len(caps) > 0:
        for i in range(len(caps)):
            if capsPoint < 1.00/manhattanDistance(caps[i], newPos):
                capsPoint = 1.00 / manhattanDistance(caps[i], newPos)

    return currentGameState.getScore() + 1.00/foodTarget * foodMulti + distanceGhost * ghostMulti + capsPoint * capsules


# Abbreviation
better = betterEvaluationFunction
