from __future__ import print_function
from bs4 import BeautifulSoup
from math import ceil
from collections import defaultdict
import time
import json
import requests
from saveToMySQL import sendToMySql

# init

home_url = "http://www.chemistwarehouse.com.au"
category_url = '/categories'
pageSize = 120    # view 120 items per page -> ?size=120
TODAY = time.strftime('%Y-%m-%d')

def GetSoup(url):
    print(url)
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    return soup

def UrlQuery(cat_url, page, size = pageSize):
    ### e.g. http://www.chemistwarehouse.com.au/Shop-OnLine/256/Health?size=120&page=1
    return '%s?size=%s&page=%s' % (cat_url, size, page)

def FindCategory(content):
    # product categories
    _itemNameClass_ = 'Name'
    _itemUrlClass_ = 'CategoryTreeItem'
    
    itemName = content.find_all(class_=_itemNameClass_)[0].text.strip()
    itemUrl = content.find_all(class_=_itemUrlClass_)[0].find_all('a')[0].get('href')
    #print(itemName, home_url + itemUrl)
    return itemName, itemUrl

def ProductLister(product_details, cat_soup, page = 1):
    #cat_url: full url link of categories

    
    #cat_soup = GetSoup( UrlQuery(cat_url, page) )
    product_box = cat_soup.find_all(class_="product-list-container")
    product_list = product_box[0].find_all('td')
    
    for i in product_list:
        try:
            temp_name = i.find('a', class_="product-container").get('title').strip()
            temp_url = i.find('a', class_="product-container").get('href').strip()
            temp_price = i.find(class_='Price').text.strip()

            #product_details[temp_name] = {'price': temp_price, 'url': temp_url}
            product_details[temp_name] = temp_price


            """
            insert to mysql
            print(temp_name, temp_price)
            """
            sendToMySql([temp_name, TODAY, temp_price])
            
        except:
            pass

    return product_details

def AllProductLister(cat_url):
    
    cat_soup = GetSoup( UrlQuery(cat_url, 1) )      # check out content of 1st page 
    pager = cat_soup.find(class_="Pager")

    temp_dict = defaultdict(str)
    temp_dict = ProductLister(temp_dict, cat_soup)   # get 1st page items
    
    if pager:
        #print(pager)
        print('-'*40)
            
        txt_arr = pager.find("b").text.strip().split()
        tot_page = int(ceil(float(txt_arr[0]) / pageSize))  # get last page number

        print(tot_page)
        for page in range(tot_page + 1)[2:]:
            print(page)
            print('-'*40)
            cat_soup = GetSoup( UrlQuery(cat_url, page) )
            temp_dict = ProductLister(temp_dict, cat_soup, page)

        #PrintDicts(temp_dict)
        print(len(temp_dict))

    return temp_dict

def PrintDicts(dict_input):
    for k, v in dict_input.iteritems():
        print(k, v)


def ExportJsonFile(data, fileName):
    s = json.dumps(data)
    with open(fileName, 'w') as f:
        f.write(s)

def main():

    # init
    exportFileName = './data/CW-pricing_%s.txt' % (time.strftime('%Y%m%d'))

    data_dict = defaultdict(str)
    cat_dict = defaultdict(str)
    #product_dict = defaultdict(str) # record all product and its price

    data_dict['TimeStamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
    
    ###    get all categories
    ###   --------------------------------------

    
    soup = GetSoup(home_url + category_url)

    table_div = soup.find_all(id="p_lt_ctl06_pageplaceholder_p_lt_ctl00_wCM_AMS_tg_tv")

    table_tree = table_div[0].find_all('table')

    for table_html in table_tree:
        
        if len(table_html.find_all('td')) == 3:
            ### use 3 to get filter sub categories
            t_name, t_url = FindCategory(table_html)
            
            cat_dict[t_name] = home_url + t_url
    
    
    ###    loop for each category
    ###   --------------------------------------
          
    products_dict = defaultdict(str)
    for k, v in cat_dict.iteritems():
        try:
            cat_url = cat_dict.get(k)
            products_dict[k] = AllProductLister(cat_url)
        except:
            print("can't get table of", k)

    #data_dict['Categories'] = products_dict

    #ExportJsonFile(data_dict, exportFileName)
      

if __name__=="__main__":
    main()
