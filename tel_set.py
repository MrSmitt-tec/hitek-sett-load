import xml.etree.ElementTree as ET
import subprocess
import pyautogui
import selenium 
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main_menu():

    user_pas = 'Password'
    user_fio = create_user.user_fio
    user_tel = create_user.user_tel

    while True:
        print ("Меню:")
        print ("1 - Новый пользователь")
        print ("2 - Создать .xml конфиг")
        print ("3 - Загрузить конфиг в телефон")
        print ("4 - Выход")

        choice = input("Введите номер выбранной опции: ")
        
        if choice == '1':
            create_user()
        elif choice == '2':
            create_file(user_fio_, user_tel_, user_pas)
        elif choice == '3':
            upload_to_tel(user_fio_)
        elif choice == '4':
            print("Программа завершена.")
            break
        else:
            print("Пожалуйста, выберите допустимую опцию.")

class create_user:
    def __init__(self):
        self.user_fio = input("Введите Фамилию И.О.: ")
        self.user_tel = input("Введите номер (короткий): ")

def create_file(user_fio, user_tel, user_pas):

    # Открываем XML-файл
    with open('cfg.xml', 'r') as file:
        lines = file.readlines()

    # Находим необходимую строку по ее тегу

    line_Account1_Label = 385
    line_Account1_SipUserId = 387
    line_Account1_AuthenticateID = 388
    line_Account1_AuthenticatePassword = 389
    line_Account1_DispalyName = 390

    new_line_Account1_Label = f'        <P20000 para="Account1_Label">{user_fio}</P20000>\n'
    new_line_Account1_SipUserId = f'        <P35 para="Account1_SipUserId">{user_tel}</P35>\n'
    new_line_Account1_AuthenticateID = f'        <P36 para="Account1_AuthenticateID">{user_tel}</P36>\n'
    new_line_Account1_AuthenticatePassword = f'        <P34 para="Account1_AuthenticatePassword">{user_pas}</P34>\n'
    new_line_Account1_DispalyName = f'        <P3 para="Account1_DispalyName">{user_fio}</P3>\n'

    lines[line_Account1_Label] = new_line_Account1_Label
    lines[line_Account1_SipUserId] = new_line_Account1_SipUserId
    lines[line_Account1_AuthenticateID] = new_line_Account1_AuthenticateID
    lines[line_Account1_AuthenticatePassword] = new_line_Account1_AuthenticatePassword
    lines[line_Account1_DispalyName] = new_line_Account1_DispalyName

        # Сохраняем изменения в файле
    new_file_name = f'cfg_xml/{user_fio}.xml'

    with open(new_file_name, 'w') as new_file:
        new_file.writelines(lines)

    print(f"Создан файл {user_fio}.xml")

def upload_to_tel(user_fio):

    ip_address = input("Введите IP адрес телефона: ")

    # Получить абсолютный путь до текущего скрипта
    script_path = os.path.abspath(__file__)

    # Получить путь до папки, содержащей текущий скрипт
    script_directory = os.path.dirname(script_path)
    time.sleep(1)

    # Запуск процесса Firefox.exe
    # firefox_process = subprocess.Popen([r'C:\Program Files\Mozilla Firefox\firefox.exe'])
    driver = webdriver.Firefox()
    time.sleep(3)

    # Перейти на нужную веб-страницу
    pyautogui.hotkey('ctrl', 'l')  # Выделить адресную строку
    pyautogui.write(f'http://{ip_address}/configuration.htm')  # Введите адрес вашей веб-страницы
    pyautogui.press('enter')
    time.sleep(0.2)
    pyautogui.write('admin')
    time.sleep(0.2)
    pyautogui.press('tab')  # Переключиться на поле ввода пароля
    pyautogui.write('admin')
    time.sleep(0.2)
    pyautogui.press('enter')  # Нажать Enter для авторизации

    # Взаимодействие с страницей "Управление" аппарата
    # wait = WebDriverWait(driver, 10)
    # element = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "body")))
    
    time.sleep(7)

    # Выбрать файл с конфигурацией
    file_input = driver.find_element(By.XPATH, '//input[@id="restore_xml"]')
    file_input.send_keys(f'{script_directory}\cfg_xml\{user_fio}.xml')
    time.sleep(1)

    submit_button = driver.find_element(By.XPATH, '//input[@id="restorexml"]')
    submit_button.click()  # Нажать на кнопку "Загрузить кофигурацию"

    time.sleep(0.2)
    pyautogui.press('enter')  # Нажать Enter для авторизации

if __name__ == "__main__":
    main_menu()
