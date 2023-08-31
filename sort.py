from ui import Window, Columns, get_time_ms


class Sort:
    """ Base class of Sort classes 
    describes the basic methods of interaction with the class
    also contains an empty method show() in which there should be an appropriate sorting algorithm
    """
    def __init__(self, tick: int, columns_count: int, random_seed:int=None) -> None:
        # window
        self.window = Window(tick=tick)

        # columns
        self.columns_count = columns_count
        self.columns = Columns(count=columns_count, random_seed=random_seed)

        # sorting information
        self.swaps_count = 0
        self.runtime = 0
        self.sorting_is_done = False # true if the sorting is done completely

    def __str__(self):
        return f"{self.__class__.__name__}, columns={self.columns_count}, tick={self.window.tick}"

    def action_await(self) -> None:
        ''' running self window until the user closed it '''
        self.window.paused = True # pausing the window to stop the timer of execution speed
        while self.window.running:
            self.window.update(self.columns)

    def window_init(self) -> None:
        ''' self window run '''
        self.window.run()

        self.runtime = 0 # set runtime to zero
        self.swaps_count = 0 # set swaps count to zero
        self.columns.shuffle() # columns shuffling
        self.sorting_is_done = False # false because sorting has just started

        while self.window.paused and self.window.running:
            self.window.update(self.columns) # waits for user to start the animation

        self.window.runtime_update()

    @staticmethod
    def show(func):
        ''' decorate function to Sort.show function '''
        # self.swaps doesn't update automatically when interacting with an columns array
        def _wrapper(*args, **kwargs):
            args[0].window_init() # initializes the window

            func(*args, **kwargs) # sorting algorithm function here

            args[0].window.runtime_update() # updates runtime timer after sorting
            args[0].runtime = args[0].window.runtime
            args[0].action_await() # updates the window so that the user can close it
            args[0].sorting_is_done = args[0].window.sorting_is_done # true if the sorting is complete
        return _wrapper
    
    def swap(self, index1: int, index2: int, update_window:bool=True) -> None:
        ''' swaps elements in columns array with indexes index1 and index2 and update self window display if update_window is True'''
        # updates window only if window is running
        update_window and self.window.running and abs(index1 - index2) > 1 and self.window.update(self.columns, index1) # marks a column only if it is not adjacent to another
        self.columns.array[index1], self.columns.array[index2] = self.columns.array[index2], self.columns.array[index1]
        update_window and self.window.running and self.window.update(self.columns, index2)
        self.swaps_count += 1

    def swap_by_value(self, value1: int, value2: int) -> None:
        ''' swaps elements in columns array with value value1 and value2 and updater self window '''
        self.swap(self.columns.array.index(value1), self.columns.array.index(value2))

    def execucion_info(self) -> str:
        ''' return str information about sorting execution (number of swaps and execution time) '''
        if self.sorting_is_done:
            return f"swaps: {self.swaps_count}, time: {self.runtime}"
        return "sorting is not completely done"

