import fitz
import re
from datetime import datetime
import pandas as pd
from dateutil import parser

name = ""
policy_num = ""
effective_date = ""
expiry_date = ""

print(fitz.__doc__)


def pdf_extractor(pdf_path):
    pdf = fitz.open(pdf_path)

    # Total page in the pdf
    num_of_pages = len(pdf)

    # print('The number of pages is ', len(pdf))
    # taking page for further processing

    for num in range(num_of_pages):
        page = pdf[num]

        # get all annotations on a page
        annots = page.annots()

        # looping through annotations
        highlighted_contents = []
        for a in annots:

            # checking the annotation type is 'highlighted'
            if a.type[0] == 8:
                arr = []
                highlighted_coordinates = a.rect
                arr.append(highlighted_coordinates.x0 - 4)
                arr.append(highlighted_coordinates.y0 - 4)
                arr.append(highlighted_coordinates.x1 + 4)
                arr.append(highlighted_coordinates.y1 + 4)
                text = page.get_textbox(arr)
                # get text from rectangle

                # to remove the unnecessary spaces in the start and the end of the word
                clean_txt = text.strip()
                highlighted_contents.append(clean_txt)

        name_regex = re.compile(r"^([A-Za-z \-]{2,25})+$", re.MULTILINE)
        number_regex = re.compile(r"^[-+]?[0-9]+$")
        date_regex1 = re.compile(r"^\d{4}\/\d{2}\/\d{2}$")

        global name
        name = [s for s in highlighted_contents if name_regex.match(s)][0]
        highlighted_contents.remove(name)

        global policy_num
        policy_num = [s for s in highlighted_contents if number_regex.match(s)][0]
        highlighted_contents.remove(policy_num)

        dates = []
        for i in highlighted_contents:
            if i[-1] == ',':
                if date_regex1.match(i[:-1]):
                    dates.append(i[:-1])

            else:
                date_time = parser.parse(i)
                # print('date time', date_time)
                strdate=str(pd.to_datetime(i))
                formated=strdate.split(' ')[0]
                dates.append(formated.replace('-','/'))

        # print('dates are ', dates)
        date_checker(dates)

        print(f'''
        ----------------------------------------------------------------------------------------
        Sample PDF Output:
    
        Name of Insured: {name}
        Policy Number: {policy_num}
        Effective Date: {effective_date}
        Expiry Date: {expiry_date}
        ----------------------------------------------------------------------------------------
        '''
              )


def date_checker(dates):
    d1 = pd.to_datetime(dates[0])
    d2 = pd.to_datetime(dates[1])

    if d1 < d2:
        global expiry_date
        expiry_date = dates[1]
        global effective_date
        effective_date = dates[0]


pdf_extractor('Resources/pdf_sample_format2.pdf')

if __name__ == '__main__':
    pass