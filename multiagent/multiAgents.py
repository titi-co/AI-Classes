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
import random
import util

from game import Agent
from pacman import GameState
import math


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gamegameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the gameState, like the
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
        newScaredTimes = [
            ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()


def scoreEvaluationFunction(currentGameState: GameState):
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

    def _min(self, gameState, depth, agent):
        agentActions = gameState.getLegalActions(agent)
        scores = []

        for action in agentActions:
            succState = gameState.generateSuccessor(agent, action)

            if agent == gameState.getNumAgents() - 1:
                scores.append(self.MiniMax(succState, depth -
                              1, 0, True)[0])
            else:
                scores.append(self.MiniMax(succState, depth,
                              agent + 1, False)[0])

        minScore = min(scores)
        minIndex = [i for i, score in enumerate(scores) if score == minScore]

        succAction = agentActions[random.choice(minIndex)]

        return minScore, succAction

    def _max(self, state, depth, agent):
        agentActions = state.getLegalActions(agent)
        scores = []

        for action in agentActions:
            succState = state.generateSuccessor(agent, action)
            scores.append(self.MiniMax(succState, depth,
                          agent + 1, False)[0])

        maxScore = max(scores)
        maxIndex = [i for i, score in enumerate(scores) if score == maxScore]
        succAction = agentActions[random.choice(maxIndex)]

        return maxScore, succAction

    def MiniMax(self, state, depth, agent, max):
        if depth == 0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state), Directions.STOP

        if max:
            return self._max(state, depth, agent)
        else:
            return self._min(state, depth, agent)

    def getAction(self, gameState):

        succAction = self.MiniMax(gameState, self.depth, 0, True)[1]
        return succAction


class AlphaBetaAgent(MultiAgentSearchAgent):

    def _min(self, gameState, depth, alpha, beta, agent):
        agentActions = gameState.getLegalActions(agent)
        scores = []
        minScore = math.inf

        for action in agentActions:
            succState = gameState.generateSuccessor(agent, action)

            if agent == gameState.getNumAgents() - 1:
                score = self.MiniMax(
                    succState, depth - 1, alpha, beta, 0, True)[0]
            else:
                score = self.MiniMax(
                    succState, depth, alpha, beta, agent + 1, False)[0]
            scores.append(score)
            minScore = min(scores)
            beta = min(beta, minScore)

            if beta < alpha:
                break

        minIndex = [i for i, score in enumerate(scores) if score == minScore]
        succAction = agentActions[random.choice(minIndex)]

        return minScore, succAction

    def _max(self, gameState, depth, alpha, beta, agent):
        agentActions = gameState.getLegalActions(agent)
        scores = []
        maxScore = -math.inf

        for action in agentActions:
            succState = gameState.generateSuccessor(agent, action)
            score = self.MiniMax(succState, depth, alpha,
                                 beta, agent + 1, False)[0]
            scores.append(score)
            maxScore = max(scores)
            alpha = max(alpha, maxScore)

            if alpha > beta:
                break

        maxIndex = [i for i, score in enumerate(scores) if score == maxScore]
        succAction = agentActions[random.choice(maxIndex)]

        return maxScore, succAction

    def MiniMax(self, gameState, depth, alpha=-math.inf, beta=math.inf, agent=0, max=True):
        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), Directions.STOP

        if max:
            return self._max(gameState, depth, alpha, beta, agent)
        else:
            return self._min(gameState, depth, alpha, beta, agent)

    def getAction(self, gameState):

        succAction = self.MiniMax(gameState, self.depth)[1]
        return succAction
        util.raiseNotDefined()


class Expecti_max(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
