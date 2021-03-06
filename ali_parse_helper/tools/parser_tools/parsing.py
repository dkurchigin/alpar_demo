from selenium import webdriver
import json
from datetime import datetime
import time
import logging
from models import session, ParsingResults, ParsingSettings, get_default_settings


logger = logging.getLogger('parser')
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
fh = logging.FileHandler('logs/parser.log', encoding='utf-8')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.setLevel(logging.DEBUG)


def get_goods_parameters_selenium():
    query_time_limit = 'select * from ' \
                       '(select distinct on (tasks.id) tasks.id, tasks.link, tasks.update_time, ' \
                       'results.task_id_id, results.datetime ' \
                       'from mainapp_parsingtasks as tasks ' \
                       'left join mainapp_parsingresults as results ' \
                       'on results.task_id_id = tasks.id order by tasks.id, results.task_id_id, results.datetime desc) ' \
                       'as final_table ' \
                       'where now() - (final_table.update_time * INTERVAL \'1 hour\') ' \
                       '> final_table.datetime or final_table.datetime is Null'
    logger.info('Browser started')
    default_settings = get_default_settings()
    profile = webdriver.FirefoxProfile(default_settings.firefox_profile)
    browser = webdriver.Firefox(profile)

    while True:
        print('Run iteration...')
        logger.info('Run iteration...')
        default_settings.start_iteration_time = datetime.now()
        default_settings.last_ping_time = datetime.now()
        session.commit()

        distinct_tasks = session.execute(query_time_limit)

        for dict_task in distinct_tasks:
            try:
                browser.get(dict_task[1])
                logger.info(f'Try get {dict_task[1]}')
                result_dict = {}

                title = browser.find_element_by_class_name('product-title')
                result_dict['title'] = title.text

                price = browser.find_element_by_class_name('product-price-value')
                result_dict['price'] = price.text

                quantity = browser.find_element_by_class_name('product-quantity-tip')
                result_dict['quantity'] = quantity.text

                rating = browser.find_element_by_class_name('overview-rating-average')
                result_dict['rating'] = rating.text

                reviews = browser.find_element_by_class_name('product-reviewer-reviews')
                result_dict['reviews'] = reviews.text

                solds = browser.find_element_by_class_name('product-reviewer-sold')
                result_dict['solds'] = solds.text

                price_mark = browser.find_element_by_class_name('product-price-mark')
                result_dict['price_mark'] = price_mark.text

                shipping_price = browser.find_element_by_class_name('product-shipping-price')
                result_dict['shipping_price'] = shipping_price.text

                shipping_info = browser.find_element_by_class_name('product-shipping-info')
                result_dict['shipping_info'] = shipping_info.text

                img_ = browser.find_element_by_class_name('magnifier-image')
                result_dict['img_'] = img_.get_attribute('src')

                json_result = json.dumps(result_dict)

                new_result_record = ParsingResults()
                new_result_record.status = 1
                new_result_record.datetime = datetime.now()
                new_result_record.task_id_id = dict_task[0]
                new_result_record.json = json_result

                session.add(new_result_record)
                default_settings.last_ping_time = datetime.now()
                session.commit()
            except Exception as e:
                print(f'Failed parse this {dict_task[1]}\n{e}')
                logger.error(f'Failed parse this {dict_task[1]}\n{e}')

        print('Sleeping time...')
        default_settings.finish_iteration_time = datetime.now()
        session.commit()
        time.sleep(60 * default_settings.sleeping_time)


get_goods_parameters_selenium()
