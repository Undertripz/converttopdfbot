import os
from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types.input_file import FSInputFile
from config_data.config import Config, load_config
from database.database import insert_database
from keyboards.keyboard import html_keyboard
from lexicon.lexicon import LEXICON_RU
from utils.utils import convert_txt_to_pdf, convert_docx_to_pdf, convert_odt_to_pdf, convert_images_to_pdf

config: Config = load_config()
bot = Bot(token=config.tg_bot.token)

class Convert(StatesGroup):
    txt = State()
    odt = State()
    docx = State()
    pics = State()
router = Router()

@router.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer(LEXICON_RU['/start'])
    await message.answer("Выберите действие:", reply_markup=html_keyboard)
    user_id = message.from_user.id
    username = message.from_user.username
    insert_database(user_id, username)

@router.message(F.text == 'TXT в PDF')
async def register_user(message: Message, state: FSMContext):
    await state.set_state(Convert.txt)
    await message.answer('Выгрузите Ваш TXT-файл.')

@router.message(Convert.txt)
async def txt_convert(message: Message, state: FSMContext):
    user_id = message.from_user.id

    document = message.document

    # Проверяем, что файл является текстовым
    if not document.file_name.endswith('.txt'):
        await message.reply("Пожалуйста, отправьте текстовый файл в формате .txt.")
        return

    # Загружаем файл
    file_info = await bot.get_file(document.file_id)
    txt_file_path = f"./temps/{document.file_name}"
    pdf_file_path = f"./temps/{document.file_name}.pdf"

    await bot.download_file(file_info.file_path, txt_file_path)  # Скачиваем текстовый файл

    # Конвертация TXT в PDF (предполагается, что функция convert_txt_to_pdf определена)
    convert_txt_to_pdf(txt_file_path, pdf_file_path)

    # Отправляем PDF пользователю
    document = FSInputFile(pdf_file_path)
    await bot.send_document(user_id, document, caption='Ваш PDF-файл!')

    # Удаляем временные файлы
    os.remove(txt_file_path)
    os.remove(pdf_file_path)
    await state.clear()
    await message.answer("Выберите действие:", reply_markup=html_keyboard)


@router.message(F.text == "Изображение в PDF")
async def register_user(message: Message, state: FSMContext):
    await state.set_state(Convert.pics)
    await message.answer('Выгрузите Ваше фото НЕ СЖИМАЯ его.')
@router.message(Convert.pics)
async def txt_convert(message: Message, state: FSMContext):
    user_id = message.from_user.id

    document = message.document

    # Проверяем, что файл является текстовым
    if not document.file_name.endswith('.png'):
        if not document.file_name.endswith('.jpg'):
            if not document.file_name.endswith('.bmp'):
                await message.reply("Пожалуйста, отправьте одно изображение в формате .png или .jpg или .bmp")
                return

    # Загружаем файл
    file_info = await bot.get_file(document.file_id)
    image_file_path = f"./temps/{document.file_name}"
    pdf_file_path = f"./temps/{document.file_name}.pdf"

    await bot.download_file(file_info.file_path, image_file_path )  # Скачиваем текстовый файл

    # Конвертация изображения в PDF
    convert_images_to_pdf(image_file_path, pdf_file_path)

    # Отправляем PDF пользователю
    document = FSInputFile(pdf_file_path)
    await bot.send_document(user_id, document, caption='Ваш PDF-файл!')

    # Удаляем временные файлы
    os.remove(image_file_path)
    os.remove(pdf_file_path)

    await state.clear()
    await message.answer("Выберите действие:", reply_markup=html_keyboard)

@router.message(F.text == 'ODT в PDF')
async def register_user(message: Message, state: FSMContext):
    await state.set_state(Convert.odt)
    await message.answer('Выгрузите Ваш ODT-файл.')
@router.message(Convert.odt)
async def txt_convert(message: Message, state: FSMContext):
    user_id = message.from_user.id
    document = message.document

    # Проверяем, что файл является ODT
    if not document.file_name.endswith('.odt'):
        await message.reply("Пожалуйста, отправьте документ в формате .odt.")
        return

    # Загружаем файл
    file_info = await bot.get_file(document.file_id)
    odt_file_path = f"./temps/{document.file_name}"
    pdf_file_path = f"./temps/{document.file_name.replace('.odt', '.pdf')}"

    await bot.download_file(file_info.file_path, odt_file_path)  # Скачиваем DOCX файл
    # Конвертация ODT в PDF
    convert_odt_to_pdf(odt_file_path, pdf_file_path)

    # Отправляем PDF пользователю
    document = FSInputFile(pdf_file_path)
    await bot.send_document(user_id, document, caption='Ваш PDF-файл!')
    # Удаляем временные файлы
    os.remove(odt_file_path)
    os.remove(pdf_file_path)

    await state.clear()
    await message.answer("Выберите действие:", reply_markup=html_keyboard)

@router.message(F.text == "DOCX в PDF")
async def register_user(message: Message, state: FSMContext):
    await state.set_state(Convert.docx)
    await message.answer('Выгрузите Ваш DOCX-файл.')
@router.message(Convert.docx)
async def txt_convert(message: Message, state: FSMContext):
    user_id = message.from_user.id
    document = message.document

    # Проверяем, что файл является DOCX
    if not document.file_name.endswith('.docx'):
        await message.reply("Пожалуйста, отправьте документ в формате .docx.")
        return

    # Загружаем файл
    file_info = await bot.get_file(document.file_id)
    docx_file_path = f"./temps/{document.file_name}"
    pdf_file_path = f"./temps/{document.file_name}.pdf"

    await bot.download_file(file_info.file_path, docx_file_path)  # Скачиваем DOCX файл

    # Конвертация DOCX в PDF
    convert_docx_to_pdf(docx_file_path)

    # Отправляем PDF пользователю
    document = FSInputFile(pdf_file_path)
    await bot.send_document(user_id, document, caption='Ваш PDF-файл!')
    # Удаляем временные файлы
    os.remove(docx_file_path)
    os.remove(pdf_file_path)
    await state.clear()
    await message.answer("Выберите действие:", reply_markup=html_keyboard)

# Обработчик команды /help
@router.message(Command(commands=["help"]))
async def start_command(message:Message):
    await message.answer(text=LEXICON_RU['/help'])
