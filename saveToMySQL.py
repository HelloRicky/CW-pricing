from __future__ import print_function
from python_mysql_dbconfig import read_db_config
from dateutil.parser import parse
import csv

import pymysql
#from mysql.connector import MySQLConnection, Error

"""
general function for any input query
return list
"""
def query_fetchone_general(query, args):
    # query_with_fetchone
    result = []
    try:
        dbconfig = read_db_config()
        conn = pymysql.connect(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query, args)
 
        row = cursor.fetchone()
 
        while row is not None:
            #print(row)
            result.append(row)
            row = cursor.fetchone()
 
    except Error as e:
        print(e)
        result = e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        
    return result

"""
general insert function
"""
def query_insert_general(query, args):
     
    try:
        db_config = read_db_config()
        conn = pymysql.connect(**db_config)
 
        cursor = conn.cursor()
        cursor.execute(query, args)
 
        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')
 
        conn.commit()
    except Error as error:
        print(error)
 
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

"""
check if the product exist, if no add it to database
"""
def insert_product(product):

    # fetch selected category
    query = "SELECT * FROM cw_pricing.simple_product where product=%s"
    args = (product)
    result = query_fetchone_general(query, [args])

    
    # return, if the catgory is alreay exist
    if result:
        print(result, "already exist")
        return

    #otherwise insert category
    insert_action = "INSERT INTO cw_pricing.simple_product (product) VALUES (%s)"
    args = (product)
    query_insert_general(insert_action, [args])


"""
return the id value
"""
def get_product_id(product):
    query = "SELECT id FROM cw_pricing.simple_product where product=%s"
    args = (product)
    result = query_fetchone_general(query, [args])

    if not result:
        return 0
    return result[0][0]

"""
check if the product exist, if no add it to database
"""
def insert_price(product, date, price):
    """
    product => string
    price => 123.89
    date => yyyy-mm-dd
    """

    checkId = get_product_id(product)
    if not checkId:
        # if product doesn't exist then insert it
        insert_product(product)
        checkId = get_product_id(product)

    
    # fetch selected category
    query = "SELECT * FROM cw_pricing.price where id=%s and dateStamp=%s"
    args = (checkId, date)
    result = query_fetchone_general(query, args)
    
    # return, if the catgory is alreay exist
    if result:
        print(result, "already exist")
        return

    #otherwise insert category
    insert_action = "INSERT INTO cw_pricing.price (id, dateStamp, price) VALUES (%s, %s, %s)"
    
    query_insert_general(insert_action, (int(checkId), date, price))


"""
convert cost with $ string to float
"""
def stringToFloat(data, replaceSet = [',', '$']):
    for x in replaceSet:
        data = data.replace(x, '')
    return float(data)

def sendToMySql(row):
    product = row[0]
    dateStamp = row[1][:10]
    newDate = parse(dateStamp).strftime("%Y-%m-%d")
    price = row[2]

    if 'Free' == price:
        float_price = 0
    else:
        float_price = stringToFloat(price)
    insert_price(product, newDate, float_price)

if __name__ == '__main__':
    #connect()
    count = 0
    fname = 'today.csv'
    with open(fname) as f:    
        content = csv.reader(f)
        for row in content:
            count += 1
            product = row[0]
            dateStamp = row[1][:10]
            newDate = parse(dateStamp).strftime("%Y-%m-%d")
            price = row[2]
    
            if 'Free' == price:
                float_price = 0
            else:
                float_price = stringToFloat(price)
            insert_price(product, newDate, float_price)
            print('working on:', count)
    print('done')
    #insert_category('Confectionery')
    
