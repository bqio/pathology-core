from PIL import Image, ImageDraw

PADDING = 30
RGBA_RED = (255, 0, 0, 255)
RGBA_BLACK = (0, 0, 0, 255)
RGBA_LIMIT = (40, 40, 40, 255)
RGBA_TRANSPARENT = (0, 0, 0, 0)
IMAGE_PATH = "C:\\Users\\admin\\Desktop\\eye.jpg"


def main():
    # Открываем изображение
    image = Image.open(IMAGE_PATH)

    # Преобразовываем изображение в формат RGBA
    image = image.convert("RGBA")

    # Определяем рамку с отступом в 30 пикселей
    box = (PADDING, PADDING, image.width - PADDING, image.height - PADDING)

    # Обрезаем изображение по рамке
    image = image.crop(box)

    # Создаем маску для удаления лишнего черного цвета за областью глаза
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, image.size[0], image.size[1]), fill=255)
    image.putalpha(mask)

    # Считаем количество прозрачных пикселей и пикселей с патологией
    transparent_pixel_count = 0
    black_pixel_count = 0
    for i in range(image.height):
        for j in range(image.width):
            pixel = image.getpixel((j, i))
            if pixel == RGBA_TRANSPARENT:
                transparent_pixel_count += 1
            if pixel <= RGBA_LIMIT and pixel != RGBA_TRANSPARENT:
                image.putpixel((j, i), RGBA_RED)
                black_pixel_count += 1

    # Высчитываем процент пикселей с патологией от общего количества пикселей
    total_pixels = (image.height * image.width) - transparent_pixel_count
    percent = round((black_pixel_count / total_pixels) * 100)

    print("Total pathology: {}%".format(percent))
    image.show()


if __name__ == "__main__":
    main()
