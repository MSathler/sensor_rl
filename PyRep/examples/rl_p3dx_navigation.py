from os.path import dirname, join, abspath
import time 
import numpy as np
from enviroment import ReacherEnv
from collections import deque
import torch
from agent import Agent
import matplotlib.pyplot as plt

EPISODES = 100000
EPISODE_LENGTH = int(50)#/4)
SCENE_FILE = join(dirname(abspath(__file__)), 'p3dx_scene.ttt')

env = ReacherEnv(SCENE_FILE)
agent = Agent(state_size=16, action_size=5, seed=0)
replay_buffer = []
agent.qnetwork_local.load_state_dict(torch.load('checkpoint_11_01.pth'))
scores = []
mean = []
scores_window = deque(maxlen=100)
eps = 0.0 #inicial
loss = []
t = 0
#e =0
best = -9999.0

for e in range(1, EPISODES + 1):
    state = env.reset()
    
    print('Starting episode %d' % e)
    score = 0

    for i in range(EPISODE_LENGTH):

        action = agent.act(state,eps) 

        done, reward, next_state = env.step(action)
        agent.step(state, action, reward, next_state, done)

        state = next_state
        score += reward 
            

        if done == True:
            break

    eps = max(0.01, 0.99*eps)
    scores_window.append(score)       # save most recent score
    if np.mean(scores_window) > best:
        best = np.mean(scores_window)
    scores.append(score)
    mean.append(np.mean(scores_window))
    print(scores)
    print()
    print('\rEpisode {}\tAverage Score: {:.2f}\tBest Average: {:.2f} '.format(e, np.mean(scores_window), best), end="")
    if np.mean(scores_window)>=best:
            print('\nEnvironment solved in {:d} episodes!\tAverage Score: {:.2f}'.format(e, np.mean(scores_window)))
            torch.save(agent.qnetwork_local.state_dict(), 'checkpoint_14_01.pth')
            #break
    # if np.mean(scores_window)>=900.0:
            # print('\nEnvironment 900 in {:d} episodes!\tAverage Score: {:.2f}'.format(e, np.mean(scores_window)))
            # torch.save(agent.qnetwork_local.state_dict(), 'checkpoint_29_900_1.pth')
    
    print('Reached target %d!' % i)
    

torch.save(agent.qnetwork_local.state_dict(), 'checkpoint_14_01f.pth')
env.shutdown()
plt.plot(np.linspace(0,EPISODES ,len(scores),endpoint=False), scores)

plt.plot(np.linspace(0,EPISODES ,len(mean),endpoint=False), mean)

plt.xlabel('Episode Number')
plt.ylabel('Average Reward (Over Next %d Episodes)')
plt.show()





# ############################# Teste file ##############################
# agent.qnetwork_local.load_state_dict(torch.load('checkpoint_11_01.pth'))
# b = 0
# for i in range(1,101):
#     state = env.reset()
#     score = 0
#     for j in range(100):
#         action = agent.act(state)

#         done, reward, next_state = env.step(action)
#         agent.step(state, action, reward, next_state, done)

#         state = next_state
#         score += reward 
        

#         if done == True:
#             break
#     print(score)
#     if reward >= 1000:
#         b +=1
# print("porcentagem de acerto = " + str(b))



            
