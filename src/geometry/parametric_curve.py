from shapely.geometry import LineString

class ParametricRailCurve:
    def __init__(self, linestring: LineString):
        self.line = linestring
        self.length = linestring.length

    def position_at_distance(self, s: float):
        """
        Return (x, y) at distance s along the rail.
        """
        if s < 0:
            s = 0
        if s > self.length:
            s = self.length

        return self.line.interpolate(s)
