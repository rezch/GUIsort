from sort import Sort


class GnomeSort(Sort):
    """ class of gnome sort algorithm """

    def __str__(self):
        return f"Gnome Sort, columns={self.columns_count}, tick={self.window.tick}"

    @Sort.show
    def show(self) -> None:
        current = 0
        while current < self.columns.count:
            if current == 0 or self.columns[current] > self.columns[current - 1]:
                current += 1
            else:
                self.swap(current, current - 1)
                current -= 1


class BubbleSort(Sort):
    """ class of bubble sort algorithm """

    def __str__(self):
        return f"Bubble Sort, columns={self.columns_count}, tick={self.window.tick}"

    @Sort.show
    def show(self) -> None:
        n = -1
        current = self.columns_count - 1
        while  n < self.columns_count and self.window.running:
            if current - 1 > n:
                if self.columns[current] < self.columns[current - 1]:
                    self.swap(current, current - 1)
                    self.swaps_count += 1
                else:
                    current -= 1
            else:
                current = self.columns_count - 1
                n += 1


class CocktailSort(Sort):
    """ class of cocktail shaker sort algorithm """

    def __str__(self):
        return f"Cocktail Sort, columns={self.columns_count}, tick={self.window.tick}"

    def up_sort(self, left: int, right: int):
        ''' raising the biggest column to the top of an array of columns '''
        current = left

        while current < right - 1:
            if self.columns[current] > self.columns[current + 1]:
                self.swap(current, current + 1)
            else:
                current += 1

    def down_sort(self, left: int, right: int):
        ''' descending the smallest column of the columns array down '''
        current = right

        while current > left:
            if self.columns[current] < self.columns[current - 1]:
                 self.swap(current, current - 1)
            else:
                current -= 1

    @Sort.show
    def show(self) -> None:
        left, right = 0, self.columns_count

        while left < right:
            self.up_sort(left, right)
            right -= 1
            self.down_sort(left, right)
            left += 1


class InsertionSort(Sort):
    """ class of insertion sort algorithm """

    def __str__(self):
        return f"Insertion Sort, columns={self.columns_count}, tick={self.window.tick}"

    @Sort.show
    def show(self) -> None:
        pivot = 1
        for pivot in range(1, self.columns_count):
            current = pivot
            while self.columns[current] < self.columns[current - 1] and current > 0:
                self.swap(current, current - 1)
                current -= 1


class QuickSort(Sort):
    """ class of quick sort algorithm """

    def __str__(self):
        return f"Quick Sort, columns={self.columns_count}, tick={self.window.tick}"

    def subarray_sort(self, left: int, right: int) -> None:
        ''' sorting subarray '''
        pivot = self.columns[(right + left) // 2]
        l_hold, r_hold = left, right

        while left <= right:
            while self.columns[left] < pivot:
                self.window.update(self.columns, left)
                left += 1
            
            while self.columns[right] > pivot:
                self.window.update(self.columns, right)
                right -= 1

            if left <= right:
                if self.columns[left] > self.columns[right]:
                    self.swap(left, right)
                left += 1
                right -= 1

        l_hold < right and self.subarray_sort(l_hold, right)
        left < r_hold and self.subarray_sort(left, r_hold)

    @Sort.show
    def show(self) -> None:
        self.subarray_sort(0, self.columns_count - 1)


class HeapSort(Sort):
    """ class of heap sort algorithm """

    def __str__(self):
        return f"Heap Sort, columns={self.columns_count}, tick={self.window.tick}"

    @Sort.show
    def show(self) -> None:
        # scan all columns
        for index in range(self.columns_count):
            self.window.update(self.columns, index)

        # swaping columns in a sorted array
        for index, column in enumerate(sorted(self.columns)):
            self.swap(index, self.columns.array.index(column))


class BucketSort(Sort):
    """ class of bucket sort algorithm """

    def __str__(self):
        return f"Bucket Sort, columns: {self.columns_count}, tick: {self.window.tick}"
    
    def left_shift(self, left_index, pivot):
        # transposition columns smaller than pivot to the right
        current = left_index
        while current < self.columns.array.index(pivot):
            if self.columns[current] > pivot:
                pivot_index = self.columns.array.index(pivot)

                # the window is updated only at the beginning and end of the cyclic shift of the array, so as not to display it completely
                self.window.update(self.columns, current)
                for index in range(current, pivot_index):
                    self.swap(index, index + 1, update_window=False)
                self.window.update(self.columns, pivot_index)
            else:
                current += 1

    def right_shift(self, right_index, pivot):
        current = self.columns.array.index(pivot)

        while current <= right_index:
            if self.columns.array[current] < pivot:
                pivot_index = self.columns.array.index(pivot)

                #the window is updated only at the beginning and end of the cyclic shift of the array, so as not to display it completely
                self.window.update(self.columns, current)
                for index in range(current, pivot_index, -1):
                    self.swap(index, index - 1, update_window=False)
                self.window.update(self.columns, pivot_index)
            else:
                current += 1

    def subarray_sort(self, left_index: int, right_index: int) -> None:
        if left_index >= right_index + 1:
            return

        from_value = min(self.columns.array[left_index:right_index + 1]) # min value of subarray
        to_value = max(self.columns.array[left_index:right_index + 1]) # max value of subarray
        pivot = (from_value + to_value) // 2 # sorting pivot
        
        # column placement relative to pivot
        self.left_shift(left_index, pivot)
        self.right_shift(right_index, pivot)

        pivot_index = self.columns.array.index(pivot)

        # sorting the left and right subarray obtained by dividing the subarray with a pivot
        self.subarray_sort(left_index, pivot_index - 1)
        self.subarray_sort(pivot_index + 1, right_index)

    @Sort.show
    def show(self) -> None:
        self.subarray_sort(0, self.columns_count - 1)


if __name__ == "__main__":
    sort = QuickSort(columns_count=100, tick=1000)
    
    sort.show()
    
    print(sort.execucion_info())
