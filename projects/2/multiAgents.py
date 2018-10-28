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
import math

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

        # Add more of your code here if you want to

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.
        """
        # Useful information you can extract from a GameState (pacman.py)

        successorGameState  = currentGameState.generatePacmanSuccessor(action)
        ghostStatesNew      = successorGameState.getGhostStates()
        foodGridNew         = successorGameState.getFood()
        capsulesNew         = successorGameState.getCapsules()
        position_new        = successorGameState.getPacmanPosition()
        newScaredTimes      = [ghostState.scaredTimer for ghostState in ghostStatesNew]

        def getDistance(p1, p2):
            x1, y1 = p1
            x2, y2 = p2
            return abs(x1 - x2) + abs(y1 - y2)
            # return math.pow(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2), 1)

        def getDistanceTo(p): return getDistance(position_new, p)

        def getClosestGhostDistance():
            ghostPositionsNew = [ghost.getPosition() for ghost in ghostStatesNew]
            if position_new in ghostPositionsNew: return -10
            min_dist = -1
            for ghost_pos in ghostPositionsNew:
                if min_dist < 0: min_dist = getDistanceTo(ghost_pos)
                else: min_dist = min(min_dist, getDistanceTo(ghost_pos))
            return min_dist

        def getClosestFoodDistance():
            if position_new in currentGameState.getFood().asList(): return -1
            min_dist = -1
            for food_pos in foodGridNew.asList():
                if min_dist < 0: min_dist = getDistanceTo(food_pos)
                else: min_dist = min(min_dist, getDistanceTo(food_pos))
            return min_dist

        def getClosestCalpuseDistance():
            if position_new in currentGameState.getCapsules(): return -1
            if len(currentGameState.getCapsules()) == 0: return 10000
            min_dist = -1
            for cap_pos in capsulesNew:
                if min_dist < 0: min_dist = getDistanceTo(cap_pos)
                else: min_dist = min(min_dist, getDistanceTo(cap_pos))
            return min_dist

        score = 0
        
        if getClosestGhostDistance() <= 3: score -= 1000
        score -= min(getClosestFoodDistance(), getClosestCalpuseDistance())

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

def evaluationFunction(gameState):
    ghostStates = gameState.getGhostStates()
    foodGrid    = gameState.getFood()
    capsules    = gameState.getCapsules()
    position    = gameState.getPacmanPosition()

    def getDistance(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        return abs(x1 - x2) + abs(y1 - y2)
        # return math.pow(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2), 1)

    def getDistanceTo(p): return getDistance(position, p)

    def getClosestGhostDistance():
        ghostPositions = [ghost.getPosition() for ghost in ghostStates]
        if position in ghostPositions: return -10
        min_dist = -1
        for ghost_pos in ghostPositions:
            if min_dist < 0: min_dist = getDistanceTo(ghost_pos)
            else: min_dist = min(min_dist, getDistanceTo(ghost_pos))
        return min_dist

    def getClosestFoodDistance():
        if position in foodGrid.asList(): return -1
        min_dist = -1
        for food_pos in foodGrid.asList():
            if min_dist < 0: min_dist = getDistanceTo(food_pos)
            else: min_dist = min(min_dist, getDistanceTo(food_pos))
        return min_dist

    def getClosestCalpuseDistance():
        if position in capsules: return -1
        if len(capsules) == 0: return 10000
        min_dist = -1
        for cap_pos in capsules:
            if min_dist < 0: min_dist = getDistanceTo(cap_pos)
            else: min_dist = min(min_dist, getDistanceTo(cap_pos))
        return min_dist

    score = 0
    
    if getClosestGhostDistance() <= 3: score -= 1000
    score -= min(getClosestFoodDistance(), getClosestCalpuseDistance())

    return score

class MMNode:
    def __init__(self, parent, func, gameState, action):
        if parent: parent.children.append(self)
        self.parent = parent
        self.children = []
        self.func = func # min or max
        self.gameState = gameState
        self.action = action
        self.utility = None

    def getBestChild(self):
        # is leaf node
        if len(self.children) == 0:
            return self
        # is inner node
        children_best_indecies = [i for i in range(len(self.children))
            if self.children[i].utility == self.utility]
        return self.children[random.choice(children_best_indecies)]

    def getBestNextAction(self):
        return self.getBestChild().action

    def calculateUtility(self):
        if len(self.children) > 0:
            self.utility = self.func(
                [ c.calculateUtility()
                for c in self.children ])
        return self.utility

    def debug(self, level=0):
        print ("  "*level)+"["+str(self.action)[0:2]+"] "+str(self.utility)
        if len(self.children) > 0:
            for c in self.children: c.debug(level+1)


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

          self.depth: depth of tree to explore

          self.evaluationFunction(gameState): get base utility of gameState
        """
        # "*** YOUR CODE HERE ***"

        pacman_actions = gameState.getLegalActions(0)

        # ghosts are in order of turn-taking
        ghosts_count   = gameState.getNumAgents() - 1
        ghosts_actions = [ gameState.getLegalActions(i+1) for i in range(ghosts_count) ]

        # MMNode(parent, func, gameState, action, utility=None)
        def makeTree(node, depth, agentIndex=0):
            # base case
            if depth == 0 or len(node.gameState.getLegalActions(agentIndex)) == 0:
                node.utility = self.evaluationFunction(node.gameState)
                # node.utility = self.evaluationFunction(node.parent.gameState, node.action)

            # induction step:
            else:
                for action_next in node.gameState.getLegalActions(agentIndex):
                    gameState_next  = node.gameState.generateSuccessor(agentIndex, action_next)
                    agentIndex_next = (agentIndex + 1) % gameState_next.getNumAgents()
                    func_next       = max if agentIndex_next == 0 else min
                    node_next       = MMNode(node, func_next, gameState_next, action_next)
                    makeTree(
                        node_next,
                        depth - 1,
                        (agentIndex + 1) % gameState_next.getNumAgents())
            return node

        # MMNode(parent, func, gameState, action, utility=None)
        tree = makeTree(MMNode(None, max, gameState, None),
            self.depth * gameState.getNumAgents())
        tree.calculateUtility()
        # print "-"*20
        # tree.debug()
        return tree.getBestChild().action

