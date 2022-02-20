import numpy as np
import copy

from contants import get_all_actions

def euclidean_dist(x1,y1,x2,y2):
    return np.linalg.norm(np.array([x1,y1]) - np.array([x2,y2]))

class FunctionApproximationAgent:
    def __init__(self, alpha, epsilon, discount, get_legal_actions):
        self.get_legal_actions = get_legal_actions
        self.alpha = alpha
        self.epsilon = epsilon
        self.discount = discount
        self.weights = [-0.4406803055045983, 0.75343154336036, 0.6132158999186154] # b s f
        self.features = [1, 1, 1]
        self.env = None

    def get_dist_to_closest_food(self, state, action):
        # player pos after taking action
        x_p, y_p = state['p']['x'], state['p']['y']
        x_p, y_p = self.env.get_pos_after_actio(x_p, y_p,action)
        dists = []
        for f in state['f']:
            dist = euclidean_dist(x_p, y_p,f[0],f[1])
            dists.append(dist)
        if len(dists) == 0:
            return 0
        return min(dists) 
        

    def get_dist_to_enemy_smaller(self, state, action):
        # player pos after taking action
        x_p, y_p = state['p']['x'], state['p']['y']
        x_p, y_p = self.env.get_pos_after_actio(x_p, y_p,action)

        dists = []

        for e in state['e']:
            dist = euclidean_dist(x_p, y_p,e['x'], e['y'])
            if state['p']['r'] > e['r']:
                dists.append(dist)
        if len(dists) == 0:
            return 0
        return min(dists) 


    def get_dist_to_enemy_bigger(self, state, action):
        # player pos after taking action
        x_p, y_p = state['p']['x'], state['p']['y']
        x_p, y_p = self.env.get_pos_after_actio(x_p, y_p,action)

        dists = []

        for e in state['e']:
            dist = euclidean_dist(x_p, y_p,e['x'], e['y'])
            if state['p']['r'] < e['r']:
                dists.append(dist)
        if len(dists) == 0:
            return 0
        return min(dists) 

    def get_feature(self, value):
        if value == 0:
            return 1
        return 1/value

    def print_w(self):
        print(self.weights)

    def get_qvalue(self, state, action):
        self.features[0] = self.get_feature(self.get_dist_to_enemy_bigger(state, action)) 
        self.features[1] = self.get_feature(self.get_dist_to_enemy_smaller(state, action)) 
        self.features[2] = self.get_feature(self.get_dist_to_closest_food(state, action))

        return self.weights[0]*self.features[0] + self.weights[1]*self.features[1] + self.weights[2]*self.features[2]


    def set_qvalue(self, state, action, value):
        self.weights[0] = self.weights[0] + self.alpha*value*self.get_feature(self.get_dist_to_enemy_bigger(state, action)) 
        self.weights[1] = self.weights[1] + self.alpha*value*self.get_feature(self.get_dist_to_enemy_smaller(state, action)) 
        self.weights[2] = self.weights[2] + self.alpha*value*self.get_feature(self.get_dist_to_closest_food(state, action))

    #---------------------START OF YOUR CODE---------------------#

    def get_value(self, state):
        possible_actions = self.get_legal_actions()
        self.pos_act = possible_actions
        # If there are no legal actions, return 0.0
        if len(possible_actions) == 0:
            return 0.0

        max_value = self.get_qvalue(state, self.get_best_action(state))

        return max_value


    def update(self, state, action, reward, next_state):
        # agent parameters
        gamma = self.discount
        if len(next_state['f']) == 0 and len(next_state['e']) == 0:
            val = (reward) - self.get_qvalue(state, action)
        else:
            val = (reward + gamma * self.get_value(next_state)) - self.get_qvalue(state, action)
        self.set_qvalue(state, action, val)


    def get_best_action(self, state):
        possible_actions = self.get_legal_actions()

        # If there are no legal actions, return None
        if len(possible_actions) == 0:
            return None

        best_actions = []
        best_value = self.get_qvalue(state, possible_actions[0])
        for a in possible_actions:
            if self.get_qvalue(state, a) > best_value:
                best_value = self.get_qvalue(state, a)
        for a in possible_actions:
            if self.get_qvalue(state, a) == best_value:
                best_actions.append(a)

        return np.random.choice(best_actions)


    def get_action(self, state,isPlayer=True, x=0,y=0,r=0,env=None):
        self.env = env
        # Pick Action
        possible_actions = self.get_legal_actions()
        self.pos_act = possible_actions

        # If there are no legal actions, return None
        if len(possible_actions) == 0:
            return None

        # agent parameters:
        epsilon = self.epsilon

        chosen_action = self.get_best_action(state)

        if len(possible_actions) != 1 and np.random.uniform(0.0, 1.0) < epsilon:
            other_actions = copy.deepcopy(possible_actions)
            other_actions.remove(chosen_action)
            chosen_action = np.random.choice(other_actions)

        return chosen_action

    def turn_off_learning(self):
        """
        Function turns off agent learning.
        """
        self.epsilon = 0
        self.alpha = 0