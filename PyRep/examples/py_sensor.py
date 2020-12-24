import roslibpy 
import cython_for
import cython_pc
import time
class sensor(object):

    def __init__(self,read = 0, topic_to_read= '/sensor_read',pointcloud_subscriber = "/point_pompy"):
        self.__read = 0
        ######################
        self.pc_x,self.pc_y,self.pc_z,self.__intensity = cython_pc.t_pc(0,200,1.675,2.35,360)

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
        self.__read =  cython_for.read_sensor(self.pc_x,self.pc_y,self.__intensity,self.x,self.y,self._sensor_dimention,self._sum_reads)

    # def callback_pc_function(self,data):
    #     #print("--------------")
    #     self.__points = data['points']
    #     self.__intensity = data['channels'][0]['values']
    #     #self._mean = self.read_sensor()
    
    # def callback_function(self,data):
    #     self.__read = data['data']

    @property
    def read(self):
        return self.__read

    # def shutdown(self):
    #     self.client.terminate()
