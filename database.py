import re
#表存在性
def table_exists(con,table_name):
    sql = '''SELECT NAME FROM SYSOBJECTS WHERE TYPE='U'
SELECT * FROM INFORMATION_SCHEMA.TABLES'''
    con.execute(sql)
    tables = con.fetchall()
    table_list = re.findall('(\'.*?\')',str(tables))
    table_list = [re.sub("'",'',each) for each in table_list]
    if table_name in table_list:
        return 1
    else:
        return 0




