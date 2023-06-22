import pymysql
from pprint import pprint
import getpass

def create_cursor(host_name, user_name, pw, db_name):
    try:
        connection = pymysql.connect(host = host_name, user = user_name, password = pw, db = db_name, \
                                    charset = "utf8mb4", cursorclass = pymysql.cursors.Cursor)
        cursor = connection.cursor()
        return cursor
    except Exception as e:
        print(e)
        print(f"Couldn't log in to MySQL server using this password: {pw}.\n")



def query0(cursor, part_num): # DONE
    '''Sample'''
    query = 'SELECT name FROM parts WHERE part_num LIKE %s'
    '''DO NOT CHANGE THE CODE BELOW'''
    cursor.execute(query, (part_num,))
    result = cursor.fetchall()
    return result

def query1(cursor): # DONE
    '''Fill in the query'''
    query = 'select inventory_id, part_num from inventory_parts where color_id=20'
    '''DO NOT CHANGE THE CODE BELOW'''
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def query2(cursor): # DONE
    '''Fill in the query'''
    query = 'select name, num_parts from sets where num_parts between 5000 and 6000'
    '''DO NOT CHANGE THE CODE BELOW'''
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def query3(cursor): # DONE
    '''Fill in the query'''
    query = 'select name from themes where parent_id = 5 order by id desc limit 5'
    '''DO NOT CHANGE THE CODE BELOW'''
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def query4(cursor, color): # DONE
    '''Fill in the query'''
    query = 'select row_id, part_num from inventory_parts where (color_id = %s) and (quantity < 4) order by inventory_id desc limit 10'
    '''DO NOT CHANGE THE CODE BELOW'''
    cursor.execute(query, (color,))
    result = cursor.fetchall()
    return result

def query5(cursor, year): # DONE
    '''Fill in the query'''
    query = 'select year, count(set_num) from sets group by year having (year = %s) or (year > %s) order by year asc'
    '''DO NOT CHANGE THE CODE BELOW'''
    cursor.execute(query, (year,))
    result = cursor.fetchall()
    return result

def query6(cursor): # DONE
    '''Fill in the query'''
    query = 'select inventory_id, sum(quantity) from inventory_parts group by inventory_id order by sum(quantity) desc limit 1'
    '''DO NOT CHANGE THE CODE BELOW'''
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def query7(cursor): # DONE
    '''Fill in the query'''
    query = "select parent_id, count(parent_id) from themes group by parent_id having parent_id like \"4%\" order by count(parent_id) asc"
    '''DO NOT CHANGE THE CODE BELOW'''
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def query8(cursor): # DONE
    '''Fill in the query'''
    query = 'select inventory_id, count(inventory_id) from inventory_sets group by inventory_id having count(inventory_id) > 5 order by count(inventory_id) desc'
    '''DO NOT CHANGE THE CODE BELOW'''
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def query9(cursor): # DONE
    '''Fill in the query'''
    query = 'select id, round(avg(num_parts)) as "mean_num_parts", themes.name from themes join sets on id = theme_id where themes.name != "Disney" group by id order by round(avg(num_parts)) desc limit 10'
    '''DO NOT CHANGE THE CODE BELOW'''
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def query10(cursor):
    '''Fill in the query'''
    query = "select part_num, sum(inventory_parts.quantity) from inventory_parts join colors on color_id = id where rgb like \"A%\" group by part_num having sum(inventory_parts.quantity) % 2 != 0 order by sum(quantity) desc limit 5"
    '''DO NOT CHANGE THE CODE BELOW'''
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def main():

    ######################## Insert MySQL Server password if applicable ########################

    user_password = getpass.getpass('\n# Enter your MySQL Server password: ')
    cursor = create_cursor('localhost', 'root', user_password, 'lego')

    ########################### Test Cases ###########################

    # query0() - cursor.fetchall() output
    print(">>> query0(cursor)")
    pprint(query0(cursor, 10))

    # query1() - cursor.fetchall() output
    print(">>> query1(cursor)")
    # pprint(query1(cursor))

    # query2() - cursor.fetchall() output
    print(">>> query2(cursor)")
    # pprint(query2(cursor))

    # Query 3 - cursor.fetchall() output
    print(">>> query3(cursor)")
    # pprint(query3(cursor))

    # query4() - cursor.fetchall() output
    print(">>> query4(cursor, 72)")
    # pprint(query4(cursor, 72))

    # query5() - cursor.fetchall() output
    print(">>> query5(cursor, 2000)")
    # pprint(query5(cursor, 2000))

    # query6() - cursor.fetchall() output
    print(">>> query6(cursor)")
    # pprint(query6(cursor))

    # query7() - cursor.fetchall() output
    print(">>> query7(cursor)")
    # pprint(query7(cursor))

    # query8() - cursor.fetchall() output
    print(">>> query8(cursor)")
    # pprint(query8(cursor))

    # query9() - cursor.fetchall() output
    print(">>> query9(cursor)")
    # pprint(query9(cursor))

    # query10() - cursor.fetchall() output
    print(">>> query10(cursor)")
    pprint(query10(cursor))

if __name__ == '__main__':
    main()
