import pygame
import random
from queue import PriorityQueue
from queue import Queue
from queue import LifoQueue

WIDTH = 665
ROWS = 35
WIN = pygame.display.set_mode((WIDTH + 200, WIDTH))
pygame.init()
pygame.display.set_caption("Path Finding Algorithm")


RED = (255, 0, 0)
PINK = (245, 66, 138)
GREEN = (0, 255, 0)
DARKGREEN = (24, 94, 14)
LIGHTORANGE = (255, 174, 0)
YELLOW = (250,250,0)
LIGHTYELLOW = (255, 255, 66)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (171, 176, 172)
LIGHTGREY = (230, 227, 227)
TURQUOISE = (64, 224, 208)
BLUE = (43, 63, 240)
LIGHTBLUE = (0,181,236)
class Cell:
    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.color = WHITE
        self.x = row * width
        self.y = col * width
        self.neighbour = []
        self.distance = float("inf") # for dijkstra algorithm

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == LIGHTORANGE

    def is_open(self):
        return self.color == LIGHTYELLOW

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == BLUE

    def is_end(self):
        return self.color == TURQUOISE

    def is_path(self):
        return self.color == GREEN
    def reset(self):
        self.color = WHITE
        self.neighbour = []

    def make_start(self):
        self.color = BLUE

    def make_closed(self):
        self.color = LIGHTORANGE

    def make_open(self):
        self.color = LIGHTYELLOW

    def make_barrier(self):
        self.color = BLACK

    def make_end(self):
        self.color = BLUE

    def make_path(self):
        self.color = GREEN

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    def update_neighbor(self,board):
        if self.row < self.total_rows - 1 and not board[self.row + 1][self.col].is_barrier():
            self.neighbour.append(board[self.row + 1][self.col])
        if self.row > 0 and not board[self.row - 1][self.col].is_barrier():
            self.neighbour.append(board[self.row - 1][self.col])
        if self.col <  self.total_rows - 1 and not board[self.row][self.col + 1].is_barrier():
            self.neighbour.append(board[self.row][self.col + 1])
        if self.col > 0 and not board[self.row][self.col - 1].is_barrier():
            self.neighbour.append(board[self.row][self.col - 1])

    def __lt__(self, other):
        return False

class Button:
    def __init__(self, color, x, y,width, height,text = ''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win, outline = None):
        if outline:  # Draw ouline
            pygame.draw.rect(win, outline, (self.x - 2,self.y - 2 ,self.width + 4, self.height + 4),0)
        pygame.draw.rect(win, self.color,(self.x, self.y, self.width,self.height), 0)
        if self.text != "":
            font = pygame.font.SysFont('comicsans',30)
            text = font.render(self.text,True,BLACK)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/ 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def is_over(self,pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


def make_board(rows, total_width):
    board = []
    width = total_width // rows  # Width of one cell
    for i in range(rows):
        board.append([])
        for j in range(rows):
            cell = Cell(i,j,width,rows)
            board[i].append(cell)

    return board

    return new

def draw_grid(win, rows, total_width):
    width = total_width // rows
    for i in range(rows):
        pygame.draw.line(win,BLACK,(0,i * width),(total_width, i * width))
        for j in range(rows + 1):
            pygame.draw.line(win, BLACK, (j * width , 0), (j * width ,total_width))


def draw(win, board, rows, total_width):
    win.fill(WHITE)
    # Draw menu
    pygame.draw.rect(win,PURPLE,(WIDTH,0,200,WIDTH),0)
    font = pygame.font.SysFont('comicsans',70)
    text = font.render('MENU',True, LIGHTBLUE)
    win.blit(text,(WIDTH + 30,40,100,100))

    A_Star_Button.draw(win, BLACK)
    Reset_Button.draw(win, BLACK)
    BFS_Button.draw(win, BLACK)
    Exit_Button.draw(win, BLACK)
    DFS_Button.draw(win, BLACK)
    Clear_Button.draw(win, BLACK)
    Random_Button.draw(win,BLACK)
    Dijkstra_button.draw(win,BLACK)

    for row in board:
        for cell in row:
            cell.draw(win)
    draw_grid(win,rows,total_width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap
    return row, col


def h(p1, p2):
    r1,c1 = p1
    r2,c2 = p2
    return abs(r1-r2) + abs(c1 - c2)

def reconstruct_path(came_from,start, end,board):
    current = end
    while came_from[current] != start:
        current = came_from[current]
        if current != end:
            current.make_path()

        draw(WIN,board,ROWS,WIDTH)
        pygame.time.wait(5)


def AStar(board, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start)) # Adding the starting node to the open_set (f_score, count, node)
    came_from = {} # To store the interior that the current node came from.
    g_score = {cell: float("inf") for row in board for cell in row}  # set every node's g_score to inf
    g_score[start] = 0
    f_score = {cell : float("inf") for row in board for cell in row}  # set every node's f_score to inf
    f_score[start] = h(start.get_pos(),end.get_pos())
    open_set_hash= {start} # To indicate whether a node is in the queue or not.
    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from,start,end,board)
            return True

        for neighbor in current.neighbour:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = g_score[neighbor] + h((neighbor.get_pos()),end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor],count,neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor != end:  # Avoid covering the end cell
                        neighbor.make_open()
        draw(WIN,board,ROWS,WIDTH)

        if current != start:  # Avoid covering the start cell
            current.make_closed()

    return False


