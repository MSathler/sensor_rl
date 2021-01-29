import roslibpy 
import cython_for
import cython_pc
import time
import numpy as np
from pompy import models, processors
from ros_pompy_point_cloud import pompy_point_cloud

class sensor(object):

    def __init__(self,read = 0, topic_to_read= '/sensor_read',pointcloud_subscriber = "/point_pompy"):
        self.__read = 0
        self.wind_angle= 0.0
        ######################

        ##sadas
        seed = 20180517
        rng = np.random.RandomState(seed)

        # Define wind model simulation region
        wind_region = models.Rectangle(x_min=0., x_max=100., y_min=-50., y_max=50.)

        # Define wind model parameters
        wind_model_params = { 
            'n_x': 21,
            'n_y': 21,
            'u_av': 1.,
            'v_av': 0.,
            'k_x': 10.,
            'k_y': 10.,
            'noise_gain': 20.,
            'noise_damp': 0.1,
            'noise_bandwidth': 0.2,
            'use_original_noise_updates': True
        }

        # Create wind model object
        wind_model = models.WindModel(wind_region, rng=rng, **wind_model_params)

        # Define plume simulation region
        # This is a subset of the wind simulation region
        sim_region = models.Rectangle(x_min=0., x_max=50., y_min=-12.5, y_max=12.5)

        # Define plume model parameters
        plume_model_params = {
            'source_pos': (0., -12., 0.),
            'centre_rel_diff_scale': 2.,
            'puff_release_rate': 20,
            'puff_init_rad': 0.001**0.5,
            'puff_spread_rate': 0.009,
            'init_num_puffs': 10,
            'max_num_puffs': 10000,
            'model_z_disp': False,
        }

        # Create plume model object
        plume_model = models.PlumeModel(
            rng=rng, sim_region=sim_region, wind_model=wind_model, **plume_model_params)

        # Define concentration array (image) generator parameters
        array_gen_params = {
            'array_z': 0.,
            'n_x': 500,
            'n_y': 500,
            'puff_mol_amount': 8.3e8
        }#8.3e8

        # Create concentration array generator object
        array_gen = processors.ConcentrationArrayGenerator(
            array_xy_region=sim_region, **array_gen_params)

        # Display initial concentration field
        conc_array = array_gen.generate_single_array(plume_model.puff_array)

        # Simulation timestep
        dt = 0.01

        # Run wind model forward to equilibrate
        
        for k in range(2000):
        
            wind_model.update(dt)
        
        pb = pompy_point_cloud( wind_model=wind_model,
                                plume_model=plume_model, 
                                conc_array = conc_array, 
                                array_gen = array_gen
                                ,use_pose_coppelia=False)

        ##############sdasdas


        self.pompy_dict = pb.without_coppelia()
        #self.pc_x,self.pc_y,self.pc_z,self.__intensity = cython_pc.t_pc(0,200,1.675,2.35,360)
        # print(self.pompy_dict)

        #######################

        # self.client=roslibpy.Ros(host='localhost', port=9090)
        # self.client.run()
        self._sum_reads = 0
        self._sensor_dimention = 0.04
        # self.pc_listener = roslibpy.Topic(self.client, pointcloud_subscriber, 'sensor_msgs/PointCloud')
        # self.listener = roslibpy.Topic(self.client, topic_to_read, 'std_msgs/Float32')
        
        # self.pc_listener.subscribe(self.callback_pc_function)
        # time.sleep(6)
        
    def update(self,x,y):
        #self.listener.subscribe(self.callback_function)
        self.x = x
        self.y = y
        self._sum_reads = 0
        return self.read_sensor()
        
    # def att_position(self,_sensor_x_pose,_sensor_y_pose):
    #     self.x = _sensor_x_pose
    #     self.y = _sensor_y_pose

    def read_sensor(self):
        # self.__read =  cython_for.read_sensor(self.pc_x,self.pc_y,self.__intensity,self.x,self.y,self._sensor_dimention,self._sum_reads)
        self.__readP, self.wind_angle = cython_for.read_pompy_sensor(self.pompy_dict, self.x,self.y, self._sensor_dimention, self._sum_reads)
        # print(self.wind_y)
    # def callback_pc_function(self,data):
    #     #print("--------------")
    #     self.__points = data['points']
    #     self.__intensity = data['channels'][0]['values']
    #     #self._mean = self.read_sensor()
    
    # def callback_function(self,data):
    #     self.__read = data['data']

    @property
    def read(self):
        # return self.__read
        return self.__readP

    @property
    def wind(self):
        return self.wind_angle

    # def shutdown(self):
    #     self.client.terminate()
