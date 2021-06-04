# -*- coding: utf-8 -*-

from solo_service import SoloServiceBase
import os


class SoloService(SoloServiceBase):
    def process_csv_row(self, dict_row):
        # Contry ===============================================================
        # try:
        country_id = False
        if dict_row['Tiers pays']:
            country_value = {
                'name': str(dict_row['Tiers pays']),
            }
            country_id = self.create_or_edit('res.country', country_value, [('name', '=', dict_row['Tiers pays'])])
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
        # # besoin module facturation
        if dict_row['Tiers type'] == '0':
            user_val['customer_rank'] = 1
        elif dict_row['Tiers type'] == '1':
            user_val['supplier_rank'] = 1
        if country_id:
            user_val['country_id'] = country_id[0] if isinstance(country_id, list) else country_id
        user_domain = [('name', 'like', "-[" + str(dict_row['Tiers numéro']) + "]")]
        user_id = self.create_or_edit('res.partner', user_val, user_domain)
        # Livraison ===============================================================
        if dict_row['Livraison intitulé'] and dict_row['Livraison numéro']:
            country_livraison_id = False
            if dict_row['Livraison pays']:
                country_livraison_value = {
                    'name': str(dict_row['Livraison pays']),
                }
                country_livraison_id = self.create_or_edit('res.country', country_livraison_value, [('name', '=', dict_row['Livraison pays'])])
            user_contact_livraison = {
                'name': str(dict_row['Livraison intitulé']) + "-{" + str(dict_row['Tiers numéro']) + "}" + "-[" + str(dict_row['Livraison numéro']) + "]",
                # 'function': dict_row['Tiers qualité'],
                'street': dict_row['Livraison adresse'],
                'street2': dict_row['Livraison complément adresse'],
                'type': 'delivery',
                'zip': dict_row['Tiers code postal'],
                'city': dict_row['Livraison ville'],
                'phone': dict_row['Livraison téléphone'],
                'email': dict_row['Livraison Email'],
                'parent_id': user_id[0] if isinstance(user_id, list) else user_id,
                # 'website': dict_row['Tite site web'],
            }
            if country_livraison_id:
                user_contact_livraison['country_id'] = country_livraison_id[0] if isinstance(country_livraison_id, list) else country_livraison_id
            user_domain = [('name', 'like', "-[" + str(dict_row['Livraison numéro']) + "]")]
            self.create_or_edit('res.partner', user_contact_livraison, user_domain)
            # Fin ===============================================================
        # except Exception as error_infos:
        #     raise Exception(error_infos)
        # print(self.search('res.users', user_domain))
        # print(self.read(self.uid, 'res.users')[0]['name'])
        # print(self.read(2, 'res.users')[0]['name'])
        # print(dict_row['Collaborateur numéro'])


# Service = SoloService()
Service = SoloService(
    host='https://dkgroup-organization-jp-arbez.odoo.com',
    db='dkgroup-organization-jp-arbez-master-2638135',
    user='admin',
    password='admin'
)
print(os.path.dirname(os.path.realpath(__file__)))
print(os.path.realpath(__file__))
Service.import_data('{}/../static/temp/vig_ - Clients adresses livraisons.csv'.format(os.path.dirname(os.path.realpath(__file__))))
# Service.import_data('{}/../static/temp/vig_ - Tiers clients fournisseurs.csv'.format(os.path.dirname(os.path.realpath(__file__))))


