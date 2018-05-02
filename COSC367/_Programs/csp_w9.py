from csp import *
import itertools, copy

def generate_and_test(csp):
    names, domains = zip(*csp.var_domains.items())
    for values in itertools.product(*domains):
        assignment = {x:v for x, v in zip(names, values)}
        if all(satisfies(assignment, c) for c in csp.constraints):
            yield assignment
            
            
            
def arc_consistent(csp):
    csp = copy.deepcopy(csp)
    tda = {(x, c) for c in csp.constraints for x in csp.var_domains}

    while tda:
        x, c = tda.pop()
        ys = list(scope(c) - {x})
        new_domain = set()
        for xval in csp.var_domains[x]:
            assignment = {x: xval}
            for yvals in itertools.product(*[csp.var_domains[y] for y in ys]):
                assignment.update({y: yval for y, yval in zip(ys, yvals)})
                if satisfies(assignment, c):
                    new_domain.add(xval)
                    break
        if csp.var_domains[x] != new_domain:
            csp.var_domains[x] = new_domain
            for cprime in set(csp.constraints) - {c}:
                if x in scope(cprime):
                    for z in scope(cprime):
                        if x != z:
                            tda.add((z, cprime))
    return csp


crossword_puzzle = CSP(
    var_domains={
        # read across:
        'a1': set("bus has".split()),
        'a3': set("lane year".split()),
        'a4': set("ant car".split()),
        # read down:
        'd1': set("buys hold".split()),
        'd2': set("search syntax".split()),
        },
    constraints={
        lambda a1, d1: a1[0] == d1[0],
        lambda d1, a3: d1[2] == a3[0],
        lambda a1, d2: a1[2] == d2[0],
        lambda d2, a3: d2[2] == a3[2],
        lambda d2, a4: d2[4] == a4[0],
        })

canterbury_colouring = CSP(
    var_domains={
        'christchurch': {'red', 'green'},
        'selwyn': {'red', 'green'},
        'waimakariri': {'red', 'green'},
        },
    constraints={
        lambda christchurch, waimakariri: christchurch != waimakariri,
        lambda christchurch, selwyn: christchurch != selwyn,
        lambda selwyn, waimakariri: selwyn != waimakariri,
        })

cryptic_puzzle = CSP(
    #var_domains={
        #'t': set(range(10)),
        #'w': set(range(10)),
        #'o': set(range(10)),
        #'f': set(range(10)),
        #'u': set(range(10)),
        #'r': set(range(10)),
        #'x1': set(range(10)),
        #'x2': set(range(10)),
        #'x3': set(range(10)),        
        #},
    
    var_domains = {x: set(range(10)) for x in ['t', 'w', 'o', 'f','u','r', 'x1','x2','x3']},
    
    constraints={
        lambda o, r, x1: o + o == r + (10*x1),
        lambda x1, w, u, x2: x1 + w + w == u + (10*x2),
        lambda x2, t, o, x3: x2 + t + t == o + (10*x3),
        lambda x3, f: x3 == f,
        lambda f: f != 0,
        #lambda t, w: t != w,
        #lambda t, o: t != o,
        #lambda t, f: t != f,
        #lambda t, u: t != u,
        #lambda t, r: t != r,
        #lambda w, o: w != o,
        #lambda w, f: w != f,
        #lambda w, u: w != u,
        #lambda w, r: w != r,      
        #lambda o, f: o != f,
        #lambda o, u: o != u,
        #lambda o, r: o != r, 
        #lambda f, u: f != u,
        #lambda u, r: u != r, 
        lambda t,w,o,f,u,r: t != w and t != o and t != f and t != u and t != r,
        lambda t,w,o,f,u,r: w != t and w != o and w != f and w != u and w != r,
        lambda t,w,o,f,u,r: o != w and t != o and o != f and o != u and o != r,
        lambda t,w,o,f,u,r: f != w and f != o and t != f and f != u and f != r,
        lambda t,w,o,f,u,r: u != w and u != o and u != f and t != u and u != r,
        lambda t,w,o,f,u,r: r != w and r != o and r != f and r != u and t != r,        
        })