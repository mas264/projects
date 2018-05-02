from search import *
import heapq
import math

class MapGraph(Graph):
    
    def __init__(self, graph):
        
        self.graph = graph
        self.starting_list = set()
        self.goal_nodes = set()
        self.obstacles = set()
        self.locations =         [('N' , (-1, 0)),
                                  ('NE', (-1, 1)),
                                  ('E' ,  (0, 1)),
                                  ('SE',  (1, 1)),
                                  ('S' ,  (1, 0)),
                                  ('SW',  (1, -1)),
                                  ('W' ,  (0, -1)),
                                  ('NW', (-1, -1))] 
        self.row_boandary = 0
        self.col_boundary = 0
        
    def read_graph(self):
        """Reads the graph provided by the string"""
        
        
        self.graph_list = self.graph.splitlines()
        row_count = 0
        col_count = 0
        
        
        for row in self.graph_list:
            for col in row:
                if col == 'X':
                    self.obstacles.add((row_count, col_count))
                if col == 'G':
                    self.goal_nodes.add((row_count, col_count))
                if col == 'S':
                    self.starting_list.add((row_count, col_count))
                
                col_count += 1
            
            self.col_boundary = col_count-2
            row_count += 1
            col_count = 0
        
        self.row_boundary = row_count-2
        
        
                
        
    def is_goal(self, node):
        """Returns true if the given node is a goal state."""
        
        return node in self.goal_nodes

    def starting_nodes(self):
        """Returns a sequence of starting nodes. Often there is only one
        starting node but even then the function returns a sequence
        with one element. It can be implemented as an iterator.

        """
        self.read_graph()
        return self.starting_list


    def get_direction(self, tail_node, head_node):
        """returns the direction from node to possible next location"""
        
        x = head_node[0]-tail_node[0]
        y = head_node[1]-tail_node[1]
        
        for direction, loc in self.locations:
            if loc == (x, y):
                return [(x, y), direction]
    
    
    def outgoing_arcs(self, tail_node):
        """Given a node it returns a sequence of arcs (Arc objects)
        which correspond to the actions that can be taken in that
        state (node)."""

        possible_locs = set()
        for row in range(tail_node[0]-1, tail_node[0]+2):
            for col in range(tail_node[1]-1, tail_node[1]+2):
                if row in range(1, self.row_boundary+1) and \
                   col in range(1, self.col_boundary+1):
                    location = (row, col)
            
                    if location not in self.obstacles and location != tail_node:
                        possible_locs.add(location)
                        
        for location, point in self.locations:
            for head_node in possible_locs:
                coordinate, direction = self.get_direction(tail_node, head_node)
                if location == direction:
                    yield Arc(tail_node, head_node, direction, cost=1)
                    

    def estimated_cost_to_goal(self, node):
        """Return the estimated cost to a goal node from the given
        state. This function is usually implemented when there is a
        single goal state. The function is used as a heuristic in
        search. The implementation should make sure that the heuristic
        meets the required criteria for heuristics."""

        """if len(self.goal_nodes) == 1:
            for x, y in self.goal_nodes:
                return abs(x-node[0]) + abs(y-node[1])"""
        
        if len(self.goal_nodes) == 1:       #euclidean
            for x, y in self.goal_nodes:
                return math.sqrt(((x-node[0])**2)+((y-node[1])**2))
            
            
            
class AStarFrontier():

    def __init__(self, graph):
        
        self.graph = graph
        self.container = []
        self.visited = set()
        self.expanded = set()
    
    def add(self, path):
        cost = 0

        for n in path:
            self.expanded.add(n.head)
            cost += n.cost + self.graph.estimated_cost_to_goal(n.head)
            
        if path[-1].head not in self.visited:            
            heapq.heappush(self.container, (cost, path))
        

    def __iter__(self):
        """Returns a generator. The generator selects and removes a path from
        the frontier and returns it. A path is a sequence (tuple) of
        Arc objects. Override this method according to the desired
        search strategy.

        """
        
        while self.container != []:
            
            cost, path = heapq.heappop(self.container)
            self.visited.add(path[-1].head)
            yield(path)        
            
            
class LCFSFrontier(Frontier):
    """Implements a frontier container appropriate for lowest cost first search
    ."""

    def __init__(self):
        """The constructor takes no argument. It initialises the
        container to an empty list."""
        self.container = []
        self.visited = set()

    def add(self, path):
        """Adds a new path to the frontier. A path is a sequence (tuple) of
                Arc objects."""
        
        cost = 0
        for n in path:
            cost += n.cost
            
        heapq.heappush(self.container, (cost, path))
        
    def __iter__(self):
        """Returns a generator. The generator selects and removes a path from
                the frontier and returns it."""        
        
        while self.container != []:
            
            cost, path = heapq.heappop(self.container)
            self.visited.add(path[-1].head)
            yield(path)
            
            

def print_map(map_graph, frontier, solution):
    """prints a map such that the position of the walls, obstacles and the goal
    point are all unchanged and they are marked by the same set of characters in
    the original map string. Those free spaces that have been expanded during 
    the search are marked with a '.' and those free spaces that are a part of 
    the solution (best path to goal) are marked with '*'."""
    
    best_paths = []
    graph_list = map_graph.graph_list
    expanded = set()
    
    print(frontier.container)
    for cost, paths in frontier.container:
        for path in paths:
            #expanded.add(path.head)
            if path.tail is not None:
                expanded.add(path.tail)
            
    for path in solution:
        best_paths.append(path.head)
        
    new_graph = []
    current_row = 0
    for line in graph_list:
        current_line = list(line)
        for row, col in sorted(expanded):
            if row == current_row and current_line[col] == ' ':
                current_line[col] = '.' 
        for row, col in sorted(best_paths):
            if row == current_row and (current_line[col] == '.' or current_line[col] == ' '):
                current_line[col] = '*'
        new_graph.append(''.join(current_line))
        current_row += 1
    
    print(expanded)
    for l in new_graph:
        print(l)

            
        
    
        
    
def main():
    map_str = """\
    +----+
    | S  |
    | SX |
    | X G|
    +----+
    """
    
    map_graph = MapGraph(map_str)
    frontier = AStarFrontier(map_graph)
    solution = next(generic_search(map_graph, frontier), None)
    print_actions(solution)    
    
if __name__ == "__main__":
    main()
    