import pygame
from time import time
from random import shuffle, seed


WIDTH, HEIGHT = (1600, 900) # ui window size in px


def get_time_ms() -> int:
    ''' return current time after 1 jun 1970 00:00:00 in ms '''
    return int(time() * 1000)


class Columns:
    """ columns array class 
    the appeal is made in the same way as with the list
    when you replace a value in the list, the window is automatically updated
    """
    def __init__(self, count: int, random_seed: int) -> None:
        self.seed = random_seed
        self.count = count # count of columns
        self.array = list(range(1, count + 1)) # array of columns values

    def shuffle(self) -> None:
        ''' shuffling columns array '''
        if self.seed is not None:
            seed(self.seed)
        shuffle(self.array)

    def __getitem__(self, index: int) -> int:
        ''' returns self array value by index '''
        return self.array[index]

    def __setitem__(self, index: int, value: int) -> None:
        ''' change value in self array by index '''
        self.array[index] = value


class Window:
    """ Window class
    interacts with the user and displays the sorting process
    """
    SCREEN_COLOR = (128, 128, 128)
    COLUMN_COLOR = (0, 0, 0)
    CURRENT_COLUMN_COLOR = (200, 0, 0)
    
    def __init__(self, tick:int=1) -> None:
        self.tick = tick

        # window status variables
        self.running = False
        self.paused = False
        self.__make_step = False # make one display update while window is paused

        # pygame objects
        self.__screen = None
        self.__clock = None

        # sorting information
        self.runtime = 0 # execution time (in ms)
        self._timer_start = 0 # timer start time (in ms)

        self.sorting_is_done = True # true if the sorting is done completely
        # (updated to False if the window was updated after it was closed)

    def __window_init(self) -> None:
        ''' window initialization '''
        # pygame display initialization and setting
        pygame.init()
        pygame.display.set_caption("GUIsort")

        # setting self pygame variables
        self.__screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.__clock = pygame.time.Clock()

    def quit(self) -> None:
        ''' window close method '''
        self.running = False
        not self.paused and self.runtime_update()
        pygame.quit()

    def runtime_update(self) -> None:
        ''' update runtime '''
        if self.paused:
            self._timer_start = get_time_ms() # if window paused - reset timer start time
        else:
            self.runtime += get_time_ms() - self._timer_start # else - add time to runtime
    
    def __event_update(self) -> None:
        ''' window events processing '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # window close button was pressed
                self.quit() # quit
                
            if event.type == pygame.KEYDOWN: # keys event
                if event.key == pygame.K_q:
                    self.quit() # quit

                if event.key == pygame.K_SPACE:
                    self.runtime_update()
                    self.paused = not self.paused # pause
                
                if event.key == pygame.K_RETURN:
                    self.paused and self.runtime_update()
                    self.paused = False # play

                if event.key == pygame.K_RIGHT or event.key == pygame.K_UP:
                    self.__make_step = True  # step

    def draw(self, columns: Columns, current_column_index: int) -> None:
        ''' columns draw '''
        if columns == []: # if draw was called with empty list parametr
            return
        
        columns_count = len(columns.array)
        for i, column in enumerate(columns):
            # column parameters
            color = Window.COLUMN_COLOR if i != current_column_index else Window.CURRENT_COLUMN_COLOR
            column_height = column * HEIGHT // columns_count

            # creating a column-sized rectangle
            rect = pygame.Rect(
                (WIDTH * i / columns_count, HEIGHT - column_height),
                (WIDTH / columns_count + 1, column_height)
            )

            # drawing rectangle on display and updating it
            pygame.draw.rect(self.__screen, color, rect)

    def make_tick(self) -> None:
        ''' make one update tick '''
        # keyboard events update
        keys = pygame.key.get_pressed()
        self.__make_step = keys[pygame.K_RIGHT] # right arrow is pressed
        self.__event_update()

    def display_tick(self, columns_array, current_column_index:int=-1) -> None:
        ''' make one update tick '''
        # window tick limitation
        self.__clock.tick(self.tick)

        # ui draw
        self.__screen.fill(Window.SCREEN_COLOR)
        self.draw(columns_array, current_column_index)
        
        # display update
        pygame.display.update()

    def update(self, columns_array, current_column_index:int=-1) -> None:
        ''' window update method '''
        # display and event update
        if self.running == False:
            self.sorting_is_done = False # updated to False because the window was updated after it was closed
            return
        
        self.display_tick(columns_array, current_column_index)
        self.make_tick()

        # pause proccesing
        while self.paused and self.running and not self.__make_step:
            self.make_tick()

    def run(self) -> None:
        ''' window run '''
        # status variables setting
        self.running = True
        self.paused = True
        self.__make_step = False
        self.sorting_is_done = True

        # window initialization
        self.__window_init()
        self.display_tick([])
