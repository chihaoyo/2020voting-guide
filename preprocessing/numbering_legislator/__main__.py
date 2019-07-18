import csv
from os import path
from typing import Iterable

import util
from parse_history_legislator import get_legislator_names

SOURCE_FILE_PATH = "../data/organized/legislator_candidate.json"
RESULT_FILE_PATH = "../data/final/legislator_id.csv"
FIELD_NAMES = ["id", "name"]

connection = util.getDbConnection()


def readResult():
    result = []

    if path.exists(RESULT_FILE_PATH):
        with open(RESULT_FILE_PATH, newline="") as f:
            result = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]

    return result


def readOldLegislator():
    with connection.cursor() as cursor:
        sql = "SELECT `name` FROM `legislator_number`"
        cursor.execute(sql)
        res = cursor.fetchall()

    return [row["name"] for row in res]


def writeResultToDb(legislation_list: Iterable[str]):
    print("Totoal", len(legislation_list), "new candidates")
    with connection.cursor() as cursor:
        sql = "INSERT INTO `legislator_number` (`name`) VALUES (%s)"
        cursor.executemany(sql, legislation_list)


if __name__ == "__main__":
    new_legislator_list = get_legislator_names(SOURCE_FILE_PATH)
    old_legislator_list = readOldLegislator()
    add_legislator_list = set(new_legislator_list) - set(old_legislator_list)
    writeResultToDb(add_legislator_list)
    connection.begin()
    connection.close()
