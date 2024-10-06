import sys
from io import BytesIO

import requests
from PIL import Image
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QApplication, QPushButton


def get_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Response code {response.status_code} not 200")
        return None


def get_character(character_name):
    url = f'https://dragonball-api.com/api/characters?name={character_name}'
    response = get_data(url)
    return response


vegeta = get_character('Goku')
print(vegeta)


class UserInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('DragonBall api')
        self.setGeometry(100, 100, 600, 600)
        self.ui_init()

    def ui_init(self):
        layout = QVBoxLayout()

        self.label_name = QLabel("Enter the character name: ")
        self.input_name = QLineEdit()
        self.search_button = QPushButton("search")
        self.search_button.clicked.connect(self.search_character)

        layout.addWidget(self.label_name)
        layout.addWidget(self.input_name)
        layout.addWidget(self.search_button)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)

        self.character_name_label = QLabel()
        layout.addWidget(self.character_name_label)

        self.setLayout(layout)

    def search_character(self):
        character_name = self.input_name.text().lower()
        try:
            data = requests.get(f'https://dragonball-api.com/api/characters?name={character_name}').json()[0]
            self.show_character(data)  # Llamar a la función para mostrar el Pokémon
        except Exception as e:
            self.character_name_label.setText(f"Error: {str(e)}")
            self.image_label.clear()

    def show_character(self, data):
        character_img_url = data['image']
        if character_img_url:
            response = requests.get(character_img_url)
            character_img = Image.open(BytesIO(response.content))
            character_img = character_img.convert("RGBA")

            character_ui_image = QPixmap()
            character_ui_image.loadFromData(BytesIO(response.content).getvalue())

            self.image_label.setPixmap(character_ui_image.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))

        # Mostrar estadísticas del Pokémon
        nombre = data['name'].capitalize()
        stats_text = f"Name: {nombre} \n Ki: {data['ki']} \n"
        self.character_name_label.setText(stats_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UserInterface()
    window.show()
    sys.exit(app.exec())