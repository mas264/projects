import itertools
import random

def conflict_count(n_queen):
    """takes a total assignment for an n-queen problem and returns the number 
    conflicts for that assignment."""
    
    count = 0
    table = []
    
    for i, n in enumerate(n_queen):
        table.append([i+1, n])
        
    
    while len(table) > 1:
        x_col, x_row = table[0] 
        for y_col, y_row in table[1:]:
            slope = abs((x_col-y_col)/(x_row-y_row))
            if x_col == y_col or x_row == y_row:
                count += 1
            if slope == 1:
                count += 1
        table.pop(0)
    
    return count
    
    
def neighbours(n_queen):
    """takes a total assignment for an n-queen problem and returns a sequence 
    (list or iterator) of total assignments that are the neighbours of the 
    current assignment. A neighbour is obtained by swapping the position of 
    two numbers in the given permutation."""
    
    curr_count = 0
    answer = set()
    in_set = set()
    copy = set(n_queen)
    
    if len(n_queen) > 2:
        while curr_count < len(n_queen):
            if curr_count == 0:
                answer.add((n_queen[1], n_queen[0])+(n_queen[2:]))
                
            if curr_count >= 1 and curr_count < len(n_queen)-1:
                answer.add((n_queen[0:curr_count]) + (n_queen[curr_count+1], n_queen[curr_count]) + \
                              (n_queen[curr_count+2:]))
            
            if curr_count == len(n_queen)-1:
                answer.add((n_queen[-1],) + (n_queen[1:-1]) + (n_queen[0],))
                
            curr_count += 1
        for index, value in enumerate(n_queen):
            for item in n_queen:
                if value == item:
                    in_set.add(item)
            missing = copy - in_set
            for element in missing:
                i = n_queen.index(element)
                a = list(n_queen)
                a[index], a[i] = a[i], a[index]
                answer.add(tuple(a))
            in_set = set()
                
    if len(n_queen) == 2:
        answer.add((n_queen[1],) + (n_queen[0],))
        
    return answer
        
def greedy_descent(assignment):
    """takes an initial total assignment for the n-queens problem and
     iteratively improves the assignment until either a solution is found or a
     local minimum is reached."""
    
    
    current_num_of_conflicts = conflict_count(assignment)
    print("Assignment:", assignment, "Number of conflicts:", current_num_of_conflicts)
    
    if current_num_of_conflicts == 0:
        print("A solution is found.")
        return assignment

        
    current = None
    for i in sorted(neighbours(assignment)):
        if current_num_of_conflicts > conflict_count(i):
            current_num_of_conflicts = conflict_count(i)
            current = i

        
    if current != None:
        greedy_descent(current)
        
    if current == None and current_num_of_conflicts > 0:
        print("A local minimum is reached.")
        return None

def random_restart(n):
    """find a solution for large values of n (e.g. n = 50) in a reasonable time 
    . In the following program it is assumed that the function greedy_descent
    returns a solution if one is found or None otherwise."""
    random.seed(0) # seeding so that the results can be replicated.
    assignment = list(range(1, n+1))
    while not greedy_descent(tuple(assignment)):
        random.shuffle(assignment)
        
        
def learn_perceptron(weights, bias, training_examples, learning_rate, 
                     max_epochs):
    for epoch in range(1, max_epochs + 1):
        #print("-" * 20, "epoch:", epoch, 20 * "-")
        #print("weights: ", weights)
        #print("bias: ", bias)
        seen_error = False
        for input_l, target in training_examples:
            a = sum(i*w for i in input_l for w in weights) + bias
            output = 1 if a >=0 else 0
            #print("input: {} output: {} target: {}".format(
               # input_l, output, target))
            if output != target:
                seen_error = True
                # Now update the weights and bias
                weights[0] = weights[0] + (learning_rate*input_l[0]*(target-output))
                weights[1] = weights[1] + (learning_rate*input_l[1]*(target-output))
                bias = bias + (learning_rate*(target-output))
                #print("updating the weights and bias to: ", weights, bias)

        if not seen_error:
            #print('Model could be learnt')
            def perceptron(input_vector):
                a = sum(i*w for i in input_vector for w in weights) + bias
                output = 1 if a >=0 else 0
                return output
            return perceptron