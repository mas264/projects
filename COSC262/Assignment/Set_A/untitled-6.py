def convex_hull(points):
    """Returns the points on the convex hull of points in CCW order."""
    hull = [min(points)]
    for p in hull:
        q = _next_hull_pt(points, p)
        if q != hull[0]:
            hull.append(q)
    return hull

def _dist(p, q):
    """Returns the squared Euclidean distance between p and q."""
    dx, dy = q[0] - p[0], q[1] - p[1]
    return dx * dx + dy * dy

def _next_hull_pt(points, p):
    """Returns the next point on the convex hull in CCW from p."""
    q = p
    for r in points:
        t = turn(p, q, r)
        if t == TURN_RIGHT or t == TURN_NONE and _dist(p, r) > _dist(p, q):
            q = r
    return q

def _next_hull_pt(points, p):
    """Returns the next point on the convex hull in CCW from p."""
    q = points[0] != p and points[0] or points[1]
    for r in (x for x in points if x != p):
        if turn(p, q, r) == TURN_RIGHT:
            q = r
    return q

TURN_LEFT, TURN_RIGHT, TURN_NONE = (1, -1, 0)

def turn(p, q, r):
    """Returns -1, 0, 1 if p,q,r forms a right, straight, or left turn."""
    return cmp((q[0] - p[0])*(r[1] - p[1]) - (r[0] - p[0])*(q[1] - p[1]), 0)

def cmp(a, b):
    return (a > b) - (a < b) 

def readDataPts(filename):
    """Reads data from an input file and returns a list of tuples
       [(x0,y0), (x1, y1), ...]
    """
    #Write code for opening input file and storing points in a list
    file = open(filename, 'r')
    lines = file.readlines()[1:]
    listPts = []
    for line in lines:
        line.rstrip()
        c_index = 0
        while len(line) > c_index and line[c_index].isspace() == False:
            c_index += 1
        x = int(line[0:c_index + 1])
        y = int(line[c_index + 1:])
        listPts.append((x, y))
    file.close()
    
    return listPts

def main():
    listPts = readDataPts('A_500.dat')
    print(convex_hull(listPts))
    
if __name__  ==  "__main__":
    main()
    
#http://tomswitzer.net/2009/12/jarvis-march/


    #chull = [find_min_point(listPts)]
    #chull_index = [listPts.index(find_min_point(listPts))]
    #for p in chull:
        #q = next_chull_pt(listPts, p)
        #if q != chull[0]:
            #chull.append(q)
            #chull_index.append(listPts.index(q))
    #return chull_index

#def next_chull_pt(listPts, p):
    #"""Returns the next point on the convex hull in CCW from p."""
    #q = p
    #for r in listPts:
        #t = lineFn(p, q, r)
        #if t < 0 or t == 0 and dist(p, r) > dist(p, q):
            #q = r
    #return q

#def dist(p, q):
    #"""Returns the combined distances from x and y point for each p and q"""

    #return abs((q[0] - p[0]) + (q[1] - p[1]))