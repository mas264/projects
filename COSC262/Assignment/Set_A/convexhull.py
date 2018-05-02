"""
   Convex Hull Assignment: COSC262 (2016)
   Student Name: Ma Alexis Lourize Sy
   Usercode: mas264
"""
import math
import time
import tests

def readDataPts(filename):
    """Reads data from an input file and returns a list of tuples
       [(x0,y0), (x1, y1), ...]
    """
    file = open(filename, 'r')
    lines = file.readlines()[1:]
    listPts = []
    for line in lines:
        line.rstrip()
        index = 0
        while len(line) > index and line[index].isspace() == False:
            index += 1
        x = int(line[0:index + 1])
        y = int(line[index + 1:])
        listPts.append((x, y))
    file.close()
    
    return listPts


def giftwrap(listPts):
    """Returns the indices of hull vertices computed using giftwrap algorithm
    """
    
    start = time.time()
    points = listPts.copy()
    min_point = find_min_point(listPts)
    min_index = listPts.index(min_point)
        
    points.append(min_point)
    i = 0
    v = 0
    k = min_index
    n = len(points)-1
    chull = []
    while k != n:
        points[i] , points[k] = points[k], points[i]
        min_angle = 361
        for j in range(i+1, len(points)):
            angle = theta(points[i], points[j])

            if ((angle < min_angle and angle > v) and points[j] != points[i]):
                min_angle = angle
                k = j

            #if point has the same y-value as the first point we found
            if (angle == 0.0 and theta(points[j], points[0]) == 0.0 \
                and points[j] != points[i]):
                min_angle = angle
                k = j
       
        i += 1
        v = min_angle
    
    for p in points[:i]:
        chull.append(listPts.index(p))
        
    end = time.time()
    global time_giftwrap
    time_giftwrap = (end - start)     #getting time 

    return chull


def grahamscan(listPts):
    """Returns the indices of hull vertices computed using grahamscan algorithm
    """
    
    start = time.time()
    points = listPts.copy()
    min_point = find_min_point(listPts)
    points.remove(min_point)
    stack = [min_point]
    ordered_points = []
    chull = []
    
    for p in points:
        ordered_points.append([theta(min_point, p), p])
        
    #orders the points based on increasing theta values
    ordered_points = sorted(ordered_points)
    for i in range(2):
        stack.append(ordered_points[i][1])
        
    for i in range(2, len(ordered_points)):
        #remove last point from stack if line created is not CCW
        while not is_CCW(stack[-2], stack[-1], ordered_points[i][1]):
            stack.pop()
        #add if line is CCW
        stack.append(ordered_points[i][1])
    
    for point in stack:
        chull.append(listPts.index(point))
    
    end = time.time()
    global time_grahamscan
    time_grahamscan = (end - start)     #getting time
    
    return chull


def amethod(listPts):
    """Returns the indices of hull vertices computed using a third algorithm
    """
    
    start = time.time()
    chull = [find_min_point(listPts)]               
    chull_index = [listPts.index(find_min_point(listPts))] 
    for p in chull:             
        q = p                  
        for r in listPts:       
            t = line_fn(q, p, r)
            
            #updates q to r if line is CCW or pr has greater distance than pq
            if t > 0 or (t == 0 and distance(p, r) > distance(p, q)): 
                q = r
                
        #if q is the initial point we have gone through all the points on chull        
        if q != chull[0]:       
            chull.append(q)
            chull_index.append(listPts.index(q))
    
    end = time.time()
    global time_amethod
    time_amethod = (end - start)     #getting time
    
    return chull_index


#other methods used below

def theta(ptA, ptB):
    """ computes an approxiamtion of the angle between the line AB and a 
    horizontal line through A."""
    
    dx = ptB[0] - ptA[0]
    dy = ptB[1] - ptA[1]
    
    if abs(dx) < 1.e-6 and abs(dy) < 1.e-6: #degenerate case
        t = 0
    else:
        t = dy/ (abs(dx) + abs(dy))
        
    if dx < 0:
        t = 2 - t
    elif dy < 0:
        t = 4 + t
    
    return t * 90


def find_min_point(listPts):
    """Finds and returns the min point (lowest y value) / if list has 
    more than one point with the min y value it returns the point with the min y
    value that has the right most x value"""
    
    min_y = min(listPts, key=lambda x: x[1])[1] #finds the min y value
    min_ys = []

    #makes a list of points that have a min y value
    for i in range(len(listPts)):
        if min_y == listPts[i][1]:
            min_ys.append(listPts[i])
    
    #returns min y value that has the max x value
    return tuple(max(min_ys))


def is_CCW(ptA, ptB, ptC):
    """returns true if the ptC is to the left of the line ptA to ptB"""
    
    return line_fn(ptA, ptB, ptC) > 0


def line_fn(ptA, ptB, ptC):
    """returns 0 if ptC is on the same line as ptA and ptB returns number > 0 if
    ptC is to the left and returns number < 0 if ptC is to the right"""
    
    return (ptB[0]-ptA[0])*(ptC[1]-ptA[1]) \
           -(ptB[1]-ptA[1])*(ptC[0]-ptA[0])


def distance(p, q):
    """Returns the squared Euclidean distance between p and q."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    return dx * dx + dy * dy

    
def main():
    tests.test_setA()   #test all files in set A against its expected output
    tests.test_setB()   #test all files in set B against its expected output
    
   
if __name__  ==  "__main__":
    main()
  