# ImageCompressor-LZ77

## Описание
ImageCompressor-LZ77 - это инструмент для сжатия и распаковки изображений, использующий алгоритм LZ77. Этот проект направлен на уменьшение размера файлов изображений, что делает их хранение и передачу более эффективными, без значительной потери качества. Программа идеально подходит для веб-разработки, архивации данных и обработки мультимедиа.

## Технологический стек
- Python
- NumPy
- Pillow

## Примеры
Ниже приведены примеры изображений до и после сжатия.

## До сжатия и экспорта сжатого файла после
<p>
  <img src="t1.jpg" alt="Light Theme" width="300"/>
  <img src="t1-decoded_image.jpg" alt="Dark Theme" width="300"/>
</p>

## Установка
Чтобы начать работу с ImageCompressor-LZ77, клонируйте репозиторий и установите зависимости:
```bash
git clone https://your-repository-link-here
cd lz77-image-encode-decode
pip install -r requirements.txt
```
Использование
Программа предлагает два режима работы: сжатие и распаковка изображений.

## Сжатие изображений
Чтобы сжать изображение:

```
python script.py compress <path_to_input_image> <path_to_output_file>
```

## Распаковка изображений
Чтобы распаковать изображение:

```
python script.py decompress <path_to_compressed_file> <path_to_output_image>
```
