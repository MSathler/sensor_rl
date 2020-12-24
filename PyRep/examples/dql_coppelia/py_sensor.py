import roslibpy 


class sensor(object):
    def __init__(self,read = 0, topic_to_read= '/sensor_read'):
        self.__read = 0
        self.client=roslibpy.Ros(host='localhost', port=9090)
        self.client.run()

        self.listener = roslibpy.Topic(self.client, topic_to_read, 'std_msgs/Float32')

        
    def update(self):
        self.listener.subscribe(self.callback_function)
    
    def callback_function(self,data):
        self.__read = data['data']

    @property
    def read(self):
        return self.__read

    def shutdown(self):
        self.client.terminate()