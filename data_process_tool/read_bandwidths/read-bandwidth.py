'''
Created on Apr 17, 2015

@author: gumengyuan
'''

import xlwt
import string
from numpy import fromstring

def create_workbook(writefilename, sheet):
    book = xlwt.Workbook()
    sh = book.add_sheet(sheet, cell_overwrite_ok=True)
    book.save(writefilename)
    return book, writefilename
    
def get_ec2_bandwidth(logfilename, book, name, title, col1, col2):  
    sh = book.get_sheet(0)
    row_num = 0
    sh.write(row_num, col1, 'time')
    sh.write(row_num, col2, title+' bandwidth in MB/sec')
    row_num += 1
    
    lines = []
    with open(logfilename) as f:
        lines = f.read().splitlines()
    
    line_num = 0         
    while line_num < len(lines) :
        sh.write(row_num, col1, lines[line_num])
        line_num += 7
        # get the line that has the bandwidth
        floats = fromstring(lines[line_num], dtype=float, sep=' ')
        sh.write(row_num, col2, floats[4]/8) # the bandwidth is originally in 10^6 bits/second. now covert it to MB/second by /8.
        line_num += 2
        
        row_num += 1
        
    book.save(name)

def get_s3_bandwidth(logfilename, book, name, title, col1, col2):  
    sh = book.get_sheet(0)
    row_num = 0
    sh.write(row_num, col1, 'time')
    sh.write(row_num, col2, title+' bandwidth in MB/sec')
    row_num += 1
    
    lines = []
    with open(logfilename) as f:
        lines = f.read().splitlines()
    
    line_num = 0         
    while line_num < len(lines) :
        sh.write(row_num, col1, lines[line_num])
        line_num += 1
        # get the line that has the bandwidth
        line = lines[line_num]
        index_comma = -1
        try:  
            index_comma = string.index(line, ',')
        except:
            line_num += 1
            continue
        index_space1 = string.index(line, ' ', index_comma+1)
        index_space2 = string.index(line, ' ', index_space1+1)
        bandwidth = float(line[(index_space1+1):(index_space2)])
        unit = (line[(index_space2+1):(index_space2+3)])
        if unit == 'MB':
            sh.write(row_num, col2, bandwidth)
        elif unit == 'kB':
            sh.write(row_num, col2, bandwidth/1024)
        else:
            line_num += 1
            continue
        
        line_num += 2
        
        row_num += 1
        
    book.save(name)
    
if __name__ == '__main__':
    book, name = create_workbook('output_bandwith.xlsx', 'bandwidth')
    get_ec2_bandwidth('ec2-us-east.log', book, name, 'ec2-us-east', 0, 1)
    get_ec2_bandwidth('ec2-us-west.log', book, name, 'ec2-us-west', 2, 3)
    get_ec2_bandwidth('ec2-ap-sydney.log', book, name, 'ec2-ap-sydney', 4, 5)
    get_ec2_bandwidth('ec2-eu-central.log', book, name, 'ec2-eu-central', 6, 7)
    #get_s3_bandwidth('s3-us-west.log', book, name, 's3-us-west', 6, 7)
    get_s3_bandwidth('s3-us-east-mnt.log', book, name, 's3-us-east-mnt', 8, 9)
    get_s3_bandwidth('s3-us-west-mnt.log', book, name, 's3-us-west-mnt', 10, 11)
    get_s3_bandwidth('s3-ap-sydney-mnt.log', book, name, 's3-ap-sydney-mnt', 12, 13)
    get_s3_bandwidth('s3-eu-west-mnt.log', book, name, 's3-eu-west-mnt', 14, 15)
    
    