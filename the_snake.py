from random import randrange

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF, 32, vsync=1
)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    Родительский класс для всех игровых объектов.

    Атрибуты:
    position: Позиция объекта на игровом поле.
    body_color: Цвет объекта.

    Методы:
    draw(): Это абстрактный метод, который предназначен для переопределения
            в дочерних классах. Этот метод будет определять,
            как объект будет отрисовываться на экране.
    """

    def __init__(self) -> None:
        """
        Инициализирует базовые атрибуты объекта,
        такие как его позиция и цвет.
        """
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """
        Это абстрактный метод, который предназначен для переопределения
        в дочерних классах.
        """
        pass


class Apple(GameObject):
    """
    Класс, унаследованный от GameObject,
    описывает яблоко и действия с ним.
    """

    def __init__(self) -> None:
        """
        Задаёт цвет яблока и вызывает метод randomize_position,
        чтобы установить начальную позицию яблока.
        """
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """
        Устанавливает случайное положение яблока на игровом поле —
        задаёт атрибуту position новое значение.
        """
        self.position = (
            (randrange(0, SCREEN_WIDTH, GRID_SIZE)),
            (randrange(0, SCREEN_HEIGHT, GRID_SIZE))
        )

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс, унаследованный от GameObject, описывающий змейку и её поведение.

    Атрибуты:
    length: Длина змейки. Изначально змейка имеет длину 1.
    positions: Список, содержащий позиции всех сегментов тела змейки.
               Начальная позиция — центр экрана.

    direction: Направление движения змейки.
               По умолчанию змейка движется вправо.
    next_direction: Следующее направление движения, которое будет применено
                    после обработки нажатия клавиши.
    body_color: Цвет змейки.

    Методы:
    __init__: Инициализирует начальное состояние змейки.
    update_direction: Обновляет направление движения змейкию
    move: Обновляет позицию змейки (координаты каждой секции), добавляя новую
          голову в начало списка positions и удаляя последний элемент, если
          длина змейки не увеличилась.
    draw(): Отрисовывает змейку на экране, затирая след.
    get_head_position: Возвращает позицию головы змейки
                       (первый элемент в списке positions).
    reset: Сбрасывает змейку в начальное состояние после столкновения с собой.
    """

    def __init__(self) -> None:
        """Инициализирует начальное состояние змейки."""
        super().__init__()
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.last = None
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.eaten = False
        self.outscreen = False

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Обновляет позицию змейки (координаты каждой секции), добавляя новую
        голову в начало списка positions и удаляя последний элемент, если длина
        змейки не увеличилась.
        """
        self.get_head_position()
        x, y = self.positions[0]  # текущие координаты головы
        dx, dy = self.direction  # получение координат направления
        new_pos = (x + dx * GRID_SIZE, y + dy * GRID_SIZE)
        # Добавление новой головы в начало списка
        self.positions.insert(0, new_pos)
        # Сохранение последнего сегмента перед его удалением
        self.last = self.positions[-1]
        # Удаление последнего элемента списка - хвоста,
        # если не съела яблоко
        if not self.eaten:
            self.positions.pop()
        else:
            self.eaten = False

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def draw(self):
        """Отрисовывает змейку на экране, затирая след."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def check_eat(self, apple):
        """Проверяет съела ли змейка яблоко."""
        if self.positions[0] == apple.position:
            self.eaten = True
            # Генерация нового яблока в случайном месте
            apple.randomize_position()

    def reset(self):
        """
        Сбрасывает змейку в начальное состояние
        после столкновения с собой.
        """
        if self.positions[0] in self.positions[1:]:
            self.positions.clear()
            self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
            screen.fill(BOARD_BACKGROUND_COLOR)

    def out_screen(self):
        """
        Контролирует выход змейки за пределы поля. При пересечении границы
        змейка выходит с противоположной границы поля.
        """
        x, y = self.positions[0]
        if x == -20:
            self.positions[0] = (x + 660, y)
        elif x == 640:
            self.positions[0] = (x - 660, y)
        elif y == -20:
            self.positions[0] = (x, y + 500)
        elif y == 480:
            self.positions[0] = (x, y - 500)


def handle_keys(game_object):
    """
    Обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """
    Основная функция игры Змейка.

    Инициализирует PyGame, создает экземпляры классов Apple и Snake,
    и управляет основным игровым циклом.
    """
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:

        handle_keys(snake)
        snake.update_direction()
        snake.move()
        snake.draw()
        apple.draw()
        snake.out_screen()
        snake.reset()
        snake.check_eat(apple)
        clock.tick(SPEED)

        pygame.display.update()

        # Тут опишите основную логику игры.
        # ...


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
# for event in pygame.event.get():
#     if event.type == pygame.QUIT:
#         pygame.quit()
#         raise SystemExit
#     elif event.type == pygame.KEYDOWN:
#         if event.key == pygame.K_UP and game_object.direction != DOWN:
#             game_object.next_direction = UP
#         elif event.key == pygame.K_DOWN and game_object.direction != UP:
#             game_object.next_direction = DOWN
#         elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#             game_object.next_direction = LEFT
#         elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#             game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
