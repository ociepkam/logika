def create_all_pairs(x, y):
    pairs = []
    for point in range((x + 1) * (y + 1)):
        if point % (x + 1) != x:
            pairs.append((point, point + 1))
        if point <= (x + 1) * y - 1:
            pairs.append((point, point + x + 1))
    return pairs


KEYS = ["left", "down", "right"]
