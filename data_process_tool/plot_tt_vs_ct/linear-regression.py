'''
Created on Apr 12, 2015

@author: gumengyuan
'''
from numpy import arange,array,ones, zeros, linalg, fromstring, empty
import pylab
#from pylab import plot,subplots,show
import sys
import argparse

class LinearRegression:
    
    def __init__(self, filename, bandwidth=None, cpu_freq=None, test_freq=None):
        self.x = zeros(shape=(1,1))
        self.y = zeros(shape=(1,1))
        print "=================================================="
        print 'data file: {0}'.format(filename)
        if bandwidth != None:
            self.bandwidth = float(bandwidth)
            print 'bandwidth: {0} MB/sec'.format(self.bandwidth)
        else:
            self.bandwidth = bandwidth
        
        if cpu_freq != None:
            self.cpu_freq = float(cpu_freq)
            print 'cpu frequency: {0} GHz'.format(self.cpu_freq)
        else:
            self.cpu_freq = cpu_freq
            
        if test_freq != None:
            self.test_freq = float(test_freq)
            print 'test cpu frequency for bandwidth estimation: {0} GHz'.format(self.test_freq)
        else:
            self.test_freq = test_freq
            
        self.read_file(filename)

    def read_file(self, filename):
        lines = []
        with open(filename) as f:
            lines = f.read().splitlines()
        
        self.x = zeros(shape=(len(lines),1))
        self.y = zeros(shape=(len(lines),1))
        
        print "=================================================="
        print 'data from input file:'
        print 'computation time (sec), output size (kb)'
        for idx, line in enumerate(lines):
            
            floats = fromstring(line, dtype=float, sep=' ')
            print '{0}, {1}'.format(floats[0], floats[1])
            self.x[idx] = floats[0]
            self.y[idx] = floats[1]
    
    def get_x_y(self):
        if self.bandwidth == None:
            transfer_time = [yi/1000  for yi in self.y]
        else:
            transfer_time = [yi/1000/self.bandwidth for yi in self.y]
            
        return self.x, transfer_time
    
#     def set_bandwidth(self, bandwidth):
#         self.bandwidth = float(bandwidth)
    
    
    def plot(self):
        print "=================================================="
        x, y = self.get_x_y()
        A = array([ x, ones(len(x))])
        w = linalg.lstsq(A.T,y)[0]
        line = w[0]*x+w[1]
        
        self.print_ct_result(w[0][0])
        
        if self.bandwidth != None: 
            fig = pylab.figure()           
            pylab.plot(x,line,'r-',x,y,'o')
            fig.suptitle('Time of Data Transfer vs. Time of Data Generation')
            pylab.xlabel('Computation Time (sec)')
            pylab.ylabel('Transfer Time (sec)')
            pylab.show() 
               
#         if self.cpu_freq != None and self.bandwidth != None:
#             f, (ax1, ax2) = subplots(1, 2, sharey=True, figsize=(15,7))
#               
#             ax1.plot(x,line,'r-',x,y,'o')
#             ax1.set_title('Output Transfer Time vs. Computation Time')
#             ax1.set_xlabel('Computation Time (sec)')
#             ax1.set_ylabel('Transfer Time (sec)')
#              
#             x2 = [xi*self.cpu_freq for xi in x]
#             A2 = array([ x2, ones(len(x2))])
#             w2 = linalg.lstsq(A2.T,y)[0]
#             line2 = w2[0]*x2+w2[1]
#             ax2.plot(x2,line2,'r-',x2,y,'o')
#             ax2.set_title('Output Transfer Time vs. Number of CPU Cycles')
#             ax2.set_xlabel('CPU Cycles (10^9)')
#             
#             self.print_cf_result(w2[0][0])
#             
#             show()
                 
        
            
        if self.test_freq != None and self.cpu_freq != None:
            times = self.test_freq/self.cpu_freq
            
            x2 = [xi/times for xi in x]
            A2 = array([ x2, ones(len(x2))])
            w2 = linalg.lstsq(A2.T,y)[0]
            line2 = w2[0]*x2+w2[1]
            
            print '--------------------------------------------------'
            print 'With a new computation power ({test_freq} GHz), below is an estimated relationship between computation time and output size:'.format(test_freq=self.test_freq)
            print 'computation time (sec), output size (kb)'
            for xi, yi in zip(x2, self.y):
                print '{x}, {y}'.format(x=xi[0], y=yi[0])
                
            if self.bandwidth != None:
                self.print_tf_result(self.bandwidth * w2[0][0])
            else:
                self.print_tf_result(w2[0][0])
            

    def print_ct_result(self, slop):
        if self.bandwidth != None:
            print "transfer time / computation time: {ratio}".format(ratio=round(slop,2))
            economic_bandwidth = self.bandwidth * slop
        else:
            economic_bandwidth = slop
                     
        print "cross over bandwidth: {eco}".format(eco=round(economic_bandwidth,4))
        print "(If the bandwidth is lower than {eco} * MB/second, the computation will be worthwhile.)".format(eco=round(economic_bandwidth,4))
    
    def print_cf_result(self, slop):
        print "transfer time / cpu cycles: {ratio}".format(ratio=round(slop,4))
        
    def print_tf_result(self, slop):
        print 'estimated cross over bandwidth: {eco}'.format(eco=round(slop,4))
        print "(With the new computation power, if the test bandwidth should be lower than {eco} * MB/second, the computation will be worthwhile.)".format(eco=round(slop,4))
        
def arg_parser():
    parser = argparse.ArgumentParser(description="Cost analysis tool is used for making comparison of the cost between computation and transferring output")
    parser.add_argument('-f', '--file',
                        help="the file that containing the data of the computation time and output size",
                        action="store", dest="filename",
                        default=None, required=True)
    
    parser.add_argument('-b', '--bandwidth',
                        help="set up the bandwidth you have to get the transfer time",
                        action="store", dest="bandwidth",
                        default=None)
    
    parser.add_argument('-c', '--cpufrequency',
                        help="set up the cpu frequency you are using to run jobs",
                        action="store", dest="cpu_freq",
                        default=None)
    
    parser.add_argument('-t', '--testcpufrequency',
                        help="the test cpu frenquency, with which you want to know the goal bandwidth to make the computation worthwhile",
                        action="store", dest="test_freq",
                        default=None)
    
    return parser
  

if __name__ == '__main__':
    
    if len(sys.argv) <= 1:
        print 'USEAGE: python liner-regression.py -f <computation_time_and_output_size_data_file> [-b <bandwidth_in_MB/sec>] [-c <cpu_frequncy_in_GHz>]'
        sys.exit(0)
        
    parser = arg_parser()
    args = parser.parse_args(sys.argv[1:])
    
    if args.filename == None or args.filename == "":
        print 'USEAGE: python liner-regression.py -f <computation_time_and_output_size_data_file> [-b <bandwidth_in_MB/sec>] [-c <cpu_frequncy_in_GHz>]'
        sys.exit(0)
       
    lr = LinearRegression(args.filename, args.bandwidth, args.cpu_freq, args.test_freq)
#     if args.bandwidth != None:
#         lr.set_bandwidth(args.bandwidth)
    lr.plot ()
    