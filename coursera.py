import requests
from bs4 import BeautifulSoup
import re
from openpyxl import Workbook
from multiprocessing import Pool, cpu_count
from args_parser import ConsoleArgsParser


def get_courses_list():
    data_from_request = requests.get('https://www.coursera.org/sitemap~www~courses.xml')
    parsed_data = BeautifulSoup(data_from_request.content, 'lxml')
    return [links.text for links in parsed_data.urlset.findAll('loc')]


def get_course_info(course_slug):
    data_from_request = requests.get(course_slug)
    parsed_data = BeautifulSoup(data_from_request.content, 'lxml')
    course_name = parsed_data.find('h1', class_=re.compile('display-3-text')).text
    course_language = parsed_data.find('div', class_=re.compile('rc-Language')).content
    course_beginning_date = parsed_data.find('div', class_=re.compile('startdate rc-StartDateString caption-text')).text
    course_length = len(parsed_data.find('div', class_=re.compile('rc-WeekView')))
    course_average_rating = parsed_data.find('div', class_=re.compile('ratings-text bt3-hidden-xs'))
    if course_average_rating:
        course_average_rating = re.findall(r'[0-9.]{3}', course_average_rating.text)[0]
        if not course_average_rating:
            course_average_rating = re.findall(r'[0-9]', course_average_rating.text)[0]
    return course_name, course_language, course_beginning_date, course_length, course_average_rating


def parallel_scraping():
    num_of_parallel_processes = cpu_count() * 2
    pool = Pool(num_of_parallel_processes)
    courses_list = get_courses_list()
    courses_info_list = pool.map(get_course_info, courses_list)
    return courses_info_list


def output_courses_info_to_xlsx(courses_info_tuples, filepath='coursera_courses.xlsx'):
    column_names = ['Course Name', 'Course Language', 'Course beginning date',
                    'Course length in weeks', 'Course rating']
    xls_column_names = ['A', 'B', 'C', 'D', 'E']
    work_book = Workbook()
    work_sheet = work_book.active
    for column_number, column_name in enumerate(column_names):
        work_sheet['{}1'.format(xls_column_names[column_number])] = column_name
    for row_number, row in enumerate(courses_info_tuples):
        work_sheet.append(courses_info_tuples[row_number])
    work_book.save(filepath)


if __name__ == '__main__':
    args_parser = ConsoleArgsParser()
    args = args_parser.parse_args()
    filepath_for_xlsx = args.saving_dist
    if not filepath_for_xlsx:
        courses_info_list = parallel_scraping()
        output_courses_info_to_xlsx(courses_info_list)
        print('File \"coursera_courses.xlsx\" created.')
    else:
        courses_info_list = parallel_scraping()
        output_courses_info_to_xlsx(courses_info_list, filepath_for_xlsx[0].name)
        print('File \"{}\" created.'.format(filepath_for_xlsx[0].name))
