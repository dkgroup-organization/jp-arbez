# -*- coding: utf-8 -*-
import csv
import json
import random
import urllib.request


class SoloServiceBase:
    def __init__(self, host='http://jp-arbez.odoo14.local', db='jp-arbez.odoo14.local', user='admin', password='admin'):
        self.HOST = host
        self.DB = db
        self.USER = user
        self.PASS = password
        self.url = '%s/jsonrpc' % self.HOST
        self.session_id = random.randint(0, 1000000000)
        self.uid = self.send_request('common', 'login', self.DB, self.USER, self.PASS)
        print("Server remote: host: {}, db: {}, user: {}".format(self.HOST, self.DB, self.USER))

    def send_request(self, service, method, *args):
        json_structur = {
                'jsonrpc': '2.0',
                'method': 'call',
                'params': {'service': service, 'method': method, 'args': args},
                'id': self.session_id,
        }
        req = urllib.request.Request(url=self.url, data=json.dumps(json_structur).encode(), headers={
            'Content-Type': 'application/json',
        })
        reply = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
        if reply.get('error'):
            raise Exception(reply['error'])
        return reply['result']

    def send_object_request(self, *execute_args):
        return self.send_request('object', 'execute', *execute_args)

    def import_data(self, file_name):
        with open(file_name, newline='') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            self.process_all_csv_row(reader)

    def create(self, model_name, new_value):
        return self.send_object_request(self.DB, self.uid, self.PASS, model_name, 'create', new_value)

    def write(self, rec_ids, model_name, new_value):
        return self.send_object_request(self.DB, self.uid, self.PASS, model_name, 'write', rec_ids, new_value)

    def read(self, rec_ids, model_name):
        return self.send_object_request(self.DB, self.uid, self.PASS, model_name, 'read', rec_ids)

    def search(self, model_name, domain=[]):
        return self.send_object_request(self.DB, self.uid, self.PASS, model_name, 'search', domain)

    def create_or_edit(self, model_name, new_value, domain):
        if not new_value:
            return False
        rec_id = self.search(model_name, domain)
        if rec_id:
            self.write(rec_id, model_name, new_value)
            # print("{} '{}' edited".format(model_name, rec_id))
            print("{} edited: {}".format(model_name, new_value))
        else:
            rec_id = self.create(model_name, new_value)
            # print("{} '{}' created".format(model_name, rec_id))
            print("{} created: {}".format(model_name, new_value))
        return rec_id

    def process_all_csv_row(self, reader):
        """
        Overload this method to process the iterator of all lines
        :param reader: iterator of all lines
        :return: None
        """
        row_index = 2
        for dict_row in reader:
            self.process_csv_row(dict_row)
            print("row no:{} -------------------------".format(row_index))
            row_index += 1

    def process_csv_row(self, dict_row):
        """
        Overload this method to process a row
        :param dict_row: one raw of csv file
        :return: None
        """
        pass

