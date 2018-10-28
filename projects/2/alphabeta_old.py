
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

#
# Alpha-Beta Node
#   + When the root of the alpha-beta tree
#     is instanciated, the alpha-beta pruning
#     process is automatically processed.
#
class ABNode:
    def __init__(self,
            parent,
            is_max, evaluationFunction,
            alpha, beta,
            gameState, agentIndex, action,
            depth
        ):
        self.parent             = parent
        self.is_max             = is_max
        self.evaluationFunction = evaluationFunction
        self.alpha, self.beta   = alpha, beta
        self.gameState          = gameState
        self.agentIndex         = agentIndex
        self.action             = action
        self.children           = []
        self.is_leaf            = False
        if parent: parent.children.append(self)

        #
        # calculate utility using minimax
        # with alpha-beta pruning
        #

        print self.alpha, self.beta, "("+("max" if self.is_max else "min")+")"

        # print self.alpha, self.beta

        # leaf node
        if depth == 0:
        # if (depth == 0 or len(self.gameState.getLegalActions(self.agentIndex)) == 0):
            self.is_leaf = True
            utility = self.evaluationFunction(self.gameState)
            print "visiting leaf:", utility
            # got lower bound
            if self.is_max:
                self.alpha, self.beta = utility, inf
            # go upper bound
            else:
                self.alpha, self.beta = -inf, utility

        # inner node
        else:
            for action_next in self.gameState.getLegalActions(self.agentIndex):
                # prune
                if self.alpha > self.beta:
                    self.children.append(None)
                    continue

                gameState_next = self.gameState.generateSuccessor(agentIndex, action_next)
                agentIndex_next = (agentIndex + 1) % gameState_next.getNumAgents()
                node_next = ABNode(self,
                    agentIndex_next == 0, self.evaluationFunction,
                    self.alpha, self.beta,
                    gameState_next, agentIndex_next, action_next,
                    depth - 1)

                # first child visit
                if (self.alpha, self.beta) == (None, None):
                    # looking for lower bound
                    if self.is_max:
                        self.alpha, self.beta = node_next.getUtility(), inf
                    # looking for upper bound
                    else:
                        self.alpha, self.beta = -inf, node_next.getUtility()

                # subsequent pass
                else:
                    # looking for new lower bound
                    if self.is_max:
                        print self.alpha, "^", node_next.getUtility(), "->", max(self.alpha, node_next.getUtility())
                        self.alpha = max(self.alpha, node_next.getUtility())
                    # looking for new upper bound
                    else:
                        print self.alpha, "v", node_next.getUtility(), "->", min(self.beta, node_next.getUtility())
                        self.beta = min(self.beta, node_next.getUtility())

    def getBestChild(self):
        # is leaf node
        if len(self.children) == 0:
            return self
        # is inner node
        children_best_indecies = [i for i in range(len(self.children))
            if self.children[i].getUtility() == self.getUtility()]
        return self.children[random.choice(children_best_indecies)]

    def getUtility(self):
        if self.is_max: return self.alpha
        else:           return self.beta

    def getBestNextAction(self):
        return self.getBestChild().action

    def debug(self, level=0):
        print (
            ("  "*level) +
            ("^ " if self.is_max else "v ") +
            str(self.getUtility()) + " : " +
            str((self.alpha, self.beta)))
        if len(self.children) > 0:
            for c in self.children:
                if c: c.debug(level+1)
                else: print(("  "*(level+1)) + "PRUNED")

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        # "*** YOUR CODE HERE ***"
        tree = ABNode(
            None,
            True, self.evaluationFunction,
            None, None,
            gameState, 0, None,
            self.depth)
        # print "-"*20
        # tree.debug()
        return tree.getBestChild().action