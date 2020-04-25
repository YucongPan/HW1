
#Yucong Pan 805434070
#1a:
for $book in doc("books.xml")/catalog/book
order by $book/price
return $book/title

#1b:
for $book in doc("books.xml")/catalog/book
where $book/author="Rajati"
return count($book)

#1c:
for $book in doc("books.xml")/catalog/book
group by $book/author
return {$book/author,count($book)}



# -*- coding: utf-8 -*-

from lxml import etree
import json
import sys


def parse_book_html(html):
    books_list = []
    with open(html, encoding='utf-8') as f:
        text = f.read()
    books_html = etree.HTML(text)
    script_nodes = books_html.xpath('//script')[9]
    info_str = script_nodes.text
    index = info_str.find("works")
    books_info = json.loads(info_str[index+8:-3])

    for book_info in books_info:
        tmp_book = dict.fromkeys(('title', 'price', 'format', 'condition', 'authors'), None)
        tmp_book['title'] = book_info.get('title', None)
        tmp_book['price'] = book_info.get('buyNowPrice', None)
        tmp_book['format'] = book_info.get('media', None)
        tmp_book['condition'] = book_info.get('qualityDescription', None)
        authors = book_info.get('authors')
        authors_name = None
        for author in authors:
            authors_name = author.get('authorName', None)
        tmp_book['authors'] = authors_name
        books_list.append(tmp_book)
    return books_list


def generate_xml(books_list, xml_name):
    f = open(xml_name, 'w')
    f.writelines(['<?xml version="1.0"?>\n', '<books>\n'])
    count = 1
    for book in books_list:
        lines = ['\t<book>\n', '\t\t<id>' + str(count) + '</id>\n']
        for key, value in book.items():
            lines.append('\t\t' + '<' + key + '>' + str(value) + '</' + key + '>\n')
        lines.append('\t</book>\n')
        count += 1
        f.writelines(lines)
    f.write('</books>')
    f.close()


if __name__ == '__main__':
    # html = './ThriftBook1.html'
    html = sys.argv[1]
    xml_name = sys.argv[2]
    books_list = parse_book_html(html)
    generate_xml(books_list, xml_name)

# 2b
#!python3
from lxml import etree
import sys


xmlname = sys.argv[1]
# xmlname = 'FoodServiceData.xml'

xml = etree.parse(xmlname)
result = xml.xpath('/foodservices/foodservice/TypeDescription')
TypeDescriptions = [r.text for r in result]
answer = {}
for td in TypeDescriptions:
    if td in answer.keys():
        answer[td] += 1
    else:
        answer[td] = 1
for td in sorted(answer.keys()):
    print(td+' ',answer[td])


#2c
#!python3
from lxml import etree
import sys


xmlname = sys.argv[1]
# xmlname = 'FoodServiceData.xml'

xml = etree.parse(xmlname)
result = xml.xpath('/foodservices/foodservice/Inspections/Inspection/Grade')
Grades = [r.text for r in result]
answer = {}
for td in Grades:
    if td == None:
        continue
    if td in answer.keys():
        answer[td] += 1
    else:
        answer[td] = 1
for td in sorted(answer.keys()):
    print(td+' ',answer[td])

#  when the grade is missing, we will get None;
# so we compare whether the grade is None or not, and if it's None, we skip it.

#xmlizer
#!python3
from lxml import etree
import pandas as pd
import numpy as np
import sys


filename = sys.argv[1]
xmlname = sys.argv[2]
# filename = 'FoodServiceData.csv'
# xmlname = 'FoodServiceData.xml'
df = pd.read_csv(filename)


# replace the nan with ''
df.replace(np.nan,'',inplace=True)


# bulid up the xml tree
counts = df.InspectionID.groupby(df.EstablishmentID).count()
foodservices = etree.Element("foodservices")
for eid in df.EstablishmentID.drop_duplicates():
    foodservice = etree.SubElement(foodservices,"foodservice")
    foodservice.set('id',str(eid))
    etree.SubElement(foodservice,"EstablishmentName").text = str(df.loc[df.EstablishmentID==eid,'EstablishmentName'].iloc[0])
    etree.SubElement(foodservice,"PlaceName").text = str(df.loc[df.EstablishmentID==eid,'PlaceName'].iloc[0])
    etree.SubElement(foodservice,"Address").text = str(df.loc[df.EstablishmentID==eid,'Address'].iloc[0])
    etree.SubElement(foodservice,"Address2").text = str(df.loc[df.EstablishmentID==eid,'Address'].iloc[0])
    etree.SubElement(foodservice,"City").text = str(df.loc[df.EstablishmentID==eid,'City'].iloc[0])
    etree.SubElement(foodservice,"State").text = str(df.loc[df.EstablishmentID==eid,'State'].iloc[0])
    etree.SubElement(foodservice,"Zip").text = str(df.loc[df.EstablishmentID==eid,'Zip'].iloc[0])
    etree.SubElement(foodservice,"TypeDescription").text = str(df.loc[df.EstablishmentID==eid,'TypeDescription'].iloc[0])
    etree.SubElement(foodservice,"Latitude").text = str(df.loc[df.EstablishmentID==eid,'Latitude'].iloc[0])
    etree.SubElement(foodservice,"Longitude").text = str(df.loc[df.EstablishmentID==eid,'Longitude'].iloc[0])
    Inspections = etree.SubElement(foodservice,"Inspections")
    for i in range(counts[eid]):
        Inspection = etree.SubElement(Inspections,"Inspection")
        Inspection.set('id',str(df.loc[df.EstablishmentID==eid,'InspectionID'].iloc[i]))
        etree.SubElement(Inspection,"InspectionDate").text = str(df.loc[df.EstablishmentID==eid,'InspectionDate'].iloc[i])
        etree.SubElement(Inspection,"Score").text = str(df.loc[df.EstablishmentID==eid,'Score'].iloc[i])
        etree.SubElement(Inspection,"Grade").text = str(df.loc[df.EstablishmentID==eid,'Grade'].iloc[i])
        etree.SubElement(Inspection,"NameSearch").text = str(df.loc[df.EstablishmentID==eid,'NameSearch'].iloc[i])
        etree.SubElement(Inspection,"Intersection").text = str(df.loc[df.EstablishmentID==eid,'Intersection'].iloc[i])
doc = etree.ElementTree(foodservices)
doc.write(xmlname, pretty_print=True,xml_declaration=True,encoding='utf-8')
# waste time less than one minute