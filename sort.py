from ui import Window


class Sort:
    """ Base class of Sort classes 
    describes the basic methods of interaction with the class
    also contains an empty method show() in which there should be an appropriate sorting algorithm
    """
    def __init__(self, tick, columns_count):
        self.window = Window(columns_count, tick)
        self.swaps_count = 0 # amount of array swaps

    def action_await(self):
        ''' running self window until the user closed it '''
        while self.window.running:
            self.window.update()

    def window_init(self):
        ''' self window run '''
        self.swaps_count = 0 # reset swaps counter
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


class GnomeSort(Sort):
    """ class of gnome sort algorithm """

    @Sort.show
    def show(self):
        ''' rewrited method Sort.show() to gnome sort '''

        current = 0
        while current < self.window.columns.count:
            if current == 0 or self.window.columns[current] > self.window.columns[current - 1]:
                current += 1
            else:
                self.window.swap(current, current - 1)
                current -= 1
                self.swaps_count += 1


class BubbleSort(Sort):
    """ class of bubble sort algorithm """

    @Sort.show
    def show(self):
        
        n = self.window.columns_count
        current = 0
        while  n > 0 and self.window.running:
            if current + 1 < n:
                if self.window.columns[current] > self.window.columns[current + 1]:
                    self.window.swap(current, current + 1)
                    self.swaps_count += 1
                else:
                    current += 1
            else:
                current = 0
                n -= 1


class CocktailSort(Sort):
    """ class of cocktail shaker sort algorithm """

    def up_sort(self, left, right):
        ''' raising the biggest column to the top of an array of columns '''
        current = left

        while current < right - 1:
            if self.window.columns[current] > self.window.columns[current + 1]:
                self.window.swap(current, current + 1)
                self.swaps_count += 1
            else:
                current += 1

    def down_sort(self, left, right):
        ''' descending the smallest column of the columns array down '''
        current = right

        while current > left:
            if self.window.columns[current] < self.window.columns[current - 1]:
                 self.window.swap(current, current - 1)
                 self.swaps_count += 1
            else:
                current -= 1

    @Sort.show
    def show(self):
        left, right = 0, self.window.columns_count

        while left < right:
            self.up_sort(left, right)
            right -= 1
            self.down_sort(left, right)
            left += 1


class InsertionSort(Sort):
    """ class of insertion sort algorithm """

    @Sort.show
    def show(self):
        pivot = 1
        while pivot < self.window.columns_count:
            temp = self.window.columns[pivot]
            
            current = pivot
            while self.window.columns[current] < self.window.columns[current - 1] and current > 0:
                self.window.swap(current, current - 1)
                current -= 1
                self.swaps_count += 1

            pivot += 1
            self.window.update()


if __name__ == "__main__":
    sort = CocktailSort(1000, 100)

    sort.show()

    print(f"swaps: {sort.swaps_count}, time: {sort.window.runtime}")
