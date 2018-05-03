import convexhull

def expected_output(filename):
    """"returns a list of points in the specified file, that is the points on
    the convex hull"""
    
    file = open(filename, 'r')
    line = file.readline().strip()
    
    chull = line.split(" ")
    chull = [int(p) for p in chull]
        
    return chull

def test_setA():
    """test all the files in set A against their expected output, prints the
    results with the time it took each method to get the convex hull"""

    # test file A_10
    filename = 'A_10.dat'
    output_file = 'A_10.out'
    print("Convex hull for file", filename + ":")
    print(expected_output(output_file))
    listPts = convexhull.readDataPts(filename)
    print('giftwrap method gives expected output:', 
          expected_output(output_file) == convexhull.giftwrap(listPts), 
          '\tTime taken:'.expandtabs(6), convexhull.time_giftwrap)
    print('grahamscan method gives expected output:',
          expected_output(output_file) == convexhull.grahamscan(listPts),
          '\tTime taken:'.expandtabs(4), convexhull.time_grahamscan)
    print('amethod method gives expected output:',
          expected_output(output_file) == convexhull.amethod(listPts),
          '\tTime taken:'.expandtabs(7), convexhull.time_amethod)
    print('------------------------------------------------')
    
    # test file A_50
    filename = 'A_50.dat'
    output_file = 'A_50.out'
    print("Convex hull for file", filename + ":")
    print(expected_output(output_file))
    listPts = convexhull.readDataPts(filename)
    print('giftwrap method gives expected output:', 
          expected_output(output_file) == convexhull.giftwrap(listPts), 
          '\tTime taken:'.expandtabs(6), convexhull.time_giftwrap)
    print('grahamscan method gives expected output:',
          expected_output(output_file) == convexhull.grahamscan(listPts),
          '\tTime taken:'.expandtabs(4), convexhull.time_grahamscan)
    print('amethod method gives expected output:',
          expected_output(output_file) == convexhull.amethod(listPts),
          '\tTime taken:'.expandtabs(7), convexhull.time_amethod)
    print('------------------------------------------------')
    
    # test file A_500
    filename = 'A_500.dat'
    output_file = 'A_500.out'
    print("Convex hull for file", filename + ":")
    print(expected_output(output_file))
    listPts = convexhull.readDataPts(filename)
    print('giftwrap method gives expected output:', 
          expected_output(output_file) == convexhull.giftwrap(listPts), 
          '\tTime taken:'.expandtabs(6), convexhull.time_giftwrap)
    print('grahamscan method gives expected output:',
          expected_output(output_file) == convexhull.grahamscan(listPts),
          '\tTime taken:'.expandtabs(4), convexhull.time_grahamscan)
    print('amethod method gives expected output:',
          expected_output(output_file) == convexhull.amethod(listPts),
          '\tTime taken:'.expandtabs(7), convexhull.time_amethod)
    print('------------------------------------------------')
    
    # test file A_3000
    filename = 'A_3000.dat'
    output_file = 'A_3000.out'
    print("Convex hull for file", filename + ":")
    print(expected_output(output_file))
    listPts = convexhull.readDataPts(filename)
    print('giftwrap method gives expected output:', 
          expected_output(output_file) == convexhull.giftwrap(listPts), 
          '\tTime taken:'.expandtabs(6), convexhull.time_giftwrap)
    print('grahamscan method gives expected output:',
          expected_output(output_file) == convexhull.grahamscan(listPts),
          '\tTime taken:'.expandtabs(4), convexhull.time_grahamscan)
    print('amethod method gives expected output:',
          expected_output(output_file) == convexhull.amethod(listPts),
          '\tTime taken:'.expandtabs(7), convexhull.time_amethod)
    print('------------------------------------------------')
    
    # test file A_6000
    filename = 'A_6000.dat'
    output_file = 'A_6000.out'
    print("Convex hull for file", filename + ":")
    print(expected_output(output_file))
    listPts = convexhull.readDataPts(filename)
    print('giftwrap method gives expected output:', 
          expected_output(output_file) == convexhull.giftwrap(listPts), 
          '\tTime taken:'.expandtabs(6), convexhull.time_giftwrap)
    print('grahamscan method gives expected output:',
          expected_output(output_file) == convexhull.grahamscan(listPts),
          '\tTime taken:'.expandtabs(4), convexhull.time_grahamscan)
    print('amethod method gives expected output:',
          expected_output(output_file) == convexhull.amethod(listPts),
          '\tTime taken:'.expandtabs(7), convexhull.time_amethod)
    print('------------------------------------------------')
    
    # test file A_9000
    filename = 'A_9000.dat'
    output_file = 'A_9000.out'
    print("Convex hull for file", filename + ":")
    print(expected_output(output_file))
    listPts = convexhull.readDataPts(filename)
    print('giftwrap method gives expected output:', 
          expected_output(output_file) == convexhull.giftwrap(listPts), 
          '\tTime taken:'.expandtabs(6), convexhull.time_giftwrap)
    print('grahamscan method gives expected output:',
          expected_output(output_file) == convexhull.grahamscan(listPts),
          '\tTime taken:'.expandtabs(4), convexhull.time_grahamscan)
    print('amethod method gives expected output:',
          expected_output(output_file) == convexhull.amethod(listPts),
          '\tTime taken:'.expandtabs(7), convexhull.time_amethod)
    print('------------------------------------------------')
    
    # test file A_15000
    filename = 'A_15000.dat'
    output_file = 'A_15000.out'
    print("Convex hull for file", filename + ":")
    print(expected_output(output_file))
    listPts = convexhull.readDataPts(filename)
    print('giftwrap method gives expected output:', 
          expected_output(output_file) == convexhull.giftwrap(listPts), 
          '\tTime taken:'.expandtabs(6), convexhull.time_giftwrap)
    print('grahamscan method gives expected output:',
          expected_output(output_file) == convexhull.grahamscan(listPts),
          '\tTime taken:'.expandtabs(4), convexhull.time_grahamscan)
    print('amethod method gives expected output:',
          expected_output(output_file) == convexhull.amethod(listPts),
          '\tTime taken:'.expandtabs(7), convexhull.time_amethod)
    print('------------------------------------------------')
    
    # test file A_30000
    filename = 'A_30000.dat'
    output_file = 'A_30000.out'
    print("Convex hull for file", filename + ":")
    print(expected_output(output_file))
    listPts = convexhull.readDataPts(filename)
    print('giftwrap method gives expected output:', 
          expected_output(output_file) == convexhull.giftwrap(listPts), 
          '\tTime taken:'.expandtabs(6), convexhull.time_giftwrap)
    print('grahamscan method gives expected output:',
          expected_output(output_file) == convexhull.grahamscan(listPts),
          '\tTime taken:'.expandtabs(4), convexhull.time_grahamscan)
    print('amethod method gives expected output:',
          expected_output(output_file) == convexhull.amethod(listPts),
          '\tTime taken:'.expandtabs(7), convexhull.time_amethod)
    print('------------------------------------------------')
    
    

