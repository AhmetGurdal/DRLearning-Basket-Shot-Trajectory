from Agent import Agent


agent = Agent(10,5,2)

state = [1,2,6]
reward = 6
#print(agent.printMatrix())
agent.addState(state,reward)

agent.printMatrix([0,1],"aaa.txt")

a,p = agent.createNextAction(state[0])
print("Angle:" + str(a) + " Power:" + str(p))

