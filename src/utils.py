import csv

class CourseTitle:

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


class CourseDetails:

    def __init__(self,elements):
        self.elements = elements
        self.credits = self.__get_value_of(0)
        self.hours = self.__get_value_of(1)
        self.lab = self.__get_value_of(2)
        self.tutorial = self.__get_value_of(3)
        self.ects = self.__get_value_of(4)
    
    def __get_value_of(self, index):
        return self.elements[index].next_sibling.strip()[0]


class CSVManager:

    def __init__(self,data):
        self.data = data

    def write(self, file_name):

        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(self.data)
