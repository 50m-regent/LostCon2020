class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def from_json(json):
        point = Point(json[0], json[1])
        return point

    def to_json(self):
        return [self.x, self.y]