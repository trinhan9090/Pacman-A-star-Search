from Problem import Node, Graph 
import math
import heapq

class Search():
    """"
    The heuristic function is aim to returns the nearest manhattan distance from pac-man position to a food or a pie
    """
    def heuristic(self, node): 
        node_y, node_x = node.pac[0], node.pac[1]
        
        nearest_food = math.inf
        nearest_pie = math.inf
        pie_pos = None

        for i in node.getFoods():
            manhattan = abs(node_y-i[0]) + abs(node_x - i[1]) 
            if manhattan <= nearest_food:
                nearest_food = manhattan

        for i in node.getPie():
            manhattan = abs(node_y-i[0]) + abs(node_x - i[1])
            if manhattan <= nearest_pie:
                nearest_pie = manhattan
                pie_pos = i

        if pie_pos and nearest_pie < nearest_food: # if we ran out of pie, didnt need to check
            # check if it eats pie, will it create a shorter way to get to any food?
            food_from_pie = math.inf
            for i in node.getFoods():
                manhattan = abs(pie_pos[0]-i[0]) + abs(pie_pos[1] - i[1])
                if manhattan <= food_from_pie:
                    food_from_pie = manhattan
            if food_from_pie + nearest_pie < nearest_food:
                return nearest_pie 
            else:
                return nearest_food 
        return nearest_food 

    """
    this function is use to handles special corners, it will returns a new node, with the position depends on the actions agent choose to make
    """
    def handler_special_corners(self, node, action, graph):
        temp = node.getPosition()
        y, x = temp[0], temp[1]
        max_y, max_x = len(graph.grid), len(graph.grid[0])
        flag = False # flag to check if the teleports makes pac-man eats a pie
        new_pos = ()

        # from the special corners, teleport pac-man to the opposite corner
        if y == x == 1:
            new_pos = (max_y - 2, max_x -2)
        elif y == 1 and x == max_x -2:
            new_pos = (max_y-2, 1)
        elif y == max_y-2 and x == 1:
            new_pos = (1, max_x-2)
        elif y == max_y-2 and x == max_x-2:
            new_pos = (1, 1)
            
        remaining_foods = list(node.getFoods())
        remaining_pies = list(node.getPie())

        if new_pos in remaining_foods:
            remaining_foods.remove(new_pos)
        elif new_pos in remaining_pies:
            remaining_pies.remove(new_pos)
            flag = True
        new_node = Node(new_pos,tuple(remaining_foods),tuple(remaining_pies),action,node)
     
        if flag == True:
            new_node.setPower(5) # set the power to pac-man
        else:
            new_node.setPower(max(0, node.power - 1))

        return new_node


    """
    Check the current position is a corner or not
    """
    def check_corners(self, pos, graph):
        max_y = len(graph.grid)
        max_x = len(graph.grid[0])
        special_corners = [(1,1), (max_y-2, 1), (max_y-2, max_x-2), (1, max_x - 2)]
        if pos in special_corners:
            return True
        return False

    def get_successors(self, node, graph):
        successors = [] # list of successors
        temp = node.getPosition() # access to pac position of current node
        y, x = temp[0], temp[1] # position of current pac

        # all actions of pacman
        
        actions = { 
            'U': (-1, 0), #go up
            'D': (+1, 0), #go down
            'L': (0, -1), #go left
            'R': (0, +1) # go right
        } 

        max_y = len(graph.grid) 
        max_x = len(graph.grid[0]) 
        
        for action, (dy, dx) in actions.items():
            new_x, new_y = x + dx, y + dy # new position of pacman, base on the action it makes
            remaining_foods = list(node.getFoods()) # make a copy list of the remaining foods of the current_node
            remaining_pies = list(node.getPie()) # make a copy list of the remaining pies of the current_node
            new_pos = (new_y, new_x) # pacman new #position

            # check whether current position of pac-man is at corners, and the action it choose makes it go towards a wall, so it will have to teleport
            if self.check_corners((y, x), graph) and graph.grid[new_y][new_x] == "%":
                successor = self.handler_special_corners(node, action, graph) # receive a node contains the opposite position of pac-man
                successors.append(successor) # append the new node to the successors list
                continue
            
            # check if there is any possible out of range error
            if new_x < 0 or new_x >= max_x or new_y < 0 or new_y >= max_y:
                continue

            # Check if pacman is attends to go through a wall
            if graph.grid[new_y][new_x] == "%":
                if node.power == 0: # if it doesn't have eaten the magical_pie, the action cannot be done
                    continue
                else:
                    successor = Node(new_pos, tuple(remaining_foods), tuple(remaining_pies), action, node)
                    successor.setPower(max(0, node.power - 1)) # if it have power, the move is gonna cost 1
                    successors.append(successor)
                    continue
            if new_pos in remaining_foods: # pac-man eats food
                remaining_foods.remove(new_pos)
                successor = Node(new_pos, tuple(remaining_foods), tuple(remaining_pies), action, node)
                successor.setPower(max(0, node.power - 1))  # if it have power, the move is gonna cost 1, if not, power will stay max at 0
            elif new_pos in remaining_pies: #pac-man eats pie
                remaining_pies.remove(new_pos)
                successor = Node(new_pos, tuple(remaining_foods), tuple(remaining_pies), action, node)
                successor.setPower(5) # if it eats a pie, set the new power
            else: # just a move
                successor = Node(new_pos, tuple(remaining_foods), tuple(remaining_pies), action, node)
                successor.setPower(max(0, node.power - 1))
            successors.append(successor)
            
        return successors 

    def search(self, filepath):
        g = Graph()
        g.load_map(filepath)
        start_node = Node(g.get_pacman(),g.get_foods(), g.get_pies()) # init state
        start_node.setG(0) 
        start_node.setF(self.heuristic(start_node))

        open = list() # frontier, store node that is not expand
        visited = set() # stored node that is exapaneded

        heapq.heapify(open) # turn list to min-heap
        heapq.heappush(open, (start_node.getF(), start_node) ) # store a tuple (f(node), node) so that heapq can sort a mini heap

        # A star search
        while len(open) > 0:
            _, curr_node = heapq.heappop(open)

            if curr_node in visited:
                continue

            visited.add(curr_node)

            if len(curr_node.getFoods()) <= 0: # goal state, will call the path construct function
                return self.reconstructPath(curr_node)

            neighbors =  self.get_successors(curr_node, g) # take all valid successors

            for neighbor in neighbors:
                neighbor.setParent(curr_node)
                neighbor.setG(curr_node.getG() + 1)
                neighbor.setF(curr_node.getG() + 1 + self.heuristic(neighbor))
                if (neighbor.getF(), neighbor) not in open:
                    heapq.heappush(open, (neighbor.getF(), neighbor))    
                      
        return self.reconstructPath(curr_node)
    
    def reconstructPath(self, node):
        tempNode = node
        path = []
        pos = [] # if there was teleport, pos can know
        cost = node.getG()
        while tempNode.getParent() is not None:
            path.append(tempNode.getAction())
            pos.append(tempNode.getPosition())
            tempNode = tempNode.getParent()
        return path[::-1], pos[::-1], cost # return the path, all the position for each path, and total cost