#
# (Python numbers) union {infinity}
#
class S:

    inf_pos_str = "+INF"
    inf_neg_str = "-INF"

    def __init__(self, x):
        self.x = x

    def lt(self, other):
        if self ==  inf or other == -inf: return False
        if self == -inf or other ==  inf: return True
        return self.x < other.x
    def gt(self, other):
        if self ==  inf or other == -inf: return True
        if self == -inf or other ==  inf: return False
        return self.x < other.x
    __lt__ = lt
    __gt__ = gt

    def eq(self, other): return (
        other.__class__ == S and self.x == other.x)
    __eq__ = eq

    def neg(self):
        if self.x == S.inf_pos_str: return S(S.inf_neg_str)
        if self.x == S.inf_neg_str: return S(S.inf_pos_str)
        return S(- self.x)
    __neg__ = neg
    
    def mul(self, other):
        if (self,other) in [(inf,  inf), (-inf, -inf)]: return  inf
        if (self,other) in [(inf, -inf), (-inf,  inf)]: return -inf
        return S(self.x * other.x)
    __mul__ = mul

    def tostring(self): return str(self.x)
    __str__ = tostring
    __repr__ = tostring

inf = S(S.inf_pos_str)

class AlphaBetaAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        # self.depth
        # self.evaluationFunction

        def get_value_func(agentIndex):
            if agentIndex == 0: return max_value # pacman
            if agentIndex >  0: return min_value # ghost

        def generateSuccessors(gameState, agentIndex):
            for action_ in gameState.getLegalActions(agentIndex):
                gameState_  = gameState.generateSuccessor(agentIndex, action_)
                agentIndex_ = (agentIndex + 1) % gameState_.getNumAgents()
                value_func_ = get_value_func(agentIndex_)
                yield (action_, gameState_, agentIndex_, value_func_)

        def max_value(alpha, beta, depth, gameState, agentIndex, actionPrev):
            # if len(gameState.getLegalActions(agentIndex)) == 0:
            #     print "agentIndex, self.evaluationFunction(gameState) =", agentIndex, self.evaluationFunction(gameState)

            if (0 in [depth, len(gameState.getLegalActions(agentIndex))]):                # print "leaf value:", self.evaluationFunction(gameState)
                return self.evaluationFunction(gameState), actionPrev
            action = None
            x = -inf
            for (action_, gameState_, agentIndex_, value_func_
            ) in generateSuccessors(gameState, agentIndex):
                x = max(x, value_func_(alpha, beta, depth - 1,
                    gameState_,agentIndex_, action_)[0])
                if x > beta: return x, action
                if alpha < x: alpha, action = x, action_
            return x, action

        def min_value(alpha, beta, depth, gameState, agentIndex, actionPrev):
            if (depth == 0 or len(gameState.getLegalActions(agentIndex)) == 0
                ): return self.evaluationFunction(gameState), actionPrev
            action = None
            x = inf
            for (action_, gameState_, agentIndex_, value_func_
            ) in generateSuccessors(gameState, agentIndex):
                x = min(x, value_func_(alpha, beta, depth - 1,
                    gameState_, agentIndex_, action_)[0])
                if x < alpha: return x, action_
                if beta > x: beta, action = x, action_
            return x, action

        return max_value(-inf, inf, self.depth * gameState.getNumAgents(), gameState, 0, None)[1]

