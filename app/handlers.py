from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from Models.person import *
from app.keyboard import sing_up_kb, in_db_kb


router = Router()

class Reg(StatesGroup):
    waiting_for_login = State()
    waiting_for_password = State()

class EditInfo(StatesGroup):
    editing_login = State()
    waiting_old_password = State()
    editing_password = State()


@router.message(CommandStart())
async def start_message(message: Message):
    query = Person.get_or_none(Person.id == message.from_user.id)
    if query:
        await message.answer('Вы уже зарегистрированы! Спасибо!', reply_markup=in_db_kb)
    else:
        await message.answer('Дарова! Здесь ты можешь протестировать мою БД на peewee', reply_markup=sing_up_kb)


@router.message(F.text == 'Зарегистрироваться')
async def registration(message: Message, state: FSMContext):
    if not Person.get_or_none(Person.id == message.from_user.id):
        await message.answer('Отлично! Введите логин:')
        await state.set_state(Reg.waiting_for_login)
    else:
        await message.answer('Вы уже', reply_markup=in_db_kb)


@router.message(Reg.waiting_for_login)
async def get_login(message: Message, state: FSMContext):
    query = Person.get_or_none(Person.login == message.text)
    if not query:
        await message.answer('Отлично! Теперь введите пароль:')
        await state.update_data(login=message.text)
        await state.set_state(Reg.waiting_for_password)
    else:
        await message.answer('Логин занят. Пожалуйста, введите другой')


@router.message(Reg.waiting_for_password)
async def get_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    Person.create(id=message.from_user.id, login=data["login"], password=data["password"])
    await message.answer(f'Отлично! Регистрация завершена!\n\nВаш логин: {data["login"]}\nВаш пароль: {data["password"]}', reply_markup=in_db_kb)
    await state.clear()


@router.message(F.text == 'Удалить акк')
async def delete_account(message: Message):
    if Person.get_or_none(Person.id == message.from_user.id):
        Person.delete().where(Person.id == message.from_user.id).execute()
        await message.answer('Аккаунт удалён')
    else:
        await message.answer('Вы ещё не зарегистрированы', reply_markup=sing_up_kb)


@router.message(F.text == 'Изменить логин')
async def edit_login(message: Message, state: FSMContext):
    if Person.get_or_none(Person.id == message.from_user.id):
        await message.answer('Введите новый логин:')
        await state.set_state(EditInfo.editing_login)
    else:
        await message.answer('Вы ещё не зарегистрированы', reply_markup=sing_up_kb)


@router.message(EditInfo.editing_login)
async def get_new_login(message: Message, state: FSMContext):
    new_login = message.text
    if not Person.get_or_none(Person.login == new_login):
        Person.update(login=new_login).where(Person.id == message.from_user.id).execute()
        await message.answer('Логин изменён')
        await state.clear()
    else:
        await message.answer('Такой пользователь уже существует. Пожалуйста введите другой логин')


@router.message(F.text == 'Изменить пароль')
async def edit_password(message: Message, state: FSMContext):
    if Person.get_or_none(Person.id == message.from_user.id):
        await message.answer('Для начала введите старый пароль:')
        await state.set_state(EditInfo.waiting_old_password)
    else:
        await message.answer('Вы ещё не зарегистрированы', reply_markup=sing_up_kb)


@router.message(EditInfo.waiting_old_password)
async def get_old_password(message: Message, state: FSMContext):
    data = Person.get_or_none(Person.id == message.from_user.id)
    if data:
        if data.password == message.text:
            await message.answer('Отлично! Теперь введите новый пароль:')
            await state.set_state(EditInfo.editing_password)
        else:
            await message.answer('Пароль неверный. Пожалуйста попробуйте снова')


@router.message(EditInfo.editing_password)
async def get_password(message: Message, state: FSMContext):
    new_password = message.text
    Person.update(password=new_password).where(Person.id == message.from_user.id).execute()
    await message.answer('Пароль изменён')
    await state.clear()


@router.message(F.text == 'Мой профиль')
async def check_profile(message: Message):
    data = Person.get_or_none(Person.id == message.from_user.id)
    if data:
        await message.answer(f'id: {data.id}\n\nЛогин: {data.login}\nПароль: {data.password}')
    else:
        await message.answer('Вы ещё не зарегистрированы', reply_markup=sing_up_kb)

