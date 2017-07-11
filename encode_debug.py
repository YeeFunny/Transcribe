# -*- coding: utf-8 -*-
from mysql_connection import MysqlConn

myConn = MysqlConn('transcribe', 'root', 'root')
myCur = myConn.cursor()


querySQL = """select id, text from element_texts where element_id = '86' and record_type = 'Item';"""
myCur.execute(querySQL)

for primaryId, text in myCur.fetchall():
    try:
        decodeText = text.encode('cp1252')
    except UnicodeEncodeError:
        decodeText = text.encode('cp1252', 'backslashreplace')
        decodeText = decodeText.replace('\\x9d', '\x9d').decode('utf8')
    else:
        try:
            decodeText = decodeText.decode('utf8')
        except UnicodeDecodeError:
            decodeText = text
    updateSQL = """update element_texts set text =%s where id = %s;"""
    myCur.execute(updateSQL, (decodeText, primaryId))
    myConn.commit()

myConn.close()
