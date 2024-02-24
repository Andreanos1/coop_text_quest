import pygame
import socket
import binascii
import time
#import sys

#ЧАСТЬ ПРО КООП

#функции коопа
def encrypt_hex(data):
    encrypted_data = binascii.hexlify(data.encode('utf-8')).decode('utf-8')
    return encrypted_data

def decrypt_hex(encrypted_data):
    decrypted_data = binascii.unhexlify(encrypted_data).decode('utf-8')
    return decrypted_data


def start_server(data):
    
    HOST = '127.0.0.1'
    PORT = 12345
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    client_socket, client_address = server_socket.accept()
    received_data = client_socket.recv(1024).decode('utf-8')
    sending_data = data + '.' + received_data
    client_socket.send(sending_data.encode('utf-8'))
    return sending_data

def connect_to_server(data):
    
    HOST = '127.0.0.1'
    PORT = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    client_socket.send(data.encode('utf-8'))
    received_data_c = client_socket.recv(1024).decode('utf-8')
    if not received_data_c:
        pass
    else:
        return received_data_c




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
        #self.next_events_option1 = []
        #self.next_events_option2 = []
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
    Event('Ну че, поехали нахуй?!', ["Да", "Хуй на!"], 2, ['3.1.3.1','4.1.4.1','5.1.5.1']),
    Event("Приехали", ["По новой"], 3,['2.1.2.1']),
    Event("Не поехали никуда", ["По новой"], 4, ['2.2.2.2']),
    Event("Определитесь уже!.", ["По новой"], 5,['2.1.2.2','2.2.2.1'])
    # Добавьте другие события с разными вариантами ответов
]


current_event_index = 0
running = True


while running:
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
                try:
                    mouse_pos = pygame.mouse.get_pos()
                    option_hovered = events[current_event_index].is_option_hovered(mouse_pos)
                    #print(str(events[current_event_index].e_id) + '.' + str(option_hovered.b_id))
                    if option_hovered is not None:
                        chosed_option = str(events[current_event_index].e_id) + '.' + str(option_hovered.b_id)

                        if chosed_option == '0.1':
                            player = 'host'
                            current_event_index = 1
                            screen.fill((0, 0, 0))
                            screen.blit(bg_image,(0,0))
                            events[current_event_index].display()
                            pygame.display.flip()
                            answer = start_server('Hi')
                            current_event_index = 2
                        elif chosed_option == '0.2':
                            player = 'guest'
                            answer = connect_to_server('Hi')
                            current_event_index = 2
                        elif player == 'host':
                            answer = start_server(chosed_option)
                            for event in events:
                                if answer in event.conditions:
                                    current_event_index = event.e_id
                                else:
                                    None
                        else:
                            while True:
                                try:
                                    answer = connect_to_server(chosed_option)
                                    break
                                except ConnectionRefusedError:
                                    time.sleep(1)
                            for event in events:
                                if answer in event.conditions:
                                    current_event_index = event.e_id
                                else:
                                    None
                        
                       
                        
                except AttributeError:
                    pass
    screen.fill((0, 0, 0))  # Очищаем экран
    screen.blit(bg_image,(0,0))
    # Отображение текущего события
    events[current_event_index].display()

    pygame.display.flip()

pygame.quit()
#sys.exit()
