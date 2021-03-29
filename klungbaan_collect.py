import sys
import os
import requests
import codecs
import re
import json
import pyautogui
import argparse
import webbrowser
import pandas as pd
import lib_helper as hp
from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep
from random import randint
from functions.mongodb_func import * 
from datetime import datetime,timedelta

# date = datetime.today().strftime('%Y-%m-%d')
date = datetime(2020,11,30).strftime('%Y-%m-%d')
_set_date = datetime(2020,11,30)

my_db = "GHBHomeProject"
coll_all = "_klungbaan_allaa"
coll_new = "_klungbaan_newaa"
chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
web = "klungbaan"
# base_url = "https://www.klungbaan.com/search-result/page/placeholder_page/?status=sale&state&keyword&type=placeholder_type&bedrooms&garages&min-price&max-price"
base_url = "https://www.klungbaan.com/search-result/page/placeholder_page/?keyword&states%5B0%5D&location%5B0%5D&type%5B0%5D=placeholder_type&bedrooms&bathrooms&min-price&max-price"
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
Headers = {'User-Agent': user_agent}

thai_month = [  'มกราคม',
                'กุมภาพันธ์',
                'มีนาคม',
                'เมษายน',
                'พฤษภาคม',
                'มิถุนายน',
                'กรกฎาคม',
                'สิงหาคม',
                'กันยายน',
                'ตุลาคม',
                'พฤศจิกายน',
                'ธันวาคม']

building_types = {
    "home"        : { "type_id" : 1, "route":"single-house", "start":1, "end":16 },
    "condo"       : { "type_id" : 2, "route":"condo", "start":1, "end":13 },
    "townhouse"   : { "type_id" : 3, "route":"townhome", "start":1, "end":15 }
}

if not os.path.isdir("pages/" + date):
    os.mkdir("pages/" + date) 
path_page_date = "pages/" + date + "/" + web
if not os.path.isdir(path_page_date):
    os.mkdir(path_page_date) 
if not os.path.isdir("links/" + date):
    os.mkdir("links/" + date)  
path_links = "links/" + date + "/" + web
if not os.path.isdir(path_links):
    os.mkdir(path_links) 

def save_list_links(building):
    path_pages = "pages/" + date + "/" + web + f"/{building}"
    if not os.path.isdir(path_pages):
        os.mkdir(path_pages) 
    
    print("---------------------::  " + building + "  ::---------------------")
    start_page = building_types[building]["start"]
    end_page = building_types[building]["end"] + 1
    route = building_types[building]["route"]
    req_url = base_url.replace("placeholder_type",route)
    for i in tqdm(range(start_page, end_page)):
        wait_time = 0.25
        url = req_url.replace("placeholder_page",str(i))
        r = requests.get(url,headers=Headers)
        while r.status_code != 200:
            r = requests.get(url,headers=Headers)
        
        all_links = extract_links(r.text)
        file_links = codecs.open(path_links + f"/links_{building}.txt", "a+", "utf-8")
        for link in all_links:
            file_links.writelines(link+"\n")
        file_links.close()
        sleep(wait_time)

def read_links(building,skip,collect_date,add_data,duplicate_data):
    file_links = codecs.open(path_links + f"/links_{building}.txt", "r", "utf-8")
    all_link = file_links.readlines()
    file_links.close()
    for i in tqdm(range(int(0),len(all_link))):
        if i < int(0) + int(skip):
            continue
        url = all_link[i].strip("\n")
        r = requests.get(url=url, headers=Headers)
        if 'login Form' in r.text:
            webbrowser.get(chrome_path).open(url)
            __ = input()
            with open("cookie_sam.txt") as f:
                cookie = str(f.read()).strip()
                f.close()
        while r.status_code != 200:
            r = requests.get(url,headers=Headers)
        r.encoding = 'utf-8'
        date_check_break,res = extract_data(r.text,url,building_types[building]["type_id"],collect_date)
        if res == "A":
            add_data += 1
        if res == "D":
            duplicate_data += 1
        print (" New add datas :",add_data," Duplicate datas :",duplicate_data)
        if date_check_break:
            break
    return add_data, duplicate_data
        
