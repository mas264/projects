import csv 

def posterior(prior, likelihood, observation):
    '''returns the posterior probability of the class variable being true, given the observation'''
    
    numerator = 1
    other = 1
    alpha = 0
    for i in range(len(observation)):
        if observation[i] == True:
            numerator *= likelihood[i][1]
        else:
            numerator *= 1 - likelihood[i][1]
    
    numerator *= prior
    alpha = numerator 
    for i in range(len(observation)):
        if observation[i] == True:
            other *= likelihood[i][0]
        else:
            other *= 1 - likelihood[i][0]    

    other *= 1 - prior
    alpha += other
    
    return numerator / alpha

def learn_prior(file_name, pseudo_count=0):
    '''takes the file name of the training set and an optional pseudo-count parameter and returns a real number that is the prior probability of spam being true. The parameter pseudo_count is a non-negative integer and it will be the same for all the attributes and all the values.'''
    
    with open(file_name) as in_file:
        training_examples = [tuple(row) for row in csv.reader(in_file)]     
    
    total_count = len(training_examples) -1
    spam_count = 0
    for row in training_examples:
        if row[-1] == '1':
            spam_count += 1

    spam_count += pseudo_count
    total_count += 2* pseudo_count
    
    return spam_count / total_count


def learn_likelihood(file_name, pseudo_count=0):
    '''takes the file name of a training set (for the spam detection problem) 
    and an optional pseudo-count parameter and returns a sequence of pairs of 
    likelihood probabilities. As described in the representation of likelihood, 
    the length of the returned sequence (list or tuple) must be 12. 
    Each element in the sequence is a pair (tuple) of real numbers such that 
    likelihood[i][False] is P(X[i]=true|Spam=false) and likelihood[i][True] is 
    P(X[i]=true|Spam=true ).'''

    true_spam_count = 0
    false_spam_count = 0
    
    count_spam_true = [0]*12
    count_spam_false = [0]*12
    answer = []
    
    with open(file_name) as in_file:
        training_examples = [tuple(row) for row in csv.reader(in_file)]
        
    for row in training_examples[1:]:
        for i in range(len(row)-1):
            if row[-1] == '1' and row[i] == '1':
                count_spam_true[i] += 1
            if row[-1] == '0' and row[i] == '1':
                count_spam_false[i] += 1
        
        if row[-1] == '1':
            true_spam_count+= 1
        if row[-1] == '0':
            false_spam_count+= 1
            
    for i in range(len(count_spam_true)):
        
        pr_false = (count_spam_false[i] +pseudo_count) / (false_spam_count + (2*pseudo_count))
        pr_true =  (count_spam_true[i] + pseudo_count) / (true_spam_count + (2*pseudo_count))   
        
        answer.append((pr_false,pr_true))
        
    return answer

def nb_classify(prior, likelihood, input_vector):
    ''' takes the learnt prior and likelihood probabilities and classifies an 
    (unseen) input vector. The input vector will be a tuple of 12 integers 
    (each 0 or 1) corresponding to attributes X1 to X12. The function should
    return a pair (tuple) where the first element is either "Spam" or "Not Spam"
    and the second element is the certainty. The certainty is the (posterior)
    probability of spam when the instance is classified as spam, or the 
    probability of 'not-spam' otherwise. If spam and 'not spam' are equally 
    likely (i.e. p=0.5) then choose 'not spam' '''
    
    answer = posterior(prior, likelihood, input_vector)
    if answer <= 0.5:
        return ('Not Spam', 1-answer)
    else:
        return ('Spam', answer)
    
def accuracy(predicted_labels, correct_labels):
    ''' returns the accuracy of a classifier based on the given arguments. 
    Both arguments are tuples of the same length and contain class labels. 
    Class labels may be of any type as long as they can be tested for equality.'''
    
    correct = 0
    for i in range(len(correct_labels)):
        if predicted_labels[i] == correct_labels[i]:
            correct += 1
            
    return correct / len(correct_labels)