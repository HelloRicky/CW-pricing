from __future__ import print_function
from bs4 import BeautifulSoup
from math import ceil
from collections import defaultdict
import requests

# init

url = "http://www.chemistwarehouse.com.au"
category_url = '/categories'
pageSize = 120    # view 120 items per page -> ?size=120
cat_dict = defaultdict(str)
product_dict = defaultdict(str) # record all product and its price


def GetSoup(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.content, "html.parser")
    return soup

def UrlQuery(cat_url, page, size = pageSize):
    ### e.g. http://www.chemistwarehouse.com.au/Shop-OnLine/256/Health?size=120&page=1
    return '%s?size=%s&page=%s' % (cat_url, size, page)


def main():
    

    soup = GetSoup(url + category_url)

    table_div = soup.find_all(id="p_lt_ctl06_pageplaceholder_p_lt_ctl00_wCM_AMS_tg_tv")

    table_tree = table_div[0].find_all('table')

    for i in table_tree:
        
        if len(i.find_all('td')) == 3:
            ### use 3 to get filter sub categories
            
            # product categories
            _itemNameClass_ = 'Name'
            _itemUrlClass_ = 'CategoryTreeItem'
            
            itemName = i.find_all(class_=_itemNameClass_)[0].text.strip()
            itemUrl = i.find_all(class_=_itemUrlClass_)[0].find_all('a')[0].get('href')
            #print(itemName, url + itemUrl)
            cat_dict[itemName] = url + itemUrl
    
    """
    for k, v in cat_dict.iteritems():
        print(k)
    """

    cat_url = cat_dict.get('Health')
    
    #cat_url = cat_dict.get('Veterinary')
    #print(UrlQuery(cat_url, 1))
    cat_soup = GetSoup( UrlQuery(cat_url, 1) )


    ### find out potential pages range
    pager = cat_soup.find(class_="Pager")
    if pager:
        #print(pager)
        txt_arr = pager.find("b").text.strip().split()
        tot_page = int(ceil(float(txt_arr[0]) / pageSize))
        
        #print(tot_page)
        for page in range(tot_page + 1)[2:]:
            print page
    else:
        #print("only 1 page")
    

    """
    ### soup out all product detail in each page
    
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
