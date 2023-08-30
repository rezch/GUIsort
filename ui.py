import pygame
from random import shuffle, seed
from time import time


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
    
    def __init__(self, random_seed: int, columns_count:int=100, tick:int=1) -> None:
        self.tick = tick

        # window status variables
        self.running = False
        self.paused = False
        self.__make_step = False # make one display update while window is paused

        # pygame objects
        self.__screen = None
        self.__clock = None

        # columns
        self.columns_count = columns_count
        self.columns = Columns(count=columns_count, random_seed=random_seed)

        # sorting information
        self.swaps_count = 0 # count of swaps in array
        self.runtime = 0 # execution time (in ms)
        self._timer_start = 0 # timer start time (in ms)

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

    def draw(self, current_column_index: int) -> None:
        ''' columns draw '''
        for i, column in enumerate(self.columns):
            # column parameters
            color = Window.COLUMN_COLOR if i != current_column_index else Window.CURRENT_COLUMN_COLOR
            column_height = column * HEIGHT // self.columns.count

            # creating a column-sized rectangle
            rect = pygame.Rect(
                (WIDTH * i / self.columns.count, HEIGHT - column_height),
                (WIDTH / self.columns.count + 1, column_height)
            )

            # drawing rectangle on display and updating it
            pygame.draw.rect(self.__screen, color, rect)

    def make_tick(self) -> None:
        ''' make one update tick '''
        # keyboard events update
        keys = pygame.key.get_pressed()
        self.__make_step = keys[pygame.K_RIGHT] # right arrow is pressed
        self.__event_update()

    def display_tick(self, current_column_index:int=-1) -> None:
        ''' make one update tick '''
        # window tick limitation
        self.__clock.tick(self.tick)

        # ui draw
        self.__screen.fill(Window.SCREEN_COLOR)
        self.draw(current_column_index)
        
        # display update
        pygame.display.update()

    def timer_update(self) -> None:
        self.runtime = 0 # execution time (in ms)

    def update(self, current_column_index:int=-1) -> None:
        ''' window update method '''
        # display and event update
        if self.running == False:
            return
        self.display_tick(current_column_index)
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
        self.swaps_count = 0

        # columns shuffling
        self.columns.shuffle()

        # window initialization
        self.__window_init()
        self.display_tick()

    def swap(self, index1: int, index2: int, update_window:bool=True) -> None:
        ''' swaps elements in columns array with indexes index1 and index2 and update self window display if update_window is True'''

        # updates window only if window is running
        update_window and self.running and abs(index1 - index2) > 1 and self.update(index1) # marks a column only if it is not adjacent to another
        self.columns.array[index1], self.columns.array[index2] = self.columns.array[index2], self.columns.array[index1]
        update_window and self.running and self.update(index2)
        self.swaps_count += 1

    def swap_by_value(self, value1: int, value2: int) -> None:
        ''' swaps elements in columns array with value value1 and value2 and updater self window '''

        self.swap(self.columns.array.index(value1), self.columns.array.index(value2))
