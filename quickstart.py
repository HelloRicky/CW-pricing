from __future__ import print_function
from bs4 import BeautifulSoup
from math import ceil
from collections import defaultdict
from datetime import datetime
import json
import requests

# init

home_url = "http://www.chemistwarehouse.com.au"
category_url = '/categories'
pageSize = 120    # view 120 items per page -> ?size=120
cat_dict = defaultdict(str)
product_dict = defaultdict(str) # record all product and its price


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

def ProductLister(cat_url, page = 1):
    #cat_url: full url link of category
    product_details = defaultdict(defaultdict)
    
    cat_soup = GetSoup( UrlQuery(cat_url, page) )
    product_box = cat_soup.find_all(class_="product-list-container")
    product_list = product_box[0].find_all('td')
    
    for i in product_list:
        try:
            temp_name = i.find('a', class_="product-container").get('title').strip()
            temp_url = i.find('a', class_="product-container").get('href').strip()
            temp_price = i.find(class_='Price').text.strip()

            product_details[temp_name]['price'] = temp_price
            product_details[temp_name]['url'] = temp_url
            product_details[temp_name]['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        except:
            pass

    return product_details

def PrintDicts(dict_input):
    for k, v in dict_input.iteritems():
        print(k, v)

def main():

    ###    get all categories
    ###   --------------------------------------
    
    soup = GetSoup(home_url + category_url)

    table_div = soup.find_all(id="p_lt_ctl06_pageplaceholder_p_lt_ctl00_wCM_AMS_tg_tv")
    
    table_tree = table_div[0].find_all('table')
    #print(table_tree[0])
    for table_html in table_tree:
        
        if len(table_html.find_all('td')) == 3:
            ### use 3 to get filter sub categories
            t_name, t_url = FindCategory(table_html)
            
            cat_dict[t_name] = home_url + t_url
    
    """
    
    # loop for each category
    
    for k, v in cat_dict.iteritems():
        print(k)
    """   
    
    ###    get all category
    ###   --------------------------------------

    cat_url = cat_dict.get('Health')
    
    #cat_url = cat_dict.get('Veterinary')
    #print(UrlQuery(cat_url, 1))
    
    


    ### find out potential pages range
    
    cat_soup = GetSoup( UrlQuery(cat_url, 1) )      # check out content of 1st page 
    pager = cat_soup.find(class_="Pager")

    temp_dict = defaultdict(defaultdict)
    
    if pager:
        #print(pager)
        txt_arr = pager.find("b").text.strip().split()
        tot_page = int(ceil(float(txt_arr[0]) / pageSize))
        
        #print(tot_page)
        for page in range(tot_page + 1)[1:]:
            print(page)
            print('-'*40)
            temp_dict = ProductLister(cat_url, page)

            PrintDicts(temp_dict)
    else:
        #print("only 1 page")
        temp_dict = ProductLister(cat_url)
        
        PrintDicts(temp_dict)
    

    """
    ### soup out all product detail in each page
    
    cat_soup = GetSoup( UrlQuery(cat_url, page) )
    product_box = cat_soup.find_all(class_="product-list-container")
    product_list = product_box[0].find_all('td')
    
    for i in product_list:
        temp_name = i.find('a', class_="product-container").get('title').strip()
        temp_url = i.find('a', class_="product-container").get('href').strip()
        temp_price = i.find(class_='Price').text.strip()
        
        print(temp_name, temp_price, temp_url)
    """
        
        

if __name__=="__main__":
    main()