def extract_data(content,link,type_id,collect_date):

    # 0 ID (int)(-1)                                13 floor (int)(-1)                      26 picture (str)("None")
    # 1 web (str)("None")                           14 room_number (int)(-1)                27 source_id (int)(0)
    # 2 name (str)("None")                          15 sell_type_id (int)(0)                28 link (str)("None")
    # 3 project_name (str)("None")                  16 bedroom (int)(-1)                    29 type_id (int)(0)
    # 4 address (str)("None")                       17 bathroom (int)(-1)                   30 seller_id (int)(0)
    # 5 subdistrict_code (int)(0)                   18 garage (int)(-1)                     31 completion_year (str)("None")   32 year (str)("None")
    # 6 district_code (int)(0)                      19 detail (str)("None")                 33 month (str)("None")
    # 7 prrovince_code (int)(0)                     20 latitude (str)("None")               34 day (str)("None")
    # 8 price (float)(0.0)                          21 longitude (str)("None")              35 post_date (str)("None")
    # 9 range_of_house_price (str)("None")          22 duplicate (int)(0)                   36 update_date (str)("None")
    # 10 area_SQM (house_space) (str)("None")       23 new (int)(0)                         37 date_time (str)("None")
    # 11 area_SQW (house_landspace) (str)("None")   24 cross_web (int)(-1)
    # 12 floor_number (int)(-1)                     25 cross_ref (int)(-1)
    
    try :
        soup = BeautifulSoup(content, "html.parser")
        try:
            house_name = soup.title.text.split(" - ")[0]
        except:
            house_name = "None"
        try:
            house_picture = soup.find("a", {"rel":"gallery-1"}).img['src']
        except:
            house_picture = "None"
        try:
            house_price = float(re.sub('[^0-9.]', '', soup.find("li", {"class": "item-price"}).text.replace("฿","").replace(",","")))
        except:
            house_price = 0.0
        try:
            agency_name = soup.find("li",{"class":"agent-name"}).text
        except:
            agency_name = "None"
        try:
            seller_phone = soup.find("li",{"class":"detail-tel"}).a.text
        except: 
            seller_phone = "None"
        try:
            seller_email = "None"
            data_detail = soup.find_all("li",{"class":"detail-address"})
            for data in data_detail:
                if str(data).find("Email") >= 0:
                    seller_email = data.a.span.text[:-1]
        except:
            seller_email = "None"
        seller_id = hp.get_sellerID(agency_name,seller_phone,seller_email,my_db)
        latitude = "None"
        longitude = "None"
        try:
            _province = soup.find("li",{"class":"detail-state"}).a.text
        except: 
            _province = "None"
        try:
            _district = soup.find("li",{"class":"detail-city"}).a.text.replace("เขต","")
        except:
            _district = "None"
        _subdistrict = "None"
        try:
            house_address = _district + ", " + _province
            house_province, house_district, house_subdistrict = hp.get_locationCODE(_subdistrict + ", " + _district + ", " + _province,my_db)
        except:
            house_address = "None, None, None"
            house_province = 0
            house_district = 0
            house_subdistrict = 0
        try:
            project_name = soup.find("li",{"class":"project_name"}).span.text
            if project_name == "-":
                project_name = "None"
        except:
            project_name = "None"
        
        try:
            floor_number = int(re.sub('[^0-9]', '', soup.find("li",{"class":"amount_floor"}).span.text))
            if floor_number == "-":
                floor_number = -1
        except:
            floor_number = -1
        
        try:
            floor = -1
            building_detail = soup.find_all("li",{"class":"building_name"})
            for _detail in building_detail:
                if str(_detail).find("ชั้นที่เท่าไร:") >= 0:
                    floor = _detail.span.text
            if floor == "-":
                floor = -1
        except:
            floor = -1

        try:
            house_space = str(re.sub('[^0-9.]', '', soup.find("li",{"class":"prop_size"}).span.text))
            if house_space == "-":
                house_space = "None"
        except:
            house_space = "None"

        try:
            house_landspace = str(float(re.sub('[^0-9.]', '', soup.find("li",{"class":"property_area_rai"}).span.text))*4)
            if house_landspace == "-":
                house_landspace = "None"
        except:
            house_landspace = "None"

        try:
            house_bedroom = int(re.sub('[^0-9]', '', soup.find("li",{"class":"bedrooms"}).span.text))
            if house_bedroom == "-":
                house_bedroom = -1
        except:
            house_bedroom = -1

        try:
            house_bathroom = int(re.sub('[^0-9]', '', soup.find("li",{"class":"bathrooms"}).span.text))
            if house_bathroom == "-":
                house_bathroom = -1
        except:
            house_bathroom = -1
        
        try:
            garage = int(re.sub('[^0-9]', '', soup.find("li",{"class":"garage"}).span.text))
            if garage == "-":
                garage = -1
        except:
            garage = -1
        try:
            house_detail = ""
            _detail = soup.find("div",{"id":"property-description-wrap"}).find_all("p")
            for data in _detail:
                house_detail += data.text.replace("<br/>","").replace("<p>","").replace("</p>","") + " "
        except:
            house_detail = "None"
        sell_type_id = 1
        source_id = 12
        house_link = link
        range_of_house_price = hp.get_range_of_price(house_price)
        try:
            _date = soup.find("span",{"class":"small-text grey"}).text
            _date = _date.split("ที่")[1]
            month = str(thai_month.index(_date.split(' ')[1])+1)
            if len(month) == 1:
                month = "0" + month 
            day = str(_date.split(' ')[2].replace(',',''))
            if len(day) == 1:
                day = "0" + day
            year = _date.split(' ')[3]
            post_date = datetime(int(year),int(month),int(day)).strftime('%Y-%m-%d')
            if datetime(int(post_date.split("-")[0]), int(post_date.split("-")[1]), int(post_date.split("-")[2])) > _set_date:
                post_date = date
                day = post_date.split("-")[2]
                month = post_date.split("-")[1]
                year = post_date.split("-")[0]
        except:
            post_date = date
            day = post_date.split("-")[2]
            month = post_date.split("-")[1]
            year = post_date.split("-")[0]

        try:
            if datetime(int(post_date.split("-")[0]), int(post_date.split("-")[1]), int(post_date.split("-")[2]))  <= collect_date:
                return False , "C"
        except:
            pass

        detail = {
                'ID' : int (mongo_count(my_db,coll_new) + 1),
                'web' : str(web),
                'name' : str(house_name),
                'project_name' : str("None"),
                'address' : str(house_address),
                'subdistrict_code' : int(house_subdistrict),
                'district_code' : int(house_district),
                'province_code' : int(house_province),
                'price' : float(house_price),
                'range_of_house_price' : int(range_of_house_price),
                'area_SQM' : str(house_space),
                'area_SQW' : str(house_landspace),
                'floor_number' : int(floor_number),
                'floor' : int(floor),
                'room_number' : -1,
                'bedroom' : int(house_bedroom),
                'bathroom' : int(house_bathroom),
                'garage' : int(garage),
                'latitude' : str(latitude),
                'longitude': str(longitude),
                'detail' : str(house_detail),
                'seller_name' : str(agency_name),
                'seller_tel' : str(seller_phone),
                'seller_email' : str(seller_email),
                'seller_id' : str(seller_id),
                'picture' : str(house_picture),
                'house_link' : str(house_link),
                'type_id' : int(type_id),
                'sell_type_id' : int(sell_type_id),
                'source_id' : int(source_id),
                'duplicate' : 0,
                'new' : 1,
                'cross_web' : -1,
                'cross_ref' : str("None"),
                'completion_year' : str("None"),
                'year' : str(year),
                'month' : str(month),
                'day' : str(day),
                'post_date' : str(post_date),
                'date_time' : str(date),
                'update_date' : str(post_date),
            }
        for key in detail:
            detail[key] = hp.normalize_attribute(detail[key],key)
        insert, detail, t_type = hp.check_duplicate_new(my_db,coll_all,detail,coll_new)
        if insert:
            mongo_insert(my_db,coll_all,detail)
            mongo_insert(my_db,coll_new,detail)
            return False , "A"
        else:
            print("Data duplicate " + str(t_type) + " not insert in " + web + " " + detail['house_link'])
            return False , "D"
    except Exception as error:
        print ("Something wrong !! not insert")
        return False , "S"

def extract_links(content):
    soup = BeautifulSoup(content, "html.parser")
    links = []
    datas = soup.find_all("div",{"class":"d-flex align-items-center h-100"})
    for data in datas:
        try:
            links.append(data.find("div",{"class":"item-header"}).find("a")['href'])
        except:
            continue
    return links

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-cdate', '--cdate', required=True, help='collect date count')
    args = parser.parse_args()
    collect_date = datetime.now() - timedelta(int(args.cdate))
    # collect_date = datetime(2020,4,22) - timedelta(int(args.cdate))
    print (collect_date.strftime('%Y-%m-%d'))
    add_data = 0
    duplicate_data = 0
    _add = []
    _dup = []
    for building in building_types:
        save_list_links(building)
        # _add_data,_duplicate_data = read_links(building,0,collect_date,add_data,duplicate_data)
        # _add.append(_add_data)
        # _dup.append(_duplicate_data)
    print (_add,_dup)
