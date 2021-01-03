import sys
from collections import deque
import heapq

# to run code: python3 blockmaze.py examples/maze1.txt

#git commands 
#git fetch --all 
#git reset --hard origin/master
#git reset --hard origin/<branch_name>
#git add blockmaze.py
#git commit -m “note”
#git push


class Node:
    def __init__(self, parent = None, location = None, isVertical = None):
        
        # Keep track of x and y coordinates: [(x1,y1), (x2,y2)]
        self.location = location

        # Boolean to store orientation of the block (vertical/horizontal)
        self.isVertical = isVertical

        # Is the next node reachable or is it a wall/obstacle?
        # self.isReachable = isReachable

        self.parent = None

        # Heuristic to store move cost so far to reach goal
        self.g = 0

        # Heuristic to store the estimated distance from current square to goal square
        self.h = 0

        # The sum of the moveCost and distEstimate heuristics
        self.f = 0
    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.location == other.location
        

def read_file(filename):
    # Read in maze files
    print("Reading maze: " + filename)

    maze_list = []

    maze = open(filename)

    # read in each row from the maze
    for row in maze:
        row = row.rstrip('\n')
        maze_list.append(row)
        print (row)
      
    maze.close()

    return maze_list


def find_path(maze_list):
    # getting coordinates of start position, obstacles, and goal position
    obstacles = []
    x = 0
    y = 0
    grid = []
    maze1 = maze_list
    for row in (maze_list):
        for char in row:
            if char == 'S':
                start = ([x,y],[x,y])
               
            if char == '*':
                obstacles.append([x,y])
               
            if char == 'G':
                #goal = ([x,y],[x,y])
                goal = ((x,y),(x,y))
            y += 1
        y = 0
        x += 1
   
    return start, goal


#returning a list of the succesors of the selected node
def get_succesor_nodes(currentNode, maze_list):
    successors = []
    #check if its vertical
    if currentNode.isVertical == True: 
        #the possible moves that the block can make
        nodePos = [((0,1),(0,2)), ((0,-1),(0,-2)), ((-1,0),(-2,0)), ((1,0),(2,0))]
        #iterates through the possible move and checks if out of bound or an obstacle
        for positions in nodePos:
            
            newPosition = ((currentNode.location[0][0] + positions[0][0], currentNode.location[0][1] + positions[0][1]), (currentNode.location[1][0] + positions[1][0], currentNode.location[1][1] + positions[1][1]))
            
            if (newPosition[0][0] > newPosition[1][0] + 1) or (newPosition[0][1] > newPosition[1][1] + 1):
                continue 

            if (newPosition[0][0] < newPosition[1][0]-1) or (newPosition[0][1] < newPosition[1][1] - 1):
                continue 

            if newPosition[0][0] > (len(maze_list) - 1) or newPosition[0][0] < 0 or newPosition[0][1] > (len(maze_list[len(maze_list) -1]) - 1) or newPosition[0][1] < 0:
                continue
            if newPosition[1][0] > (len(maze_list) - 1) or newPosition[1][0] < 0 or newPosition[1][1] > (len(maze_list[len(maze_list) -1]) - 1) or newPosition[1][1] < 0:
                continue

            if maze_list[newPosition[0][0]][newPosition[0][1]] == '*':
                continue
            if maze_list[newPosition[1][0]][newPosition[1][1]] == '*':
                continue
            #we want to create the node that are possible after the checks 
            print('A')
            newNode = Node(currentNode, newPosition, False)
            newNode.parent = currentNode
            #add it to the successors list 
            successors.append(newNode)
    else:
        #meaing its horizontal
        #checking the orientation of the horizontal block
        if currentNode.location[0][0] == currentNode.location[1][0]: 
            #or currentNode.location[0][1] == currentNode.location[1][1]:
            nodePos = [((1,0),(1,0)), ((-1,0),(-1,0)), ((0,2), (0,1)), ((0,-1),(0,-2))]
            print('yes')
        else:
            nodePos = [((2,0),(1,0)), ((-1,0),(-2,0)), ((0,1),(0,1)), ((0,-1),(0,-1))]
            print('no')
        #iterates through the possible move and checks if out of bound or an obstacle
        for positions in nodePos:
            newPosition = ((currentNode.location[0][0] + positions[0][0], currentNode.location[0][1] + positions[0][1]), (currentNode.location[1][0] + positions[1][0], currentNode.location[1][1] + positions[1][1]))
            
            if (newPosition[0][0] > newPosition[1][0] + 1) or (newPosition[0][1] > newPosition[1][1] + 1):
                continue
            if (newPosition[0][0] < newPosition[1][0] - 1) or (newPosition[0][1] < newPosition[1][1] - 1):
                continue

            if newPosition[0][0] > (len(maze_list) - 1) or newPosition[0][0] < 0 or newPosition[0][1] > (len(maze_list[len(maze_list) -1]) - 1) or newPosition[0][1] < 0:
                continue
            if newPosition[1][0] > (len(maze_list) - 1) or newPosition[1][0] < 0 or newPosition[1][1] > (len(maze_list[len(maze_list) -1]) - 1) or newPosition[1][1] < 0:
                continue

            if maze_list[newPosition[0][0]][newPosition[0][1]] == '*':
                continue
            if maze_list[newPosition[1][0]][newPosition[1][1]] == '*':
                continue
            #we want to create the node that are possible after the checks
            newNode = Node(currentNode, newPosition, False)
            newNode.parent = currentNode
            #before appending it we wan to check if its horizontal now or if its vertical 
            if newNode.location[0][0] == newNode.location[1][0] and newNode.location[0][1] == newNode.location[1][1]:
                newNode.isVertical = True
            print(newNode.isVertical)
            successors.append(newNode)
    numNodes = len(successors)     
    return successors, numNodes



