from ui import Window


class Sort:
    """ Base class of Sort classes 
    describes the basic methods of interaction with the class
    also contains an empty method show() in which there should be an appropriate sorting algorithm
    """
    def __init__(self, tick: int, columns_count: int, random_seed:int=None) -> None:
        self.window = Window(columns_count=columns_count, tick=tick, random_seed=random_seed)

    def action_await(self) -> None:
        ''' running self window until the user closed it '''
        while self.window.running:
            self.window.update()

    def window_init(self) -> None:
        ''' self window run '''
        self.window.run()
        while self.window.paused and self.window.running:
            self.window.update() # waits for user to start the animation

    @staticmethod
    def show(func):
        ''' decorate function to Sort.show function '''
        # self.swaps doesn't update automatically when interacting with an columns array
        def _wrapper(*args, **kwargs):
            args[0].window_init() # initializes the window
            args[0].swaps_count = 0 # set swaps count to zero

            func(*args, **kwargs) # sorting algorithm function here

            args[0].action_await() # updates the window so that the user can close it
        return _wrapper

