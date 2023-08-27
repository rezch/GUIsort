import pygame


WIDTH, HEIGHT = (1600, 900) # ui window size in px


class SortWin:
    SCREEN_COLOR = (128, 128, 128)
    COLUMN_COLOR = (0, 0, 0)
    CURRENT_COLUMN_COLOR = (200, 0, 0)
    
    def __init__(self, screen, columns_count, position, size):
        self.screen = screen
        self.position = position
        self.size = size
        self.rect = pygame.Rect(position, size)

        # columns
        self.current = -1
        self.columns_count = columns_count
        self.columns = []
    
    def update(self, columns):
        self.columns = columns

    def draw(self):
        pygame.draw.rect(self.screen, SortWin.SCREEN_COLOR, self.rect)

        for i, column in enumerate(self.columns):
            x = self.position[0] + self.size[0] * i / self.columns_count
            color = SortWin.COLUMN_COLOR if i != self.current else SortWin.CURRENT_COLUMN_COLOR

            column_size = column * self.size[1] // self.columns_count
            rect = pygame.Rect(
                (x, self.position[1] + self.size[1] - column_size),
                (self.size[0] / self.columns_count + 1, column_size)
            )
            pygame.draw.rect(
                self.screen,
                color, # color
                rect
            )
                


class Window:
    SCREEN_COLOR = (128, 128, 128)
    
    def __init__(self, columns=100, tick=10):
        self.tick = tick
        self.columns = columns
        self.running = False
        self.screen = None
        self.__clock = None
        self.sort_win = None
        self.paused = False
        self.__make_step = False

    def run(self):
        self.running = True
        self.paused = False
        self.__make_step = False
        self.__window_init()
        self.sort_win = SortWin(
            self.screen, self.columns,
            (0, 0), # position
            (WIDTH, HEIGHT) # size
        )

    def __window_init(self):
        pygame.init()
        pygame.display.set_caption("GUIsort")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.__clock = pygame.time.Clock()

    def quit(self):
        self.running = False
        pygame.quit()
    
    def __event_update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                
            if event.type == pygame.KEYDOWN: # keys event
                if event.key == pygame.K_q:
                    self.quit()

                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused

                if event.key == pygame.K_RIGHT or event.key == pygame.K_UP:
                    self.__make_step = True

    def make_tick(self):
        keys = pygame.key.get_pressed()
        self.__make_step = keys[pygame.K_RIGHT]
        self.__event_update()

    def display_tick(self):
        # ui draw
        self.screen.fill(Window.SCREEN_COLOR)
        self.sort_win.draw()
        
        # display update
        pygame.display.update()

    def update(self):
        self.__clock.tick(self.tick)

        # display and event update
        self.display_tick()
        self.make_tick()

        # pause
        while self.paused and self.running and not self.__make_step:
            self.make_tick()



