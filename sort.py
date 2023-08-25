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


class RadixLSDSort(Sort):
    def __init__(self, tick=1000, column_count=100):
        Sort.__init__(self, tick, column_count)

    @staticmethod
    def get_max_digit_count(array):
        return len(str(max(array)))

    @staticmethod
    def columns_to_str_array(columns, max_digit_count):
        return [
            '0' * (max_digit_count - len(str(val))) + str(val) for val in columns
            ]

    def show(self):
        self.win_init()
        columns = self.make_columns()
        swaps = 0

        n = RadixLSDSort.get_max_digit_count(columns)

        for i in range(n): # (n - i - 1) - processed digit
            count_array = [[] for _ in range(10)]
            array = RadixLSDSort.columns_to_str_array(columns, n)
            
            for curr, value in enumerate(array):
                self.win_update(columns, curr)
                count_array[int(value[n - i - 1])].append(value)
            
            array = []
            for j in range(10):
                array += count_array[j]

            for ind, value in enumerate(array):
                temp = columns.index(int(value))
                self.win_update(columns, temp)
                self.win_update(columns, ind)
                columns[ind], columns[temp] = columns[temp], columns[ind]
                swaps += 1

        self.win_update(columns, -1)
        while self.win.running:
            self.win.update()
            
        return swaps, self.operations_count


class RadixMSDBinSort(Sort):
    def __init__(self, tick=1000, column_count=100):
        Sort.__init__(self, tick, column_count)
        self.temp_columns = []
        self.swaps = 0

    @staticmethod
    def get_max_digit_count(array):
        return max(len(bin(x)[2:]) for x in array)

    def __msd_sort(self, array, bit_position):
        if bit_position == 0 or len(array) < 2:
            return array

        # Split numbers based on bit at bit_position from the right
        zeros = []
        ones = []
        for number in array:
            if (number >> (bit_position - 1)) & 1:
                ones.append(number)
            else:
                zeros.append(number)

        # recursively split both lists further
        zeros = self.__msd_sort(zeros, bit_position - 1)
        ones = self.__msd_sort(ones, bit_position - 1)

        # recombine lists
        array = zeros + ones

        # sorting vizualization
        for ind, value in enumerate(array):
            temp = self.temp_columns.index(value)
            self.win_update(self.temp_columns, temp)
            self.win_update(self.temp_columns, ind)
            self.temp_columns[ind], self.temp_columns[temp] = self.temp_columns[temp], self.temp_columns[ind]
            self.swaps += 1
    
        return array

    def show(self):
        self.win_init()
        columns = self.make_columns()
        self.temp_columns = columns
        self.swaps = 0

        n = RadixMSDBinSort.get_max_digit_count(columns)
        columns = self.__msd_sort(columns, n)

        self.win_update(columns, -1)
        while self.win.running:
            self.win.update()
            
        return self.swaps, self.operations_count


class RadixMSDSort(Sort):
    def __init__(self, tick=1000, column_count=100):
        Sort.__init__(self, tick, column_count)
        self.temp_columns = []
        self.swaps = 0

    @staticmethod
    def get_max_digit_count(array):
        return len(str(max(array)))

    @staticmethod
    def get_digit_from_number(number, position):
        if len(str(number)) < position:
            return 0
        number = str(number)[::-1]
        return int(number[position - 1])

    def __msd_sort(self, array, position):
        if position == 0 or len(array) < 2:
            return array

        # Split numbers based on digit at position from the right
        digit_list = [[] for _ in range(10)]
        for number in array:
            digit = RadixMSDSort.get_digit_from_number(number, position)
            digit_list[digit].append(number)
        
        # recursively split all lists further
        for digit in range(10):
            digit_list[digit] = self.__msd_sort(digit_list[digit], position - 1)

        # recombine lists
        array = []
        for digit in range(10):
            array += digit_list[digit]
        
        # sorting vizualization
        for ind, value in enumerate(array):
            temp = self.temp_columns.index(value)
            self.win_update(self.temp_columns, temp)
            self.win_update(self.temp_columns, ind)
            self.temp_columns[ind], self.temp_columns[temp] = self.temp_columns[temp], self.temp_columns[ind]
            self.swaps += 1
    
        return array

    def show(self):
        self.win_init()
        columns = self.make_columns()
        self.temp_columns = columns
        self.swaps = 0

        n = RadixMSDSort.get_max_digit_count(columns)
        columns = self.__msd_sort(columns, n)

        self.win_update(columns, -1)
        while self.win.running:
            self.win.update()
            
        return self.swaps, self.operations_count

if __name__ == "__main__":    
    sort = RadixMSDBinSort(300, 999)
    
    swaps, operations = sort.show()
    
    print(swaps, operations)
