from docx2pdf import convert
from fpdf import FPDF
import aspose.words as aw
import img2pdf

def convert_txt_to_pdf(txt_file_path, pdf_file_path):
    # Создаем объект FPDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Устанавливаем шрифт
    pdf.set_font("Arial", size=12)

    # Читаем текстовый файл
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Добавляем строку в PDF
            pdf.cell(0, 10, line.encode('latin-1', 'replace').decode('latin-1'), ln=True)

    # Сохраняем PDF файл
    pdf.output(pdf_file_path)

def convert_docx_to_pdf(docx_file_path):
    convert(docx_file_path)


def convert_odt_to_pdf(odt_file_path, pdf_file_path):
    fileNames = [odt_file_path]

    output = aw.Document()
    # Удаляем все содержимое из целевого документа перед добавлением
    output.remove_all_children()

    for fileName in fileNames:
        input = aw.Document(fileName)
        # Добавляем исходный документ в конец документа назначения
        output.append_document(input, aw.ImportFormatMode.KEEP_SOURCE_FORMATTING)

    output.save(pdf_file_path)


def convert_images_to_pdf(image_files_path, pdf_file_path):
        with open(pdf_file_path, "wb") as f:
            f.write(img2pdf.convert(image_files_path))