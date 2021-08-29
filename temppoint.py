
class TempPoint():
    def __init__(self, time, temp):
        self.time = int(time) * 1000
        self.temp = temp

    def get_temp_point(self):
        return (f'{{x: {self.time}, y: {self.temp}}}')


def temp_arr_to_string(arr):
    result = ''
    for point in arr:
        if point.temp == 157 or point.temp == -127:
            continue
        result += point.get_temp_point() + ','
    return result[0:-1]
