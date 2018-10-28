class AlphaBetaAgent(MultiAgentSearchAgent):

    def getAction(self, gameState):
        # self.depth
        # self.evaluationFunction

        def get_value_func(agentIndex):
            if agentIndex == 0: return max_value # pacman
            if agentIndex >  0: return min_value # ghost

        def generateSuccessors(gameState, agentIndex):
            for action_ in gameState.getLegalActions(agentIndex):
                gameState_  = gameState.generateSuccessor(agentIndex, agentIndex_)
                agentIndex_ = (agentIndex + 1) % gameState_.getNumAgents()
                value_func_ = get_value_func(agentIndex_)
                yield (action_, gameState_, agentIndex_, value_func_)

        def max_value(alpha, beta, gameState, agentIndex):
            x = -inf
            for (action_, gameState_, agentIndex_, value_func_
            ) in generateSuccessors(gameState, agentIndex):
                x = max(x, value_func_next(alpha, beta, gameState_, agentIndex_))
                if x > beta: return x
                alpha = max(alpha, x)
            return x

        def min_value(alpha, beta, gameState, agentIndex):
            x = inf
            for (action_, gameState_, agentIndex_, value_func_
            ) in generateSuccessors(gameState, agentIndex):
                x = min(x, value_func_next(alpha, beta, gameState_, agentIndex_))
                if x < alpha: return x
                beta = min(beta, x)
            return x

        return max_value(-inf, inf, gameState, 0)