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
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    from util import Stack
    stack_xy = Stack()

    visited = []
    path = []

    if problem.isGoalState(problem.getStartState()):
        return []

    stack_xy.push((problem.getStartState(),[]))

    while(True):

        if stack_xy.isEmpty():
            return []

        xy,path = stack_xy.pop()
        visited.append(xy)

        if problem.isGoalState(xy):
            return path

        successors = problem.getSuccessors(xy)
        if successors:
            for item in successors:
                if item[0] not in visited:
                    new_path = path + [item[1]]
                    stack_xy.push((item[0],new_path))

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue

    visited = []
    path = []

    queue_xy = Queue()
    if problem.isGoalState(problem.getStartState()):
        return []

    queue_xy.push((problem.getStartState(),path))

    while(True):
        if queue_xy.isEmpty():
            return []

        xy,path = queue_xy.pop()

        visited.append(xy)

        if problem.isGoalState(xy):
            return path

        successors = problem.getSuccessors(xy)
        if successors:
            for item in successors:
                if item[0] not in visited and item[0] not in (state[0] for state in queue_xy.list):
                    newPath = path + [item[1]]
                    queue_xy.push((item[0],newPath))

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue

    visited = []
    path = []
    queue_xy = PriorityQueue()

    if problem.isGoalState(problem.getStartState()):
        return []

    queue_xy.push((problem.getStartState(),path), 0)

    while(True):
        if queue_xy.isEmpty():
            return []

        xy,path = queue_xy.pop()
        visited.append(xy)

        if problem.isGoalState(xy):
            return path

        successors = problem.getSuccessors(xy)
        if successors:
            for item in successors:
                if item[0] not in visited and (item[0] not in (state[2][0] for state in queue_xy.heap)):
                    new_path = path + [item[1]]
                    priority = problem.getCostOfActions(new_path)
                    queue_xy.push((item[0],new_path), priority)
                elif item[0] not in visited and (item[0] in (state[2][0] for state in queue_xy.heap)):
                    for state in queue_xy.heap:
                        if state[2][0] == item[0]:
                            old_priority = problem.getCostOfActions(state[2][1])
                    new_path = path + [item[1]]
                    new_priority = problem.getCostOfActions(new_path)
                    if new_priority < old_priority:
                        queue_xy.update((item[0],new_path), new_priority)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0
from util import PriorityQueue
class MyPriorityQueueWithFunction(PriorityQueue):
    """
    Implements a priority queue with the same push/pop signature of the
    Queue and the Stack classes. This is designed for drop-in replacement for
    those two classes. The caller has to provide a priority function, which
    extracts each item's priority.
    """
    def  __init__(self, problem, priorityFunction):
        "priorityFunction (item) -> priority"
        self.priorityFunction = priorityFunction      # store the priority function
        PriorityQueue.__init__(self)        # super-class initializer
        self.problem = problem
    def push(self, item, heuristic):
        "Adds an item to the queue with priority from the priority function"
        PriorityQueue.push(self, item, self.priorityFunction(self.problem,item,heuristic))

# Calculate f(n) = g(n) + h(n) #
def f(problem,state,heuristic):
    return problem.getCostOfActions(state[1]) + heuristic(state[0],problem)

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    queue_xy = MyPriorityQueueWithFunction(problem,f)

    path = []
    visited = []

    if problem.isGoalState(problem.getStartState()):
        return []

    queue_xy.push((problem.getStartState(),[]),heuristic)

    while(True):
        if queue_xy.isEmpty():
            return []

        xy,path = queue_xy.pop()

        if xy in visited:
            continue

        visited.append(xy)

        if problem.isGoalState(xy):
            return path

        successors = problem.getSuccessors(xy)

        if successors:
            for item in successors:
                if item[0] not in visited:
                    newPath = path + [item[1]]
                    queue_xy.push((item[0], newPath), heuristic)
# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
