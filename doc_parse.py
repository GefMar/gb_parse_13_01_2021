import re
import typing
from pathlib import Path
import PyPDF2
from PyPDF2.utils import PdfReadError
from PIL import Image
import pytesseract

IMAGES_PATH = Path(__file__).parent.joinpath('images')
if not IMAGES_PATH.exists():
    IMAGES_PATH.mkdir()


# TODO: Извлечь изображения из PDF
def pdf_image_extract(pdf_path: Path, images_path: Path) -> typing.List[Path]:
    result = []
    with pdf_path.open('rb') as file:
        try:
            pdf_file = PyPDF2.PdfFileReader(file)
        except PdfReadError as e:
            # TODO: Записать в базу что файл битый
            return result
        print(1)
        for idx, page in enumerate(pdf_file.pages):
            file_name = f'{pdf_path.name}.{idx}'
            img_data = page['/Resources']['/XObject']['/Im0']._data
            img_path = images_path.joinpath(file_name)
            img_path.write_bytes(img_data)
            result.append(img_path)
    return result


# TODO: Распознать Номера на Изображении
def get_serial_numbers(img_path: Path) -> typing.List[str]:
    numbers = []
    pattern = re.compile(r'(заводской.*номер)')
    image = Image.open(img_path)
    text_rus = pytesseract.image_to_string(image, 'rus')
    matchs = len(re.findall(pattern, text_rus))
    if not matchs:
        return numbers
    text_eng = pytesseract.image_to_string(image, 'eng').split('\n')
    for idx, line in enumerate(text_rus.split('\n')):
        if re.match(pattern, line):
            numbers.append(text_eng[idx].split()[-1])
        if len(numbers) == matchs:
            break

    return numbers

if __name__ == '__main__':
    pdf_temp = Path(__file__).parent.joinpath('8416_4.pdf')
    images = pdf_image_extract(pdf_temp, IMAGES_PATH)
    numbers = list(map(get_serial_numbers, images))
    print(1)
