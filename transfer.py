from mysql_operation import MysqlOpn

mysqlOpn = MysqlOpn('transcribe', 'root', 'root')

# List all records need to be merged
mergeDict = mysqlOpn.query_merge_records()
mergeList = mergeDict.keys()
# List records with same number of rows as number of files
keepFileList = mysqlOpn.check_record_files(mergeDict)
separateList = list(set(mergeList) - set(keepFileList))

mysqlOpn.create_temp_table()
mysqlOpn.concat_max_len(100000)

mysqlOpn.merge_text(mergeList, separateList)
mysqlOpn.delete_temp_table()

# Transfer records in keepFileList to scripto
mysqlOpn.transfer_file_record(keepFileList)

bothList = mysqlOpn.query_both_records()
textList = mysqlOpn.query_text_records()

mysqlOpn.delete_scripto_record(bothList)
updateList = list(set(bothList + textList))
mysqlOpn.transfer_item_record(updateList)


mysqlOpn.release()
