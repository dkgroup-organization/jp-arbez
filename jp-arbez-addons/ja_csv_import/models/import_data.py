# -*- coding: utf-8 -*-

from solo_service import SoloServiceBase
import re


class SoloService(SoloServiceBase):
    def process_csv_row(self, dict_row):
        # User ===============================================================
        user_val = {
            'name': str(dict_row['Tiers intitulé']) + "-[" + str(dict_row['Tiers numéro']) + "]",
            'function': dict_row['Tiers qualité'],
            'street': dict_row['Tiers complément adresse'],
            'zip': dict_row['Tiers code postal'],
            'city': dict_row['Tiers ville'],
            'phone': dict_row['Tiers téléphone'],
            'email': dict_row['Tiers Email'],
            'website': dict_row['Tite site web'],
        }
        # affect tva debut ---------------------------------
        tva = dict_row['Tiers n° entreprise'].replace(' ', '')
        country_code = re.sub(r"^([a-zA-Z_]+)([0-9]+)$", r"\1", tva)
        vat_number = re.sub(r"^([a-zA-Z_]+)([0-9]+)$", r"\2", tva)
        valid_vat = False
        if country_code != tva:
            valid_vat = self.send_object_request(self.DB, self.uid, self.PASS, 'res.partner', 'simple_vat_check', country_code, vat_number)
        if valid_vat:
            self.affect_col_value(user_val, 'vat', tva)
            self.affect_country_id(user_val, dict_row['Tiers pays'], country_code)
        else:
            self.affect_country_id(user_val, dict_row['Tiers pays'])
        # affect tva fin ---------------------------------
        if tva:
            user_val['is_company'] = True
        # # besoin module facturation
        if dict_row['Tiers type'] == '0':
            user_val['customer_rank'] = 1
        elif dict_row['Tiers type'] == '1':
            user_val['supplier_rank'] = 1
        user_domain = [('name', 'like', "-[" + str(dict_row['Tiers numéro']) + "]")]
        user_id = self.create_or_edit('res.partner', user_val, user_domain)
        # Livraison ===============================================================
        if dict_row.get('Livraison intitulé') and dict_row.get('Livraison numéro'):
            user_contact_livraison = {
                'name': str(dict_row['Livraison intitulé']) + "-{" + str(dict_row['Tiers numéro']) + "}" + "-[" + str(dict_row['Livraison numéro']) + "]",
                'street': dict_row['Livraison adresse'],
                'street2': dict_row['Livraison complément adresse'],
                'type': 'delivery',
                'zip': dict_row['Tiers code postal'],
                'city': dict_row['Livraison ville'],
                'phone': dict_row['Livraison téléphone'],
                'email': dict_row['Livraison Email'],
            }
            self.affect_country_id(user_contact_livraison, dict_row['Livraison pays'])
            self.atach_many2one(user_contact_livraison, 'parent_id', user_id)
            user_domain = [('name', 'like', "-[" + str(dict_row['Livraison numéro']) + "]")]
            self.create_or_edit('res.partner', user_contact_livraison, user_domain)
        # principal contact ===============================================================
        if dict_row.get('Tiers contact principal'):
            user_contact_principale = {
                'name': str(dict_row['Tiers contact principal']) + "-{" + str(dict_row['Tiers numéro']) + "}",
                'function': dict_row['Tiers qualité'],
                'street': dict_row['Tiers complément adresse'],
                'zip': dict_row['Tiers code postal'],
                'city': dict_row['Tiers ville'],
            }
            self.atach_many2one(user_contact_principale, 'parent_id', user_id)
            contact_principale = [('name', 'like', user_contact_principale['name'])]
            self.create_or_edit('res.partner', user_contact_principale, contact_principale)
            # Fin ===============================================================
        # except Exception as error_infos:
        #     raise Exception(error_infos)
        # print(self.search('res.users', user_domain))
        # print(self.read(self.uid, 'res.users')[0]['name'])
        # print(dict_row['Collaborateur numéro'])