def BFS(board,start,end):
    queue = Queue()
    queue.put(start)
    visited = {start}
    came_from = {}
    while not queue.empty():
        current = queue.get()
        if current == end:
            reconstruct_path(came_from,start,end,board)
            return True
        if current != start:
            current.make_closed()
        for neighbour in current.neighbour:
            if neighbour not in visited:
                queue.put(neighbour)
                visited.add(neighbour)
                came_from[neighbour] = current
                if neighbour != end:
                    neighbour.make_open()
        draw(WIN,board,ROWS,WIDTH)
    return False


def DFS(board,start,end):
    stack = LifoQueue()
    came_from = {}
    stack.put(start)
    visited = {start}
    while not stack.empty():
        current = stack.get()
        if current == end:
            reconstruct_path(came_from,start,end,board)
            return True
        if current != start:
            current.make_closed()
        for neighbour in current.neighbour:
            if neighbour not in visited:
                stack.put(neighbour)
                visited.add(neighbour)
                came_from[neighbour] = current
                if neighbour != end:
                    neighbour.make_open()

        draw(WIN,board,ROWS,WIDTH)
    return False


def sort_set_by_distance(set):
    set = sorted(set,key= lambda x: x.distance)
    return set


def dijkstra(board,start,end):
    if (not start) or (not end):
        return False
    came_from = {}
    start.distance = 0
    unvisited = {cell for row in board for cell in row}
    while len(unvisited) > 0:
        unvisited = sort_set_by_distance(unvisited)
        closestNode = next(iter(unvisited))
        unvisited.remove(closestNode)
        if closestNode != start and closestNode != end:
            closestNode.make_closed()
        if closestNode == end:
            reconstruct_path(came_from,start,end,board)
            return True
        for neighbour in closestNode.neighbour:
            alt = closestNode.distance + 1
            if alt < neighbour.distance:
                neighbour.distance = alt
                came_from[neighbour] = closestNode
                if neighbour != end:
                    neighbour.make_open()
        draw(WIN,board,ROWS,WIDTH)


def clear(board):
    for row in board:
        for cell in row:
            if not (cell.is_barrier() or cell.is_start() or cell.is_end()):
                cell.reset()


def show_path(board):
    for row in board:
        for cell in row:
            if not (cell.is_barrier() or cell.is_start() or cell.is_end() or cell.is_path()):
                cell.reset()


def random_obs(board):
        for i in range(int(ROWS ** 2 * 0.3)):
            row = random.randint(0,ROWS - 1)
            col = random.randint(0,ROWS-1)
            board[row][col].make_barrier()
