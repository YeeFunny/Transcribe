from mysql_operation import MysqlOpn

mysqlOpn = MysqlOpn('transcribe', 'root', 'root')

mergeList = mysqlOpn.query_merge_records()

mysqlOpn.create_temp_table()
mysqlOpn.concat_max_len(100000)

mysqlOpn.merge_text(mergeList)
mysqlOpn.delete_temp_table()

bothList = mysqlOpn.query_both_records()
textList = mysqlOpn.query_text_records()

updateList = list(set(bothList + textList))
mysqlOpn.delete_scripto_record(updateList)
mysqlOpn.transfer_record(updateList)


