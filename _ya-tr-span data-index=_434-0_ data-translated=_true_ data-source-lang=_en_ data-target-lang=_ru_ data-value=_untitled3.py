import random

class Ship:
    def __init__(self, size, position):
        self.size = size
        self.position = position
        self.hits = [False] * size

    def hit(self, index):
        self.hits[index] = True
        
    def is_sunk(self):
        return all(self.hits)

class Board:
    def __init__(self):
        self.size = 6
        self.ships = []
        self.grid = [['о'] * self.size for _ in range(self.size)]

    def add_ship(self, ship):
        self.ships.append(ship)

        # проверяем, чтобы корабли не находились слишком близко друг к другу
        for i, j in ship.position:
            for x, y in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                if 0 <= x < self.size and 0 <= y < self.size:
                    if self.grid[x][y] == '■':
                        raise Exception("корабли находятся слишком близко друг к другу")
        
        # размещаем корабль на доске
        for i, j in ship.position:
            self.grid[i][j] = '■'

    def display(self):
        print('   | 1 | 2 | 3 | 4 | 5 | 6|')
        for i in range(self.size):
            row = ' | '.join(self.grid[i])
            print(f'{i+1} | {row} |')

    def shoot(self, x, y):
        if self.grid[x][y] == '■':
            for ship in self.ships:
                for index, (i, j) in enumerate(ship.position):
                    if i == x and j == y:
                        ship.hit(index)
                        self.grid[x][y] = 'x'
                        if ship.is_sunk():
                            print("вы потопили корабль!")
                        else:
                            print("вы попали!")
                        return
        elif self.grid[x][y] == 'о':
            self.grid[x][y] = 't'
            print("вы промахнулись!")
        else:
            raise Exception("вы уже стреляли в эту клетку!")

class Game:
    def __init__(self):
        self.player_board = Board()
        self.computer_board = Board()
        self.player_turn = True

    def place_ships(self):
        player_ships = [(3, [(0, 0), (0, 1), (0, 2)]),
                        (2, [(1, 4), (2, 4)]),
                        (2, [(3, 0), (3, 2)]),
                        (1, [(3, 4)]),
                        (1, [(4, 4)]),
                        (1, [(5, 1)])]
            
        computer_ships = [(3, [(0, 0), (0, 1), (0, 2)]),
                          (2, [(1, 4), (2, 4)]),
                          (2, [(3, 0), (3, 2)]),
                          (1, [(3, 4)]),
                          (1, [(4, 4)]),
                          (1, [(5, 1)])]
        
        for size, position in player_ships:
            ship = Ship(size, position)
            self.player_board.add_ship(ship)
        
        for size, position in computer_ships:
            ship = Ship(size, position)
            self.computer_board.add_ship(ship)

    def play(self):
        self.place_ships()
        
        while True:
            if self.player_turn:
                print("ваша доска:")
                self.player_board.display()
                print("доска компьютера:")
                self.computer_board.display()
                
                while True:
                    try:
                        x = int(input("введите номер строки: ")) - 1
                        y = int(input("введите номер столбца: ")) - 1
                        self.player_board.shoot(x, y)
                        break
                    except Exception as e:
                        print(str(e))
                    
                if all(ship.is_sunk() for ship in self.computer_board.ships):
                    print("вы победили!")
                    break
            else:
                while True:
                    x = random.randint(0, 5)
                    y = random.randint(0, 5)
                    try:
                        self.computer_board.shoot(x, y)
                        break
                    except Exception:
                        pass
                    
                if all(ship.is_sunk() for ship in self.player_board.ships):
                    print("компьютер победил!")
                    break
            
            self.player_turn = not self.player_turn

game = Game()
game.play()