# Making buttons
y = 100
gap = 70
height = 40
A_Star_Button = Button(YELLOW, WIDTH + 40, y, 120, height, "A*")
y += gap
Dijkstra_button = Button(YELLOW, WIDTH + 40, y, 120, height, "DIJKSTRA")
y += gap
BFS_Button = Button(YELLOW, WIDTH + 40, y, 120, height, "BFS")
y += gap
DFS_Button = Button(YELLOW, WIDTH + 40, y, 120, height, "DFS")
y += gap
Reset_Button = Button(RED, WIDTH + 40, y, 120, height, "Reset")
y += gap
Clear_Button = Button(RED, WIDTH + 40, y, 120, height, "Clear")
y += gap
Random_Button = Button(RED, WIDTH + 40, y, 120, height, "Random")
y += gap
Exit_Button = Button(RED, WIDTH + 40, y, 120, height, "Exit")


def main():
    board = []
    board = make_board(ROWS, WIDTH)
    start = None
    end = None
    run = True
    while run:
        draw(WIN,board,ROWS,WIDTH)
        for event in pygame.event.get():
            m_pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEMOTION:  # Check motion for button
                if A_Star_Button.is_over(m_pos):
                    A_Star_Button.color = GREEN
                else:
                    A_Star_Button.color = YELLOW

                if Reset_Button.is_over(m_pos):
                    Reset_Button.color = GREEN
                else:
                    Reset_Button.color = RED

                if BFS_Button.is_over(m_pos):
                    BFS_Button.color = GREEN
                else:
                    BFS_Button.color = YELLOW

                if Exit_Button.is_over(m_pos):
                    Exit_Button.color = GREEN
                else:
                    Exit_Button.color = RED

                if DFS_Button.is_over(m_pos):
                    DFS_Button.color = GREEN
                else:
                    DFS_Button.color = YELLOW

                if Clear_Button.is_over(m_pos):
                    Clear_Button.color = GREEN
                else:
                    Clear_Button.color = RED

                if Random_Button.is_over(m_pos):
                    Random_Button.color = GREEN
                else:
                    Random_Button.color = RED

                if Dijkstra_button.is_over(m_pos):
                    Dijkstra_button.color = GREEN
                else:
                    Dijkstra_button.color = YELLOW
            if pygame.mouse.get_pressed()[0]:
                if A_Star_Button.is_over(m_pos):  # Click on button to start A* algo
                    for row in board:
                        for cell in row:
                            cell.update_neighbor(board)
                    if start and end:
                        AStar(board,start,end)
                elif Reset_Button.is_over(m_pos):  # Reset the board
                    board = make_board(ROWS,WIDTH)
                    start = None
                    end = None
                elif BFS_Button.is_over(m_pos):  # Start BFS Algo
                    for row in board:
                        for cell in row:
                            cell.update_neighbor(board)
                    if start and end:
                        BFS(board,start,end)
                elif Exit_Button.is_over(m_pos):  # Exit
                    run = False
                elif DFS_Button.is_over(m_pos):  # Start DFS Algo
                    for row in board:
                        for cell in row:
                            cell.update_neighbor(board)
                    if start and end:
                        DFS(board,start,end)
                elif Clear_Button.is_over(m_pos):  # Clear
                    clear(board)
                elif Random_Button.is_over(m_pos):
                    board = make_board(ROWS,WIDTH)
                    start = None
                    end = None
                    random_obs(board)
                elif Dijkstra_button.is_over(m_pos):
                    for row in board:
                        for cell in row:
                            cell.update_neighbor(board)
                    dijkstra(board,start,end)
                else:
                    row,col = get_clicked_pos(m_pos,ROWS,WIDTH)
                    cell = board[row][col]
                    if not start and cell != end:
                        start = cell
                        cell.make_start()
                    if not end and cell != start:
                        end = cell
                        cell.make_end()
                    elif cell != end and cell != start:
                        board[row][col].make_barrier()

            if pygame.mouse.get_pressed()[2]:
                m_pos = pygame.mouse.get_pos()
                row,col = get_clicked_pos(m_pos,ROWS,WIDTH)
                cell = board[row][col]
                cell.reset()
                cell.update_neighbor(board)
                if cell == start:
                    start = None
                if cell == end:
                    end = None
    pygame.quit()


main()




        


