from operator import ne
from bs4 import BeautifulSoup
from scraper_api import ScraperAPIClient
import os
from dotenv import load_dotenv
from utils import CourseDetails, CourseTitle, CSVManager
load_dotenv()

Client = ScraperAPIClient(os.environ.get('API_KEY'))

def main():

    url = input('EMU curriculum URL> ')
    file_name = input('File name. NOTE: add .csv> ')
    file_location = input('CSV file location> ')
    html_text = Client.get(url = url).text
    soup = BeautifulSoup(html_text,"lxml")
    body = soup.find('body')
    course_DATA = []

    try:

        for course in body.find_all('div', class_='cur_course'):
        
            divs = course.find_all('div')
            strongs = divs[1].find_all('strong')
            courseDetails = CourseDetails(strongs)
            h3 = divs[0].find('h3')
            title = CourseTitle(h3)
            description = ''

            if len(divs) > 2:
                description = divs[2].string

            course_DATA.append([title.get_name(),title.get_code(),courseDetails.credits,courseDetails.hours,courseDetails.lab,courseDetails.tutorial,courseDetails.ects,description.strip()])

    except:
        return 'URL not valid'
       
    
    csvManager = CSVManager(course_DATA)
    csvManager.write(f'{file_location}/{file_name}')
            


if __name__ == '__main__':
    main()