# -*- coding: utf-8 -*-
#coding=gbk

#coding=utf-8

#-*- coding: UTF-8 -*

import requests
import json
from bs4 import BeautifulSoup

class EntInfo:
    def __init__(self):
        self.ent_name = ""
        self.introduce = ""
        self.contact_person = ""
        self.products = ""
        self.industry = ""
        self.address = ""
        self.district_no = ""
        self.tele_number = ""
        self.phone_number = ""
        self.official_website = ""
        self.chanpin_shop = ""


    def setValue(self, ent_name, introduce, contact_person, products, industry, address, district_no, tele_number, phone_number, official_website, chanpin_shop):
        self.ent_name = ent_name
        self.introduce = introduce
        self.contact_person = contact_person
        self.products = products
        self.industry = industry
        self.address = address
        self.district_no = district_no
        self.tele_number = tele_number
        self.phone_number = phone_number
        self.official_website = official_website
        self.chanpin_shop = chanpin_shop

def read_detail(url):
    try:
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, features="lxml")
        ent = EntInfo()
        ent.introduce = soup.find('div', id="jieshao").find('div', class_="boxcontent").text
        #print(ent.introduce)
        ent.ent_name = soup.find('div', id="lianxi").find('div', class_="boxcontent").strong.text
        # print(soup.find('div', id="lianxi").find('div', class_="boxcontent").strong.text)
        # print(soup.find('div', id="lianxi").find('div', class_="boxcontent").find_all('li'))
        lianxi = soup.find('div', id="lianxi").find('div', class_="boxcontent").find_all('li')
        # print(lianxi[0].text)
        ent.address = lianxi[0].text
        ent.district_no = lianxi[1].text
        ent.tele_number = lianxi[2].text
        ent.phone_number = lianxi[3].text
        ent.official_website = lianxi[4].text
        ent.chanpin_shop = lianxi[5].text
        # print(soup.find_all('div', class_="box")[1].find('div', class_="boxcontent").find_all('li'))
        industry = soup.find_all('div', class_="box")[1].find('div', class_="boxcontent").find_all('li')
        if len(industry) == 3:
            ent.contact_person = industry[0].text
            ent.products = industry[1].text
            ent.industry = industry[2].text
        elif len(industry) == 2:
            ent.products = industry[0].text
            ent.industry = industry[1].text
        else:
            ent.products = industry[0].text


        # with open("company_list.txt", 'a', encoding='utf-8') as fp:
        #     fp.write(
        #         ent.ent_name.encode("utf8").decode() + ent.contact_person.encode("utf8").decode() + ent.industry.encode(
        #             "utf8").decode() + ent.products.encode("utf8").decode() + ent.introduce.encode("utf8").decode()
        #         + '\n' + ent.address.encode("utf8").decode() + '\n' + ent.district_no.encode(
        #             "utf8").decode() + '\n' + ent.tele_number.encode("utf8").decode() + '\n' + ent.phone_number.encode(
        #             "utf8").decode()
        #         + '\n' + ent.official_website.encode("utf8").decode() + '\n' + ent.chanpin_shop.encode(
        #             "utf8").decode() + '\n')

        outputobj = ent.__dict__
        print(outputobj)
        with open("shipin.json", "a", encoding='utf-8') as f:
            json.dump(outputobj, f, ensure_ascii=False)
            f.write(",")
        return True
    except:
        return False

    # return ent

def read_page(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features="lxml")
    companies = soup.find(class_="box_body border_n_l_r").div.table.tbody.find_all('a')
    for company in companies:
        # print(company)
        child_url = company['href']
        print(child_url)
        if read_detail(child_url) is False:
            print('company '+company.text+' fail, its website is saved!')
            file_error = open("qiye_error", 'a', encoding='utf-8')
            file_error.write(child_url)
            file_error.write('\n')
            file_error.close()
            print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        else:
            print('company '+company.text+' success!')
            print('------------------------------------------------------------------------')


if __name__ == '__main__':
    with open("shipin.json", "a", encoding='utf-8') as f:
        f.write("[")
    url = ''
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, features="lxml")
    urls = soup.
    for link in urls:
        child_url = link['href']
        for i in range(1,28):
            url_i = child_url + '/pn' + str(i)#haishuiyangzhi
            read_page(url_i)
    with open("shipin.json", "a", encoding='utf-8') as f:
        f.write("]")
    # for i in range(1,27):
    #     url_i = 'http://qiye.pe168.com/sort/625/pn' + str(i)
    #     read_page(url_i)


