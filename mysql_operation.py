from mysql_connection import MysqlConn


class MysqlOpn:

    def __init__(self, database, user, password):
        self.__mysqlConn = MysqlConn(database, user, password)
        self.__cursor = self.__mysqlConn.cursor()

    def create_temp_table(self):
        # Create a temporary table
        self.__cursor.execute("""create temporary table if not exists temp_table (
              `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
              `record_id` int(10) unsigned NOT NULL,
              `record_type` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
              `element_id` int(10) unsigned NOT NULL,
              `html` tinyint(1) NOT NULL,
              `text` mediumtext COLLATE utf8_unicode_ci NOT NULL,
              PRIMARY KEY (`id`), KEY `element_id` (`element_id`), KEY `record_type_record_id` (`record_type`,`record_id`),
              KEY `text` (`text`(20))
              ) ENGINE=InnoDB AUTO_INCREMENT=207205 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;""")
        self.__mysqlConn.commit()

    def delete_temp_table(self):
        # Delete the temporary table
        self.__cursor.execute("drop table temp_table;")
        self.__mysqlConn.commit()

    def query_ongoing_records(self):
        # List all ongoing transcribed recordId
        ongoing = []
        self.__cursor.execute("""select distinct(record_id) from element_texts where element_id in ('1', '86') and record_type = 'Item' and text like '%transcription%'
            union select distinct(record_id) from element_texts where element_id in ('1', '86') and record_type = 'Item' and text like '%transcribe%';""")
        for recordId in self.__cursor.fetchall():
            if recordId[0] != 1193:
                ongoing.append(recordId[0])
        ongoing.append(1252)
        return ongoing

    def query_merge_records(self):
        # List all records need to be merged
        merge = []
        self.__cursor.execute("select record_id, count(*) from element_texts where element_id = '1' and record_type = 'Item' group by record_id;")
        for recordId, entryNum in self.__cursor.fetchall():
            if entryNum > 1:
                merge.append(recordId)
        return merge

    def query_both_records(self):
        # List all recordId with both text and Scripto entries and text entries is longer
        self.__cursor.execute(
            """select distinct(t1.record_id) from element_texts t1 join element_texts t2 on t1.record_id = t2.record_id
            where t1.element_id = '1' and t2.element_id = '86' and char_length(t1.text) > char_length(t2.text)
            and t1.record_id in (select distinct(record_id) from element_texts where element_id = '86' and record_type = 'Item'
            and record_id in (select record_id from element_texts where element_id = '1' and record_type = 'Item'));"""
        )
        both = [item[0] for item in self.__cursor.fetchall()]
        return both

    def query_text_records(self):
        # List all finished recordId with only text field entries
        self.__cursor.execute("""select distinct(record_id) from element_texts where element_id = '1' and record_type = 'Item' and record_id not in
            (select distinct(record_id) from element_texts where element_id = '86' and record_type = 'Item');""")
        text = [item[0] for item in self.__cursor.fetchall()]
        return text

    def records_need_transfer(self, records):
        transfer = []
        for recordId in records:
            self.__cursor.execute("select text from element_texts where element_id = '1' and record_type = 'Item' and record_id = {};".format(recordId))
            text = self.__cursor.fetchone()
            if len(text[0]) >= 500:
                transfer.append(recordId)
        return transfer

    def transfer_record(self, records):
        for recordId in records:
            self.__cursor.execute("update element_texts set element_id = '86' where record_id = {} and record_type = 'Item' and element_id = '1';".format(recordId))
        self.__mysqlConn.commit()

    def delete_scripto_record(self, records):
        for recordId in records:
            self.__cursor.execute("delete from element_texts where element_id = '86' and record_id = {} and record_type = 'Item';".format(recordId))
            self.__mysqlConn.commit()

    def merge_text(self, record_id_list):
        # Merge entries
        for recordId in record_id_list:
            self.__cursor.execute(
                """insert into temp_table
                select min(id), record_id, record_type, element_id, max(html), group_concat(text order by id separator ' ') from element_texts
                where record_id = {} and element_id = '1' and record_type = 'Item' group by record_id;""".format(recordId))
            self.__cursor.execute("delete from element_texts where record_id = {} and element_id = '1' and record_type = 'Item';".format(recordId))
        self.__mysqlConn.commit()
        self.__cursor.execute("insert into element_texts select * from temp_table;")
        self.__cursor.execute("truncate temp_table;")
        self.__mysqlConn.commit()

    def concat_max_len(self, max_len):
        # Set group concat max length
        self.__cursor.execute("set group_concat_max_len = {};".format(max_len))

    def release(self):
        self.__mysqlConn.close()
