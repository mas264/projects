from search import *
from itertools import dropwhile
import math
import heapq



class LocationGraph(Graph):
    """computes the cost of the arcs based on the information provided"""
    
    
    def __init__(self, nodes, locations, edges, starting_list, goal_nodes, estimates=None):
        """Initialises an explicit graph.
        Keyword arguments:
        nodes -- a set of nodes
        locations -- 2d location of nodes (x, y)
        edges -- a sequence of tuples in the form (tail, head)
        starting_list -- the list of starting nodes (states)
        goal_node -- the set of goal nodes (states)
        """

        # A few assertions to detect possible errors in
        # instantiation. These assertions are not essential to the
        # class functionality.
        assert all(tail in nodes and head in nodes for tail, head, *_ in edges)\
           , "edges must link two existing nodes!"
        assert all(node in nodes for node in starting_list),\
            "The starting_states must be in nodes."
        assert all(node in nodes for node in goal_nodes),\
            "The goal states must be in nodes."

        self.nodes = nodes      
        self.edge_list = edges
        self.locations = locations
        self.starting_list = starting_list
        self.goal_nodes = goal_nodes
        self.estimates = estimates

    def starting_nodes(self):
        """Returns (via a generator) a sequece of starting nodes."""
        for starting_node in self.starting_list:
            yield starting_node

    def is_goal(self, node):
        """Returns true if the given node is a goal node."""
        return node in self.goal_nodes

    def calculate_cost(self, tail, head):
        """calculates the cost of edges"""
        
        x1, y1 = head
        x2, y2 = tail
        return math.sqrt(((x1-x2)**2) + ((y1-y2)**2))
    
    def outgoing_arcs(self, node):
        """Returns a sequence of Arc objects corresponding to all the
        edges in which the given node is the tail node. The label is
        automatically generated."""

        if type(self.edge_list) is set:
            other_direction = {(x[1], x[0]) for x in self.edge_list}
            self.edge_list = self.edge_list.union(other_direction)
            for tail, head in sorted(self.edge_list, key=lambda x: x[1]):
                if tail == node:
                    yield Arc(tail, head, str(tail) + '->' + str(head), 
                              cost=self.calculate_cost(self.locations[tail],
                                              self.locations[head]))
        else: #edge_list is of type list
            other_direction = [(x[1], x[0]) for x in self.edge_list]
            self.edge_list = self.edge_list + other_direction
            for tail, head in sorted(self.edge_list, key=lambda x: x[1]):
                if tail == node:
                    yield Arc(tail, head, str(tail) + '->' + str(head), 
                                cost=self.calculate_cost(self.locations[tail],
                                                          self.locations[head]))            
                
                
class FunkyNumericGraph(Graph):
    """A graph where nodes are numbers. A node (number) n leads to n-1 and
    n+2. Nodes that are divisible by 10 are goal nodes."""
    
    def __init__(self, starting_number):
        self.starting_number = starting_number

    def outgoing_arcs(self, tail_node):
        yield Arc(tail_node, head=tail_node-1, label="1down", cost=1)
        yield Arc(tail_node, head=tail_node+2, label="2up", cost=1)
        
    def starting_nodes(self):
        yield self.starting_number

    def is_goal(self, node):
        return node % 10 == 0
    
    
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


class LCFSFrontier(Frontier):
    """Implements a frontier container appropriate for lowest cost first search
    ."""

    def __init__(self):
        """The constructor takes no argument. It initialises the
        container to an empty list."""
        self.container = []


    def add(self, path):
        
        cost = 0
        for n in path:
            cost += n.cost
            
        heapq.heappush(self.container, (cost, path))
        
    def __iter__(self):
        
        while self.container != []:
            
            cost, path = heapq.heappop(self.container)
            yield(path)


class OrderedExplicitGraph(ExplicitGraph):
    """Subclass of Explicit graph where nodes are expanded in alphabetical order
    """
    
    def __init__(self, nodes, edges, starting_list, goal_nodes, estimates=None):
            """Initialises an explicit graph.
            Keyword arguments:
            nodes -- a set of nodes
            edge_list -- a sequence of tuples in the form (tail, head) or 
                         (tail, head, cost)
            starting_list -- the list of starting nodes (states)
            goal_node -- the set of goal nodes (states)
            """
    
            # A few assertions to detect possible errors in
            # instantiation. These assertions are not essential to the
            # class functionality.
            assert all(tail in nodes and head in nodes for tail, head, *_ in edges)\
               , "edges must link two existing nodes!"
            assert all(node in nodes for node in starting_list),\
                "The starting_states must be in nodes."
            assert all(node in nodes for node in goal_nodes),\
                "The goal states must be in nodes."
    
            self.nodes = nodes      
            self.edge_list = edges
            self.starting_list = starting_list
            self.goal_nodes = goal_nodes
            self.estimates = estimates    
            
    def outgoing_arcs(self, node):
        """Returns a sequence of Arc objects corresponding to all the
        edges in which the given node is the tail node. The label is
        automatically generated."""

        #in reversed alphabetical because LIFO
        for edge in sorted(self.edge_list, key=lambda x: x[1], reverse=True):
            if len(edge) == 2:  # if no cost is specified
                tail, head = edge
                cost = 1        # assume unit cost
            else:
                tail, head, cost = edge
            if tail == node:
                yield Arc(tail, head, str(tail) + '->' + str(head), cost)
    
def main():
    # Example 1
    
    
    graph = LocationGraph(nodes=set('ABC'),
                          locations={'A': (0, 0),
                                     'B': (3, 0),
                                     'C': (3, 4)},
                          edges={('A', 'B'), ('B','C'),
                                 ('B', 'A'), ('C', 'A')},
                          starting_list=['A'],
                          goal_nodes={'C'})
    
    solution = next(generic_search(graph, LCFSFrontier()))
    print_actions(solution)
    
    graph = LocationGraph(nodes=set('ABC'),
                          locations={'A': (0, 0),
                                     'B': (3, 0),
                                     'C': (3, 4)},
                          edges={('A', 'B'), ('B','C'),
                                 ('B', 'A')},
                          starting_list=['A'],
                          goal_nodes={'C'})
    
    solution = next(generic_search(graph, LCFSFrontier()))
    print_actions(solution)    

    pythagorean_graph = LocationGraph(
        nodes=set("abc"),
        locations={'a': (5, 6),
                   'b': (10,6),
                   'c': (10,18)},
        edges=[tuple(s) for s in {'ab', 'ac', 'bc'}],
        starting_list=['a'],
        goal_nodes={'c'})
    
    solution = next(generic_search(pythagorean_graph, LCFSFrontier()))
    print_actions(solution)
    
    graph = ExplicitGraph(nodes=set('ABCD'),
                          edge_list=[('A', 'D', 7), ('A', 'B', 2),
                                     ('B', 'C', 3), ('C', 'D', 1)],
                          starting_list=['A'],
                          goal_nodes={'D'})
    
    solution = next(generic_search(graph, LCFSFrontier()))
    print_actions(solution)    
if __name__ == "__main__":
    main()
