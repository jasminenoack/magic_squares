from copy import copy, deepcopy
from sys import argv


class RowColumnMixin(object):
        def find_column(self, number):
            for index, column in enumerate(self.columns):
                if number in column:
                    return column, index

        def find_row(self, number):
            for index, row in enumerate(self.rows):
                if number in row:
                    return row, index

        def index_from_row_column(self, row, column):
            return self.order * row + column

        def find_number_in_row(self, square, order, index):
            row = index/order
            first_index = self.index_from_row_column(row, 0)
            for number in square[first_index:first_index + order]:
                if number:
                    return number

        def find_number_in_column(self, square, order, index):
            column_index = index % order
            for number in square[column_index::order]:
                if number:
                    return number


class SquareSet(RowColumnMixin):
    def __init__(self, rows, columns, diagonals, groups, order):
        self.order = order
        self.base_square = [0] * self.order * self.order
        self.rows = rows
        self.columns = columns
        self.diagonals = diagonals
        self.diagonal_1_groups = groups
        self.squares = self.create_squares()

    def create_squares(self):
        rows_to_create = range(self.order / 2)
        row_sets = self.diagonal_1_groups
        diagonals = self.get_diagonals([], self.diagonal_1_groups)
        results = []

        for diagonal in diagonals:
            square = copy(self.base_square)
            for i in range(self.order):
                square[self.index_from_row_column(i, i)] = diagonal[i]

            for index, number in enumerate(square):
                if number:
                    continue
                number_in_row = self.find_number_in_row(
                    square, self.order, index
                )
                row, row_index = self.find_row(number_in_row)
                number_in_column = self.find_number_in_column(
                    square, self.order, index
                )
                column, column_index = self.find_column(number_in_column)
                new_number = list(set(row).intersection(column))[0]
                square[index] = new_number
            results.append(square)
        return results

    def print_square(self, square):
        for i in range(len(square))[::self.order]:
            print "    " + " ".join(
                format(x, '2') for x in square[i:i+self.order]
            )
        print ""

    def get_diagonals(self, numbers=[], groups=[], diagonals=[]):
        diagonals = self.create_diagonals(
            numbers, groups, diagonals
        )
        return diagonals

    def create_diagonals(self, numbers=[], groups=[], diagonals=[]):
        if not len(groups):
            diagonals = copy(diagonals)
            diagonals.append(numbers)
            return diagonals

        new_diagonals = []
        for i in range(len(groups)):
            current_set = groups[i]
            for number in current_set:
                new_numbers = copy(numbers)
                new_numbers.append(number)
                current_diagonals = self.create_diagonals(new_numbers, [
                    x for x in groups
                    if x != current_set
                ])
                next_number = [
                    x for x in current_set
                    if x != number
                ][0]
                for diag in current_diagonals:
                    diag.append(next_number)
                new_diagonals += current_diagonals
                if len(numbers) == 0:
                    break
        return new_diagonals

    def print_data(self):
        print "Set of groups:"
        print "    rows:"
        for row in self.rows:
            print("        " + " ".join(format(x, '2') for x in row))

        print "    columns:"
        for column in self.columns:
            print("        " + " ".join(format(x, '2') for x in column))

        print "    diagonal options:"
        for diagonal in self.diagonals:
            print "        " + " ".join(format(x, '2') for x in diagonal)

        print ""

        print "Unique Squares"
        for square in self.squares:
            self.print_square(square)
        print ""


class OddSquareSet(SquareSet):
    odd = True

    def get_diagonals(self, numbers=[], groups=[], diagonals=[]):
        mid_number = list(
            set(self.diagonals[0]).intersection(self.diagonals[1])
        )[0]
        diagonals = self.create_diagonals(
            numbers, groups, diagonals
        )
        for index, diagonal in enumerate(diagonals):
            mid_index = self.order / 2
            diagonals[index] = (
                diagonal[:mid_index] + [mid_number] + diagonal[mid_index:]
            )
        return diagonals


class EvenSquareSet(SquareSet):
    even = False


