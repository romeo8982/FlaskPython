import io
import copy
import sys


def file_len(f_name):
    with open(f_name) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def print_list2d(temp):
    print("")
    for row in temp:
        print(row)


def read_dictionary(txt_file):
    with io.open(txt_file, 'r', encoding='utf8') as f:
        dictionary = f.read().splitlines()
    return dictionary


class Crossword:
    def __init__(self):
        self.word_size_list_x = []
        self.word_size_list_y = []
        self.x = None
        self.y = None
        self.T = None
        self.solved = None

    def init_from_file(self, txt_file):
        with open(txt_file) as f:
            self.x = len(f.readline()) - 1
            self.y = file_len(txt_file)

            if 10 <= self.x <= 30:
                if 10 <= self.y <= 30:
                    self.T = [["0"] * self.x for _ in range(self.y)]
        with open(txt_file) as f:
            index_i = 0
            for line in f:
                index_j = 0
                for sign in line:
                    if sign != "\n":
                        self.T[index_i][index_j] = sign
                    index_j += 1
                index_i += 1

        if 10 <= self.x <= 30:
            if 10 <= self.y <= 30:
                self.solved = [["0"] * self.x for _ in range(self.y)]

    def init_from_data(self, x, y, T, solved):
        self.x = x
        self.y = y
        self.T = T
        self.solved = solved

    def get_t(self):
        return self.T

    def check_horizontal(self, x, y, T, currentWord):
        n = len(currentWord)
        if any(n in sublist for sublist in self.word_size_list_x):
            for i in range(n):
                if T[x][y + i] == "0" or T[x][y + i] == currentWord[i]:
                    T[x][y + i] = currentWord[i]
                else:
                    T[0][0] = "@"
                    return T
        else:
            T[0][0] = "@"
            return T
        return T

    def check_vertical(self, x, y, T, currentWord):
        n = len(currentWord)
        if any(n in sublist for sublist in self.word_size_list_y):
            n = len(currentWord)
            for i in range(n):
                if T[x + i][y] == "0" or T[x][y] == currentWord[i]:
                    T[x + i][y] = currentWord[i]
                else:
                    T[0][0] = "@"
                    return T
        else:
            T[0][0] = "@"
            return T
        return T

    def if_its_fill(self, T):
        for i in range(self.x):
            for j in range(self.y):
                if T[i][j] == "0":
                    return False
        return True

    def solve_puzzle(self, dictionary, T, index, n):
        if not self.if_its_fill(T) and index < len(dictionary):
            current_word = dictionary[index]
            max_len = n - len(current_word)
            for i in range(n):
                for j in range(max_len + 1):
                    _copy = copy.deepcopy(T)
                    temp = self.check_vertical(j, i, _copy, current_word)
                    if temp[0][0] != '@':
                        self.solve_puzzle(dictionary, _copy, index + 1, n)

            for i in range(n):
                for j in range(max_len + 1):
                    _copy = copy.deepcopy(T)
                    temp = self.check_horizontal(i, j, _copy, current_word)
                    if temp[0][0] != '@':
                        self.solve_puzzle(dictionary, _copy, index + 1, n)
        elif self.if_its_fill(T):
            self.solved = T
            #print_list2d(T)
            return

    def get_word_size_list_x(self):
        for i in range(self.x):
            word_size = 0
            temp_list_word = []
            for j in range(self.y):
                if self.T[i][j] == "*":
                    if word_size != 0:
                        temp_list_word.append(word_size)
                        word_size = 0
                elif self.T[i][j] != "*":
                    word_size += 1
                    if j == self.y - 1:
                        temp_list_word.append(word_size)
                        word_size = 0
            self.word_size_list_x.append(temp_list_word)

    def get_word_size_list_y(self):
        for j in range(self.y):
            word_size = 0
            temp_list_word = []
            for i in range(self.x):
                if self.T[i][j] == "*":
                    if word_size != 0:
                        temp_list_word.append(word_size)
                        word_size = 0
                elif self.T[i][j] != "*":
                    word_size += 1
                    if i == self.y - 1:
                        temp_list_word.append(word_size)
                        word_size = 0
            self.word_size_list_y.append(temp_list_word)
