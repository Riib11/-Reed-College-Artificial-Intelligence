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
    # "*** YOUR CODE HERE ***"

    startState = problem.getStartState()
    goalState = None

    # new stack
    S = util.Stack()
    prevs = {}

    # initialize with startState
    S.push(startState)
    prevs[str(startState)] = (None, 0)

    # keep track of visited nodes
    visited = []
    
    # depth-first search rest of nodes
    while not S.isEmpty():
        state = S.pop()
        visited.append(str(state))
        # at goal?
        if problem.isGoalState(state):
            goalState = state
            break
        # check successors
        successors = problem.getSuccessors(state)
        for (nextState, direction, cost) in successors:
            if not str(nextState) in visited:
                S.push(nextState)
                prevs[str(nextState)] = (state, direction)

    # recover path from `prevs` record
    path = []
    state = goalState
    while state != startState:
        prevState, direction = prevs[str(state)]
        path.insert(0, direction)
        state = prevState

    return path



def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    # "*** YOUR CODE HERE ***"

    startState = problem.getStartState()
    goalState = None

    # new stack
    Q = util.Queue()
    prevs = {}

    # initialize with startState
    Q.push(startState)
    prevs[str(startState)] = (None, 0)
    
    # breadth-first search rest of nodes
    while not Q.isEmpty():
        state = Q.pop()
        # at goal?
        if problem.isGoalState(state):
            goalState = state
            break
        # check successors
        for (nextState, direction, cost) in problem.getSuccessors(state):
            if not str(nextState) in prevs:
                Q.push(nextState)
                prevs[str(nextState)] = (state, direction)

    # recover path from `prevs` record
    path = []
    state = goalState
    while state != startState:
        prevState, direction = prevs[str(state)]
        path.insert(0, direction)
        state = prevState

    return path
    

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    # "*** YOUR CODE HERE ***"

    #
    # containers
    Q         = util.PriorityQueue() # Priority<Node : PathCost>
    prevs     = {}                   # Node => (State, Dir)
    pathcosts = {}                   # Node => PathCost
    visited   = []                   # [Node]

    def make_str_getter(d): return (lambda k: d[str(k)])
    def make_str_setter(d):
        def f(k,v): d[str(k)] = v
        return f

    getPrev = make_str_getter(prevs)
    setPrev = make_str_setter(prevs)
    getPathCost = make_str_getter(pathcosts)
    setPathCost = make_str_setter(pathcosts)
    visit = lambda x: visited.append(x)

    def getTakenDir(sourceState, targetState, successors):
        for (state, direction, _) in successors:
            if state == targetState:
                return direction

    #
    # initialize
    startState = problem.getStartState()
    goalState = None

    #
    # visit start
    Q.push(startState , 0)
    setPrev(startState, (None, None))
    setPathCost(startState, 0)
    visit(startState)

    while not Q.isEmpty():
        currState = Q.pop()
        currPathCost = getPathCost(currState)

        if problem.isGoalState(currState):
            goalState = currState
            break

        visit(currState)
        for (nextNode, nextDirection, nextCost) in problem.getSuccessors(currState):
            if not nextNode in visited:
                if Q.update(nextNode, nextCost + currPathCost):
                    setPathCost(nextNode, nextCost + currPathCost)
                    setPrev(nextNode, (currState, nextDirection))
    
    #
    # recover path from `prevs` record
    path = []
    state = goalState
    while state != startState:
        prevState, direction = getPrev(state)
        path.insert(0, direction)
        state = prevState

    return path


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    # "*** YOUR CODE HERE ***"
    
    visited         = [] # {Node}              # nodes that we've already visited
    horizon         = [] # {Node}              # nodes seen but not yet visited
    prevs           = {} # Node => (Node, Dir) # best previous node to get here
    pathCosts       = {} # Node => Num         # total weight of best known path to node


    #
    ## setters and getters
    #

    def make_str_getter(d): return (lambda k: d[str(k)])
    def make_str_setter(d):
        def f(k,v): d[str(k)] = v
        return f

    getPrev = make_str_getter(prevs)
    setPrev = make_str_setter(prevs)

    getPathCost = make_str_getter(pathCosts)
    setPathCost = make_str_setter(pathCosts)

    def getPriority(node):
        return getPathCost(node) + heuristic(node, problem)

    def contains(xs, x):
        x_str = str(x)
        return any([str(i) == x_str for i in xs])

    def getNextNode():
        minNode = horizon[0]
        minPriority = getPriority(minNode)
        for node in horizon:
            priority = getPriority(node)
            if priority < minPriority:
                minPriority = priority
                minNode = node
        return minNode

    start = problem.getStartState()
    horizon.append(start)
    setPathCost(start, 0)

    goal = None

    while len(horizon) > 0:
        currNode = getNextNode()
        currPathCost = getPathCost(currNode)

        # at goal?
        if problem.isGoalState(currNode):
            goal = currNode
            break

        # visit node
        horizon.remove(currNode)
        visited.append(currNode)

        # check neighbors
        for (nextNode, nextDirection, nextCostNew) in problem.getSuccessors(currNode):
            if contains(visited, nextNode): continue

            nextPathCostNew = currPathCost + nextCostNew

            # never seen this node before
            if not contains(horizon, nextNode):
                horizon.append(nextNode)
                setPathCost(nextNode, nextPathCostNew)
                setPrev(nextNode, (currNode, nextDirection))
            # seen this node before
            else:
                nextPathCost = getPathCost(nextNode) # known pathCost
                nextPriority = getPriority(nextNode) # known priority
                nextPriorityNew = nextPathCostNew + heuristic(nextNode, problem)
                if nextPriority <= nextPriorityNew:
                    # known path is better than this new one
                    continue
                else:
                    # this is a better path than known
                    setPrev(nextNode, (currNode, nextDirection))
                    setPathCost(nextNode, nextPathCostNew)

    # recover path from `prevs` record
    path = []
    node = goal
    while node != start:
        prev, direction = getPrev(node)
        path.insert(0, direction)
        node = prev
    return path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
