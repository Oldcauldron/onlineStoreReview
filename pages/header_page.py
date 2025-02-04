import allure
from selenium.webdriver.common.action_chains import ActionChains as AC
from locators.locs_region_page import RegionPageLocators
from pages.base_page import BasePage
from elements.base_elements import *
from locators.locs_header_page import HeaderPageLocators
from locators.locs_login_page import LoginPageLocators
from locators.locs_profile_page import ProfilePageLocators
from locators.locs_product_page import ProductPageLocators
from utils.data import *
from selenium.webdriver.common.by import By


class HeaderPage(BasePage):

    def __init__(self, browser, url, timeout=10):
        super().__init__(browser, url, timeout)

        # login
        self.login_link = Button(self.browser, "Линк на форму логина", *HeaderPageLocators.LOGIN_LINK)
        self.user_link = Button(self.browser, "Линк на ЛК пользователя", *HeaderPageLocators.USER_LINK)
        self.login_input = Input(self.browser, "Инпут Логин", *LoginPageLocators.LOGIN_INPUT)
        self.password_input = Input(self.browser, "Инпут Пароль", *LoginPageLocators.PASSWORD_INPUT)
        self.main_input = Input(self.browser, "Инпут Поиск в хэдере", *HeaderPageLocators.MAIN_SEARCH_INPUT)
        self.main_search_button = (
            Button(self.browser, "Кнопка Искать", *HeaderPageLocators.SEARCH_BUTTON_IN_MAIN_SEARCH_INPUT))
        self.sign_in_button = Button(self.browser, "Кнопка Войти", *LoginPageLocators.SIGN_IN_BUTTON)
        self.catalogue_button = Button(self.browser, "Кнопка Каталог", *HeaderPageLocators.CATALOGUE_BUTTON)

        # region
        self.choose_region_button = Button(self.browser, "Выбрать регион", *HeaderPageLocators.CHOOSE_REGION_BUTTON)

        # profile
        self.profile_link = Button(self.browser, "Ссылка на профиль юзера", *HeaderPageLocators.USER_LINK)

    def go_to_login_page(self):
        with allure.step("Переход на страницу логина"):
            self.login_link.click()
        self.should_be_login_form()

    def should_be_login_form(self):
        with allure.step("Проверка наличия формы для авторизации"):
            assert self.is_element_visible(*LoginPageLocators.LOGIN_FRAME), "Форма для авторизации не отображается!"

    def user_login(self, login, password):
        with allure.step("Авторизация пользователя"):
            self.login_input.clear_input()
            self.login_input.send_keys_in_input(login)
            self.password_input.clear_input()
            self.password_input.send_keys_in_input(password)
            self.sign_in_button.click()

    def should_be_user_link(self):
        with allure.step("Проверка наличия ссылки на личный кабинет пользователя"):
            assert self.is_element_visible(*HeaderPageLocators.USER_LINK), \
                "Ссылка на личный кабинет пользователя не отображается!"

    def should_be_login_link(self):
        with allure.step("Проверка наличия ссылки на страницу авторизации"):
            self.is_element_visible(*HeaderPageLocators.LOGIN_LINK)

    def open_region_modal(self):
        with allure.step("Открыть модалку выбора региона"):
            self.choose_region_button.click()
        with allure.step("Проверить отображение модалки выбора региона"):
            assert self.is_element_visible(*RegionPageLocators.CHOOSE_REGION_MODAL), \
                'Не отображается модалка выбора региона!'

    def choose_region(self, name):
        with allure.step(f"Выбрать регион: {name}"):
            region = self.search_element_by_text(name)
            region.click()

    def should_be_correct_region_in_header(self, exp_res):
        with (allure.step("Проверка корректности выбранного региона")):
            self.is_element_visible(*HeaderPageLocators.REGION_NAME_IN_HEADER)
            act_res = self.browser.find_element(*HeaderPageLocators.REGION_NAME_IN_HEADER).text
            assert act_res in exp_res, \
                f'В хэдере отображается некорректный регион ОР: {exp_res} ФР: {act_res}'

    def open_catalogue(self):
        with allure.step("Открыть каталог"):
            self.catalogue_button.click()
        with allure.step("Проверить отображение каталога на экране"):
            assert self.is_element_visible(*HeaderPageLocators.CATALOGUE_MODAL), "Не отображается каталог с товарами!"

    def select_product_in_catalogue(self, item, product_name):
        with allure.step(f"Выбрать категорию: {item} и товар: {product_name}"):
            actions = AC(self.browser)
            product_type = self.get_product_type(item)
            actions.move_to_element(product_type).perform()
            product = self.search_element_by_attribute_and_value(HeaderPageLocators.CATALOGUE_SUB_CATEGORY_ATTRIBUTE,
                                                                 product_name)
        with allure.step(f"Клик по линку: {product_name}"):
            product.click()

    def get_product_type(self, item):
        element = None
        items_list = self.browser.find_elements(*HeaderPageLocators.CATALOGUE_LEFT_SIDEBAR_ITEMS)
        for el in items_list:
            if item.lower() == el.text.lower():
                element = el
        return element

    # def check_searching_result(self, exp_res):
    #     with allure.step(f"Проверка результатов поиска товара: {exp_res}"):
    #         product_list = self.browser.find_elements(*ProductsListPageLocators.PRODUCT_TITLE)
    #         for el in product_list:
    #             assert exp_res.lower() in el.text.lower(), (f"Некорректный результат поиска в списке товаров! "
    #                                                         f"Товар: {el.text} не содержит подстроки: {exp_res}")

    def search_product_by_main_search_input(self, data):
        with allure.step("Главная: Поиск товара через инпут поиска в хэдере"):
            self.main_input.send_keys_in_input(data)
            self.main_search_button.click()
