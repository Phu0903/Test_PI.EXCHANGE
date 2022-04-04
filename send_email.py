import json
import csv
from datetime import datetime
import logging
import sys
import unittest

nowTime = datetime.now().strftime('%d %b %Y')

LOG = logging
LOG.basicConfig(level=logging.DEBUG, stream=sys.stdout,
                format='[%(thread)6d - %(asctime)s]: %(name)s - %(levelname)s - %(message)s')
OUTPUT_PATH = 'path/to/outputs_email'
ERRORS_PATH = 'path/to/errors.csv'


def readFileJson(filename):
    try:
        with open(filename, 'r') as f:
            dataTemp = json.load(f)
            return dataTemp
    except Exception as e:
        LOG.error(f'readFileJson {e}')
        return False


def readFileCustomer(filename):
    try:
        rows = []
        with open(filename, 'r') as f:
            customer = csv.reader(f)
            header = next(customer)
            for row in customer:
                rows.append(row)
            return header, rows
    except Exception as e:
        LOG.error(f'readFileJson {e}')
        return False


def writeToFileJson(msgJson, targetEmail):
    try:
        filename = f'{OUTPUT_PATH}/{targetEmail}.json'
        json_object = json.dumps(msgJson, indent=4)
        LOG.info(f'Import file json output {json_object}')
        with open(filename, "w") as outfile:
            outfile.write(json_object)
        return True
    except Exception as e:
        LOG.error(f'writeToFileJson errors {e}')
        return False


def writeToFileCSV(header, datas):
    try:
        with open(ERRORS_PATH, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerow(datas)
        return True
    except Exception as e:
        LOG.error(f'writeToFileCSV {e}')
        return False


class Application(object):
    def __init__(self):
        self.__dataTemplate = None
        self.__msg = dict()
        self.__msg['from'] = None
        self.__msg['to'] = None
        self.__msg['subject '] = None
        self.__msg['mimeType'] = None
        self.__msg['body'] = None
        self.__customersInfo = None
        self.__listHeader = None

    def getData(self, filenameTemp, fileNameCustomer):
        self.__dataTemplate = readFileJson(filenameTemp)
        if self.__dataTemplate is not False:
            self.__msg['from'] = self.__dataTemplate.get('from')
            self.__msg['subject '] = self.__dataTemplate.get('subject')
            self.__msg['mimeType'] = self.__dataTemplate.get('mimeType')
            LOG.info(f'template data {self.__msg}')
        else:
            return False
        customerFile = readFileCustomer(fileNameCustomer)
        if customerFile is not False:
            self.__customersInfo = customerFile[1]
            LOG.info(f'User data {self.__customersInfo}')
            self.__listHeader = customerFile[0]
            LOG.info(f'Header data {self.__listHeader}')
        else:
            return False
        self.__replaceString()
        return True

    def __replaceString(self):
        try:
            i = 0
            while i < len(self.__customersInfo):
                newBody = self.__dataTemplate.get('body')
                j = 0
                while j < len(self.__customersInfo[i]):
                    newBody = newBody.replace("{{" + self.__listHeader[j] + "}}", self.__customersInfo[i][j])
                    newBody = newBody.replace("{{TODAY}}", nowTime)
                    self.__msg['body'] = newBody
                    j += 1
                if self.__customersInfo[i][3] == '':
                    LOG.debug('Customer doesn’t have an email address')
                    if writeToFileCSV(self.__listHeader, self.__customersInfo[i]) is False:
                        LOG.error('Errors write file')
                        return False
                else:
                    self.__msg['to'] = self.__customersInfo[i][3]
                    LOG.info(f'Email {self.__msg}')
                    if writeToFileJson(self.__msg, self.__customersInfo[i][3]) is False:
                        LOG.error('Errors write file')
                        return False
                i += 1
            return True
        except Exception as e:
            LOG.error(f'Replace body or email errors {e}')
            return False


if __name__ == '__main__':
    TEMP_PATH = 'path/to/email_template.json'
    CUSTOMERS_PATH = 'path/to/customers.csv'
    app = Application()
    app.getData(TEMP_PATH,CUSTOMERS_PATH)
