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
import searchAgents

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
    if problem.isGoalState(problem.getStartState()):
        return []

    actions = []       # Actions list to store all the directions in which pacman moves. This will store our final output
    vis = []           # Visited list to maintain all the visited nodes
    s = util.Stack()   # Stack for dfs
    s.push((problem.getStartState(),'', actions))

    while not s.isEmpty():
        #The Stack pops Current node, the direction , the actions list which stores direction up to that node
        currNode, act, actions = s.pop()

        #Marking the node current node visited
        vis.append(currNode)

        #Avoiding action of first node
        if act is not '':
            actions = actions + [act]

        #Checking Goal state
        if problem.isGoalState(currNode) == True:
            return actions

        #Getting children of the current node
        children = problem.getSuccessors(currNode)

        for child in children:
            # Take the next node , direction from the successor
            node = child[0]
            act = child[1]

            # If the node is already visited once, do not visit again!
            if node not in vis:
                s.push((node,act,actions))

    #Return list of actions if not already returned
    return actions

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""

    q = util.Queue()    # Queue to run BFS
    actions = []        # Actions list to store all the directions in which pacman moves. This will store our final output
    vis = []            # Visited list to store visited nodes



    q.push((problem.getStartState(), '', actions))
    vis.append(problem.getStartState())     # Marking the first node visited as the node is already in queue

    while not q.isEmpty():
        #The Stack pops Current node, the direction , the actions list which stores direction up to that node
        currNode, act, actions = q.pop()

        #Checks the Goal state
        if problem.isGoalState(currNode):
            return actions

        #Finds all the successors of current node
        children = problem.getSuccessors(currNode)


        for child in children:
            # Take the next node , direction from the successor
            node = child[0]
            act = child[1]
            if node not in vis:
                #Marks the child node visited here
                vis.append(node)
                q.push((node, act, actions + [act]))
    #Return list of actions if not already returned
    return actions

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    q = util.PriorityQueue()  # Priority Queue to run UCS
    actions = []  # Actions list to store all the directions in which pacman moves. This will store our final output
    vis = []  # Visited list to store visited nodes


    q.push(problem.getStartState(), 0)
    vis.append(problem.getStartState())


    # Maintaining a separate costList so I can update priority queue elements later
    costList = []
    costList.append((problem.getStartState(), actions, 0))

    while not q.isEmpty():
        # The Priority Queue pops Current node
        # and CostList pops current direction , the actions list which stores direction up to that node, the cost of the path till now

        currNode = q.pop()
        for node in costList:
            if currNode == node[0]:
                actions = node[1]
                costTillNow = node[2]
                break

        if problem.isGoalState(currNode):
            return actions

        children = problem.getSuccessors(currNode)

        for child in children:
            #Take the next node , direction and cost from the successor
            node = child[0]
            act = child[1]
            cost = child[2]
            # Push child node with new cost
            if node not in vis :
                vis.append(node)
                costList.append((node, actions + [act] , costTillNow + cost))
                q.push(node, costTillNow + cost )
            else:
                # Updating the cost in the costList if a better path (hence cost) to Goal appears
                for x in costList:
                    if x[0]==node:
                        if cost + costTillNow < x[2]:
                            #Updating new cost in Priority Queue
                            q.update(node, costTillNow + cost)
                            # Deleting tuple which has old path and appending the new one in costList
                            costList = [i for i in costList if x[0] is not node]
                            costList.append((node, actions + [act], costTillNow + cost))
                            break

    #Return list of actions if not already returned
    return actions


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    q = util.PriorityQueue() # Priority Queue to run A star
    actions = []  # Actions list to store all the directions in which pacman moves. This will store our final output
    vis = []  # Visited list to store visited nodes
    newCost = heuristic(problem.getStartState(), problem)
    q.push(problem.getStartState(), newCost)
    vis.append(problem.getStartState())

    # Maintaining a separate costList so I can update priority queue elements later
    costList = []
    costList.append((problem.getStartState(), actions, 0))

    while not q.isEmpty():
        # The Priority Queue pops Current node
        # and CostList pops current direction , the actions list which stores direction up to that node, the cost of the path till now

        currNode = q.pop()
        for node in costList:
            if currNode == node[0]:
                actions = node[1]
                costTillNow = node[2]
                break

        if problem.isGoalState(currNode):
            return actions

        children = problem.getSuccessors(currNode)

        for child in children:
            # Take the next node , direction and cost from the successor
            node = child[0]
            act = child[1]
            cost = child[2]
            newCost = heuristic(node, problem)
            # Push child node with new cost


            """""
            A star code is similar to UCS except the fact, now the heuristic is being added
            to the priority in the priority queue, thus the node which has minimum f(n)
            where f(n) is

            f(n) = g(n) + h(n)

            gets popped first and thus will lead to optimal path

            """""
            if node not in vis:
                vis.append(node)
                costList.append((node, actions + [act], costTillNow + cost))
                q.push(node, costTillNow + cost + newCost)
            else:
                # Updating the cost in the costList if a better path (hence cost) to Goal appears
                for x in costList:
                    if x[0] == node:
                        if cost + costTillNow < x[2]:
                            # Updating new cost in Priority Queue which includes the heuristic value
                            q.update(node, costTillNow + cost + newCost)
                            # Deleting tuple which has old path and appending the new one in costList
                            costList = [i for i in costList if x[0] is not node]
                            costList.append((node, actions + [act], costTillNow + cost))
                            break

    # Return list of actions if not already returned
    return actions





# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
