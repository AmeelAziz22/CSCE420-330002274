import sys


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
    print(initial_state)


def main():
    if len(sys.argv) < 1:
        print("Usage: python blocksworld.py <filename>")
        sys.exit(1)
    file_path = 'probs\\' + sys.argv[1]

    content = read_file(file_path)
    process_content(content)


if __name__ == "__main__":
    main()
