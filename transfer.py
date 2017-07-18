from mysql_operation import MysqlOpn

mysqlOpn = MysqlOpn('transcribe', 'root', 'root')

mergeDict = mysqlOpn.query_merge_records()
mergeList = mergeDict.keys()
keepFileList = mysqlOpn.check_record_files(mergeDict)
separateList = list(set(mergeList) - set(keepFileList))

mysqlOpn.create_temp_table()
mysqlOpn.concat_max_len(100000)

mysqlOpn.merge_text(mergeList)
mysqlOpn.delete_temp_table()
mysqlOpn.delete_separate_record(separateList)

# Transfer records in keepFileList to scripto


bothList = mysqlOpn.query_both_records()
textList = mysqlOpn.query_text_records()

updateList = list(set(bothList + textList))
mysqlOpn.delete_scripto_record(updateList)
mysqlOpn.transfer_record(updateList)

mysqlOpn.release()
