#from pkg_resources import cleanup_resources
from ui import Window
from random import shuffle


class Sort:
    def __init__(self, tick, columns_count):
        self.columns_count = columns_count
        self.tick = tick
        self.win = None
        self.operations_count = 0

    def win_update(self, columns, curr):
        self.operations_count += 1
        self.win.sort_win.curr = curr
        self.win.sort_win.update(columns)
        self.win.running and self.win.update()

    def win_init(self):
        self.operations_count = 0
        self.win = Window(self.columns_count, self.tick)
        self.win.run()

    def make_columns(self):
        columns = list(range(1, self.columns_count + 1))
        shuffle(columns)
        return columns

    def show(self):
        return 0, self.operations_count


class BubbleSort(Sort):
    def __init__(self, tick=1000, columns_count=100):
        Sort.__init__(self, tick, columns_count)

    def show(self):
        self.win_init()
        columns = self.make_columns()
        n = self.columns_count
        swaps = 0
        
        curr = 0
        while self.win.running:
            if n == 0:
                break
            if curr + 1 < n:
                if columns[curr] > columns[curr + 1]:
                    columns[curr], columns[curr + 1] = columns[curr + 1], columns[curr]
                    swaps += 1
                else:
                    curr += 1
            else:
                curr = 0
                n -= 1
            self.win_update(columns, curr)

        self.win_update(columns, -1)
        while self.win.running:
            self.win.update()
            
        return swaps, self.operations_count


class QuickSort(Sort):
    def __init__(self, tick=1000, columns_count=100):
        Sort.__init__(self, tick, columns_count)
        self.swaps = 0

    def subarray_sort(self, columns, left, right):
        
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
                    self.swaps += 1
                    self.win_update(columns, left)
                left += 1
                right -= 1
                
        if l_hold < right:
            self.subarray_sort(columns, l_hold, right)
        if left < r_hold:
            self.subarray_sort(columns, left, r_hold)

    def show(self):
        self.win_init()
        columns = self.make_columns()
        self.swaps = 0
        
        self.subarray_sort(columns, 0, self.columns_count - 1)

        self.win_update(columns, -1)

        while self.win.running:
            self.win.update()
            
        return self.swaps, self.operations_count


class CocktailSort(Sort):
    def __init__(self, tick=1000, columns_count=100):
        Sort.__init__(self, tick, columns_count)
        self.swaps = 0

    def up_sort(self, left, right, columns):
        curr = left
        while curr < right - 1:
            if columns[curr] > columns[curr + 1]:
                columns[curr], columns[curr + 1] = columns[curr + 1], columns[curr]
                self.swaps += 1
            else:
                curr += 1
            self.win_update(columns, curr)

    def down_sort(self, left, right, columns):
        curr = right
        while curr > left:
            if columns[curr] < columns[curr - 1]:
                 columns[curr], columns[curr - 1] = columns[curr - 1], columns[curr]
                 self.swaps += 1
            else:
                curr -= 1
            self.win_update(columns, curr)

    def show(self):
        self.win_init()
        columns = self.make_columns()
        self.swaps = 0
        
        left, right = 0, self.columns_count
        while left < right:
            self.up_sort(left, right, columns)
            right -= 1
            self.down_sort(left, right, columns)
            left += 1
        
        self.win_update(self.win.sort_win.columns, -1)
        while self.win.running:
            self.win.update()
            
        return self.swaps, self.operations_count


class HeapSort(Sort):
    def __init__(self, tick=1000, columns_count=100):
        Sort.__init__(self, tick, columns_count)

    def show(self):
        self.win_init()
        columns = self.make_columns()
        swaps = 0
        
        for i in range(self.columns_count):
            self.win_update(columns, i + 1)
        
        for i in range(self.columns_count):
            ind = columns.index(i + 1)
            self.win_update(columns, ind)
            columns[i], columns[ind] = columns[ind], columns[i]
            swaps += 1
            self.win_update(columns, i)
        
        self.win_update(columns, -1)
        while self.win.running:
            self.win.update()
            
        return swaps, self.operations_count


class InsertionSort(Sort):
    def __init__(self, tick=1000, columns_count=100):
        Sort.__init__(self, tick, columns_count)

    def show(self):
        self.win_init()
        ccolumns = self.make_columns()
        
        pivot = 1
        while pivot < self.columns_count:
            temp = columns[pivot]
            self.win_update(columns, pivot)
            columns[0], columns[pivot] = columns[pivot], columns[0]
            pivot += 1
            columns[:pivot] = sorted(columns[:pivot])
            self.win_update(columns, columns.index(temp))
            
        
        self.win_update(columns, -1)
        while self.win.running:
            self.win.update()
            
        return self.columns_count, self.operations_count # swaps count = len of array


class GnomeSort(Sort):
    def __init__(self, tick=1000, column_count=100):
        Sort.__init__(self, tick, column_count)

    def show(self):
        self.win_init()
        columns = self.make_columns()
        swaps = 0

        curr = 0
        while curr < self.columns_count:
            if curr == 0 or columns[curr] > columns[curr - 1]:
                curr += 1
            else:
                columns[curr], columns[curr - 1] = columns[curr - 1], columns[curr]
                curr -= 1
                swaps += 1
            self.win_update(columns, curr)

        self.win_update(columns, -1)
        while self.win.running:
            self.win.update()

        return swaps, self.operations_count


if __name__ == "__main__":
    sort = GnomeSort(100, 50)
    
    swaps, operations = sort.show()
    
    print(swaps, operations)
