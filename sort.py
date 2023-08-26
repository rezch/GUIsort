from ui import Window
from random import shuffle


class Sort:
    def __init__(self, tick, columns_count):
        self.columns_count = columns_count
        self.tick = tick
        self.win = None
        self.operations_count = 0
        self.swaps = 0

    def win_update(self, columns, curr):
        self.operations_count += 1
        self.win.sort_win.curr = curr
        self.win.sort_win.update(columns)
        self.win.running and self.win.update()

    def win_init(self):
        self.swaps = 0
        self.operations_count = 0
        self.win = Window(self.columns_count, self.tick)
        self.win.run()

    def make_columns(self):
        columns = list(range(1, self.columns_count + 1))
        shuffle(columns)
        return columns

    def show(self):
        return self.swaps, self.operations_count

    def show_columns_update(self, old_columns, new_columns):
        for ind, value in enumerate(new_columns):
            if old_columns[ind] == value:
                continue
            temp = old_columns.index(value)
            self.win_update(old_columns, temp)
            self.win_update(old_columns, ind)
            old_columns[ind], old_columns[temp] = old_columns[temp], old_columns[ind]
            self.swaps += 1

    def action_await(self, columns):
        self.win_update(columns, -1)
        while self.win.running:
            self.win.update()


class BubbleSort(Sort):
    def show(self):
        self.win_init()
        columns = self.make_columns()
        n = self.columns_count
        
        curr = 0
        while self.win.running:
            if n == 0:
                break
            if curr + 1 < n:
                if columns[curr] > columns[curr + 1]:
                    columns[curr], columns[curr + 1] = columns[curr + 1], columns[curr]
                    self.swaps += 1
                else:
                    curr += 1
            else:
                curr = 0
                n -= 1
            self.win_update(columns, curr)

        self.action_await(columns)
            
        return self.swaps, self.operations_count


class QuickSort(Sort):
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

        self.action_await(columns)
            
        return self.swaps, self.operations_count


class CocktailSort(Sort):
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
        
        self.action_await(columns)
            
        return self.swaps, self.operations_count


class HeapSort(Sort):
    def show(self):
        self.win_init()
        columns = self.make_columns()
        
        for i in range(self.columns_count):
            self.win_update(columns, i + 1)
        
        self.show_columns_update(columns, list(range(1, self.columns_count)))
        
        self.action_await(columns)
            
        return self.swaps, self.operations_count


class InsertionSort(Sort):
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
            
        
        self.action_await(columns)
            
        return self.columns_count, self.operations_count # swaps count = len of array


class GnomeSort(Sort):
    def show(self):
        self.win_init()
        columns = self.make_columns()

        curr = 0
        while curr < self.columns_count:
            if curr == 0 or columns[curr] > columns[curr - 1]:
                curr += 1
            else:
                columns[curr], columns[curr - 1] = columns[curr - 1], columns[curr]
                curr -= 1
                self.swaps += 1
            self.win_update(columns, curr)

        self.action_await(columns)

        return self.swaps, self.operations_count


class RadixLSDSort(Sort):
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

            self.show_columns_update(columns, list(map(int, array)))

        self.action_await(columns)
            
        return self.swaps, self.operations_count


class RadixMSDBinSort(Sort):
    def __init__(self, tick=1000, column_count=100):
        Sort.__init__(self, tick, column_count)
        self.temp_columns = []

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

        # sorting visualization
        self.show_columns_update(self.temp_columns, list(map(int, array)))
    
        return array

    def show(self):
        self.win_init()
        columns = self.make_columns()
        self.temp_columns = columns

        n = RadixMSDBinSort.get_max_digit_count(columns)
        columns = self.__msd_sort(columns, n)

        self.action_await(columns)
            
        return self.swaps, self.operations_count


class RadixMSDSort(Sort):
    def __init__(self, tick=1000, column_count=100):
        Sort.__init__(self, tick, column_count)
        self.temp_columns = []

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
        self.show_columns_update(self.temp_columns, list(map(int, array)))
    
        return array

    def show(self):
        self.win_init()
        columns = self.make_columns()
        self.temp_columns = columns
        self.swaps = 0

        n = RadixMSDSort.get_max_digit_count(columns)
        columns = self.__msd_sort(columns, n)

        self.action_await(columns)
            
        return self.swaps, self.operations_count


class BeadHTLSort(Sort):
    """
    * Bead sort from lower to higher digit
    """
    def __init__(self, tick=1000, column_count=100):
        Sort.__init__(self, tick, column_count)
        self.counting_array = []

    def array_to_columns(self):
        return [sum(arr) for arr in self.counting_array]

    def drop_column(self, pos):
        counter = 0
        for val in self.counting_array:
            counter += val[pos]

        for i in range(self.columns_count):
            if i < counter:
                self.counting_array[self.columns_count - i - 1][pos] = 1
            else:
                self.counting_array[self.columns_count - i - 1][pos] = 0

    '''def __slow_drop_column(self, pos):
        start_ind = self.columns_count - 1
        while start_ind >= 0 and self.counting_array[start_ind][pos] == 1:
            start_ind -= 1

        if start_ind == -1:
            return False

        flag = False
        for i in range(start_ind, -1, -1):
            if self.counting_array[i][pos] == 1:
                self.counting_array[i][pos] = 0
                self.counting_array[i + 1][pos] = 1
                flag = True
                break
            
        return flag'''

    def show(self):
        self.win_init()
        columns = self.make_columns()

        n = max(columns)
        self.counting_array = []
        for i, val in enumerate(columns):
            self.counting_array.append([0] * (self.columns_count - val) + [1] * val)
            self.win_update(columns, i)

        for pos in range(self.columns_count):
            self.drop_column(pos)
            new_columns = self.array_to_columns()
            columns = new_columns
            self.win_update(columns, -1)
            
        self.action_await(columns)

        return self.swaps, self.operations_count


class BeadLTHSort(BeadHTLSort):
    """
    * Bead sort from higher to lower digit
    """
    def show(self):
        self.win_init()
        columns = self.make_columns()

        n = max(columns)
        self.counting_array = []
        for i, val in enumerate(columns):
            self.counting_array.append([0] * (self.columns_count - val) + [1] * val)
            self.win_update(columns, i)

        for pos in range(self.columns_count - 1, -1, -1):
            self.drop_column(pos)
            new_columns = self.array_to_columns()
            columns = new_columns
            self.win_update(columns, -1)
            
        self.action_await(columns)

        return self.swaps, self.operations_count


class BucketSort(Sort):
    def make_bucket(self, columns, from_val, to_val, left, right):
        if from_val == to_val:
            return

        old_columns = columns.copy()
        mid = (from_val + to_val) // 2
        columns[left:right] = [val for val in columns[left:right] if val <= mid] + \
                              [val for val in columns[left:right] if val > mid]

        self.show_columns_update(old_columns, columns)
        
        mid_ind = (left + right) // 2
        self.make_bucket(columns, from_val, mid, left, mid_ind + 1)
        self.make_bucket(columns, mid + 1, to_val, mid_ind, right)
            
    def show(self):
        self.win_init()
        columns = self.make_columns()

        self.make_bucket(columns, 1, self.columns_count, 0, self.columns_count)
        
        self.action_await(columns)
        
        return self.swaps, self.operations_count


if __name__ == "__main__":
    sort = BucketSort(tick=300, columns=1000)
    
    swaps, operations = sort.show()
    
    print(swaps, operations)
