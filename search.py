"""
In search.py, you will implement generic search algorithms
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

	print("Start:", problem.get_start_state().state)
    print("Is the start a goal?", problem.is_goal_state(problem.get_start_state()))
    print("Start's successors:", problem.get_successors(problem.get_start_state()))
    """
    "*** YOUR CODE HERE ***"
    #util.raiseNotDefined()
    stack = util.Stack()
    return bfs_or_dfs(problem, stack)

def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    queue = util.Queue()
    return bfs_or_dfs(problem, queue)


def bfs_or_dfs(problem, data_structure):
    """
    the function that runs dfs or bfs with the given data structure.
    :param problem: the game's problem.
    :param data_structure: the data structure that works with bfs or dfs accordingly.
    :return: list of all the moves to reach the goal state of the problem.
        """
    visited = set()
    cur_state = problem.get_start_state()
    data_structure.push((cur_state, []))
    while not data_structure.isEmpty():
        cur_state, cur_moves = data_structure.pop()
        if cur_state in visited:
            continue
        if problem.is_goal_state(cur_state):
            return cur_moves
        for state in problem.get_successors(cur_state):
            data_structure.push((state[0], cur_moves + [state[1]]))
        visited.add(cur_state)


def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    "*** YOUR CODE HERE ***"
    # util.raiseNotDefined()
    priority_queue = util.PriorityQueue()
    visited = dict()
    cur_state = problem.get_start_state()
    priority_queue.push(HeapState(cur_state, []), 0)
    while not priority_queue.isEmpty():
        heap_state = priority_queue.pop()
        cur_state = heap_state.state
        if visited.get(cur_state):
            continue
        if problem.is_goal_state(cur_state):
            return heap_state.actions
        for state in problem.get_successors(cur_state):
            new_actions = heap_state.actions + [state[1]]
            priority_queue.push(HeapState(state[0], new_actions),
                                heap_state.pieces + state[2])
        visited[cur_state] = True


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    # util.raiseNotDefined()
    priority_queue = util.PriorityQueue()
    visited = dict()
    cur_state = problem.get_start_state()
    priority_queue.push(HeapState(cur_state, []), 0)
    while not priority_queue.isEmpty():
        heap_state = priority_queue.pop()
        cur_state = heap_state.state
        actions = heap_state.actions
        if visited.get(cur_state):
            continue
        if problem.is_goal_state(cur_state):
            return actions
        for state in problem.get_successors(cur_state):
            new_actions = actions + [state[1]]
            cost = problem.get_cost_of_actions(new_actions)
            priority_queue.push(HeapState(state[0], new_actions), cost + heuristic(state[0], problem))
        visited[cur_state] = True


class HeapState:
    """
    a class that represents a state inside the priority queue holding the state
    the moves and a set of pieces on the board
    """
    def __init__(self, state, actions):
        self.state = state
        self.actions = actions

# Abbreviations


bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
