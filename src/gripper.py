from pyDHgripper import RGD
import time


gripper = RGD(port='COM3')
while gripper.read_state() != 1:
    time.sleep(0.05)

gripper.set_pos(val=500)

def set_abs_rot(val : int) -> None:
    """Установка угла поворота гриппера с блокировкой других команд до конца прокручивания гриппера"""
    gripper.set_abs_rot(val=val)
    while gripper.read_state() != 1:
        time.sleep(0.05)


def main():
   # print(gripper.read_pos(), gripper.read_state(), gripper.read_uart())
   #  # Для ожидания конца действий гриппера при его инициализации
   #  while gripper.read_state() != 1:
   #      time.sleep(0.05)
   #      print("2")
   #
   #  set_abs_rot(1)
   #  # gripper.set_pos()
   #
   #  # метод set_pos уже имеет блокировку других команд внутри себя
   # # gripper.set_pos(val=0)
   ...



def united():
    a = 1
    while a>0:
        gripper.set_pos(val=0)
        set_abs_rot(50)
        set_abs_rot(0)
        set_abs_rot(180)

    # Короче, я не знаю, как реализовать подключение к грипперу без его инициализации, как будто бы так низя сделать
    # Поэтому мне кажется, шо нужно написать этот скрипт так, чтобы его не приходилось много раз запускать
    # Я думаю, легче всего это делается через ввод кодов команд с консоли вс необходимыми параметрами в бесконечном цикле while
    # Т.е., например, написанная в консоль 1 - это вызвать метод set_pose и передать ему ещё одно считанное число val (насколько сжать/отпустить гриппер)
    # 2 - вывести в консоль текущий val сжатия гриппера (результат метода read_pos) и т.д.
    # Для просмотра всех методов можешь зайти в файл Gripper.py выше или просто с зажатой клавишей CTRL нажать ЛКМ по RGD или написанному в коде методу
if __name__ == "__main__":
    main()