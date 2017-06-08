from __future__ import print_function
from mysql.connector import MySQLConnection, Error
from python_mysql_dbconfig import read_db_config


"""
general function for any input query
return list
"""
def query_fetchone_general(query, args):
    # query_with_fetchone
    result = []
    try:
        dbconfig = read_db_config()
        conn = MySQLConnection(**dbconfig)
        cursor = conn.cursor()
        cursor.execute(query, [args])
 
        row = cursor.fetchone()
 
        while row is not None:
            #print(row)
            result.append(row)
            row = cursor.fetchone()
 
    except Error as e:
        print(e)
        result = e
    finally:
        cursor.close()
        conn.close()
        
    return result

"""
general insert function
"""
def query_insert_general(query, args):
     
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
 
        cursor = conn.cursor()
        cursor.execute(query, [args])
 
        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')
 
        conn.commit()
    except Error as error:
        print(error)
 
    finally:
        cursor.close()
        conn.close()




def insert_category(cat_val):
    query = "INSERT INTO cw_pricing.category (category) VALUES (%s)"
    args = (cat_val)
     
    try:
        db_config = read_db_config()
        conn = MySQLConnection(**db_config)
 
        cursor = conn.cursor()
        cursor.execute(query, [args])
 
        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')
 
        conn.commit()
    except Error as error:
        print(error)
 
    finally:
        cursor.close()
        conn.close()

"""
check if the category exist, if no add it to database
"""
def insert_category(cat_val):

    # fetch selected category
    query = "SELECT * FROM cw_pricing.category where category=%s"
    result = query_fetchone_general(query, (cat_val))

    
    # return, if the catgory is alreay exist
    if result:
        print(result, "already exist")
        return

    #otherwise insert category
    insert_action = "INSERT INTO cw_pricing.category (category) VALUES (%s)"
    query_insert_general(insert_action, (cat_val))

"""
return the id value
"""
def get_category_id(cat_val):
    query = "SELECT id FROM cw_pricing.category where category=%s"
    result = query_fetchone_general(query, (cat_val))

    if not result:
        return 0
    return result[0][0]



if __name__ == '__main__':
    #connect()
    insert_category('Samples')
    #insert_category('Confectionery')
    
