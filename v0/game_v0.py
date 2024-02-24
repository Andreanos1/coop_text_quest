import pygame
#import sys

pygame.init()

# Определение размера экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Текстовый квест")

# Шрифт для текста
font = pygame.font.Font(None, 28)

bg_image = pygame.image.load('images/background.jpg')

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, b_id):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.hovered = False
        self.b_id = b_id + 1

    def update(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.hovered = True
        else:
            self.hovered = False

    def draw(self):
        if self.hovered:
            pygame.draw.rect(screen, (150,100,200), self.rect)
            #pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, (200,100,200), self.rect)
            #pygame.draw.rect(screen, self.color, self.rect)
        draw_text(self.text, 50, self.rect.centery, (0, 0, 0))
        #draw_text(self.text, self.rect.centerx, self.rect.centery, (0, 0, 0))

class Event:
    def __init__(self, text, options, e_id, conditions):
        self.text = text
        self.options = [Button(50, 200 + i * 50, 300, 50, option, (0, 0, 255), (0, 100, 255), i) for i, option in enumerate(options)]
        self.next_events_option1 = []
        self.next_events_option2 = []
        self.e_id = e_id
        self.conditions = conditions

    def display(self):
        draw_text(self.text, 50, 150, (0, 0, 0))
        for option in self.options:
            option.draw()

    def is_option_hovered(self, mouse_pos):
        for option in self.options:
            if option.rect.collidepoint(mouse_pos):
                return option
        return None

def draw_text(text, x, y, color):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Остальной код остается без изменений

events = [
    Event('Меню ебать', ['Создать игру','Подключиться'], 0, []),
    Event('Ждем ебать', [], 1, ['0.1']),
    Event('Ну че, поехали нахуй?!', ["Да", "Хуй на!"], 2, ['3.1','4.1','5.1','0.2']),
    Event("Приехали", ["По новой"], 3,['2.1']),#.2.1']),
    Event("Не поехали никуда", ["По новой"], 4, ['2.2'])]#.2.2']),
    #Event("Определитесь уже!.", ["По новой"], 5,['2.1'])# ['2.1.2.2','2.2.2.1'])
    # Добавьте другие события с разными вариантами ответов
#]

events[0].next_events_option1 = [1]
events[0].next_events_option2 = [2]
events[1].next_events_option1 = [0]
events[1].next_events_option2 = [2]
events[2].next_events_option1 = [3]
events[2].next_events_option2 = [1]
events[3].next_events_option1 = [0]
events[3].next_events_option2 = [0]

current_event_index = 0
running = True


while running:
    try:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:  # Обработка движения мыши
                mouse_pos = pygame.mouse.get_pos()  # Получаем текущие координаты мыши
                for option in events[current_event_index].options:
                    if option.rect.collidepoint(mouse_pos):
                        option.hovered = True  # Кнопка наведена
                    else:
                        option.hovered = False  # Кнопка не наведена
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левая кнопка мыши
                    mouse_pos = pygame.mouse.get_pos()
                    option_hovered = events[current_event_index].is_option_hovered(mouse_pos)
                    print(str(events[current_event_index].e_id) + '.' + str(option_hovered.b_id))
                    if option_hovered is not None:
                        chosed_option = str(events[current_event_index].e_id) + '.' + str(option_hovered.b_id)
                        for event in events:
                            #print(event.text)
                            #print(event.conditions)
                            if chosed_option in event.conditions:
                                current_event_index = event.e_id
                                #print(chosed_option)
                            else:
                                None
                                #print(chosed_option)
                        #if option_hovered == events[current_event_index].options[0]:
                        #    current_event_index = events[current_event_index].next_events_option1[0]
                        #elif option_hovered == events[current_event_index].options[1]:
                        #    current_event_index = events[current_event_index].next_events_option2[0]

        screen.fill((0, 0, 0))  # Очищаем экран
        screen.blit(bg_image,(0,0))
        # Отображение текущего события
        events[current_event_index].display()

        pygame.display.flip()
    except AttributeError:
        pass
pygame.quit()
#sys.exit()
