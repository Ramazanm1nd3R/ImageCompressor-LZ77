import os
from PIL import Image
import numpy as np
from collections import Counter

# Класс кодировщика LZ77
class LZ77Encoder:
    def __init__(self, window_size=20):
        self.window_size = window_size

    def encode(self, data):
        dictionary = []
        buffer = list(map(str, data[:self.window_size]))
        encoded = []
        i = 0

        while i < len(data):
            match = None
            match_length = 0

            for j in range(max(0, len(dictionary) - self.window_size), len(dictionary)):
                l = 0
                while l < len(buffer) and j + l < len(dictionary) and dictionary[j + l] == buffer[l]:
                    l += 1
                if l > match_length:
                    match_length = l
                    match = j

            if match is not None and match_length > 0:
                encoded.append((match, match_length, buffer[match_length] if match_length < len(buffer) else ''))
                i += match_length + 1
                dictionary.extend(buffer[:match_length + 1])
                buffer = list(map(str, data[i:i + self.window_size]))
            else:
                encoded.append((None, None, buffer[0]))
                i += 1
                dictionary.append(buffer[0])
                buffer = list(map(str, data[i:i + self.window_size]))

        return encoded


# Класс декодировщика LZ77
class LZ77Decoder:
    @staticmethod
    def decode(encoded_data):
        decoded_data = []

        for entry in encoded_data:
            match_offset, match_length, literal = entry

            if match_offset is not None and match_length is not None:
                for i in range(match_length):
                    decoded_data.append(decoded_data[-match_offset + i])

            if literal:
                decoded_data.append(literal)

        return decoded_data


# Функция для преобразования изображения в RGB
def to_rgb(img):
    return img.convert('RGB')


# Функция для вычисления энтропии
def calculate_entropy(data):
    counts = Counter(data)
    total = len(data)
    entropy = -sum((count / total) * np.log2(count / total) for count in counts.values())
    return entropy


# Функция для определения размера файла
def get_file_size(file_path):
    if os.path.exists(file_path):
        return os.path.getsize(file_path)
    return 0


# Шифровка изображения
def encode_image(image_name):
    for ext in ['.png', '.jpg', '.jpeg', '.bmp']:
        if os.path.exists(image_name + ext):
            img_path = image_name + ext
            img = Image.open(img_path)
            break
    else:
        print("Файл не найден.")
        return

    original_size = get_file_size(img_path)

    img = to_rgb(img)
    img_data = np.array(img)
    flat_data = img_data.flatten()

    encoder = LZ77Encoder()
    encoded_data = encoder.encode(flat_data)

    height, width, channels = img_data.shape
    encoded_file = f"{image_name}-encode.txt"
    with open(encoded_file, 'w') as f:
        f.write(f"{height},{width},{channels}\n")
        for item in encoded_data:
            f.write(f"{item}\n")

    encoded_size = get_file_size(encoded_file)

    # Рассчитываем энтропию
    original_entropy = calculate_entropy(flat_data)
    encoded_entropy = calculate_entropy([x[2] for x in encoded_data if x[2] is not None])

    # Рассчитываем коэффициенты
    compression_ratio = original_size / encoded_size
    redundancy = (1 - (encoded_entropy / original_entropy)) * 100

    print(f"Исходный размер изображения: {original_size} байт")
    print(f"Размер зашифрованного файла: {encoded_size} байт")
    print(f"Исходная энтропия: {original_entropy:.4f}")
    print(f"Энтропия закодированных данных: {encoded_entropy:.4f}")
    print(f"Коэффициент сжатия: {compression_ratio:.2f}")
    print(f"Коэффициент избыточности: {redundancy:.2f}%")
    print(f"Изображение {image_name} успешно зашифровано и сохранено как {encoded_file}.")


# Расшифровка изображения
def decode_image(file_name):
    if not os.path.exists(file_name):
        print("Файл для расшифровки не найден.")
        return

    encoded_data = []
    with open(f'{file_name}', 'r') as f:
        dimensions = f.readline().strip().split(',')
        height, width, channels = map(int, dimensions)

        for line in f:
            item = eval(line.strip())
            encoded_data.append(item)

    decoder = LZ77Decoder()
    decoded_data = decoder.decode(encoded_data)
    decoded_array = np.array(list(map(int, decoded_data))).reshape((height, width, channels))

    file_name_split = file_name.split('-')[0]
    decoded_image = Image.fromarray(decoded_array.astype('uint8'))
    decoded_image.save(f'{file_name_split}-decoded_image.jpg')
    print("Декодированное изображение сохранено как decoded_image.jpg.")


# Основная функция
def main():
    print("1. Шифровка изображения")
    print("2. Расшифровка изображения")

    choice = input("Выберите 1 для шифровки или 2 для расшифровки: ").strip()

    if choice == '1':
        image_name = input("Введите название изображения без расширения: ").strip()
        encode_image(image_name)

    elif choice == '2':
        file_name = input("Введите название файла с закодированными данными: ").strip()
        decode_image(file_name)

    else:
        print("Неверная команда. Пожалуйста, введите 1 или 2.")


if __name__ == "__main__":
    main()
