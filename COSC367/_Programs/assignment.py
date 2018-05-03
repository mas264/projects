from search import *
import heapq
import math

class MapGraph(Graph):
    
    def __init__(self, graph):
        
        self.graph = graph
        self.starting_list = set()
        self.goal_nodes = []
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
                    self.goal_nodes.append((row_count, col_count))
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


        x, y = self.goal_nodes[0]       
        dx = abs(x-node[0])
        dy = abs(y-node[1])
                
        return (dx + dy) + (1 - 2 * 1) * min(dx, dy)
        
        
            
            
            
class AStarFrontier():

    def __init__(self, graph):
        
        self.graph = graph
        self.container = []
        self.visited = []
        self.counter = 0
    
    def add(self, path):
        cost = 0

        for n in path:
            cost += n.cost 
        cost += self.graph.estimated_cost_to_goal(path[-1].head)
            
        if path[-1].head not in self.visited:
            heapq.heappush(self.container, (cost, [self.counter, path]))
            self.counter += 1
    
        

    def __iter__(self):
        """Returns a generator. The generator selects and removes a path from
        the frontier and returns it. A path is a sequence (tuple) of
        Arc objects. Override this method according to the desired
        search strategy.

        """
        
        while self.container != []:
            
            cost, path = heapq.heappop(self.container)
            
            if path[1][-1].head not in self.visited:
                self.visited.append(path[1][-1].head)
                yield(path[1])        
            
            
class LCFSFrontier(Frontier):
    """Implements a frontier container appropriate for lowest cost first search
    ."""

    def __init__(self):
        """The constructor takes no argument. It initialises the
        container to an empty list."""
        self.container = []
        self.visited = []
        self.counter = 0

    def add(self, path):
        """Adds a new path to the frontier. A path is a sequence (tuple) of
                Arc objects."""
        
        cost = 0
        for n in path:
            cost += n.cost
        
        if path[-1].head not in self.visited:
            heapq.heappush(self.container, (cost, [self.counter, path]))
            self.counter += 1
        
    def __iter__(self):
        """Returns a generator. The generator selects and removes a path from
                the frontier and returns it."""        
        
        while self.container != []:
            
            cost, path = heapq.heappop(self.container)
            
            if path[1][-1].head not in self.visited:
                self.visited.append(path[1][-1].head)
                yield(path[1])
            
            

def print_map(map_graph, frontier, solution):
    """prints a map such that the position of the walls, obstacles and the goal
    point are all unchanged and they are marked by the same set of characters in
    the original map string. Those free spaces that have been expanded during 
    the search are marked with a '.' and those free spaces that are a part of 
    the solution (best path to goal) are marked with '*'."""
    
    best_paths = []
    graph_list = map_graph.graph_list

    if solution != None:
        for path in solution:
            best_paths.append(path.head)
        
    graph = []
    new_graph = []
    for line in graph_list:
        current_line = list(line)
        graph.append(current_line)
        
    for row, col in frontier.visited:
        if graph[row][col] == ' ':
            graph[row][col] = '.' 
    for row, col in best_paths:
        if graph[row][col] == '.':
            graph[row][col]= '*'
            
    for line in graph:
        new_graph.append(''.join(line))
    
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
    from search import *
    import heapq
    import math
    
    class MapGraph(Graph):
        
        def __init__(self, graph):
            
            self.graph = graph
            self.starting_list = set()
            self.goal_nodes = []
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
                        self.goal_nodes.append((row_count, col_count))
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
    
    
            x, y = self.goal_nodes[0]       
            dx = abs(x-node[0])
            dy = abs(y-node[1])
                    
            return (dx + dy) + (1 - 2 * 1) * min(dx, dy)
            
            
                
                
                
    class AStarFrontier():
    
        def __init__(self, graph):
            
            self.graph = graph
            self.container = []
            self.visited = []
            self.counter = 0
        
        def add(self, path):
            cost = 0
    
            for n in path:
                cost += n.cost 
            cost += self.graph.estimated_cost_to_goal(path[-1].head)
                
            if path[-1].head not in self.visited:
                heapq.heappush(self.container, (cost, [self.counter, path]))
                self.counter += 1
        
            
    
        def __iter__(self):
            """Returns a generator. The generator selects and removes a path from
            the frontier and returns it. A path is a sequence (tuple) of
            Arc objects. Override this method according to the desired
            search strategy.
    
            """
            
            while self.container != []:
                
                cost, path = heapq.heappop(self.container)
                
                if path[1][-1].head not in self.visited:
                    self.visited.append(path[1][-1].head)
                    yield(path[1])        
                
                
    class LCFSFrontier(Frontier):
        """Implements a frontier container appropriate for lowest cost first search
        ."""
    
        def __init__(self):
            """The constructor takes no argument. It initialises the
            container to an empty list."""
            self.container = []
            self.visited = []
            self.counter = 0
    
        def add(self, path):
            """Adds a new path to the frontier. A path is a sequence (tuple) of
                    Arc objects."""
            
            cost = 0
            for n in path:
                cost += n.cost
            
            if path[-1].head not in self.visited:
                heapq.heappush(self.container, (cost, [self.counter, path]))
                self.counter += 1
            
        def __iter__(self):
            """Returns a generator. The generator selects and removes a path from
                    the frontier and returns it."""        
            
            while self.container != []:
                
                cost, path = heapq.heappop(self.container)
                
                if path[1][-1].head not in self.visited:
                    self.visited.append(path[1][-1].head)
                    yield(path[1])
                
                
    
    def print_map(map_graph, frontier, solution):
        """prints a map such that the position of the walls, obstacles and the goal
        point are all unchanged and they are marked by the same set of characters in
        the original map string. Those free spaces that have been expanded during 
        the search are marked with a '.' and those free spaces that are a part of 
        the solution (best path to goal) are marked with '*'."""
        
        best_paths = []
        graph_list = map_graph.graph_list
    
        if solution != None:
            for path in solution:
                best_paths.append(path.head)
            
        graph = []
        new_graph = []
        for line in graph_list:
            current_line = list(line)
            graph.append(current_line)
            
        for row, col in frontier.visited:
            if graph[row][col] == ' ':
                graph[row][col] = '.' 
        for row, col in best_paths:
            if graph[row][col] == '.':
                graph[row][col]= '*'
                
        for line in graph:
            new_graph.append(''.join(line))
        
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
        
        

