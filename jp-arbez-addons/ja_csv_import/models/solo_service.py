# -*- coding: utf-8 -*-
import csv
import json
import random
import urllib.request


class SoloServiceBase:
    def __init__(self, host='http://jp-arbez.odoo14.local', db='jp-arbez.odoo14.local', user='admin', password='admin'):
        self.row_index = 2
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
        json_dump_value = json.dumps(json_structur).encode()
        req = urllib.request.Request(url=self.url, data=json_dump_value, headers={
            'Content-Type': 'application/json',
        })
        reply = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
        if reply.get('error'):
            print("Error to import line: {}".format(self.row_index))
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

    def search_read(self, model_name, domain=[], fields=None, offset=0, limit=None, order=None):
        return self.send_object_request(self.DB, self.uid, self.PASS, model_name, 'search_read', domain, fields, offset, limit, order)

    def create_or_edit(self, model_name, new_value, domain):
        if not new_value:
            return False
        rec_id = self.search(model_name, domain)
        if rec_id:
            self.write(rec_id, model_name, new_value)
            # print("{} edited: {}".format(model_name, new_value))
        else:
            rec_id = self.create(model_name, new_value)
            # print("{} created: {}".format(model_name, new_value))
        return rec_id

    def create_or_use(self, model_name, new_value, domain):
        if not new_value:
            return False
        rec_id = self.search(model_name, domain)
        if not rec_id:
            # print(domain)
            rec_id = self.create(model_name, new_value)
            # print("{} created: {}".format(model_name, new_value))
        return rec_id

    @staticmethod
    def use_many2one(rec_ids):
        return rec_ids[0] if isinstance(rec_ids, list) else rec_ids

    def atach_many2one(self, dict_value, key, rec_ids):
        if rec_ids:
            dict_value[key] = self.use_many2one(rec_ids)

    @staticmethod
    def affect_col_value(dict_value, field, col_value, affect_null=False):
        if affect_null or col_value:
            dict_value[field] = col_value
        return dict_value

    def process_all_csv_row(self, reader):
        """
        Overload this method to process the iterator of all lines
        :param reader: iterator of all lines
        :return: None
        """
        self.row_index = 2
        for dict_row in reader:
            self.process_csv_row(dict_row)
            # print("row no:{} -------------------------".format(row_index))
            if self.row_index % 100 == 0:
                print("Line: {}".format(self.row_index))
            self.row_index += 1

    def get_source_translate(self, value, translation_key=''):
        source_translate = ''
        domain = [('value', '=ilike', value)]
        if translation_key:
            domain.append(('name', '=', translation_key))
        see = self.search_read(model_name='ir.translation', domain=domain, fields=['src'], limit=1)
        if see:
            source_translate = see[0]['src']
        return source_translate

    def affect_country_id(self, dict_value, country, country_code=''):
        country_value = {'name': country}
        if not country_code and not country:
            return
        elif country_code:
            country_value['code'] = country_code
        domain = [('code', '=', country_code.upper())]
        if not country_code and country:
            name_src = country
            country_src = self.get_source_translate(country, 'res.country,name')
            if country_src:
                name_src = country_src
            domain = [('name', '=', name_src)]
        # print(country_value)
        country_id = self.create_or_use('res.country', country_value, domain)
        self.atach_many2one(dict_value, 'country_id', country_id)

    def process_csv_row(self, dict_row):
        """
        Overload this method to process a row
        :param dict_row: one raw of csv file
        :return: None
        """
        pass

