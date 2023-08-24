#from pkg_resources import cleanup_resources
from ui import Window


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

        self.win_update(columns, -1)
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


class CocktailSort(Sort):
    def __init__(self, tick=1000, columns_count=100):
        Sort.__init__(self, tick, columns_count)

    def up_sort(self, left, right, columns):
        curr = left
        while curr < right - 1:
            if columns[curr] > columns[curr + 1]:
                columns[curr], columns[curr + 1] = columns[curr + 1], columns[curr]
            else:
                curr += 1
            self.win_update(columns, curr)

    def down_sort(self, left, right, columns):
        curr = right
        while curr > left:
            if columns[curr] < columns[curr - 1]:
                 columns[curr], columns[curr - 1] = columns[curr - 1], columns[curr]
            else:
                curr -= 1
            self.win_update(columns, curr)

    def show(self):
        self.win_init()

        columns = self.win.sort_win.columns
        n = len(columns)
        
        left, right = 0, n
        while left < right:
            self.up_sort(left, right, columns)
            right -= 1
            self.down_sort(left, right, columns)
            left += 1
        
        self.win_update(self.win.sort_win.columns, -1)
        while self.win.running:
            self.win.update()


class HeapSort(Sort):
    def __init__(self, tick=1000, columns_count=100):
        Sort.__init__(self, tick, columns_count)

    def show(self):
        self.win_init()

        columns = self.win.sort_win.columns
        n = len(columns)
        
        for i in range(n):
            self.win_update(columns, i + 1)
        
        for i in range(n):
            ind = columns.index(i + 1)
            self.win_update(columns, ind)
            columns[i], columns[ind] = columns[ind], columns[i]
            self.win_update(columns, i)
        
        self.win_update(columns, -1)
        while self.win.running:
            self.win.update()

    
if __name__ == "__main__":
    csort = CocktailSort(100, 40)
    bsort = BubbleSort(100, 40)
    qsort = QuickSort(100, 40)
    hsort = HeapSort(100, 40)
    
    hsort.show()
    

