import random
import numpy as np

from sources.matrix import Matrix
from sources.parameters import create_all_pairs


class Trial:
    def __init__(self, n, x=4, y=4, n_answers=3):
        assert x > 0 and y > 0, "x and y have to be higher than 0"
        assert n <= (x + 1) * (y + 1), "n can't be higher than (x+1) * (y+1)"
        assert n > 0, "n must be higher than 0"
        self.x = x
        self.y = y
        self.n = n
        self.n_answers = n_answers
        self.possible_pairs = create_all_pairs(x, y)
        self.xor_lines = self.choose_lines()
        self.main_lines = self.choose_lines()

        if random.random() < 0.5:
            self.left_matrix = Matrix(n, self.main_lines + self.xor_lines[:n//2], "main_left", x=self.x, y=self.y)
            self.right_matrix = Matrix(n, self.main_lines + self.xor_lines[n // 2:], "main_right", x=self.x, y=self.y)
        else:
            self.left_matrix = Matrix(n, self.main_lines + self.xor_lines[n // 2:], "main_left", x=self.x, y=self.y)
            self.right_matrix = Matrix(n, self.main_lines + self.xor_lines[:n // 2], "main_right", x=self.x, y=self.y)

        self.answers = [Matrix(n, self.xor_lines, "correct", x=self.x, y=self.y)]

        while len(self.answers) < n_answers:
            m = self.generate_wrong_answer()
            if set(m.lines) not in [set(elem.lines) for elem in self.answers]:
                self.answers.append(self.generate_wrong_answer())
        random.shuffle(self.answers)

    def generate_wrong_answer(self):
        if self.n == 1:
            number_of_different_lines = 1
        else:
            number_of_different_lines = random.choice([1, 2])
        new_lines = self.xor_lines[:]
        for _ in range(number_of_different_lines):
            if random.random() < 0.5:
                while True:
                    new_line = random.choice(self.main_lines)
                    if new_line not in new_lines:
                        new_lines.pop(random.randrange(len(new_lines)))
                        new_lines.append(new_line)
                        break
            else:
                while True:
                    new_line = random.choice(self.possible_pairs)
                    if new_line not in new_lines:
                        new_lines.pop(random.randrange(len(new_lines)))
                        new_lines.append(new_line)
                        break

        return Matrix(self.n, new_lines, "wrong_{}".format(number_of_different_lines), x=self.x, y=self.y)

    def choose_lines(self):
        lines = []

        while len(lines) < self.n:
            line = self.possible_pairs[np.random.choice(range(len(self.possible_pairs)))]
            self.possible_pairs.remove(line)
            lines.append(line)
            if len([1 for l in lines if line[0] in l]) == 2:
                self.possible_pairs = [l for l in self.possible_pairs if line[0] not in l]
            if len([1 for l in lines if line[1] in l]) == 2:
                self.possible_pairs = [l for l in self.possible_pairs if line[1] not in l]

        return lines

    def prepare_draw(self, window, matrix_offset, line_len, main_move_y=0, answers_move_y=-150,  line_width=3.5,
                     grid_width=2, line_color='black', grid_color='grey'):
        pos = [-matrix_offset/2, main_move_y]
        self.left_matrix.prepare_draw(window, pos, line_len, line_width=line_width, grid_width=grid_width,
                                      line_color=line_color, grid_color=grid_color)
        pos = [matrix_offset / 2, main_move_y]
        self.right_matrix.prepare_draw(window, pos, line_len, line_width=line_width, grid_width=grid_width,
                                       line_color=line_color, grid_color=grid_color)

        pos = [-matrix_offset*(self.n_answers-1)/2, answers_move_y]
        for matrix in self.answers:
            matrix.prepare_draw(window, pos, line_len, line_width=line_width, grid_width=grid_width,
                                line_color=line_color, grid_color=grid_color)
            pos[0] += matrix_offset

    def set_auto_draw(self, draw):
        for stim in [self.left_matrix, self.right_matrix] + self.answers:
            stim.set_auto_draw(draw)