def test_setB():
    """test all the files in set B against their expected output, prints the
    results with the time it took each method to get the convex hull"""

    # test file B_10
    filename = 'B_10.dat'
    output_file = 'B_10.out'
    print("Convex hull for file", filename + ":")
    print(expected_output(output_file))
    listPts = convexhull.readDataPts(filename)
    print('giftwrap method gives expected output:', 
          expected_output(output_file) == convexhull.giftwrap(listPts), 
          '\tTime taken:'.expandtabs(6), convexhull.time_giftwrap)
    print('grahamscan method gives expected output:',
          expected_output(output_file) == convexhull.grahamscan(listPts),
          '\tTime taken:'.expandtabs(4), convexhull.time_grahamscan)
    print('amethod method gives expected output:',
          expected_output(output_file) == convexhull.amethod(listPts),
          '\tTime taken:'.expandtabs(7), convexhull.time_amethod)
    print('------------------------------------------------')
    
    # test file B_50
    filename = 'B_50.dat'
    output_file = 'B_50.out'
    print("Convex hull for file", filename + ":")
    print(expected_output(output_file))
    listPts = convexhull.readDataPts(filename)
    print('giftwrap method gives expected output:', 
          expected_output(output_file) == convexhull.giftwrap(listPts), 
          '\tTime taken:'.expandtabs(6), convexhull.time_giftwrap)
    print('grahamscan method gives expected output:',
          expected_output(output_file) == convexhull.grahamscan(listPts),
          '\tTime taken:'.expandtabs(4), convexhull.time_grahamscan)
    print('amethod method gives expected output:',
          expected_output(output_file) == convexhull.amethod(listPts),
          '\tTime taken:'.expandtabs(7), convexhull.time_amethod)
    print('------------------------------------------------')
    
    # test file B_500
    filename = 'B_500.dat'
    output_file = 'B_500.out'
    print("Convex hull for file", filename + ":")
    print(expected_output(output_file))
    listPts = convexhull.readDataPts(filename)
    print('giftwrap method gives expected output:', 
          expected_output(output_file) == convexhull.giftwrap(listPts), 
          '\tTime taken:'.expandtabs(6), convexhull.time_giftwrap)
    print('grahamscan method gives expected output:',
          expected_output(output_file) == convexhull.grahamscan(listPts),
          '\tTime taken:'.expandtabs(4), convexhull.time_grahamscan)
    print('amethod method gives expected output:',
          expected_output(output_file) == convexhull.amethod(listPts),
          '\tTime taken:'.expandtabs(7), convexhull.time_amethod)
    print('------------------------------------------------') 
    
    # test file B_3000
    filename = 'B_3000.dat'
    output_file = 'B_3000.out'
    print("Convex hull for file", filename + ":")
    print(expected_output(output_file))
    listPts = convexhull.readDataPts(filename)
    print('giftwrap method gives expected output:', 
          expected_output(output_file) == convexhull.giftwrap(listPts), 
          '\tTime taken:'.expandtabs(6), convexhull.time_giftwrap)
    print('grahamscan method gives expected output:',
          expected_output(output_file) == convexhull.grahamscan(listPts),
          '\tTime taken:'.expandtabs(4), convexhull.time_grahamscan)
    print('amethod method gives expected output:',
          expected_output(output_file) == convexhull.amethod(listPts),
          '\tTime taken:'.expandtabs(7), convexhull.time_amethod)
    print('------------------------------------------------')
    
    # test file B_6000
    filename = 'B_6000.dat'
    output_file = 'B_6000.out'
    print("Convex hull for file", filename + ":")
    print(expected_output(output_file))
    listPts = convexhull.readDataPts(filename)
    print('giftwrap method gives expected output:', 
          expected_output(output_file) == convexhull.giftwrap(listPts), 
          '\tTime taken:'.expandtabs(6), convexhull.time_giftwrap)
    print('grahamscan method gives expected output:',
          expected_output(output_file) == convexhull.grahamscan(listPts),
          '\tTime taken:'.expandtabs(4), convexhull.time_grahamscan)
    print('amethod method gives expected output:',
          expected_output(output_file) == convexhull.amethod(listPts),
          '\tTime taken:'.expandtabs(7), convexhull.time_amethod)
    print('------------------------------------------------')
    
    # test file B_9000
    filename = 'B_9000.dat'
    output_file = 'B_9000.out'
    print("Convex hull for file", filename + ":")
    print(expected_output(output_file))
    listPts = convexhull.readDataPts(filename)
    print('giftwrap method gives expected output:', 
          expected_output(output_file) == convexhull.giftwrap(listPts), 
          '\tTime taken:'.expandtabs(6), convexhull.time_giftwrap)
    print('grahamscan method gives expected output:',
          expected_output(output_file) == convexhull.grahamscan(listPts),
          '\tTime taken:'.expandtabs(4), convexhull.time_grahamscan)
    print('amethod method gives expected output:',
          expected_output(output_file) == convexhull.amethod(listPts),
          '\tTime taken:'.expandtabs(7), convexhull.time_amethod)
    print('------------------------------------------------')
    
    # test file B_15000
    filename = 'B_15000.dat'
    output_file = 'B_15000.out'
    print("Convex hull for file", filename + ":")
    print(expected_output(output_file))
    listPts = convexhull.readDataPts(filename)
    print('giftwrap method gives expected output:', 
          expected_output(output_file) == convexhull.giftwrap(listPts), 
          '\tTime taken:'.expandtabs(6), convexhull.time_giftwrap)
    print('grahamscan method gives expected output:',
          expected_output(output_file) == convexhull.grahamscan(listPts),
          '\tTime taken:'.expandtabs(4), convexhull.time_grahamscan)
    print('amethod method gives expected output:',
          expected_output(output_file) == convexhull.amethod(listPts),
          '\tTime taken:'.expandtabs(7), convexhull.time_amethod)
    print('------------------------------------------------')
    
    # test file B_30000
    filename = 'B_30000.dat'
    output_file = 'B_30000.out'
    print("Convex hull for file", filename + ":")
    print(expected_output(output_file))
    listPts = convexhull.readDataPts(filename)
    print('giftwrap method gives expected output:', 
          expected_output(output_file) == convexhull.giftwrap(listPts), 
          '\tTime taken:'.expandtabs(6), convexhull.time_giftwrap)
    print('grahamscan method gives expected output:',
          expected_output(output_file) == convexhull.grahamscan(listPts),
          '\tTime taken:'.expandtabs(4), convexhull.time_grahamscan)
    print('amethod method gives expected output:',
          expected_output(output_file) == convexhull.amethod(listPts),
          '\tTime taken:'.expandtabs(7), convexhull.time_amethod)
    print('------------------------------------------------')
    