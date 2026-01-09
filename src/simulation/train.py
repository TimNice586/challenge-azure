from shapely.geometry import Point

class Train:
    def __init__(self, rail_curve, speed=10, train_id="T1", start_distance=0):
        self.rail_curve = rail_curve
        self.speed = speed  # meters per second
        self.train_id = train_id
        self.distance = start_distance  # current distance along curve

    def move(self, dt=1):
        """
        Move the train forward by dt seconds.
        Returns current shapely Point position.
        """
        self.distance += self.speed * dt
        if self.distance > self.rail_curve.length:
            self.distance = self.rail_curve.length  # stop at end
        return self.rail_curve.position_at_distance(self.distance)
