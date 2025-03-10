from pyrep import PyRep
from pyrep.robots.mobiles.p3dx import P3dx
from pyrep.objects.shape import Shape
from pyrep.const import PrimitiveShape
import numpy as np
from pyrep.backend import sim
from py_sensor import sensor
import time
import random
from collections import namedtuple, deque


class ReacherEnv(object):

    def __init__(self,SCENE_FILE):

        self.pr = PyRep()
        self.pr.launch(SCENE_FILE, headless=True)
        self.pr.start()

        self.agent = P3dx()
        self.sensor = sensor()
        self.memory_len = 5

        self.done = False
        self._reward = 0
        self.last_read = 0
        self.gradient = 0
        self.concentration_memory = deque(maxlen=self.memory_len)
        self.wind_x_memory = deque(maxlen=self.memory_len)
        self.wind_y_memory = deque(maxlen= self.memory_len)
        self.distance_memory = deque(maxlen=self.memory_len)
        self.angle_memory = deque(maxlen=self.memory_len)
        self.initiate_Vmemory()
        self.zeros = 0
        self.read = 0.0
        self.wind_x, self.wind_y = 0.0,0.0
        self.h = 0
        self.n = 0
        self.m_read = 0.0
        self.starting_pose = self.agent.get_2d_pose()
        self.s_x, self.s_y, self.s_z = self.starting_pose
        self.last_x,self.last_y = self.s_x, self.s_y
        self.agent.set_motor_locked_at_zero_velocity(True)
        self.sensor.update(self.s_x, self.s_y)
        
    ## Q table state
    # def Q_get_state(self)


    # def step(self, action):

    #     wheel_action = self.actions(action)
    #     self.agent.set_joint_target_velocities(wheel_action)  # Execute action

    #     for i in range(20):
    #         self.pr.step()  # Step the physics simulation

    #     self.x,self.y,z = self.agent.get_2d_pose()
    #     self.sensor.update(self.x,self.y)
    #     self.read = self.sensor.read
    #     #time.sleep(0.8)
    #     #self.m_read = sum(self.read)/len(self.read)
    #     #self.sensor.update()
    #     self.gradient = 1 if (self.read - self.last_read) > 0 else 0
    #     self.last_read = self.read
    #     self.reward()
    #     return self.done, self._reward, self._get_state()

    ##


    def _get_state(self):

        ################## Q Table States ################

        # concentration_state = np.zeros((30))
        # for i in range(30):
        #     if self.sensor.read <= i*1000 and self.sensor.read >= (i-1)*1000:
        #         concentration_state[i] = 1
        # return np.concatenate([concentration_state,np.array([self.gradient, distance, angle])])
        
        ################## Q Table States #################

        ############### Relative Position ################
        x, y, z = self.agent.get_2d_pose()

        distance_n = ( ( ( (x - self.last_x) ** 2 ) + ( (y - self.last_y) ** 2 ) ) ** (1/2) ) / 2
        distance = ( ( ( (x - self.last_x) ** 2 ) + ( (y - self.last_y) ** 2 ) ) ** (1/2) )

        if distance == 0:
            angle = 0

        else:
            angle = ( ( y / distance ) + 1 ) / 2 

        self.last_x = x
        self.last_y = y
        ############### Relative Position end ################

        norm_read = self.read / 10000.0
        self.wind_x_memory.append(self.wind_x)
        self.wind_y_memory.append(self.wind_y)
        self.concentration_memory.append( norm_read )
        self.distance_memory.append( distance_n )
        self.angle_memory.append( angle )
        # print(sum(self.distance_memory))
        return np.concatenate( [ self.concentration_memory, self.distance_memory, self.angle_memory, np.array( [self.gradient] ), self.wind_x_memory, self.wind_y_memory ] ) #( self.sensor.read / 10000 ),


    

    def actions(self,action):

        if action == 0:
            return [2.0,2.0]
        elif action == 1:
            return [3.0,1.0]
        elif action == 2:
            return [1.0,3.0]
        elif action == 3:
            return [2.0,-2.0]
        elif action == 4:
            return [-2.0,2.0]

    def step(self, action):

        wheel_action = self.actions(action)
        self.agent.set_joint_target_velocities(wheel_action)  # Execute action

        for i in range(20):
            self.pr.step()  # Step the physics simulation

        self.x,self.y,z = self.agent.get_2d_pose()
        self.sensor.update(self.x,self.y)
        self.read = self.sensor.read
        self.wind_x, self.wind_y = self.sensor.wind
        # print(self.read)
        #time.sleep(0.8)
        #self.m_read = sum(self.read)/len(self.read)
        #self.sensor.update()
        self.gradient = 1 if (self.read - self.last_read) > 0 else 0 # (self.read / (self.last_read + 1)) if (self.last_read) == 0 else (self.read / self.last_read)
        self.last_read = self.read
        self.reward()
        return self.done, self._reward, self._get_state()
    
    def reward(self):

        self._reward = -1

        if sum(self.distance_memory) <= 0.16:
            self._reward -= 5

        if self.read > 0:
            self._reward += 1
            self.zeros = 0

        else: 
            self.zeros += 1

            if self.zeros >= 10:
                self._reward -= 100
                self.done = True

        if self.gradient > 0:
            self.h += 1 
            self.n = 0
            self._reward += self.h
            
        else:
            self.h = 0
            self.n += 1
            self._reward -= self.n
            
        
        if self.read > 9000:
            self._reward += 1000
            self.done = True


        # elif self.sensor.read >= 5000:
        #     self._reward += 5
        #     self.zeros = 0
        # elif self.sensor.read >= 4000:
        #     self._reward += 4
        #     self.zeros = 0
        # elif self.sensor.read >= 3000:
        #     self._reward += 3
        #     self.zeros = 0
        # elif self.sensor.read >= 2000:
        #     self._reward += 2
        #     self.zeros = 0
        # elif (self.sensor.read > 1250):
        #     self._reward += 1
        #     self.zeros = 0

        
    def initiate_Vmemory(self):

        self.wind_x_memory = deque(maxlen=self.memory_len)
        self.wind_y_memory = deque(maxlen=self.memory_len)
        self.concentration_memory = deque(maxlen=self.memory_len)
        self.distance_memory = deque(maxlen=self.memory_len)
        self.angle_memory = deque(maxlen=self.memory_len)
        for _ in range(4):
            self.wind_x_memory.append(0.0)
            self.wind_y_memory.append(0.0)
            self.concentration_memory.append(0.0)
            self.distance_memory.append(0)
            self.angle_memory.append(0)


    def x_y_start(self):

        source_size = 0.8
        self.x_start, self.y_start = random.uniform(-4.025,7.375),random.uniform(-3.35,8.05)

        while (self.x_start < 1.675 + source_size and self.x_start > 1.675 - source_size and self.y_start < 2.35 + source_size and self.y_start > 2.35 - source_size ):
            
            self.x_start, self.y_start = random.uniform(-4.025,7.375),random.uniform(-3.35,8.05)
            



    def reset(self):
        
        #   Random initial position

        # self.x_y_start()
        # self.agent.set_2d_pose([self.x_start, self.y_start,0.0])
        
        #   Fixed initial position
        self.agent.set_2d_pose(self.starting_pose)

        self._reward = -1
        self.last_read = 0
        self.gradient = 0
        self.h = 0
        self.n = 0
        self.read = 0.0
        self.wind_x, self.wind_y = 0.0,0.0
        self.zeros = 0
        self.initiate_Vmemory()
        self.done = False
        self.last_x,self.last_y = self.s_x, self.s_y
        return self._get_state()


    def shutdown(self):

        # self.sensor.shutdown()
        self.pr.stop()
        self.pr.shutdown()
