from action_layer import ActionLayer
from util import Pair
from proposition import Proposition
from proposition_layer import PropositionLayer


class PlanGraphLevel(object):
    """
    A class for representing a level in the plan graph.
    For each level i, the PlanGraphLevel consists of the actionLayer and propositionLayer at this level in this order!
    """
    independent_actions = set()  # updated to the independent_actions of the problem (graph_plan.py line 32)
    actions = []  # updated to the actions of the problem (graph_plan.py line 33 and planning_problem.py line 36)
    props = []  # updated to the propositions of the problem (graph_plan.py line 34 and planning_problem.py line 36)

    @staticmethod
    def set_independent_actions(independent_actions):
        PlanGraphLevel.independent_actions = independent_actions

    @staticmethod
    def set_actions(actions):
        PlanGraphLevel.actions = actions

    @staticmethod
    def set_props(props):
        PlanGraphLevel.props = props

    def __init__(self):
        """
        Constructor
        """
        self.action_layer = ActionLayer()  # see action_layer.py
        self.proposition_layer = PropositionLayer()  # see proposition_layer.py

    def get_proposition_layer(self):  # returns the proposition layer
        return self.proposition_layer

    def set_proposition_layer(self, prop_layer):  # sets the proposition layer
        self.proposition_layer = prop_layer

    def get_action_layer(self):  # returns the action layer
        return self.action_layer

    def set_action_layer(self, action_layer):  # sets the action layer
        self.action_layer = action_layer

    def update_action_layer(self, previous_proposition_layer):
        """
        Updates the action layer given the previous proposition layer (see proposition_layer.py)
        You should add an action to the layer if its preconditions are in the previous propositions layer,
        and the preconditions are not pairwise mutex.
        all_actions is the set of all the action (include noOp) in the domain
        You might want to use those functions:
        previous_proposition_layer.is_mutex(prop1, prop2) returns true
        if prop1 and prop2 are mutex at the previous propositions layer
        previous_proposition_layer.all_preconds_in_layer(action) returns true
        if all the preconditions of action are in the previous propositions layer
        self.actionLayer.addAction(action) adds action to the current action layer
        """
        all_actions = PlanGraphLevel.actions
        "*** YOUR CODE HERE ***"
        for action in all_actions:
            if not previous_proposition_layer.all_preconds_in_layer(action):
                continue
            else:
                all_combinations = [previous_proposition_layer.is_mutex(cond1, cond2) for cond1 in action.get_pre()
                                    for cond2 in action.get_pre() if cond1 != cond2]
                if not any(all_combinations):
                    self.action_layer.add_action(action)

    def update_mutex_actions(self, previous_layer_mutex_proposition):
        """
        Updates the mutex set in self.action_layer,
        given the mutex proposition from the previous layer.
        current_layer_actions are the actions in the current action layer
        You might want to use this function:
        self.actionLayer.add_mutex_actions(action1, action2)
        adds the pair (action1, action2) to the mutex set in the current action layer
        Note that an action is *not* mutex with itself
        """
        current_layer_actions = self.action_layer.get_actions()
        "*** YOUR CODE HERE ***"
        all_combinations = [(action1, action2) for action1 in current_layer_actions
                            for action2 in current_layer_actions if action1 != action2]
        for combination in all_combinations:
            if mutex_actions(combination[0], combination[1], previous_layer_mutex_proposition):
                if Pair(combination[0], combination[1]) not in self.action_layer.get_mutex_actions():
                    self.action_layer.add_mutex_actions(combination[0], combination[1])

    def update_proposition_layer(self):
        """
        Updates the propositions in the current proposition layer,
        given the current action layer.
        don't forget to update the producers list!
        Note that same proposition in different layers might have different producers lists,
        hence you should create two different instances.
        current_layer_actions is the set of all the actions in the current layer.
        You might want to use those functions:
        dict() creates a new dictionary that might help to keep track on the propositions that you've
               already added to the layer
        self.proposition_layer.add_proposition(prop) adds the proposition prop to the current layer

        """
        dic = dict()
        current_layer_actions = self.action_layer.get_actions()
        "*** YOUR CODE HERE ***"
        for action in current_layer_actions:
            for proposition in action.get_add():
                if proposition.get_name() not in dic.values():
                    new_prop = Proposition(proposition.get_name())
                    self.proposition_layer.add_proposition(new_prop)
                    dic[new_prop] = new_prop.get_name()
                keys = list(dic.keys())
                values = list(dic.values())
                new_prop = keys[values.index(proposition.name)]
                new_prop.add_producer(action)

    def update_mutex_proposition(self):
        """
        updates the mutex propositions in the current proposition layer
        You might want to use those functions:
        mutex_propositions(prop1, prop2, current_layer_mutex_actions) returns true
        if prop1 and prop2 are mutex in the current layer
        self.proposition_layer.add_mutex_prop(prop1, prop2) adds the pair (prop1, prop2)
        to the mutex set of the current layer
        """
        current_layer_propositions = self.proposition_layer.get_propositions()
        current_layer_mutex_actions = self.action_layer.get_mutex_actions()
        "*** YOUR CODE HERE ***"
        combinations = [(proposition1, proposition2) for proposition1 in current_layer_propositions
                        for proposition2 in current_layer_propositions if proposition1 != proposition2]
        for pair in combinations:
            if mutex_propositions(pair[0], pair[1], current_layer_mutex_actions) and \
                    Pair(pair[0], pair[1]) not in self.proposition_layer.get_mutex_props():
                self.proposition_layer.add_mutex_prop(pair[0], pair[1])

    def expand(self, previous_layer):
        """
        Your algorithm should work as follows:
        First, given the propositions and the list of mutex propositions from the previous layer,
        set the actions in the action layer.
        Then, set the mutex action in the action layer.
        Finally, given all the actions in the current layer,
        set the propositions and their mutex relations in the proposition layer.
        """
        previous_proposition_layer = previous_layer.get_proposition_layer()
        previous_layer_mutex_proposition = previous_proposition_layer.get_mutex_props()
        "*** YOUR CODE HERE ***"
        self.update_action_layer(previous_proposition_layer)
        self.update_mutex_actions(previous_layer_mutex_proposition)
        self.update_proposition_layer()
        self.update_mutex_proposition()
        # print("actions")
        # for action in self.action_layer.get_actions():
        #     print(action, end = " ")
        # print("mutex_action")
        # for mutex_action in self.action_layer.get_mutex_actions():
        #    print(mutex_action, end = " ")
        # print("props")
        # for prop in self.proposition_layer.get_propositions():
        #    print(prop, end = " ")
        # print("mutex_props")
        # for mutex_prop in self.proposition_layer.get_mutex_props():
        #    print(mutex_prop, end = " ")
        # print("end")

    def expand_without_mutex(self, previous_layer):
        """
        Questions 11 and 12
        You don't have to use this function
        """
        previous_layer_proposition = previous_layer.get_proposition_layer()
        "*** YOUR CODE HERE ***"
        self.update_action_layer(previous_layer_proposition)
        self.update_proposition_layer()


