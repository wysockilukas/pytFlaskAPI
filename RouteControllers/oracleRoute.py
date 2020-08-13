import cx_Oracle
import datetime
from openpyxl import Workbook
from flask import request

from helpers.myutils import getSKP, logInfo, config, xlsx_to_response


def getOracleSql(id):
    logTxt = "\n\n****************\n"
    startAll = datetime.datetime.utcnow()

    start = datetime.datetime.utcnow()
    connection = cx_Oracle.connect(
        config["ORACLE"]["USER"],
        config["ORACLE"]["PASSWORD"],
        config["ORACLE"]["HOST"],
        encoding="UTF-8",
    )
    end = datetime.datetime.utcnow()
    logTxt += logInfo(start, end, "connection")

    # connection.outputtypehandler = OutputTypeHandler

    start = datetime.datetime.utcnow()
    cur = connection.cursor()
    cur.execute("select SQL_CMD from SQL_QUERIES where SQL_ID = {0}".format(id))
    c = cur.fetchone()
    strSQL = c[0].read()
    strSQL = strSQL.replace("$SKP", getSKP(request.headers))
    end = datetime.datetime.utcnow()
    logTxt += logInfo(start, end, "maly SQL")

    filter = request.args.get("FILTER")
    if filter:
        for kv in filter.split(","):
            key, value = kv.split(":")
            strSQL = strSQL.replace("$" + key, value)
    filename = request.args.get("FILENAME")

    wb = Workbook()
    ws = wb.active

    columns = []
    start = datetime.datetime.utcnow()
    cur.execute(strSQL)
    end = datetime.datetime.utcnow()
    logTxt += logInfo(start, end, "Duzy SQL")

    for column in cur.description:
        columns.append(column[0])
    ws.append(columns)

    start = datetime.datetime.utcnow()

    # rows = cur.fetchall()
    # for row in rows:
    #     ws.append(row)
    # while True:
    #     row = cur.fetchone()
    #     if row is None:
    #         break
    #     ws.append(row)

    numRows = 100
    while True:
        rows = cur.fetchmany(numRows)
        if not rows:
            break
        for row in rows:
            ws.append(row)
    end = datetime.datetime.utcnow()
    logTxt += logInfo(start, end, "Petla z danymi")

    cur.close()

    start = datetime.datetime.utcnow()
    connection.close()
    end = datetime.datetime.utcnow()
    logTxt += logInfo(start, end, "Zamkniecie connection")

    start = datetime.datetime.utcnow()
    if filename:
        res = xlsx_to_response(wb, filename)
    else:
        res = xlsx_to_response(wb)
    end = datetime.datetime.utcnow()
    logTxt += logInfo(start, end, "Zapis do excela")

    endAll = datetime.datetime.utcnow()
    logTxt += str(endAll - startAll) + " Razem\n*****\n\n"

    f = open("log.txt", "a")
    f.write(logTxt)
    f.close()

    return res
