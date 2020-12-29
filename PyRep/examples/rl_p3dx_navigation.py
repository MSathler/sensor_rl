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
#agent.qnetwork_local.load_state_dict(torch.load('checkpoint_22_12_1.pth'))
scores = []
mean = []
scores_window = deque(maxlen=100)
eps = 1.0
loss = []
t = 0
#e =0
best = -9999.0

for e in range(1, EPISODES + 1):
    #while True:
    #    e += 1
    state = env.reset()
    print('Starting episode %d' % e)
    score = 0
        # t = time.clock_gettime(time.CLOCK_MONOTONIC)
        #print(t - time.clock_gettime(time.CLOCK_MONOTONIC))
    for i in range(EPISODE_LENGTH):
        # if i == 0:
            #    t = time.clock_gettime(time.CLOCK_MONOTONIC)
        action = agent.act(state,eps) # [1,1] agent.act(state,eps)
        if action == 0:
            ret = [2.0,2.0]
        elif action == 1:
            ret = [3.0,1.0]
        elif action == 2:
            ret = [1.0,3.0]
        elif action == 3:
            ret = [2.0,-2.0]
        elif action == 4:
            ret = [-2.0,2.0]

    
        done, reward, next_state = env.step(ret)
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
    print('\rEpisode {}\tAverage Score: {:.2f}\tBest Average: {:.2f} '.format(e, np.mean(scores_window), best), end="")
    if np.mean(scores_window)>=1000.0:
            print('\nEnvironment solved in {:d} episodes!\tAverage Score: {:.2f}'.format(e, np.mean(scores_window)))
            torch.save(agent.qnetwork_local.state_dict(), 'checkpoint_28_12.pth')
            break
    if np.mean(scores_window)>=900.0:
            print('\nEnvironment 900 in {:d} episodes!\tAverage Score: {:.2f}'.format(e, np.mean(scores_window)))
            torch.save(agent.qnetwork_local.state_dict(), 'checkpoint_900_1.pth')
    print('Reached target %d!' % i)
    print(scores)

torch.save(agent.qnetwork_local.state_dict(), 'checkpoint_27_12.pth')
env.shutdown()
plt.plot(np.linspace(0,EPISODES ,len(scores),endpoint=False), scores)

plt.plot(np.linspace(0,EPISODES ,len(mean),endpoint=False), mean)

plt.xlabel('Episode Number')
plt.ylabel('Average Reward (Over Next %d Episodes)')
plt.show()





# ############################# Teste file ##############################
# agent.qnetwork_local.load_state_dict(torch.load('checkpoint_28_12.pth'))

# for i in range(10):
#     state = env.reset()
#     score = 0
#     for j in range(200):
#         action = agent.act(state)
        
#         if action == 0:
#             ret = [2.0,2.0]
#         elif action == 1:
#             ret = [3.0,1.0]
#         elif action == 2:
#             ret = [1.0,3.0]
#         elif action == 3:
#             ret = [2.0,-2.0]
#         elif action == 4:
#             ret = [-2.0,2.0]
#         done, reward, next_state = env.step(ret)
#         agent.step(state, action, reward, next_state, done)

#         state = next_state
#         score += reward 
        

#         if done == True:
#             break
#     print(reward)



            
