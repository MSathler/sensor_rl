import math

def read_sensor(x,y,_intensity,_sensor_x,_sensor_y,_sensor_dimention,_sum_reads):
        w = 1
        mean_reads = 0
        for i in range(len(_intensity)):
		
            if ((x[i] >= (_sensor_x - _sensor_dimention)) and (x[i] <= (_sensor_x + _sensor_dimention)) and (y[i] >= (_sensor_y - _sensor_dimention)) and (y[i] <= (_sensor_y + _sensor_dimention))):
                
                #for j in range(len(_intensity)): 

                    #if ((_points[j].y >= (_sensor_y - _sensor_dimention)) and (_points[j].y <= (_sensor_y + _sensor_dimention))):
                       
                        #_xy_reads.append(self._intensity[i])
                        #_pos_reads.append(i)
                _sum_reads += _intensity[i]          

                        #print(self._sum_reads)              
                        
        mean_reads = _sum_reads/w
        w += 1 
        return mean_reads



## Alto custo computacional
def cython_distance(_points,_intensity,_sensor_x,_sensor_y,_sensor_dimention,_sum_reads):
    
    for i in range(len(_points)):
        dist = math.sqrt(math.pow(_points[i].x - _sensor_x, 2) + math.pow(_points[i].y - _sensor_y, 2))
        if (dist < (_sensor_dimention*2)):
            _sum_reads += _intensity[i]
    return _sum_reads
