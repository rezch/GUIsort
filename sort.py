#from pkg_resources import cleanup_resources
import pygame
from random import shuffle


WIDTH, HEIGHT = (1200, 600) # ui window size in px


class SortWin:
    SCREEN_COLOR = (128, 128, 128)
    COL_COLOR = (0, 0, 0)
    CURR_COL_COLOR = (200, 0, 0)
    
    def __init__(self, screen, col_count, pos, size):
        self.screen = screen
        self.pos = pos
        self.size = size
        self.rect = pygame.Rect(pos, size)

        # columns
        self.curr = -1
        self.col_count = col_count
        self.columns = list(range(1, col_count + 1))
        shuffle(self.columns)
        

    def update(self, columns):
        self.columns = columns

    def draw(self):
        pygame.draw.rect(self.screen, SortWin.SCREEN_COLOR, self.rect)

        for i, col in enumerate(self.columns):
            x = self.pos[0] + self.size[0] * i / self.col_count
            color = SortWin.COL_COLOR if i != self.curr else SortWin.CURR_COL_COLOR

            col_size = col * self.size[1] // self.col_count
            rect = pygame.Rect(
                (x, self.pos[1] + self.size[1] - col_size),
                (self.size[0] / self.col_count, col_size)
            )
            pygame.draw.rect(
                self.screen,
                color, # color
                rect
            )
                


class Window:
    SCREEN_COLOR = (72, 72, 72)
    
    def __init__(self, columns=100, tick=1):
        self.tick = tick
        self.columns = columns
        self.running = False
        self.tick = tick
        self.screen = None
        self.clock = None
        self.sort_win = None

    def run(self):
        self.running = True
        self.__window_init()
        self.sort_win = SortWin(
            self.screen, self.columns,
            (WIDTH // 8, HEIGHT // 8), # pos
            (6 * (WIDTH // 8), 6 * (HEIGHT // 8)) # size
        )

    def __window_init(self):
        pygame.init()
        pygame.display.set_caption("---")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

    def quit(self):
        self.running = False
        pygame.quit()
    
    def event_update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                
            if event.type == pygame.KEYDOWN: # keys event
                if event.key == pygame.K_q:
                    self.quit()
                
    def update(self):
        # ui draw
        self.screen.fill(Window.SCREEN_COLOR)
        self.sort_win.draw()

        # display update
        pygame.display.update()
        
        # clock and event update
        self.clock.tick(self.tick)
        self.event_update()


class Sort:
    def __init__(self, tick, columns_count):
        self.columns_count = columns_count
        self.tick = tick
        self.win = None

    def win_update(self, columns, curr):
        self.win.sort_win.curr = curr
        self.win.sort_win.update(columns)
        self.win.update()

    def win_init(self):
        self.win = Window(self.columns_count, self.tick)
        self.win.run()

    def show(self):
        pass


class BubbleSort(Sort):
    def __init__(self, tick=1000, columns_count=100):
        Sort.__init__(self, tick, columns_count)

    def show(self):
        self.win_init()

        columns = self.win.sort_win.columns
        n = len(columns)
        
        curr = 0
        while self.win.running:
            # sorting
            if n == 0:
                self.win_update(columns, -1)
                break
            if curr + 1 < n:
                if columns[curr] > columns[curr + 1]:
                    columns[curr], columns[curr + 1] = columns[curr + 1], columns[curr]
                else:
                    curr += 1
            else:
                curr = 0
                n -= 1
            self.win_update(columns, curr)

        while self.win.running:
            self.win.update()


class QuickSort(Sort):
    def __init__(self, tick=1000, columns_count=100):
        Sort.__init__(self, tick, columns_count)

    def subarray_sort(self, left, right):
        columns = self.win.sort_win.columns
        
        pivot = columns[(right + left) // 2]
        l_hold, r_hold = left, right

        while left <= right:
            while columns[left] < pivot:
                self.win_update(columns, left)
                left += 1
            
            while columns[right] > pivot:
                self.win_update(columns, right)
                right -= 1

            if left <= right:
                if columns[left] > columns[right]:
                    columns[left], columns[right] = columns[right], columns[left]
                    self.win_update(columns, left)
                left += 1
                right -= 1
                
        if l_hold < right:
            self.subarray_sort(l_hold, right)
        if left < r_hold:
            self.subarray_sort(left, r_hold)

    def show(self):
        self.win_init()

        self.subarray_sort(0, self.columns_count - 1)

        self.win_update(self.win.sort_win.columns, -1)

        while self.win.running:
            self.win.update()
       
    
if __name__ == "__main__":
    sort = QuickSort(100, 300)

    sort.show()
    

