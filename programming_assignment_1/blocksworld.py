import sys

import heapq
from itertools import count


class PriorityQueue:
    def __init__(self):
        self._queue = []
        self.counter = count()  # Counter to ensure unique ordering of nodes

    def push(self, item, score):
        count = next(self.counter)
        heapq.heappush(self._queue, (score, count, item))

    def pop(self):
        if not self._queue:
            raise IndexError("pop from an empty priority queue")
        _, _, item = heapq.heappop(self._queue)
        return item

    def __len__(self):
        return len(self._queue)

    def is_empty(self):
        return len(self) == 0


class State:
    def __init__(self, state_list):
        self.grid = [list(row) for row in state_list]

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.grid])

    def is_goal(self, goal_state):
        return str(self) == str(goal_state)

    def move_block(self, block, destination_row):
        for row in self.grid:
            if block in row:
                row.remove(block)
        self.grid[destination_row].append(block)


class Node:
    def __init__(self, state, parent=None, action=None):
        self.state = state  # BlocksworldState object
        self.parent = parent  # Parent Node
        self.action = action  # Action that led to this state from the parent
        self.children = []  # Child Nodes
        self.depth = 0  # Depth in the tree, initialized to 0
        self.heur = None

        if parent is not None:
            self.depth = parent.depth + 1
            parent.children.append(self)


def get_all_possible_states(state):
    possible_states = []
    unique_states = set()  # To store unique states

    # Get the grid and blocks in the current state
    grid = state.grid

    # Iterate through each row
    for row_index, row in enumerate(grid):
        # Get the rightmost block in the current row (if any)
        rightmost_block = row[-1] if row else None

        # If there is a rightmost block, consider moving it to another row
        if rightmost_block:
            for destination_row in range(0, len(grid)):
                # Copy the current state
                new_state = State([row[:] for row in grid])
                new_state.move_block(
                    rightmost_block, destination_row)  # Move the block
                # Convert state to a string for uniqueness check
                state_str = str(new_state)
                if state_str not in unique_states and state_str != str(state):
                    unique_states.add(state_str)
                    possible_states.append(new_state)

    return possible_states


def read_file(file_path):
    content_between_delimiters = []
    current_content = []

    try:
        with open(file_path, 'r') as file:
            for line in file:
                stripped_line = line.strip()
                if stripped_line == ">>>>>>>>>>":
                    if current_content:
                        content_between_delimiters.append(
                            current_content.copy())
                        current_content.clear()
                else:
                    current_content.append(stripped_line)

            # Append the last section of content (if any) after the last delimiter
            if current_content:
                content_between_delimiters.append(current_content.copy())
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

    return content_between_delimiters


def process_content(content):
    stacks, blocks, moves = [int(num)for num in content[0][0].split()]
    initial_state_content = content[1]
    initial_state = State(initial_state_content)
    goal_state_content = content[2]
    goal_state = State(goal_state_content)
    return stacks, blocks, moves, initial_state, goal_state


def generate_block_list(state, num_stacks, num_blocks):
    """
    Generate a flattened list of blocks with empty spaces based on the number of stacks and blocks.

    Args:
    state (State): The state to generate the list from.
    num_stacks (int): The number of stacks in the state.
    num_blocks (int): The number of blocks in each stack.

    Returns:
    list: The flattened list of blocks and empty spaces.
    """
    grid = state.grid
    flattened_blocks = []

    # Iterate through the rows and blocks and fill with blocks or empty spaces
    for stack in range(num_stacks):
        for block in range(num_blocks):
            if len(grid[stack]) > block:
                flattened_blocks.append(grid[stack][block])
            else:
                flattened_blocks.append(' ')

    return flattened_blocks


def count_blocks_out_of_place(state1, state2, num_stacks, num_blocks):
    state1_f = generate_block_list(state1, num_stacks, num_blocks)
    state2_f = generate_block_list(state2, num_stacks, num_blocks)

    state1_combined = ''.join(state1_f)
    state2_combined = ''.join(state2_f)

    matching_count = 0

    # Compare characters at the same index, ignoring spaces
    for char1, char2 in zip(state1_combined, state2_combined):
        if char1 != ' ' and char1 == char2:
            matching_count += 1

    return (num_blocks-matching_count)

def count_matching_letters(state1, state2, num_stacks, num_blocks):

    state1_f = generate_block_list(state1, num_stacks, num_blocks)
    state2_f = generate_block_list(state2, num_stacks, num_blocks)

    stack_size = num_blocks
    string1 = ''.join(state1_f)
    string2 = ''.join(state2_f)
    matching_count = 0
    # Compare characters at the same index and before
    for i in range(0, len(string1)):
        if string1[i] != ' ' and string1[i]==string2[i]:
            if i % stack_size != 0 and string1[i-1] != string2[i-1]:
                matching_count += 2
            # if i % stack_size != stack_size-1 and string1[i+1] != string2[i+1]:
            #     matching_count += 1

            


    return matching_count

