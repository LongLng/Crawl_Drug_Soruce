import mysql.connector
from mysql.connector import Error
import scrapy
from drug.items import DrugItem
from drug._condata import host, database, user, port, password


class MysqlPipeline:
    def __init__(self, db_params):
        self.db_params = db_params
        self.create_connection()
        if self.checkTableExists('drug_info') == False:
            self.create_table()
    def checkTableExists(self, tableName):
        self.cursor.execute(
            """
                    SELECT COUNT(*)
                    FROM information_schema.tables
                    WHERE table_name = '{0}'
                    """.format(tableName.replace('\'', '\'\''))
        )
        if self.cursor.fetchone()[0] == 1:
            return True
        return False

    def create_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS drug_info")
        # self.curr.execute("DROP TABLE IF EXISTS medical_equipment_info")
        self.cursor.execute(
            """ CREATE TABLE drug_info (id INT AUTO_INCREMENT PRIMARY KEY, 
            name VARCHAR(255), 
            source_link VARCHAR(255),
            UNIQUE(name),
            drug_no VARCHAR(255),
            effect VARCHAR(255),
            category VARCHAR(255),
            drug_base VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)""")

    @classmethod
    def from_crawler(cls, crawler):
        db_params = {
            'host': host,
            'user': user,
            'password': password,
            'db': database,
            'port': port,
        }
        return cls(db_params)

    def create_connection(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='root',
            passwd='root',
            database='drug_data'
        )
        self.cursor = self.connection.cursor()
    def open_spider(self, spider):
        self.create_connection()

    def process_item(self, item, spider):
        query = 'select * from drug_info where id = %s'
        param = (item['id'],)
        # params = (
        #     item['id_res'], item['drug_no'], item['effect'], item['category'], item['drug_base'], item['source_link'])
        self.cursor.execute(query, param)
        existing_data = self.cursor.fetchone()
        if existing_data:
            print('thuocbietduoc')
            print(item['id_res'])
            print('Source Link', item['source_link'])
            if not existing_data[4]:
                update_query = "update drug_info set effect=%s where id =%s"
                param = (item['effect'], item['id'])
                self.cursor.execute(update_query, param)
                print('Effect', item['effect'])

            if not existing_data[5]:
                update_query = "update drug_info set category=%s where id =%s"
                param = (item['category'], item['id'])
                self.cursor.execute(update_query, param)
                print('Category', item['category'])

            if not existing_data[6]:
                update_query = "update drug_info set drug_base=%s where id =%s"
                param = (item['drug_base'], item['id'])
                self.cursor.execute(update_query, param)
                print('Drug Base', item['drug_base'])
            # update_query = "update drug_info set effect=%s,category=%s,drug_base = %s, name=%s where id =%s"
            # update_params = (item['effect'], item['category'], item['drug_base'], item['name'], item['id'])
            self.connection.commit()

    def close_spider(self, spider):
        self.cursor.close()
        self.connection.close()
