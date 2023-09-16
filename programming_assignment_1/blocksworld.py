import sys

import heapq


class PriorityQueue:
    def __init__(self):
        self._queue = []

    def push(self, item, score):
        heapq.heappush(self._queue, (score, item))

    def pop(self):
        if not self._queue:
            raise IndexError("pop from an empty priority queue")
        return heapq.heappop(self._queue)[1]

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
            for destination_row in range(0, len(grid)):  # Only consider rows below
                # Copy the current state
                new_state = State([row[:] for row in grid])
                new_state.move_block(rightmost_block, destination_row)  # Move the block
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

    print(content_between_delimiters)
    return content_between_delimiters


def process_content(content):
    stacks, blocks, moves = [int(num)for num in content[0][0].split()]
    initial_state_content = content[1]
    initial_state = State(initial_state_content)
    goal_state_content = content[2]
    goal_state = State(goal_state_content)
    return stacks, blocks, moves, initial_state, goal_state


def main():
    if len(sys.argv) < 1:
        print("Usage: python blocksworld.py <filename>")
        sys.exit(1)
    file_path = 'probs\\' + sys.argv[1]

    content = read_file(file_path)
    stacks, blocks, moves, initial_state, goal_state = process_content(content)
    all_possible_states = get_all_possible_states(initial_state)
    print(len(all_possible_states))
    print(initial_state)
    print()
    for state in all_possible_states:
        print(state)
        print()



if __name__ == "__main__":
    main()
