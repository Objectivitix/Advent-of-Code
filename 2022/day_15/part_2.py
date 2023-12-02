import re

SENSOR_REPORT_REGEX = (
    r"Sensor at x=(-?\d+), y=(-?\d+): "
    r"closest beacon is at x=(-?\d+), y=(-?\d+)"
)

COORDS_LOWER_LIMIT = 0
COORDS_UPPER_LIMIT = 4_000_000

TUNING_COEFFICIENT  = 4_000_000

class Sensor:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def __repr__(self):
        props = ", ".join(f"{key}={value}" for key, value in self.__dict__.items())
        return f"{self.__class__.__name__}({props})"

    def get_slice_at_y(self, y):
        if (distance := abs(y - self.y)) > self.radius:
            return None

        return (
            self.x - self.radius + distance,
            self.x + self.radius - distance,
        )

def get_slices_at_y(sensors, y):
    return (
        (
            max(interval[0], COORDS_LOWER_LIMIT),
            min(interval[1], COORDS_UPPER_LIMIT),
        )
        for sensor in sensors
        if (interval := sensor.get_slice_at_y(y)) is not None
    )

def get_available_x(sorted_intervals):
    _, max_end = sorted_intervals[0]

    for next_start, next_end in sorted_intervals[1:]:
        if max_end < (tentative := next_start - 1):
            return tentative

        max_end = max(max_end, next_end)

    return -1

with open("input.txt") as file:
    raw = file.read().splitlines()

sensors = []

for line in raw:
    data = re.match(SENSOR_REPORT_REGEX, line).groups()
    sensor_x, sensor_y, beacon_x, beacon_y = map(int, data)

    dist_to_nearest_beacon = (
        abs(sensor_x - beacon_x)
        + abs(sensor_y - beacon_y)
    )

    sensors.append(Sensor(sensor_x, sensor_y, dist_to_nearest_beacon))

for y in range(COORDS_LOWER_LIMIT, COORDS_UPPER_LIMIT + 1):
    intervals = sorted(get_slices_at_y(sensors, y))
    result = get_available_x(intervals)

    if result != -1:
        break

print(result * TUNING_COEFFICIENT + y)
