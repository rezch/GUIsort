import pygame
from random import shuffle

WIDTH, HEIGHT = (1600, 900) # ui window size in px


class Columns:
    """ columns array class 
    the appeal is made in the same way as with the list
    when you replace a value in the list, the window is automatically updated
    """
    def __init__(self, count, window):
        self.count = count # count of columns
        self.array = list(range(1, count + 1)) # array of columns values
        #shuffle(self.array) # shuffling columns array
        self.window = window # pygame window (class Window)

    def __getitem__(self, index):
        ''' returns self array value by index '''
        return self.array[index]

    def __setitem__(self, index, value):
        ''' change value in self array by index '''
        self.array[index] = value

    def swap(self, index1, index2):
        ''' swaps elements in self.array with indexes index1 and index2 and updater self window '''

        # updates window only if window is running
        self.window.running and self.window.display_tick(index1)
        self.array[index1], self.array[index2] = self.array[index2], self.array[index1]
        self.window.running and self.window.display_tick(index2)


class Window:
    """ Window class
    interacts with the user and displays the sorting process
    """
    SCREEN_COLOR = (128, 128, 128)
    COLUMN_COLOR = (0, 0, 0)
    CURRENT_COLUMN_COLOR = (200, 0, 0)
    
    def __init__(self, columns_count=100, tick=1):
        self._tick = tick

        # window status variables
        self.running = False
        self.paused = False
        self.__make_step = False # make one display update while window is paused

        # pygame objects
        self.__screen = None
        self.__clock = None

        # columns
        self.columns_count = columns_count
        self.columns = Columns(columns_count, self)

    def __window_init(self):
        ''' window initialization '''
        # pygame display initialization and setting
        pygame.init()
        pygame.display.set_caption("GUIsort")

        # setting self pygame variables
        self.__screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.__clock = pygame.time.Clock()

    def quit(self):
        ''' window close method '''
        self.running = False
        pygame.quit()
    
    def __event_update(self):
        ''' window events processing '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # window close button was pressed
                self.quit() # quit
                
            if event.type == pygame.KEYDOWN: # keys event
                if event.key == pygame.K_q:
                    self.quit() # quit

                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused # pause

                if event.key == pygame.K_RIGHT or event.key == pygame.K_UP:
                    self.__make_step = True  # step

    def draw(self, current_column_index=-1):
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

    def make_tick(self):
        ''' make one update tick '''
        # keyboard events update
        keys = pygame.key.get_pressed()
        self.__make_step = keys[pygame.K_RIGHT] # right arrow is pressed
        self.__event_update()

    def display_tick(self, current_column_index=-1):
        ''' make one update tick '''
        # window tick limitation
        self.__clock.tick(self._tick)

        # ui draw
        self.__screen.fill(Window.SCREEN_COLOR)
        self.draw(current_column_index)
        
        # display update
        pygame.display.update()

    def update(self):
        ''' window update method '''
        # display and event update
        self.display_tick()
        self.make_tick()

        # pause proccesing
        while self.paused and self.running and not self.__make_step:
            self.make_tick()

    def run(self):
        ''' window run '''
        # status variables setting
        self.running = True
        self.paused = False
        self.__make_step = False

        # window initialization
        self.__window_init()
        self.display_tick()


class Sort:
    """ Base class of Sort classes 
    describes the basic methods of interaction with the class
    also contains an empty method show() in which there should be an appropriate sorting algorithm
    """
    def __init__(self, tick, columns_count):
        self.window = Window(columns_count, tick)
        self.swaps_count = 0 # amount of array swaps

    def window_init(self):
        ''' self window run '''
        self.swaps_count = 0 # reset swaps counter
        self.window.run()

    def action_await(self):
        ''' running self window until the user closed it '''
        while self.window.running:
            self.window.update()

    def show(self):
        ''' *sorting algorithm code here* (also self.swaps should be updated after interacting with the array) '''
        return self.swaps_count # return amount of swaps performed during the operation of the algorithm


class GnomeSort(Sort):
    """ class of gnome sort algorithm """

    def show(self):
        ''' rewrited method Sort.show() to gnome sort '''
        self.window_init()

        self.window.columns.swap(2, 3)
        self.window.columns.swap(4, 3)

        self.action_await()

        return self.swaps_count
    

if __name__ == "__main__":
    sort = GnomeSort(5, 10)

    sort.show()