class MagicSquareGroup(RowColumnMixin):
    def __init__(self, rows, columns, constant, order):
        # rows in the square group
        self.rows = rows
        # columns in the square group
        self.columns = columns
        # the magic constant
        self.magic_constant = constant
        # diagonals that are possible with the rows and columns
        self.diagonals = self.find_diagonals()
        # order of the square
        self.order = order
        # find unique sets of rows, columns, diagonals
        self.unique_square_sets = self.find_diagonal_pairs()

    def find_diagonals(self):
        results = []

        def _find_diagonals(current_numbers, numbers_disallowed,
                            remaining_sets):
            new_remain = deepcopy(remaining_sets)
            if not len(remaining_sets):
                if sum(current_numbers) == self.magic_constant:
                    results.append(current_numbers)
                return
            next_set = new_remain.pop(0)
            for number in next_set:
                if number in numbers_disallowed:
                    continue
                new_numbers = copy(current_numbers)
                new_numbers.append(number)
                new_disallowed = (
                    numbers_disallowed + self.find_column(number)[0]
                )
                _find_diagonals(new_numbers, new_disallowed, new_remain)
        _find_diagonals([], [], self.rows)

        return results

    def is_valid(self):
        return len(self.unique_square_sets)

    def find_diagonal_pairs(self):
        results = []
        matching_numbers = self.order % 2
        for index, org_first_diagonal in enumerate(self.diagonals):
            for org_second_diagonal in self.diagonals[index + 1:]:
                first_diagonal = copy(org_first_diagonal)
                second_diagonal = copy(org_second_diagonal)

                intersection = set(first_diagonal).intersection(
                    second_diagonal
                )
                # check if the number of matching number is the expected amount
                if len(intersection) != matching_numbers:
                    continue

                groups = []
                while len(first_diagonal):
                    first_row_first_num = first_diagonal[0]
                    first_row, first_row_index = self.find_row(
                        first_row_first_num
                    )
                    # find the second number in the same row
                    first_row_second_num = list(
                        set(first_row).intersection(second_diagonal)
                    )[0]

                    first_column, first_column_index = self.find_column(
                        first_row_first_num
                    )
                    second_column, second_column_index = self.find_column(
                        first_row_second_num
                    )
                    first_column_second_num = list(set(
                        first_column
                    ).intersection(second_diagonal))[0]
                    second_column_second_number = list(set(
                        second_column
                    ).intersection(first_diagonal))[0]

                    if (
                        self.find_row(first_column_second_num)[1]
                        == self.find_row(second_column_second_number)[1]
                    ):
                        if first_row_first_num != first_row_second_num:
                            groups.append(
                                [
                                    first_row_first_num,
                                    second_column_second_number
                                ]
                            )
                        numbers_to_remove = [
                            first_row_first_num,
                            first_row_second_num,
                            first_column_second_num,
                            second_column_second_number
                        ]
                        first_diagonal = [
                            x for x in first_diagonal
                            if x not in numbers_to_remove
                        ]
                        second_diagonal = [
                            x for x in second_diagonal
                            if x not in numbers_to_remove
                        ]
                    else:
                        break
                # if we managed to remove all numbers we found a solution
                if not first_diagonal:
                    if matching_numbers:
                        results.append(OddSquareSet(
                            deepcopy(self.rows),
                            deepcopy(self.columns),
                            [
                                copy(org_first_diagonal),
                                copy(org_second_diagonal)
                            ],
                            groups,
                            self.order
                        ))
                    else:
                        results.append(EvenSquareSet(
                            deepcopy(self.rows),
                            deepcopy(self.columns),
                            [
                                copy(org_first_diagonal),
                                copy(org_second_diagonal)
                            ],
                            groups,
                            self.order
                        ))
        return results


class MagicSquareOfOrder(object):
    def __init__(self, order):
        # the order of the magic square
        self.order = order
        # the magic constant
        self.magic_constant = self.get_magic_constant()
        # the magic series for the order and constant
        self.series = self.find_series()
        # the groups of series that could be used as rows or columns
        self.groups = self.groups_of_all_numbers()
        # square groups with matching row and column sets
        # they also calculate their possible diagonals
        self.square_groups = self.find_square_groups()
        # remove invalid squares(no diagonals)
        self.clean_squares()

    def print_information(self):
        print "The order of the square is {}.".format(self.order)
        print "The magic constant is {}.".format(self.magic_constant)
        print "Found {} magic series.".format(len(self.series))
        print "Found {} groups of rows and columns.".format(len(self.groups))
        print "Found valid {} groups of squares.".format(
            len(self.square_groups)
        )
        total = 0
        for group in self.square_groups:
            total += len(group.unique_square_sets)
        print "Found {} unique row, column, square sets".format(total)
        print ""

        print "Iterating showing all the squares"
        for group in self.square_groups:
            for unique in group.unique_square_sets:
                unique.print_data()

    def print_squares(self):
        for group in self.square_groups:
            for unique in group.unique_square_sets:
                for square in unique.squares:
                    print " ".join(format(x, '2') for x in square)

    def find_series(self):
        numbers = range(1, self.order * self.order + 1)

        results = []

        def _find_series(current_series, numbers_left):
            if len(current_series) == self.order:
                if sum(current_series) == self.magic_constant:
                    results.append(current_series)
                return
            if not len(numbers_left):
                return
            for index, number in enumerate(numbers_left):
                new_series = copy(current_series)
                new_series.append(number)
                _find_series(new_series, numbers_left[index + 1:])

        _find_series([], numbers)
        return results

    def groups_of_all_numbers(self):
        results = []

        def _find_sets(current_sets, other_sets):
            if len(current_sets) == self.order:
                results.append(current_sets)
                return

            for index, single_set in enumerate(other_sets):
                new_sets = deepcopy(current_sets)
                new_sets.append(single_set)
                flat = [one for s_set in new_sets for one in s_set]
                as_set = set(flat)
                if len(as_set) == len(flat):
                    _find_sets(new_sets, other_sets[index + 1:])

        _find_sets([], self.series)
        return results

    def find_square_groups(self):
        results = []

        def _find_matching_sets(current_set, other_sets):
            for other_set in other_sets:
                solution = True
                for other_group in other_set:
                    for current_group in current_set:
                        intersection = set(other_group).intersection(
                            current_group
                        )
                        if len(intersection) != 1:
                            solution = False
                            break
                    if not solution:
                        break
                if solution:
                    results.append(
                        MagicSquareGroup(
                            deepcopy(current_set),
                            deepcopy(other_set),
                            self.magic_constant,
                            self.order
                        )
                    )

        for index, current_set in enumerate(self.groups):
            _find_matching_sets(current_set, self.groups[index + 1:])
        return results

    def get_magic_constant(self):
        return self.order * (self.order**2 + 1) / 2

    def clean_squares(self):
        self.square_groups = [
            group for group in self.square_groups
            if group.is_valid()
        ]

    def find_diagonal_sets(self):
        for group in self.square_groups:
            group.find_diagonal_pairs()


if __name__ == '__main__':
    if len(argv) == 3:
        output_type = argv.pop()
        order = int(argv.pop())
    elif len(argv) == 2:
        output_type = "info"
        order = int(argv.pop())
    else:
        output_type = "info"
        order = 3

    group = MagicSquareOfOrder(order)
    if output_type == "info":
        group.print_information()
    elif output_type == "squares":
        group.print_squares()
