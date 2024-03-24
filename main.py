from PIL import Image, ImageDraw


class Node:
    def __init__(self, state, action, parent):
        self.state = state
        self.action = action
        self.parent = parent


class QueuedFrontier:
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            return None

        node = self.frontier[0]
        self.frontier = self.frontier[1:]
        return node


class StackedFrontier(QueuedFrontier):
    def remove(self):
        if self.empty():
            return None

        node = self.frontier[-1]
        self.frontier = self.frontier[:-1]
        return node


class Maze:
    def __init__(self, txt_maze):
        self.maze = []
        with open(txt_maze, "r") as f:
            lines = f.readlines()
        for line in lines:
            self.maze.append(list(line[:-1]))

    def start(self):
        for i in range(len(self.maze)):
            for j in range(len(self.maze)):
                if self.maze[i][j] == "A":
                    return tuple([i, j])

    def terminal(self, state):
        if self.maze[state[0]][state[1]] == "B":
            return True
        return False

    def neighbours(self, state):
        neighbours = []
        x, y = state[0], state[1]
        if y + 1 < len(self.maze) and self.maze[x][y + 1] != "#":
            neighbours.append(tuple([x, y + 1]))
        if x + 1 < len(self.maze) and self.maze[x + 1][y] != "#":
            neighbours.append(tuple([x + 1, y]))
        if x - 1 > -1 and self.maze[x - 1][y] != "#":
            neighbours.append(tuple([x - 1, y]))
        if y - 1 > -1 and self.maze[x][y - 1] != "#":
            neighbours.append(tuple([x, y - 1]))

        return neighbours

    def draw(self):

        size = 40

        img = Image.new(mode="RGB", size=(size * len(self.maze), size * len(self.maze)))

        draw = ImageDraw.Draw(img)

        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if self.maze[i][j] == "#":
                    draw.rectangle(
                        (float(j * size), float(i * size), float(j * size + size), float(i * size + size)),
                        fill="blue",
                        outline="black",
                    )
                if self.maze[i][j] == " ":
                    draw.rectangle(
                        (float(j * size), float(i * size), float(j * size + size), float(i * size + size)),
                        fill="yellow",
                        outline="black",
                    )
                if self.maze[i][j] == "*":
                    draw.rectangle(
                        (float(j * size), float(i * size), float(j * size + size), float(i * size + size)),
                        fill="red",
                        outline="black",
                    )
                if self.maze[i][j] == "A":
                    draw.rectangle(
                        (float(j * size), float(i * size), float(j * size + size), float(i * size + size)),
                        fill="green",
                        outline="black",
                    )
                if self.maze[i][j] == "B":
                    draw.rectangle(
                        (float(j * size), float(i * size), float(j * size + size), float(i * size + size)),
                        fill="white",
                        outline="black",
                    )

        img.show()


def main():
    maze = Maze("./mazes/maze1.txt")

    frontier = StackedFrontier()

    explored = []

    start = Node(maze.start(), None, None)

    frontier.add(start)

    while True:
        if frontier.empty():
            raise Exception("No solution found")

        node = frontier.remove()

        explored.append(node.state)

        if maze.terminal(node.state):
            actions = []
            while node.parent is not None:
                actions.append(node.action)
                node = node.parent

            print(f"actions: {actions[::-1]}")
            maze.draw()

            return

        else:
            neighbours = maze.neighbours(node.state)
            for neighbour in neighbours:
                if neighbour not in explored:
                    action = tuple([neighbour[0] - node.state[0], neighbour[1] - node.state[1]])
                    child = Node(neighbour, action, node)
                    maze.maze[node.state[0]][node.state[1]] = "*"
                    frontier.add(child)


if __name__ == "__main__":
    main()
    