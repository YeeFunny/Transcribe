# -*- coding: utf-8 -*-
from mysql_connection import MysqlConn

myConn = MysqlConn('transcribe', 'root', 'root')
myCur = myConn.cursor()


querySQL = """select id, text from element_texts where element_id in ('1', '86') and record_type = 'Item'
              and record_id not in ('208', '217', '141', '181', '296', '297', '298', '300', '303', '327',
              '328', '329');"""
myCur.execute(querySQL)

for primaryId, text in myCur.fetchall():
    try:
        decodeText = text.encode('cp1252')
    except UnicodeEncodeError:
        decodeText = text.encode('cp1252', 'backslashreplace')
        try:
            decodeText = decodeText.replace('\\x9d', '\x9d').decode('utf8')
        except UnicodeDecodeError:
            print primaryId
    else:
        try:
            decodeText = decodeText.decode('utf8')
        except UnicodeDecodeError:
            decodeText = text
    updateSQL = """update element_texts set text =%s where id = %s;"""
    myCur.execute(updateSQL, (decodeText, primaryId))
    myConn.commit()

myConn.close()