def mutex_actions(a1, a2, mutex_props):
    """
    This function returns true if a1 and a2 are mutex actions.
    We first check whether a1 and a2 are in PlanGraphLevel.independent_actions,
    this is the list of all the independent pair of actions (according to your implementation in question 1).
    If not, we check whether a1 and a2 have competing needs
    """
    if Pair(a1, a2) not in PlanGraphLevel.independent_actions:
        return True
    return have_competing_needs(a1, a2, mutex_props)


def have_competing_needs(a1, a2, mutex_props):
    """
    Complete code for deciding whether actions a1 and a2 have competing needs,
    given the mutex proposition from previous level (list of pairs of propositions).
    Hint: for propositions p  and q, the command  "Pair(p, q) in mutex_props"
          returns true if p and q are mutex in the previous level
    """
    "*** YOUR CODE HERE ***"
    for cond1 in a1.get_pre():
        for cond2 in a2.get_pre():
            if Pair(cond1, cond2) in mutex_props:
                return True
    return False


def mutex_propositions(prop1, prop2, mutex_actions_list):
    """
    complete code for deciding whether two propositions are mutex,
    given the mutex action from the current level (set of pairs of actions).
    Your update_mutex_proposition function should call this function
    You might want to use this function:
    prop1.get_producers() returns the set of all the possible actions in the layer that have prop1 on their add list
    """
    "*** YOUR CODE HERE ***"
    for action1 in prop1.get_producers():
        for action2 in prop2.get_producers():
            if Pair(action1, action2) not in mutex_actions_list:
                return False
    return True
