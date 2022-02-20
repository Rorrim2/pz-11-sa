import numpy as np

from contants import get_all_actions

class RandomAgent():
	def __init__(self, eps=0.8):
		self.__eps = eps
		self.__previous_action = None
  
	def get_action(self, state,isPlayer=True, x=0,y=0,r=0,env=None):
		new_action = np.random.choice(get_all_actions())
		if self.__previous_action is not None:
			act = np.random.choice([self.__previous_action, new_action], p=[self.__eps, 1.0 - self.__eps])
			if act is not self.__previous_action: self.__previous_action = act
			return act
		else:
			self.__previous_action = new_action
			return self.__previous_action


def euclidean_dist(x1,y1,x2,y2):
    return np.linalg.norm(np.array([x1,y1]) - np.array([x2,y2]))

        
class CloseFoodAgent():
	def __init__(self):
		self.first = True
	
	def get_action(self, state,isPlayer=True, x=0,y=0,r=0,env=None):
		if state is not None:
			# take a list of other players
			enemies = state['e']
			player = state['p']
			if not isPlayer:
				enemies.append(player)
				player =  {'r':r, 'x':x, 'y':y}
				enemies.remove(player)
			# remove those bigger than you
			smaller_enemies = []
			for e in enemies:
				if e['r'] < player['r']:
					smaller_enemies.append(e)
			# search for the nearest one - near_enemy
			near_enemy = next(iter(smaller_enemies), None)
			for se in smaller_enemies:
				if euclidean_dist(se['x'],se['y'],player['x'],player['y']) < euclidean_dist(near_enemy['x'],near_enemy['y'],player['x'],player['y']):
					near_enemy = se
			# search for the closest food - near_food
			foods = state['f']
			near_food = next(iter(foods), None)
			for f in foods:
				if euclidean_dist(f[0],f[1],player['x'],player['y']) < euclidean_dist(near_food[0],near_food[1],player['x'],player['y']):
					near_food = f
			if near_food:
				near_food = {'x':near_food[0], 'y': near_food[1]}
			# eating other player is more important than food, but food is also good
			near = near_enemy if near_enemy is not None else near_food
			if near_enemy and near_food and euclidean_dist(near_enemy['x'],near_enemy['y'],player['x'],player['y'])/euclidean_dist(near_food['x'],near_food['y'],player['x'],player['y']) >= 1.5:
				near = near_food
			# check in what direction to go
			direction = ""
			if near:
				if near['x'] < player['x']:
					direction += "L"
				elif near['x'] > player['x']:
					direction += "R"
				if near['y'] < player['y']:
					direction += "D"
				elif near['y'] > player['y']:
					direction += "U"
				if direction == "": direction += "U"
				return direction
		return np.random.choice(get_all_actions())