def Asearch(maze_list):   # A* search:
    
    # Create start and end node
        startPos, goalPos = find_path(maze_list)
    
        startNode = Node(None, startPos, True)
        goalNode = Node(None, goalPos, True)
      #init our hueristics 
        startNode.g = startNode.h = startNode.f = 0
        goalNode.g = goalNode.h = goalNode.f = 0
       
       # Initialize both open and closed list
        frontier = []
        heapq.heapify(frontier)
        visited = []
       #keeping track of nodes generated
        totalNodes = 0

        heapq.heappush(frontier, startNode)
        #Loop until the frontier is empty
        while len(frontier) > 0:
            # Look at acceptable neighbors (not a wall or obstacle) and find the one with the lowest costTotal
            currentNode = frontier[0]
            currentIndex = 0
            for index, item in enumerate(frontier):
                if item.f < currentNode.f:
                    currentNode = item
                    currentIndex = index

            # Pop current off open list, add to closed list
            heapq.heappop(frontier)
            heapq.heapify(frontier)
            visited.append(currentNode)
            print('cur')
            print(currentNode.location)
            print('goal')
            print(goalNode.location)
            # Found the goal
            if currentNode.location[0][0] == goalNode.location[0][0] and currentNode.location[0][1] == goalNode.location[0][1]:
                if currentNode.isVertical:
                    print ('Goal')
                    path = []
                    current = currentNode
                    while current is not None:
                        path.append(current.location)
                        current = current.parent
                    print('Length of Path: ')
                    print (len(path))
                    print('Number of nodes visited: ')
                    print (len(visited))
                    for a in path:
                        print(a)
                    return path[::-1]
                    #return path.reverse()

            successors, numNodes = get_succesor_nodes(currentNode, maze_list)
            totalNodes = totalNodes + numNodes
            print('Total Nodes: ')
            print (totalNodes)
            # Loop through children
            for child in successors:
             # Child is on the closed list
                for visitedChild in visited:
                    if child.location == visitedChild.location:
                        continue
                # Create and update the f, g, and h values
                child.g = currentNode.g + 1
                child.h = (((child.location[0][0] - goalNode.location[0][0]) ** 2) + ((child.location[0][1] - goalNode.location[0][1]) ** 2))
                child.f = child.g + child.h
                # Child is already in the open lis
                for item in frontier:
                    if child.location == item.location:
                        if child.g > item.g:
                        #remove old child
                            continue
                        else:
                            frontier.remove(item)
                            heapq.heapify(frontier)
                     
               # Add the child to the open list        
                heapq.heappush(frontier, child)
                heapq.heapify(frontier)
        


            

                

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 blockmaze.py mazeFile")
    else: 
        mazeFile = sys.argv[1]
        maze_list = read_file(mazeFile)
        find_path(maze_list)
        path = Asearch(maze_list)
        for a in path:
            print (a)
        
        

if __name__ == "__main__":
    main()
