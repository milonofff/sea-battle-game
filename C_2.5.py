from random import randint
# Классы исключений
class BoardException(Exception): # Общий класс исключений, который содержит все остальные классы исключений
    pass

# Два класса пользовательских исключений:
class BoardOutException(BoardException): # Если пользователь выстрелит за доску, выйдет это исключение
    def __str__(self):
        return "Вы пытаетесь выстрельить за доску!"

class BoardUsedException(BoardException): # Если пользователь стрелял в эту клетку, выйдет это исключение
    def __str__(self):
        return "Вы уже стреляли в эту клетку!"

class BoardWrongShipException(BoardException): # Исключение для того чтобы нормально размещать корабли на доске
    pass


# Класс координаты точек (выстрелов, расположение кораблей)

class Dot:
    def __init__(self, x, y): # x, y передаются в конструкторе init
        self.x = x
        self.y = y
# например, сравним координаты без repr
# a = Dot(1, 1)ы
# b = Dot(2, 3)
# c = Dot(1, 1)
# print(a.x == c.x and a.y == c.y) #True

    # Сравниваем друг с другом точки, а также находится ли эта точка в списке, например, при выстреле в корабль проверяем
    # есть ли в списке точек корабля и т.д.

    def __eq__(self, other): # Оператор равенства, в нашем случае проверяет совпадают ли одни координаты от других координат (x, y) или нет!
        return self.x == other.x and self.y == other.y

    def __repr__(self): # выводит координаты на консоль
        return f"Dot({self.x}, {self.y}"

# Класс корабли:

class Ship:
    def __init__(self, bow, l, o):
        self.bow = bow # нос корабля
        self.l = l # длина корабля
        self.o = o # ориентация корабля
        self.lives = l

    @property # метод который вычисляет какое-то свойство корабля
    def dots(self): # точки - не просто метод, а непосредсвенно свойство
        ship_dots = []
        for i in range(self.l):
            cur_x = self.bow.x # self.bow.x и self.bow.y текущие точки - это нос корабля
            cur_y = self.bow.y # берем нос корабля и начинаем шагать на y клеток

            if self.o == 0: # вертикальное положение корабля
                cur_x += i # идет сдвиг на x точек от носа

            elif self.o == 1: # горизотальное положение корабля
                cur_y += i # идет сдвиг на y точек от носа

            ship_dots.append(Dot(cur_x,cur_y)) # получаем список точек

        return ship_dots # точки всего корабля

    def shooten(self,shot): # метод который показывает попал или нет
        return shot in self.dots # проверка на попадание
# Тестирование

#s = Ship(Dot(1, 2), 4, 0) # 1) Задаем координаты носа корабля (Dot(1,2), 4 - длина корабля, 0 - ориентация корабля
#print(s.dots())
#print(s.shooten(Dot(2,2))) # True, мы попали в корабль


# Игровое поле
class Board:
    def __init__(self, hid = False, size = 6):
        self.hid = hid # нужно ли наше поле скрывать
        self.size = size # размер поля

        self.count = 0 # количество пораженных кораблей

        self.field = [["0"] * size for _ in range(size)] # Сеть 6 на 6, в котором храниться состояние поля, изначально 0

        self.busy = [] # Хранится занятые точки, либо занятые кораблем точки, либо точки от выстрелов

        self.ships = [] # Список кораблей доски

    def __str__(self): # Делаем вывод корабля на доску, метод str не просто печатает
        res = ""
        res +="    1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate (self.field):
            res += f"\n{i + 1} | " + " | ".join(row) + " |"

        if self.hid: # нужно ли скрывать корабли на доске
            res = res.replace("*", "0") # replace - замена
        return res

    #b = Board()  # нам не нужно вызывать какой либо метод, мы уже определили в методе __str__
    # print(b)

    def out(self, d): # метод который проверяет находится ли точка за пределами доски. Передаем точку d (dots)
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size)) # точки d.x лежат в интервале от 0 до size
        # проверка на то что точка выходит за границы это отрицание этого услования поэтому стоит not

    # Добавление корабля на доску
    def contour(self, ship, verb = False): # в списке near объявлены все точки вокруг той в которой мы находимся
        # например, (0,0) - это сама точка, (0,-1) - точка выше исходной, (0,1) - точка ниже (0,0).
        # Таким образом в списке находится все сдвиги точки которые приходят к соседним как по диагонали так и по стороне.

        near = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 0), (0, 1),
            (1, -1), (1, 0), (1, 1),
        ]
        # Таким образом в двойном цикле мы пройдемся по всем точкам которые соседствуют с кораблем.
        # Это нужно для расположение кораблей на доске
        for d in ship.dots: # Мы берем каждую точку корабля
            for dx, dy in near: # Проходимся циклом по списку near
                cur = Dot(d.x + dx, d.y + dy) # Сдвигаем исходную точку на dx и dy, т.е. из первой переменной на вторую (в кортеже (-1,-1))
                if not(self.out(cur)) and cur not in self.busy: # Если точки не выходят за границы доски и если точка не занята еще
                    if verb: # Параметр verb говорит нужно ли ставить точку или нет вокруг кораблей
                    # Нам нужно ставить точки вокруг кораблей когда у нас будет реальная игра, а когда раставляем корабли
                    # нам достаточно внести в список busy
                        self.field[cur.x][cur.y] = "." # Во-вторых, мы ставим на это место символ - ".", чтобы показать что эта точка занята
                    self.busy.append(cur) # Во-первых, мы добавляем в список busy(список занятых точек)
    def add_ship(self, ship):
        for d in ship.dots: # Проверяет что каждая точка корабля
            if self.out(d) or d in self.busy: # во-первых, не выходят за границы self.out(d), во-вторых не занята self.busy
                raise BoardWrongShipException() # Если это не так мы выбрасываем исключение
        for d in ship.dots: # Пройдемся по точкам корабля
            self.field[d.x][d.y] = '*' # И ставим каждой из этих точек "*"
            self.busy.append(d) # И запишем что эти точки заняты. В списке busy будут точки корабля или которая с ней соседствует

        self.ships.append(ship) # Добавляем в список собственных кораблей
        self.contour(ship) # Обводим их по контуру

    def shot(self, d): # Делаем выстрел
        if self.out(d): # Если выходим за границы то выбрасываем исключение BoardOutException
            raise BoardOutException()

        if d in self.busy: # Проверяем занята ли точка, если занята выбрасываем ислючение BoardUsedException
            raise BoardUsedException()

        self.busy.append(d) # Если точка была не занята, то добавляем в список busy

        for ship in self.ships: # Проверяем принаждлежит ли точка к какому то кораблю или нет
            if ship.shooten(d):
                ship.lives -= 1 # Если есть попадание убираем -1 жизни
                self.field[d.x][d.y] = "X" # Если корабль поражен
                if ship.lives == 0: # Если у корабля кончились жизни
                    self.count += 1 # Прибавляем к счетчику уничтоженных кораблей +1
                    self.contour(ship, verb=True) # Обводим точками уничтоженный корабль, точки рядом с кораблем мы не можем стрелять
                    print("Корабль уничтожен!")
                    return False # Дальше ход не нужно делать
                else: # Если кол-во жизни не равен 0, то:
                    print("Корабль ранен!")
                    return True # Нужно повторить ход
            # Если ни один корабль не был поражен, выполняется код дальше:
        self.field[d.x][d.y] = "." # Ставим точку в точке выстрела
        print("Мимо!")
        return False

    # Важно когда начнем игру, нам нужно чтобы список busy обновился.
    def begin(self):
        self.busy = [] #Теперь busy нужна для хранения точек куда игрок стрелял. Метод contour становиться универсальным:
        # для расстановки и для того чтобы выполнять саму игру
