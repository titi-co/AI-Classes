# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from queue import Empty
import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem: SearchProblem):

    # Stack of nodes to explore
    ft = util.Stack()
    # List of visited nodes
    visited = []
    # Start node is defined and pushed
    initState = problem.getStartState()
    initNode = (initState, [])

    ft.push(initNode)

    while not ft.isEmpty():
        # explore the last added node
        state, actions = ft.pop()

        # check if node is not already visited
        if state not in visited:
            # mask as visited
            visited.append(state)

            # check if this state is the goal state and returns its actions
            if problem.isGoalState(state):
                return actions
            else:
                # get the list of possivle sucessors from this current node
                successors = problem.getSuccessors(state)

                # push the sucessors to the frontier
                for successState, successAction, successCost in successors:
                    nextAction = actions + [successAction]
                    nextNode = (successState, nextAction)
                    ft.push(nextNode)

    return actions


def breadthFirstSearch(problem: SearchProblem):

    # Stack of nodes to explore
    ft = util.Queue()
    # List of visited nodes
    visited = []
    # Start node is defined and pushed
    initState = problem.getStartState()
    initNode = (initState, [], 0)

    ft.push(initNode)

    while not ft.isEmpty():
        # explore the last added node
        state, actions, cost = ft.pop()

        # check if node is not already visited
        if state not in visited:
            # mask as visited
            visited.append(state)

            # check if this state is the goal state and returns its actions
            if problem.isGoalState(state):
                return actions
            else:
                # get the list of possivle sucessors from this current node
                successors = problem.getSuccessors(state)

                # push the sucessors to the frontier
                for successState, successAction, successCost in successors:
                    nextAction = actions + [successAction]
                    nextCost = cost + successCost
                    nextNode = (successState, nextAction, nextCost)
                    ft.push(nextNode)

    return actions


def uniformCostSearch(problem: SearchProblem):
    # Stack of nodes to explore
    ft = util.PriorityQueue()
    # List of visited nodes
    visited = {}
    # Start node is defined and pushed
    initState = problem.getStartState()
    initNode = (initState, [], 0)

    ft.push(initNode, 0)

    while not ft.isEmpty():
        # explore the last added node
        state, actions, cost = ft.pop()

        # check if node is not already visited
        if (state not in visited) or (cost < visited[state]):
            # mask as visited
            visited[state] = cost

            # check if this state is the goal state and returns its actions
            if problem.isGoalState(state):
                return actions
            else:
                # get the list of possivle sucessors from this current node
                successors = problem.getSuccessors(state)

                # push the sucessors to the frontier
                for successState, successAction, successCost in successors:
                    nextAction = actions + [successAction]
                    nextCost = cost + successCost
                    nextNode = (successState, nextAction, nextCost)
                    ft.update(nextNode, nextCost)

    return actions


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    # Stack of nodes to explore
    ft = util.PriorityQueue()

    visited = []  # holds (state, cost)

    initState = problem.getStartState()
    initNode = (initState, [], 0)

    ft.push(initNode, 0)

    while not ft.isEmpty():
        # explore the last added node
        state, actions, cost = ft.pop()

        currNode = (state, cost)
        visited.append(currNode)

        if problem.isGoalState(state):
            return actions
        else:
            # get the list of possivle sucessors from this current node
            successors = problem.getSuccessors(state)

            # examine each successor
            for successState, successAction, successCost in successors:
                nextAction = actions + [successAction]
                nextCost = problem.getCostOfActions(nextAction)
                nextNode = (successState, nextAction, nextCost)

                explored = False
                for e in visited:
                    visitedState, visitedCost = e

                    if (successState == visitedState) and (nextCost >= visitedCost):
                        explored = True

                if not explored:
                    ft.push(nextNode, nextCost +
                            heuristic(successState, problem))
                    visited.append((successState, nextCost))

    return actions


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