'''
Alternative Solution
search import *
import itertools, heapq

class MapGraph(Graph):
    """Represents a routing problem. The problem is given by a
    rectangular map in the form of a string. The map contains a
    starting state a goal state and typicaly a few obstacles. The
    objective is to find the shortest path from the starting point to
    the goal point."""

    def __init__(self, map_str):
        # cleaning up the map_str
        self.map =  map_str.splitlines()
        self.starting_list = []

        # initialising the starting and goal states
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] in "S":
                    self.starting_list.append((i,j))
                if self.map[i][j] in "G":
                    self.goal_node = (i,j)

    def starting_nodes(self):
        return self.starting_list

    def is_goal(self, node):
        return self.goal_node == node

    def outgoing_arcs(self, node):
        row, col = node
        directions_to_consider = [('N' , -1, 0),
                                  ('NE', -1, 1),
                                  ('E' ,  0, 1),
                                  ('SE',  1, 1),
                                  ('S' ,  1, 0),
                                  ('SW',  1, -1),
                                  ('W' ,  0, -1),
                                  ('NW', -1, -1)]
        return [Arc((row, col), (row + dr, col + dc), label, 1) for label, dr, dc in 
                directions_to_consider if self.map[row+dr][col+dc] in 'SG ']


    def estimated_cost_to_goal(self, node):
        """Reutrn the estimated cost to a goal state from the given
        state."""
        goal_row, goal_col = self.goal_node
        row, col = node
        delta_r, delta_c = abs(goal_row-row), abs(goal_col-col)
        return max(delta_r, delta_c)
        # return delta_r + delta_c #Manhattan
        # return math.sqrt(delta_r**2 + delta_c**2) #Euclidean
        

class PriorityFrontier(Frontier):
    """Implements a priority queue for lowest-cost-first search."""
    def __init__(self, heuristic=None, pruning=False, greedy=False):
        self.container = []
        self.count = itertools.count()
        self.heuristic = (heuristic.__getitem__ if type(heuristic) is dict
                          else heuristic)
        self.pruning = pruning
        self.visited = set()
        self.greedy = greedy
        assert not greedy or heuristic


    def add(self, path):
        cost = sum(arc.cost for arc in path) if not self.greedy else 0
        if self.heuristic:
            cost += self.heuristic(path[-1].head)
        if path[-1].head not in self.visited: #always satisfied without pruning
            heapq.heappush(self.container, (cost, next(self.count), path))


    
    def __iter__(self):
        while self.container:
            cost, _, path = heapq.heappop(self.container)
            if self.pruning:
                if path[-1].head in self.visited:
                    continue
                else:
                    self.visited.add(path[-1].head)
            yield path

class AStarFrontier(PriorityFrontier):
    def __init__(self, graph):
        super().__init__(heuristic=graph.estimated_cost_to_goal, pruning=True)


class LCFSFrontier(PriorityFrontier):
    def __init__(self):
        super().__init__(pruning=True)

        
def print_map(map_graph, frontier=[], solution=None):
    stars = {arc.head for arc in solution[1:-1]} if solution else set()
    for i in range(len(map_graph.map)):
        for j in range(len(map_graph.map[i])):
            if (i, j) in stars:
                print('*', end='')
            elif (i, j) in frontier.visited and map_graph.map[i][j] not in 'SG':
                print('.', end='')
            else:
                print(map_graph.map[i][j], end='')
        print()
'''