def hill_climbing(state1, state2, num_stacks, num_blocks):
    state1_f = generate_block_list(state1, num_stacks, num_blocks)
    state2_f = generate_block_list(state2, num_stacks, num_blocks)
    

    matrix1 = [state1_f[i:i + num_blocks] for i in range(0, len(state1_f), num_blocks)]
    matrix2 = [state2_f[i:i + num_blocks] for i in range(0, len(state1_f), num_blocks)]


    total_count = 0
    
    for i in range(len(matrix1)):
        stack1 = matrix1[i]
        stack2 = matrix2[i]
        no_match = False
        for j in range(len(stack1)):
            block1 = stack1[j]
            block2 = stack2[j]
            if block1 != block2:
                no_match = True
            if no_match:
                if block1 == ' ' and block2 == ' ':
                    pass
                else:
                    total_count += 1
            else:
                if block1 == ' ' and block2 == ' ':
                    pass
                elif j == 0:
                    pass
                else:
                    total_count -= 2



    return total_count





def pathCost(node, goal_state, num_stacks, num_blocks,bfs):
    if bfs:
        return node.depth
    return (node.depth) + hill_climbing(node.state,goal_state,num_stacks,num_blocks)


def best_first_search(initial_state, goal_state, moves, max_iters, num_stacks, num_blocks,print_iters,bfs):
    reached = {}
    pq = PriorityQueue()
    initial_node = Node(initial_state)
    depth = initial_node.depth
    initial_node.heur=pathCost(initial_node,goal_state,num_stacks,num_blocks,bfs)
    max_qsize = 0
    pq.push(initial_node, depth)
    i = 0
    while not pq.is_empty() and i < max_iters:
        current_node = pq.pop()
        current_state = current_node.state
        if (str(current_state) == str(goal_state)):
            return current_node, max_qsize, i
        successors = get_all_possible_states(current_state)
        if(print_iters):
            print("iter=",i," depth =",current_node.depth,", heurisitc=",pathCost(current_node,goal_state,num_stacks,num_blocks,bfs)-current_node.depth,", score=",pathCost(current_node,goal_state,num_stacks,num_blocks,bfs),"children=",len(successors),"Queue size = ",pq.__len__())
        if (i%50000==0 and print_iters==False):
            print("iter=",i," depth =",current_node.depth,", heurisitc=",pathCost(current_node,goal_state,num_stacks,num_blocks,bfs)-current_node.depth,", score=",pathCost(current_node,goal_state,num_stacks,num_blocks,bfs),"children=",len(successors),"Queue size = ",pq.__len__())
        if pq.__len__() > max_qsize:
            max_qsize = pq.__len__()
        if current_node.depth < moves:
            for state in successors:
                state_node = Node(state, parent=current_node)
                state_cost = pathCost(
                    state_node, goal_state, num_stacks, num_blocks,bfs)
                state_node.heur = state_cost-state_node.depth
                if str(state) not in reached or state_cost < reached[str(state)]:
                    reached[str(state)] = state_cost
                    pq.push(state_node, state_cost)
        i += 1

    return None, max_qsize, i


def main():
    max_iters = 1000000
    print_iters=True
    bfs = False
    if len(sys.argv) < 1:
        print("Usage: python blocksworld.py <filename>")
        sys.exit(1)
    if len(sys.argv)==3:
        if sys.argv[2]=="N":
            print_iters = False
    
    if len(sys.argv)==4:
        if sys.argv[2]=="N":
            print_iters = False
        max_iters = int(sys.argv[3])

    if len(sys.argv) == 5:
        if sys.argv[2]=="N":
            print_iters = False
        max_iters = int(sys.argv[3])
        if sys.argv[4] == "Y":
            bfs=True
    
    file_path = 'probs/' + sys.argv[1]
    content = read_file(file_path)
    stacks, blocks, moves, initial_state, goal_state = process_content(content)
    result, max_qsize, iter = best_first_search(
        initial_state, goal_state, moves, max_iters, stacks, blocks,print_iters,bfs)
    method = "Astar"
    if bfs:
        method = "BFS"
    if result:
        # Traverse the path from the goal state to the initial state
        path = []
        heur_path = []
        while result:
            path.append(result.state)
            heur_path.append(result.heur)
            result = result.parent
        path.reverse()  # Reverse the path to start from the initial state
        heur_path.reverse()
        move = 0
        for state in path:
            score = heur_path[move]
            score += move
            print("move ",move, " pathcost=",move," heurisitc=",heur_path[move]," f(n) = g(n)+h(n)=",score)
            print(state)
            print(">>>>>>")
            move += 1
        
        

        print("Statistics:",file_path," method",method," planlen ", len(path)-1," iter ",iter, " maxq ",max_qsize)
    else:
        print("Statistics:",file_path," method",method," planlen FAILED"," iter ",iter, " maxq ",max_qsize)

if __name__ == "__main__":
    main()