class EMNode:
    def __init__(self, parent, func, gameState, action):
        if parent: parent.children.append(self)
        self.parent = parent
        self.children = []
        self.func = func # min or evg
        self.gameState = gameState
        self.action = action
        self.utility = None

    def getBestChild(self):
        # is leaf node
        if len(self.children) == 0:
            return self
        # is inner node
        children_best_indecies = [i for i in range(len(self.children))
            if self.children[i].utility == self.utility]
        return self.children[random.choice(children_best_indecies)]

    def getBestNextAction(self):
        return self.getBestChild().action

    def calculateUtility(self):
        if len(self.children) > 0:
            self.utility = self.func(
                [ c.calculateUtility()
                for c in self.children ])
        return self.utility

    def debug(self, level=0):
        print ("  "*level)+("^ " if self.func == max else "% ")+"["+str(self.action)[0:2]+"] "+str(self.utility)
        if len(self.children) > 0:
            for c in self.children: c.debug(level+1)

def mean(xs): return float(sum(xs)) / float(len(xs))

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
        # "*** YOUR CODE HERE ***"
        pacman_actions = gameState.getLegalActions(0)

        # ghosts are in order of turn-taking
        ghosts_count   = gameState.getNumAgents() - 1
        ghosts_actions = [ gameState.getLegalActions(i+1) for i in range(ghosts_count) ]

        def makeTree(node, depth, agentIndex):
            # base case
            if depth == 0 or len(node.gameState.getLegalActions(agentIndex)) == 0:
                node.utility = self.evaluationFunction(node.gameState)
                # node.utility = self.evaluationFunction(node.parent.gameState, node.action)

            # induction step:
            else:
                for action_next in node.gameState.getLegalActions(agentIndex):
                    gameState_next  = node.gameState.generateSuccessor(agentIndex, action_next)
                    agentIndex_next = (agentIndex + 1) % gameState_next.getNumAgents()
                    func_next       = max if agentIndex_next == 0 else mean
                    node_next       = EMNode(node, func_next, gameState_next, action_next)
                    makeTree(node_next, depth - 1, agentIndex_next)
            return node

        tree = makeTree(EMNode(None, max, gameState, None), self.depth * gameState.getNumAgents(), 0)
        tree.calculateUtility()
        # print "-"*20
        # tree.debug()
        return tree.getBestChild().action

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    # "*** YOUR CODE HERE ***"
    
    # closest food
    # closest capsule

    gameState = currentGameState
    position  = gameState.getPacmanPosition()
    foods     = gameState.getFood().asList()
    capsules  = gameState.getCapsules()
    ghosts    = gameState.getGhostStates()

    def distance(p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        # return abs(float(x1) - float(x2)) + abs(float(y1) - float(y2))
        return math.pow(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2), 0.5)

    def distanceTo(p): return distance(position, p)

    def foodScore():
        if len(foods) == 0: return 0
        return 1.0/min([distanceTo(f) for f in foods])
    foodScore = foodScore()

    return (10 * foodScore) + (1 * gameState.getScore())

# Abbreviation
better = betterEvaluationFunction

