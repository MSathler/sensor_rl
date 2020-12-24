from pyrep import PyRep
from pyrep.robots.mobiles.p3dx import P3dx
from pyrep.objects.shape import Shape
from pyrep.const import PrimitiveShape
import numpy as np
from pyrep.backend import sim
from py_sensor import sensor
import time
from collections import namedtuple, deque
class ReacherEnv(object):

    def __init__(self,SCENE_FILE):
        self.pr = PyRep()
        self.pr.launch(SCENE_FILE, headless=True)
        self.pr.start()

        self.agent = P3dx()
        self.sensor = sensor()

        self.done = False
        self._reward = 0
        self.last_read = 0
        self.gradient = 0
        self.concentration_memory = deque(maxlen=5)
        self.distance_memory = deque(maxlen=5)
        self.angle_memory = deque(maxlen=5)
        self.initiate_Vmemory()
        self.zeros = 0
        self.read = np.zeros(32)
        self.h = 0
        self.n = 0
        self.m_read = 0.0
        self.starting_pose = self.agent.get_2d_pose()
        self.s_x, self.s_y, self.s_z = self.starting_pose
        self.last_x,self.last_y = self.s_x, self.s_y
        self.agent.set_motor_locked_at_zero_velocity(True)
        self.sensor.update(self.s_x, self.s_y)
        

    def _get_state(self):

        ################## Q Table States ################

        ############### Relative Position ################
        x, y, z = self.agent.get_2d_pose()

        distance_n = ( ( ( (x - self.last_x) ** 2 ) + ( (y - self.last_y) ** 2 ) ) ** (1/2) ) / 2
        distance = ( ( ( (x - self.last_x) ** 2 ) + ( (y - self.last_y) ** 2 ) ) ** (1/2) )
        #print(distance_n)
        if distance == 0:
            angle = 0
        else:
            angle = ( ( y / distance ) + 1 ) / 2 
        self.last_x = x
        self.last_y = y
        ############### Relative Position end ################
        
        # concentration_state = np.zeros((30))
        # for i in range(30):
        #     if self.sensor.read <= i*1000 and self.sensor.read >= (i-1)*1000:
        #         concentration_state[i] = 1
        # return np.concatenate([concentration_state,np.array([self.gradient, distance, angle])])
        
        ################## Q Table States #################

        ############## Adicionar memoria depois ###########
        self.concentration_memory.append( ( self.m_read / 10000 ) )
        self.distance_memory.append( distance_n )
        self.angle_memory.append( angle )
        #print(np.concatenate([self.v_memory,np.array( [self.gradient, angle, distance_n])]))
        return np.concatenate( [ self.concentration_memory, self.distance_memory, self.angle_memory, np.array( [self.gradient] ) ] ) #( self.sensor.read / 10000 ),
        #####################################################
        
        # return np.concatenate([np.array( [( self.sensor.read / 10000 ),self.gradient, angle, distance_n])]) #( self.sensor.read / 10000 ),

    def reset(self):
        # Get a random position within a cuboid and set the target position
        self.agent.set_2d_pose(self.starting_pose)
        self._reward = -1
        self.last_read = 0
        self.gradient = 0
        self.h = 0
        self.n = 0
        self.read = np.zeros(32)
        self.zeros = 0
        self.initiate_Vmemory()
        self.done = False
        self.last_x,self.last_y = self.s_x, self.s_y
        return self._get_state()

    def step(self, action):
        self.agent.set_joint_target_velocities(action)  # Execute action
        for i in range(20):
            self.pr.step()  # Step the physics simulation
        self.x,self.y,z = self.agent.get_2d_pose()
        #t = time.clock_gettime(time.CLOCK_MONOTONIC)
        self.sensor.update(self.x,self.y)
        
        #print(time.clock_gettime(time.CLOCK_MONOTONIC) - t)
        self.read = self.sensor.read
        # print(self.read)
        #time.sleep(0.8)
        #self.m_read = sum(self.read)/len(self.read)
        #print(self.m_read)
        #self.sensor.update()
        self.gradient = 1 if (self.read - self.last_read) > 0 else 0
        self.last_read = self.read
        #  print(self.gradient)
        self.reward()
        return self.done, self._reward, self._get_state()
    
    def reward(self):
        #print(self.sensor.read)
        self._reward = -1
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
        self.concentration_memory = deque(maxlen=5)
        self.distance_memory = deque(maxlen=5)
        self.angle_memory = deque(maxlen=5)
        for _ in range(4):
            self.concentration_memory.append(0)
            self.distance_memory.append(0)
            self.angle_memory.append(0)

    def shutdown(self):
        # self.sensor.shutdown()
        self.pr.stop()
        self.pr.shutdown()
