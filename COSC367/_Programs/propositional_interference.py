import re
from search import *

def clauses(knowledge_base):
    """Takes the string of a knowledge base; returns an iterator for pairs
    of (head, body) for propositional definite clauses in the
    knowledge base. Atoms are returned as strings. The head is an atom
    and the body is a (possibly empty) list of atoms.

    Author: Kourosh Neshatian
    Last Modified: 31 Jul 2015

    """
    ATOM   = r"[a-z][a-zA-z\d_]*"
    HEAD   = r"\s*(?P<HEAD>{ATOM})\s*".format(**locals())
    BODY   = r"\s*(?P<BODY>{ATOM}\s*(,\s*{ATOM}\s*)*)\s*".format(**locals())
    CLAUSE = r"{HEAD}(:-{BODY})?\.".format(**locals())
    KB     = r"^({CLAUSE})*$".format(**locals())

    assert re.match(KB, knowledge_base)

    for mo in re.finditer(CLAUSE, knowledge_base):
        yield mo.group('HEAD'), re.findall(ATOM, mo.group('BODY') or "")
        
        
def forward_deduce(knowledge_base):
    """Takes a string of knowledge base containing propositional definite clauses
    and returns a set of atoms that can be derived as true from the knowledge base
    """
    
    kb_list = list(clauses(knowledge_base))
    derived = []
    
    for head, body in kb_list:
        if body == []:
            derived.append(head)
            
    count = 0
    
    while count < len(kb_list):
        for head, body in kb_list:
            all_in_body = True
            for atom in body:
                if atom not in derived:
                    all_in_body = False
            
            
            if all_in_body == True:
                derived.append(head)
            
        count += 1

                
    return set(derived)
                
class KBGraph(Graph):
    """Poses a knowledge base and a query as a graph"""
    
    def __init__(self, knowledge_base, query):
        """initialises the knowledge base and the query"""
        
        self.kb = list(clauses(knowledge_base))
        self.query = query
    
    def is_goal(self, node):
        """Returns true if the given node is a goal state."""
        
        flag = False
        n = node[0]
        for head, tail in self.kb:
            if n == head:
                flag = True
        
        return flag

        

    def starting_nodes(self):
        """Returns a sequence of starting nodes. Often there is only one
            starting node but even then the function returns a sequence
            with one element. It can be implemented as an iterator.
        
        """
        for node in self.query:
            yield node

        
        
    def outgoing_arcs(self, tail_node):
        """Given a node it returns a sequence of arcs (Arc objects)
        which correspond to the actions that can be taken in that
        state (node)."""  
        
        for head, body in self.kb:
            if tail_node == head:
                
                yield Arc(tail_node, body, str(tail_node) + '->' +str(body), 1)
        
    
class DFSFrontier(Frontier):
    """Implements a frontier container appropriate for depth-first
    search."""


    def __init__(self):
        """The constructor takes no argument. It initialises the
        container to an empty list."""
        self.container = []


    def add(self, path):
        self.container.append(path)

    def __iter__(self):
        
        while self.container != []:
            yield self.container.pop(0)
    
            
            
class BFSFrontier(Frontier):
    """Implements a frontier container appropriate for breath-first
    search."""

    def __init__(self):
        """The constructor takes no argument. It initialises the
        container to an empty list."""
        self.container = []


    def add(self, path):
        self.container.append(path)

    def __iter__(self):
        
        while self.container != []:
            yield self.container.pop(0)
                
