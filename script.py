import os
from PIL import Image
import numpy as np

# Преобразование изображения в черно-белое
def to_grayscale(img):
    return img.convert('L')

# Шифровка с использованием LZ77
def lz77_encode(data, window_size=20):
    dictionary = []
    buffer = list(map(str, data[:window_size]))
    encoded = []
    i = 0

    while i < len(data):
        match = None
        match_length = 0

        for j in range(max(0, len(dictionary) - window_size), len(dictionary)):
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
            buffer = list(map(str, data[i:i + window_size]))
        else:
            encoded.append((None, None, buffer[0]))
            i += 1
            dictionary.append(buffer[0])
            buffer = list(map(str, data[i:i + window_size]))

    return encoded

# Декодирование данных LZ77
def lz77_decode(encoded_data):
    decoded_data = []

    for entry in encoded_data:
        match_offset, match_length, literal = entry

        if match_offset is not None and match_length is not None:
            for i in range(match_length):
                decoded_data.append(decoded_data[-match_offset + i])

        if literal:
            decoded_data.append(literal)

    return decoded_data

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

    # Определяем исходный размер файла
    original_size = get_file_size(img_path)

    img = to_grayscale(img)
    img_data = np.array(img)
    flat_data = img_data.flatten()
    encoded_data = lz77_encode(flat_data)

    height, width = img_data.shape
    encoded_file = f"{image_name}-encode.txt"
    with open(encoded_file, 'w') as f:
        f.write(f"{height},{width}\n")
        for item in encoded_data:
            f.write(f"{item}\n")

    # Определяем размер файла после шифровки
    encoded_size = get_file_size(encoded_file)

    print(f"Исходный размер изображения: {original_size} байт")
    print(f"Размер зашифрованного файла: {encoded_size} байт")
    print(f"Изображение {image_name} успешно зашифровано и сохранено как {encoded_file}.")

# Расшифровка изображения
def decode_image(file_name):
    if not os.path.exists(file_name):
        print("Файл для расшифровки не найден.")
        return

    encoded_data = []
    with open(f'{file_name}', 'r') as f:
        dimensions = f.readline().strip().split(',')
        height, width = int(dimensions[0]), int(dimensions[1])

        for line in f:
            item = eval(line.strip())
            encoded_data.append(item)

    decoded_data = lz77_decode(encoded_data)
    decoded_array = np.array(list(map(int, decoded_data))).reshape((height, width))

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
