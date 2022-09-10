from http.client import responses
from bs4 import BeautifulSoup
from scraper_api import ScraperAPIClient
import re
import os
from dotenv import load_dotenv
load_dotenv()



Client = ScraperAPIClient(os.environ.get('API_KEY'))
url = 'https://www.emu.edu.tr/en/programs/software-engineering-undergraduate-program/896?tab=curriculum'




def get_value_of(element):
    return element.next_sibling.strip()[0]


class Title:

    def __init__(self, element):
        self.string = self.__convert_to_string(element)
    
    def __convert_to_string(self, element):
        if element.string:
            return element.string

        a = element.find('a')
        return a.string + a.next_sibling
      

    def get_name(self):
        return self.string[0: self.string.index('(')].strip()

    def get_code(self):
        return self.string[self.string.index('(')+1:self.string.index(')')].strip()




def main():


    html_text = Client.get(url = url).text
    soup = BeautifulSoup(html_text,"lxml")
    body = soup.find('body')

    for course in body.find_all('div', class_='cur_course'):
    
        divs = course.find_all('div')

        h3 = divs[0].find('h3')
        title = Title(h3)
        description = ''

        if len(divs) > 2:
            description = divs[2].string

        strongs = divs[1].find_all('strong')

        credits = get_value_of(strongs[0])
        hours = get_value_of(strongs[1])
        lab = get_value_of(strongs[2])
        tutorial = get_value_of(strongs[3])
        ects = get_value_of(strongs[4])

        course_DATA = {
            'name': title.get_name(),
            'code': title.get_code(),
            # 'details':{
            #     'credits': credits,
            #     'hours': hours,
            #     'lab': lab,
            #     'tutorial': tutorial,
            #     'ECTS':ects
            #},
            #'description': description.strip()
        }

        
        print(course_DATA)
        print('\n ------------- \n')



main()