import mysql.connector
from mysql.connector import Error
from itemadapter import ItemAdapter

host = 'localhost'
database = 'drug_data'
user = 'root'
port = '3306'
password = 'root'


# def data_readed():
#     try:
#         connection = mysql.connector.connect(
#             host=host,
#             database=database,
#             user=user,
#             port=port,
#             password=password
#         )
#         # sql_query = "SELECT * FROM drug_info where category is null or effect is null or drug_base is null"
#         sql_query = "SELECT * FROM drug_info where category is null"
#         cursor = connection.cursor()
#         cursor.execute(sql_query)
#         record = cursor.fetchall()
#         record_list = list(record)
#         return record_list
#     except Error as e:
#         print("Error reading data from Mysql", e)
#     finally:
#         if (connection.is_connected()):
#             connection.close()
#             cursor.close()
#             print("MySQL connection is closed")
