import psychopy

from sources.parameters import create_all_pairs


class Matrix:
    def __init__(self, n, lines, name,  x=4, y=4):
        assert x > 0 and y > 0, "x and y have to be higher than 0"
        assert n <= (x + 1) * (y + 1), "n can't be higher than (x+1) * (y+1)"
        self.x = x
        self.y = y
        self.n = n
        self.name = name
        self.lines = lines
        self.stimulus = []

    def prepare_draw(self, window, center_pos, line_len, line_width=3.5,
                     grid_width=2, line_color='black', grid_color='grey'):
        pos = (center_pos[0] - self.x * line_len / 2, center_pos[1] + self.y * line_len / 2)
        for line in create_all_pairs(self.x, self.y):
            if line in self.lines:
                stim = psychopy.visual.Line(win=window, units="pix", lineColor=line_color, lineWidth=line_width)
            else:
                stim = psychopy.visual.Line(win=window, units="pix", lineColor=grid_color, lineWidth=grid_width)

            stim.start = pos
            if line[0] == line[1] - 1:
                stim.end = (pos[0] + line_len, pos[1])
            else:
                stim.end = (pos[0], pos[1] - line_len)

            if line[0] != line[1] - 1 or line[0] >= self.x * (self.y + 1):
                pos = (pos[0] + line_len, pos[1])
            if line[0] != line[1] - 1 and line[1] % (self.x + 1) == self.x:
                pos = (pos[0] - (self.x + 1) * line_len, pos[1] - line_len)

            self.stimulus.append(stim)

    def set_auto_draw(self, draw):
        for stim in self.stimulus:
            stim.setAutoDraw(draw)

