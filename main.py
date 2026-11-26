import stat
import os
import cv2
import datetime


def write_log(filename, status):
    log_path = r"C:\Lab2_Media\logs\history.txt"
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

    log_entry = f"[{timestamp}] Файл: {filename} | Фильтр: Фильтр Гаусса + Выравнивание гистограммы | Статус: {status}\n"

    try:
        with open(log_path, 'a', encoding='UTF-8') as log_file:
            log_file.write(log_entry)
    except Exception as e:
        print("Ошибка записи:",e)


def main():
    filename = input("Введите имя файла (image1.jpg или image2.jpg): ")

    input_path = rf"C:\Lab2_Media\data\input\{filename}"
    output_path = r"C:\Lab2_Media\data\output\result.jpg"


    try:
        with open(input_path, 'rb') as f:
            pass

        attrs = os.stat(input_path).st_file_attributes
        if attrs & stat.FILE_ATTRIBUTE_READONLY:
            raise PermissionError

    except FileNotFoundError:
        print("Ошибка: Файл не найден")
        write_log(filename, "Файл не найден")
        return
    except PermissionError:
        print(f"Ошибка: Нет прав на чтение файла {filename}. Обратитесь к администратору")
        write_log(filename, "Ошибка доступа")
        return
    except Exception as e:
        print(f"Неизвестная ошибка при доступе к файлу: {e}")
        write_log(filename, "Ошибка доступа")
        return

    img = cv2.imread(input_path)
    if img is None:
        print("Ошибка: Файл найден, но не является изображением или поврежден.")
        write_log(filename, "Ошибка (поврежденный файл)")
        return

    try:
        blurred_img = cv2.GaussianBlur(img, (7,7), 0)

        img_y_cr_cb = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2YCrCb)
        y, cr, cb = cv2.split(img_y_cr_cb)
        y_eq = cv2.equalizeHist(y)
        img_eq = cv2.merge((y_eq, cr, cb))
        result_img = cv2.cvtColor(img_eq, cv2.COLOR_YCrCb2BGR)

        cv2.imwrite(output_path, result_img)
        print(f"Обработанное изображение сохранено в {output_path}")

        write_log(filename, "Успешно")

    except Exception as e:
        print(f"Ошибка во время обработки изображения: {e}")
        write_log(filename, "Ошибка обработки")


if __name__ == "__main__":
    main()