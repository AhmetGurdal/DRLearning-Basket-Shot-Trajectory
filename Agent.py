import random
import numpy as np

class Agent():
	
	def __init__(self, power_range, angle_range, position_range):
		self.currentState = 0
		self.states = list() # [x,power,angle]
		self.rewards = list()
		self.angle_range = angle_range
		self.power_range = power_range
		self.matrix =  np.zeros((position_range,angle_range,power_range), dtype=int) #[[[0] * power_range] * angle_range] * position_range
		self.shotsFrom = np.zeros((position_range,angle_range,power_range), dtype=int)
	
	def printMatrix(self, s_list, fname):
		f = open(fname, "w")
		for s in s_list:
			for j in self.matrix[s]:
				j = str(j)[1:-1]
				while(j[0] == " "):
					j = j[1:]
				#print(j)
				f.write(str(j) + "\n")
			f.write("\n")
			#print("")
		f.close()	


	def addState(self, state, reward):
		self.states.append(state)
		self.rewards.append(reward)
		print(state)
		for i in range(state[1] - 1, state[1] + 2):
			iscurrent = 0
			if i == state[1]:
				iscurrent = 1
			for j in range(state[2] - (1 + iscurrent), state[2] + (2 + iscurrent)):
				if(i < 0 or j < 0 or i >= self.angle_range or j >= self.power_range):
					continue
				self.matrix[state[0]][i][j] += ((self.rewards[-1]) / (1 + abs(state[1] - i)) + ((2 * self.rewards[-1]) / (1 + abs(state[2] - j))))
			 

	def createNextAction(self, xPosition):
		s = np.sum(self.matrix[xPosition])
		r = random.randint(0,(s + (self.power_range * self.angle_range)))
		print("NPSUM: {}, Power R: {}, Angle R: {}".format(str(s), str(self.power_range), str(self.angle_range)))
				

		for i in range(len(self.matrix[xPosition])):
			for j in range(len(self.matrix[xPosition][i])):
				#print("Random   " + str(r))
				#print("I: {}, J:{}, xPosition: {}, value:{}".format(str(i), str(j), str(xPosition), str(self.matrix[xPosition][i][j])))

				if(self.matrix[xPosition][i][j] == 0):
					r -= 1
				else:
					r -= self.matrix[xPosition][i][j]
				if(r <= 0):
					self.shotsFrom[xPosition][i][j] += 1	
					self.currentState += 1
					return i,j

		return 0,0
		