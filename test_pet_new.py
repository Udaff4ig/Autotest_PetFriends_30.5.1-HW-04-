import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# python -m pytest -v --driver Chrome --driver-path C:\driverchrome\chromedriver.exe test_pet_new.py

@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome()
    # Переходим на страницу авторизации
    driver.get('https://petfriends.skillfactory.ru/login')

    yield driver

    driver.quit()

def test_show_pet_friends(driver):
    '''Проверка карточек питомцев'''

    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('jkjkh@gmail.com')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('555333111')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    # Переход на строницу "Мои питомцы"
    driver.find_element(By.XPATH, '//a[text()= "Мои питомцы"]').click()

    # Устанавливаем неявное ожидание
    driver.implicitly_wait(3)

    # Ищем все карточки питомцев на страницу "Мои питомцы"
    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    # Находим внутри каждой карточки имя, фото, вид и возраст питомца
    for i in range(len(names)):

        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


def test_all_pets_are_present(driver):
    """проверка наличия всех питомцев на странице пользователя"""

    # Устанавливаем явное ожидание
    element = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, 'email')))

    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('udaff4ig@mail.ru')

    element = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, "pass")))
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('555555')

    element = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button[type="submit"]')))
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    element = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a[href="/my_pets"]')))
    # Переход на страницу "Мои питомцы"
    driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()

    # Записываем в переменную "all_pets" количество питомцев из статистики и в "count_pets" все карточки питомцев
    all_pets = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(':')[1]
    count_pets = driver.find_elements(By.XPATH, '//table[@class="table table-hover"]/tbody/tr')

    # Сравниваем численное значение "all_pets" общее количество карточек "count_pets"
    assert int(all_pets) == len(count_pets)


def test_half_of_the_pets_have_photos(driver):
    """ Проверка, что хотя бы у половины питомцев есть фото """

    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('udaff4ig@mail.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('555555')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Переход на страницу "Мои питомцы"
    driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()

    # Сохраняем в переменную all_pets количество питомцев из статистики
    all_pets = driver.find_element(By.XPATH, '//div[@class=".col-sm-4 left"]').text.split('\n')[1].split(':')[1]

    # Сохраняем в переменную images элементы с атрибутом img
    images = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets > table > tbody > tr > th > img')

    # Считаем количество карточек питомцев с фотографией
    count = 0
    for i in range(len(images)):
        if images[i].get_attribute('src') != '':
            count += 1

    # Проверяем что хотя бы половина питомцем имела фотографию
    assert (int(all_pets) // 2) <= count


def test_show_info_my_pets(driver):
    """проверка всех питомцев пользователя на наличие имени, породы и возраста"""

    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('udaff4ig@mail.ru')
    time.sleep(1)
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('555555')
    time.sleep(1)
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    time.sleep(1)
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    time.sleep(1)
    # Переход на страницу "Мои питомцы"
    driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()

    # Сохраняем в переменную all_pets данные о питомцах
    all_pets = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets > table > tbody > tr')

    # Создаем массивы для имени, породы и возраста и проверяем что нет пустых полей
    name = []
    for i in range(len(all_pets)):
        data = all_pets[i].text.replace('\n', '').replace('×', '')
        split_data = data.split(' ')
        name.append(split_data[0])
    for i in range(len(name)):
        assert name[i] != ''

    species = []
    for i in range(len(all_pets)):
        data = all_pets[i].text.replace('\n', '').replace('×', '')
        split_data = data.split(' ')
        species.append(split_data[1])
    for i in range(len(species)):
        assert species[i] != ''

    ages = []
    for i in range(len(all_pets)):
        data = all_pets[i].text.replace('\n', '').replace('×', '')
        split_data = data.split(' ')
        ages.append(split_data[2])
    for i in range(len(ages)):
        assert ages[i] != ''


def test_not_double_name(driver):
    """ Проверка, что у всех питомцев разные имена """

    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('udaff4ig@mail.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('555555')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Переход на страницу "Мои питомцы"
    driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()

    # Сохраняем в переменную all_pets данные о питомцах
    all_pets = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets > table > tbody > tr')

    # Перебираем данные из all_pets, оставляем элементы с текстом (имя, возраст, порода), остальное меняем на
    # пустую строку и разделяем по пробелу. Выбираем первый элемент (имя) и добавляем их в список name
    name = []
    for i in range(len(all_pets)):
        data = all_pets[i].text.replace('\n', '').replace('×', '')
        split_data = data.split(' ')
        name.append(split_data[0])

    # Запускаем цикл проверки имен. Если есть повторение добавляем к счетчику еденицу
    double = 0
    for i in range(len(name)):
        if name.count(name[i]) > 1:
            double += 1

    # Проверяем, что что нет повторений имен (счетчик равен "0")
    assert double == 0

def test_list_not_have_double_pet(driver):
    """ Проверка, что в списке моих питомцев нет повторяющихся питомцев """

 # Вводим email
    driver.find_element(By.ID, 'email').send_keys('udaff4ig@mail.ru')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('555555')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"
    # Переход на страницу "Мои питомцы"
    driver.find_element(By.CSS_SELECTOR, 'a[href="/my_pets"]').click()

    # Сохраняем в переменную all_pets данные о питомцах
    all_pets = driver.find_elements(By.CSS_SELECTOR, '#all_my_pets > table > tbody > tr')

    # Перебираем данные из pet_data, оставляем имя, возраст, и породу остальное меняем на пустую строку
    # и разделяем по пробелу.
    pets_info = []
    for i in range(len(all_pets)):
        data_pet = all_pets[i].text.replace('\n', '').replace('×', '')
        split_data_pet = data_pet.split(' ')
        pets_info.append(split_data_pet)

    # Склеиваем имя, возраст и породу, получившиеся склееные слова добавляем в строку
    # и между ними вставляем пробел
    line = ''
    for i in pets_info:
        line += ''.join(i)
        line += ' '

    # Получаем список из строки line
    list_line = line.split(' ')

    # Превращаем список в множество
    set_list_line = set(list_line)

    # Находим количество элементов списка и множества
    a = len(list_line)
    b = len(set_list_line)

    # Из количества элементов списка вычитаем количество элементов множества
    result = a - b

    # Если количество элементов == 0 значит карточки с одинаковыми данными отсутствуют
    assert result == 0
