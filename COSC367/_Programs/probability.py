import itertools
def joint_prob(network, assignment):
    '''Returns the probability of the assignment being true'''
    

    r = 1
    for a in assignment:
        if assignment[a] == True:
            if network[a]['Parents'] == []:
                r =  r * network[a]['CPT'][()]               
            else:
                    if len(network[a]['Parents']) == 1:
                        r = r * network[a]['CPT'][(assignment[network[a]['Parents'][0]],)]
                        

                    if len(network[a]['Parents']) == 2:
                        r = r * network[a]['CPT'][(assignment[network[a]['Parents'][0]],assignment[network[a]['Parents'][1]])]

                    
        if assignment[a] == False:
            if network[a]['Parents'] == []:
                r = r * (1 - network[a]['CPT'][()])
            else:
                    
                if len(network[a]['Parents']) == 1:
                    r = r * (1 - network[a]['CPT'][(assignment[network[a]['Parents'][0]],)])
                                  
                                  
                
                if len(network[a]['Parents']) == 2:
                    r = r * (1 - network[a]['CPT'][(assignment[network[a]['Parents'][0]],assignment[network[a]['Parents'][1]])])       
                    
    result = r
    return result
            
            
def query(network, query_var, evidence):
    '''Returns dictionary with True and False values'''
    
    answer = {}
    sumTrue = 0
    sumFalse = 0
    num_true = 0
    num_false = 0
    denom = 0

    hidden_vars = network.keys() - evidence.keys() - {query_var}
    for values in itertools.product((True, False), repeat=len(hidden_vars)):
        hidden_assignments = {var:val for var,val in zip(hidden_vars, values)}    

        d = evidence.copy()
        d.update(hidden_assignments)
        query_true = d.copy()
        query_false = d.copy()
        
        query_true[query_var] = True
        num_true += joint_prob(network, query_true)
        
        
        query_false[query_var] = False
        num_false += joint_prob(network, query_false)  
        
        for y in [True, False]:
                
            d[query_var] = y
            denom += joint_prob(network, d)

        

    answer[True] = num_true/denom
    answer[False] = num_false/denom
    
    return answer
        
          
network1 = {
    'Disease': {
        'Parents': [],
        'CPT': {
            (): 1/100000,
            }},
    'Test': {
        'Parents': ['Disease'],
        'CPT': {
            (True,):0.99,
            (False,):0.01,
        }},
    }
        
network = {
    'Virus': {
        'Parents': [],
        'CPT': {
            (): 0.01,
            }},
    'A': {
        'Parents': ['Virus'],
        'CPT': {
            (True,):0.95,
            (False,):0.1,
        }},
    'B': {
            'Parents': ['Virus'],
            'CPT': {
                (True,):0.9,
                (False,):0.05,
            }},    
    }            

new = {
    'Prior': {
        'Parents': [],
        'CPT': {
            (): 0.05,
            }},
    'A': {
        'Parents': ['Prior'],
        'CPT': {
            (True,):0.3,
            (False,):0.001,
        }},
    'B': {
            'Parents': ['Prior'],
            'CPT': {
                (True,):0.9,
                (False,):0.05,
            }},
    'C': {
            'Parents': ['Prior'],
            'CPT': {
                (True,):0.99,
                (False,):0.7,
            }},    
    }            

