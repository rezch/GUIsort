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

    def show(self):
        ''' *sorting algorithm code here* (also self.swaps should be updated after interacting with the array) '''
        return self.swaps_count # return amount of swaps performed during the operation of the algorithm


class GnomeSort(Sort):
    """ class of gnome sort algorithm """

    def show(self):
        ''' rewrited method Sort.show() to gnome sort '''
        self.window_init()

        current = 0
        while current < self.window.columns.count:
            if current == 0 or self.window.columns[current] > self.window.columns[current - 1]:
                current += 1
            else:
                self.window.swap(current, current - 1)
                current -= 1
                self.swaps_count += 1

        self.action_await()

        return self.swaps_count
    

if __name__ == "__main__":
    sort = GnomeSort(1000, 100)

    swaps = sort.show()

    print(swaps)
