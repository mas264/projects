''' min_max no pruning ----------
def max_value(tree):
    """returns the number of utility root when the root is max node"""
    
    if isinstance(tree, int):
        return tree
    else:
        v = float('-inf')
        for item in tree:
            if isinstance(item, list):
                v = max(v, min_value(item))
            else:
                if item > v:
                    v = item
                
        return v
    
    
def min_value(tree):
    """returns the number of utility root when the root is min node"""
    
    if isinstance(tree, int):
        return tree
    else:
        v = float('inf')
        for item in tree:
            if isinstance(item, list):
                v = min(v, max_value(item))
            else:
                if item < v:
                    v = item            
        return v    
'''



def max_value(tree, alpha=float('-inf'), beta=float('inf')):
    """return the utility root given max node, using alpha-beta pruning"""
    
    if isinstance(tree, int):
        return tree
    else:
        v = float('-inf')
        for i in range(len(tree)):
            v = max(v, min_value(tree[i], alpha, beta))
            alpha = max(alpha, v)
            print('Alpha: ' +str(alpha) + '\tBeta: ' + str(beta))
            if beta <= alpha:
                if tree[i+1:]:
                    print('Alpha: ' +str(alpha) + '\tBeta: ' + str(beta))
                    print("Pruning:", ", ".join(map(str, tree[i+1:])))                
                break
            
        return v
  
  
def min_value(tree, alpha=float('-inf'), beta=float('inf')):  
    """return the utility root given min node, using alpha-beta pruning"""
    
    if isinstance(tree, int):
        return tree
    else:
        v = float('inf')
        for i in range(len(tree)):
            v = min(v, max_value(tree[i], alpha, beta))   
            beta = min(beta, v)
            #print('Alpha: ' +str(alpha) + '\tBeta: ' + str(beta))
            if beta <= alpha:
                if tree[i+1:]:
                    print('Alpha: ' +str(alpha) + '\tBeta: ' + str(beta))
                    print("Pruning:", ", ".join(map(str, tree[i+1:])))                
                break
        return v        