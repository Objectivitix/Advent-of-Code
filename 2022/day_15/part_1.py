import re

SENSOR_REPORT_REGEX = (
    r"Sensor at x=(-?\d+), y=(-?\d+): "
    r"closest beacon is at x=(-?\d+), y=(-?\d+)"
)

TARGET_Y = 2_000_000

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
            self.x + self.radius - distance
        )

def get_slices_at_y(sensors, y):
    return (
        interval
        for sensor in sensors
        if (interval := sensor.get_slice_at_y(y)) is not None
    )

def merge_intervals(sorted_intervals):
    result = [sorted_intervals[0]]

    for curr_start, curr_end in sorted_intervals[1:]:
        prev_start, prev_end = result[-1]

        if prev_end >= curr_start:
            merged = (prev_start, max(prev_end, curr_end))
            result[-1] = merged
        else:
            result.append((curr_start, curr_end))

    return result

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

intervals = sorted(get_slices_at_y(sensors, TARGET_Y))
merged_intervals = merge_intervals(intervals)

print(sum(end - start for start, end in merged_intervals))