# Класс игрока
class Player:
    def __init__(self, board, enemy): # передаются две доски
        self.board = board
        self.enemy = enemy

    def ask(self): # метод ask мы не определяем
        raise NotImplementedError()

    def move(self): # в бесконечном цикле пытаемся сделать выстрел
        while True:
            try:
                target = self.ask() # просим компьютера или пользователя координаты выстрела
                repeat = self.enemy.shot(target) #выполняем выстрел, если выстрел хорошо прошел, то повторяем ход
                return repeat
            except BoardException as e:
                print(e)
# Классы "игрок-компьютер" и "игрок - пользователь"
class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5)) # Случайно генерируем две точки от 0 до 5
        print(f"Ход компьютера: {d.x + 1}{d.y + 1}")
        return d

class User(Player):
    def ask(self):
        while True:
            cords = input("Ваш ход:   ").split()

            if len(cords) != 2:
                print(" Введите две координаты! ")
                continue

            x, y = cords

            if not (x.isdigit()) or not (y.isdigit()): #Проверяем что это числа
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)
            return Dot(x - 1, y - 1) # индексация в списках идет с 0, а пользователю показывается с 1

# Класс игра и генерация досок

class Game:
    # Создаем конструктор и приветсвие
    def __init__(self, size = 6):
        self.size = size # Размер доски
        pl = self.random_board() # Генерируем случайную доску для игрока
        co = self.random_board() # Генерируем случайную доску для компьютера
        co.hid = True # Для компьютера скрываем корабли

        self.ai = AI(co, pl) # Создаем игрока AI
        self.us = User(pl, co) # Создаем игрока User

    def try_board(self): # Генерируем доску заполенную кораблями. Пытаемся каждый корабль расставить на доску
        lens = [3, 2, 2, 1, 1, 1, 1] # Длины кораблей
        board = Board(size=self.size) # Создаем доску
        attempts = 0 # Количество попыток поставить корабли на доску
        for l in lens: # Для каждой длины корабля, в бесконечном цикле пытаемся расставить
            while True:
                attempts += 1
                if attempts > 2000: # Если > 2000, возвращем пустую доску
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)  # Добавляем корабль
                    break # если удачно добавили корабль до делаем break
                except BoardWrongShipException: # Если выпадает исключение то проводим итерацию заново
                    pass
        board.begin()
        return board
    # Метод который гарантировано генерирует случайную доску
    def random_board(self):
        board = None # сначала доска пустая
        while board is None: # пока доска пустая мы пытаемся ее создать
            board = self.try_board()
        return board

    def greet(self):
        print("_________________________")
        print("     Приветсвуем вас     ")
        print("         в игре          ")
        print("       морской бой       ")
        print("_________________________")
        print("    формат ввода: x  y   ")
        print("    x - номер строки     ")
        print("    y - номер столбца    ")

    # Создаем игровой цикл
    def loop(self):
        num = 0 # номер хода
        while True:
            print('-' * 20)
            print("Доска пользователя:")
            print(self.us.board)
            print('-' * 20)
            print("Доска компьютера:")
            print(self.ai.board)
            print('-' * 20)
            if num % 2 == 0:
                print("Ходит пользователь!")
                repeat = self.us.move()
            else:
                print("Ходит компьютер!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.count == 7:
                print('-' * 20)
                print("Пользователь выиграл!")
                break

            if self.us.board.count == 7:
                print('-' * 20)
                print("Компьютер выиграл!")
                break
            num += 1

    def start(self):
        self.loop()
        self.greet()



g = Game()
g.start()








