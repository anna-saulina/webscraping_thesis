import json
import time
from random import randint
from collections import deque

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from constants import ALPHABET
from data_analysis import process_data, visualize_data
from services import convert_string_to_set


def scrape_trials():
    url = 'https://clinicaltrials.gov/ct2/results?recrs=e&rslt=With&cond=covid'

    # ### Определяем драйвера браузера для взаимодействия с веб-ресурсами ###

    # Chrome
    service = Service(executable_path=ChromeDriverManager().install())
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # Получаем веб-страницу по определенной ссылке
    driver.get(url)
    html = driver.page_source
    # print(html)

    # Эмулируем поведение пользователя на веб-странице (скроллинг страницы вниз)
    # Задержки до и после скроллинга для гарантированной загрузки всех динамических ресурсов
    time.sleep(randint(3, 4))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(randint(4, 5))  # sleep between loadings

    # Находим все элементы по CSS-селектору содержащие полную информацию
    # получаем объект в виде списка элементов
    # result_table = driver.find_element(By.ID, value='theDataTable')
    trial_list_odd = driver.find_elements(By.CLASS_NAME, value='odd.parent')
    trial_list_even = driver.find_elements(By.CLASS_NAME, value='even.parent')
    trial_list_odd.extend(trial_list_even)
    trial_links = []

    for trial in trial_list_odd:
        link_list = trial.find_elements(By.TAG_NAME, value='a')
        for link in link_list:
            # if link.text:
            #     print(link.text)
            if link.text == 'Has Results':
                trial_links.append(link.get_attribute('href'))

    print(trial_links[0])

    trial_data_list = []

    # Переходим по ссылкам из сформированного списка
    for link in trial_links:

        driver.get(link)
        trial_data = {}

        time.sleep(randint(3, 4))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(randint(3, 5))  # sleep between loadings

        # Информация о клиническом исследовании
        sponsor = driver.find_element(By.ID, value='sponsor')
        print(sponsor.text)
        trial_data['sponsor'] = sponsor.text

        trial_info_table = driver.find_element(By.CLASS_NAME, value='tr-studyInfo')
        trial_info_rows = trial_info_table.find_elements(By.TAG_NAME, value='tr')

        for row in trial_info_rows:
            row_header = row.find_element(By.CLASS_NAME, value='ct-header3').text.strip()
            row_description = row.find_element(By.CLASS_NAME, value='ct-body3').text.strip()

            if row_header == 'Condition':
                condition = row_description
                trial_data['condition'] = condition
                print(condition)

            if row_header == 'Intervention':
                intervention = row_description
                intervention_split = intervention.split(':')
                trial_subject = intervention_split[0].strip()
                trial_data['intervention'] = intervention_split[1].strip()
                trial_data['subject'] = trial_subject
                print(intervention)

            if row_header == 'Enrollment':
                enrollment = row_description
                trial_data['enrollment'] = int(enrollment)
                print(enrollment)

        expanding_blocks = driver.find_elements(By.CLASS_NAME, value='ct-header2')
        # print(len(expanding_blocks))

        trial_data['events'] = {}
        for block in expanding_blocks:
            block.click()
            if driver.find_element(By.ID, value='EXPAND_CONTROL-SERIOUS-row').text.strip() in 'Serious Adverse Events':

                tr_list = driver.find_elements(By.TAG_NAME, value='tr')
                tr_header_list = []
                for tr in tr_list:
                    # print(tr.text)
                    if tr.text.strip() == 'Serious Adverse Events':
                        idx = tr_list.index(tr)
                        tr_header_list = tr_list[idx + 1:idx + 3]

                # Подготавливаем структуру для заголовков таблицы
                header_level_1 = [tag.text for tag in tr_header_list[0].find_elements(By.TAG_NAME, value='td') if
                                  tag.text]
                header_level_2 = [tag.text for tag in tr_header_list[1].find_elements(By.TAG_NAME, value='td') if
                                  tag.text]

                values_magnitude = 0
                for tag in tr_header_list[0].find_elements(By.TAG_NAME, value='td'):
                    if tag.text:
                        # print(tag.text)
                        values_magnitude = int(tag.get_attribute('colspan'))
                        # print(f'Values magnitude: {values_magnitude}')
                        break

                event_list = driver.find_elements(By.CLASS_NAME, value='EXPAND-SERIOUS-row')
                events = {}
                for event in event_list:
                    # print(event)
                    value_list = event.find_elements(By.CLASS_NAME, value='de-dataCellAdEv_numValue')
                    if value_list:
                        label = event.find_element(By.CLASS_NAME, value='de-labelCellAdEv').text.strip()
                        label_splitted = label.split()
                        label_list = []
                        alpha_set = convert_string_to_set(ALPHABET)

                        # Очищаем название нежелательного явления от символьных значений
                        for element in label_splitted:
                            element_set = convert_string_to_set(element)
                            if not element_set.isdisjoint(alpha_set):
                                label_list.append(element)

                        label_final = ' '.join(label_list)

                        # print(f'label: {label}')
                        # for label in label_list:
                        #     print(label.text)

                        events[label_final] = {}
                        values = []

                        header_level_2_container = deque(header_level_2)
                        values_list_container = deque(value_list)

                        for header in header_level_1:
                            events[label_final][header] = {}

                            for i in range(values_magnitude):
                                header_element = header_level_2_container.popleft()

                                # Парсим заголовок показателя
                                header_element_splitted = header_element.split()
                                header_element_list = []
                                header_element_final = None
                                header_element_risk = None

                                for element in header_element_splitted:
                                    if ('#' or '%') not in element.strip():
                                        header_element_list.append(element)
                                    if '%' in element:
                                        header_element_risk = element.strip('()')

                                header_element_final = ' '.join(header_element_list).strip()

                                # Парсим значение показателя
                                value = values_list_container.popleft().text
                                value_splitted = value.split()
                                value_final = None
                                value_risk = None

                                if len(value_splitted) == 1:
                                    value_final = int(value_splitted[0]) or 0
                                else:
                                    for value in value_splitted:
                                        if '%' in value:
                                            value_risk = float(value.strip().strip('()').strip('%'))
                                            # print(value_risk)
                                        else:
                                            value_final = value.strip()

                                if header_element_final:
                                    events[label_final][header].update({header_element_final: value_final})
                                if header_element_risk:
                                    events[label_final][header].update({header_element_risk: value_risk})

                                # print(f'header_element: {header_element}')
                                # print(f'value: {value}')
                                # print(f'events: {events}')

                        for value in value_list:
                            values.append(value.text)

                        # print(values)
                        # events[label]['Affected / at Risk (%)'] = values[0]
                        # events[label]['Events number'] = values[1]

                trial_data['events'].update(events)
                break
            else:
                time.sleep(randint(1, 2))
                continue

        print(trial_data)
        trial_data_list.append(trial_data)

        # break

    # Анализ данных
    # Количество появлений нежелательных явлений в исследованиях
    events_occurances = []
    for trial in trial_data_list:
        events = trial['events'].keys()
        events_occurances.extend(events)

    from collections import Counter
    count_events = Counter(events_occurances)


    # Количество зарегистрированных случаев нежелательных явлений

    # Записываем в JSON-файл словарь
    # Записываем в JSON-файл словарь, содержащий продукт с минимальной ненулевой ценой
    with open('trial_data.json', 'w', encoding='utf-8') as outfile:
        json.dump(trial_data_list, outfile, indent=4, ensure_ascii=False)

    return trial_data_list


if __name__ == '__main__':
    # result = scrape_trials()
    # print(result)
    trial_data = scrape_trials()
    processed_data = process_data(trial_data)
    visualize_data(processed_data)
