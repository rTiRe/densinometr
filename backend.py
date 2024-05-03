import serial

COLOR_LENGTH = 7
CONFIGURE_COD = 100

class Statictic:
    def __init__(
        self,
        current_colors_optical_density: dict[str, float],
        current_avg_optical_density: float,
        avg_colors_optical_density: dict[str, float],
        avg_optical_optical_density: float
    ) -> None:
        """
        Args:
            current_colors_optical_density (dict[str, float]): оптическая плотность полученная на данный момент времени
            current_avg_optical_density (float): среднее между current_colors_optical_density
            avg_colors_optical_density (dict[str, float]): средняя оптическая плотность полученная за всё время (красная: среднее всех красных, и.т.д)
            avg_optical_optical_density (float): среднее мужду avg_colors_optical_density
        """
        self.current_colors_optical_density = current_colors_optical_density
        self.current_avg_optical_density = current_avg_optical_density
        self.avg_colors_optical_density = avg_colors_optical_density
        self.avg_optical_optical_density = avg_optical_optical_density

    def __str__(self) -> str:
        return f"current_colors_optical_density: {self.current_colors_optical_density} \n \
            current_avg_optical_density: {self.current_avg_optical_density} \n \
            avg_colors_optical_density: {self.avg_colors_optical_density} \n \
            avg_optical_optical_density: {self.avg_optical_optical_density} \n \
        "

class Densitometr:
    COLOR_LENGTH = 7
    densitometr_values: list[list[float]] = []

    def __init__(self, port) -> None:
        self.port = port
        self.serial = serial.Serial(self.port, 9600)

    def initialize(self):
        self.serial.write(str(CONFIGURE_COD).encode())
        self.serial.readline()

    def clear_():
        densitometr_values = []

    def _avg_optical_optical_density(self):
        return sum(self._avg_colors_optical_density().values()) / COLOR_LENGTH

    def _avg_colors_optical_density(self) -> dict[str, float]:
        result = {}
        for values in self.densitometr_values:
            for color, value in values.items():
                start_val = result.get(color, 0)
                result[color] = value + start_val
        for color in result.keys():
            result[color] /= len(self.densitometr_values)
        return result
    
    def get_statistic(self) -> Statictic:
        self.serial.write("1".encode())
        values = [float(val) for val in self.serial.readline().split()]
        current_colors_optical_density = {
            "blue": values[0],
            "green": values[1],
            "lightblue": values[2],
            "red": values[3],
            "purple": values[4],
            "yellow": values[5],
            "white": values[6]
        }
        self.densitometr_values.append(current_colors_optical_density)
        current_avg_optical_density = sum(current_colors_optical_density.values()) / len(current_colors_optical_density)


        return Statictic(current_colors_optical_density,
                current_avg_optical_density,
                self._avg_colors_optical_density(),
                self._avg_optical_optical_density())
