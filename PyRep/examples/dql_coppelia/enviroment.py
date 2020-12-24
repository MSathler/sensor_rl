from pyrep import PyRep
from pyrep.robots.mobiles.p3dx import P3dx
from pyrep.objects.shape import Shape
from pyrep.const import PrimitiveShape
import numpy as np
from pyrep.backend import sim
from py_sensor import sensor

class ReacherEnv(object):

    def __init__(self,SCENE_FILE):
        self.pr = PyRep()
        self.pr.launch(SCENE_FILE, headless=False)
        self.pr.start()

        self.agent = P3dx()
        self.sensor = sensor()

        self.done = False
        #self._reward = 0
        self.last_read = 0
        self.gradient = 0

        self.starting_pose = self.agent.get_2d_pose()
        #self.initial_joint_positions = self.agent.get_joint_positions()
        self.agent.set_motor_locked_at_zero_velocity(True)
        self.sensor.update()
        
    def _get_state(self):
        ### Sc,Sx,Sy Estados [gas concentration,x position, y position]
        # Return state
        return np.concatenate([self.agent.get_2d_pose()])

    def reset(self):
        # Get a random position within a cuboid and set the target position
        self.agent.set_2d_pose(self.starting_pose)
        #self._reward = 0
        self.last_read = 0
        self.gradient = 0
        self.done = False
        #self.agent.set_joint_positions(self.initial_joint_positions)
        return self._get_state()

    def step(self, action):
        self.agent.set_joint_target_velocities(action)  # Execute action
        for i in range(10):
            self.pr.step()  # Step the physics simulation
        self.sensor.update()
        self.gradient = self.sensor.read - self.last_read
        self.last_read = self.sensor.read
        print(self.gradient)
        return self.done, self._reward, self._get_state()
    
    def reward(self):
        #print(self.sensor.read)
        self._reward = -1
        if self.sensor.read > 0:
            self._reward += 1
        if self.gradient > 0:
            self._reward += 1
        if self.sensor.read > 30000:
            self._reward += 100
            self.done = True
        return self.done

    def shutdown(self):
        self.sensor.shutdown()
        self.pr.stop()
        self.pr.shutdown()
