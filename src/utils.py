import logging
import re

from bs4 import BeautifulSoup
from exceptions import ParserFindTagException, PreviewStatusNotFound
from requests import RequestException
from urllib.parse import urljoin

from constants import EXPECTED_STATUS, PEPS_URL


def get_response(session, url):
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы {url}',
            stack_info=True
        )


def find_tag(soup, tag, attrs=None, string=None):
    searched_tag = soup.find(tag, attrs=(attrs or {}), string=string)
    if searched_tag is None:
        error_msg = (f'Не найден тег {tag} {attrs}')
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def mapping_and_counting_statuses(session, table_rows, links_to_pep_pages):
    count_statuses = {
            'Active': 0,
            'Accepted': 0,
            'Deferred': 0,
            'Final': 0,
            'Provisional': 0,
            'Rejected': 0,
            'Superseded': 0,
            'Withdrawn': 0,
            'Draft': 0,
        }

    for row, pep_a_tag in zip(table_rows, links_to_pep_pages):
        preview_status_tag = row.find_all('td')[0]
        preview_status = preview_status_tag.string[1:]

        if preview_status not in EXPECTED_STATUS.keys():
            error_msg = (
                f'Табличный статус PEP "{preview_status}" не опознан, '
                'его сравнение со статусом со страницы PEP невозможно.'
            )
            logging.error(error_msg)
            raise PreviewStatusNotFound(error_msg)

        pep_single_page_href = pep_a_tag['href']
        pep_link = urljoin(PEPS_URL, pep_single_page_href)
        response = get_response(session, pep_link)
        if response is None:
            continue
        single_pep_soup = BeautifulSoup(response.text, features='lxml')
        info_table = find_tag(single_pep_soup, 'dl')

        possible_statuses = re.compile(
            r'^(Active|Accepted|Deferred|Final|Provisional|'
            r'Rejected|Superseded|Withdrawn|Draft)$'
        )

        try:
            status_tag = find_tag(info_table, 'dd', string=possible_statuses)
        except ParserFindTagException:
            left_table_column = info_table.find_all('dt')
            for field in left_table_column:
                if field.text == 'Status:':
                    pre_status_tag = field
                    break
            status_tag = pre_status_tag.find_next_sibling()
        status = status_tag.string

        count_statuses[status] = count_statuses.get(status, 0) + 1

        if status not in EXPECTED_STATUS[preview_status]:
            pep_title = pep_a_tag['title']
            expected_status = EXPECTED_STATUS[preview_status]
            logging.info(f'''
                        Для {pep_title} табличный статус
                        "{preview_status}" не совпадает со статусом
                        "{status}", указанном на странице {pep_link}.
                        Ожидаемый статус: {expected_status}''')
    return count_statuses
