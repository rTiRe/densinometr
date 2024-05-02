## Пример использования
from backend import Densitometr, Statictic


densitometr = Densitometr("COM4")
input("Положите в устройсто колбу с водой. (Введите что-то что бы продолжить)")
densitometr.initialize()
input("Положите в устройсто колбу с вашей жидкостью. (Введите что-то что бы продолжить)")
while True:
    statictic: Statictic = densitometr.get_statistic()
    print(statictic)