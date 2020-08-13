import configparser
import os
import tempfile
from flask import send_file

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), "..", "config.ini"))


def getSKP(d):
    if "Oam-Remote-User" in d:
        return str(d["Oam-Remote-User"]).split(",")[0]
    elif "Username" in os.environ:
        return str(os.environ["Username"])
    else:
        return "99999"


def logInfo(start, end, proces):
    return str(end - start) + " zadanie: " + proces + "\n"


def xlsx_to_response(wb, filename="Raport"):
    f = tempfile.TemporaryFile()
    wb.save(f)
    f.seek(0)
    response = send_file(
        f, as_attachment=True, attachment_filename=filename + ".xlsx", add_etags=False
    )
    f.seek(0, os.SEEK_END)
    size = f.tell()
    f.seek(0)
    response.headers.extend(
        {
            "Content-Length": size,
            "Cache-Control": "no-cache, no-store, must-revalidate, public, max-age=0",
            "Pragma": "no-cache",
            "Expires": "0",
            "TestHeader": "ok",
        }
    )
    return response
