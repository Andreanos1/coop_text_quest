import pygame
pygame.init()

# Размеры окна
screen_width = 800
screen_height = 600

# Цвета
white = (255, 255, 255)
black = (0, 0, 0)

# Инициализация шрифта
font = pygame.font.Font(None, 24)

# Создание окна
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Текстовый квест")

# Игровой диалог в виде словаря
dialogue = {
    "start": {
        "text": "Ты находишься перед развилкой. Куда пойдешь?",
        "options": ["Пойти налево", "Пойти направо"]
    },
    "Пойти налево": {
        "text": "Ты увидел старую хижину. Что будешь делать?",
        "options": ["Заглянуть в окно", "Пройти мимо"]
    },
    "Пойти направо": {
        "text": "Ты наткнулся на ядовитую змею. Что будешь делать?",
        "options": ["Попытаться обойти", "Атаковать"]
    },
    "Заглянуть в окно": {
        "text": "Не стоило...",
        "options": []
    },
    "Пройти мимо": {
        "text": "Ну и все, ушел с концами",
        "options": []
    },
    "Попытаться обойти": {
        "text": "Обошел",
        "options": []
    },
    "Атаковать": {
        "text": "Атаковал",
        "options": []
}}

# Функция для отображения диалога
def display_dialog(state):
    current_text = dialogue[state]["text"]
    text_render = font.render(current_text, True, black)
    screen.blit(text_render, (50, 50))

    if "options" in dialogue[state]:
        options = dialogue[state]["options"]
        button_rects = []  # Создаем список для хранения областей кнопок
        for i, option in enumerate(options):
            option_render = font.render(f"{i + 1}. {option}", True, black)
            screen.blit(option_render, (50, 150 + i * 50))
            button_rect = pygame.Rect(50, 150 + i * 50, option_render.get_width(), option_render.get_height())
            button_rects.append(button_rect)

        return button_rects

# Текущее состояние диалога
current_state = "start"
current_button_rects = display_dialog(current_state)

# Основной цикл игры
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, button_rect in enumerate(current_button_rects):
                if button_rect.collidepoint(event.pos):
                    current_state = dialogue[current_state]["options"][i]
                    current_button_rects = display_dialog(current_state)

    # Очистка экрана
    screen.fill(white)

    # Отображение текущего диалога
    current_button_rects = display_dialog(current_state)

    # Обновление экрана
    pygame.display.flip()

# Завершение работы
pygame.quit()
