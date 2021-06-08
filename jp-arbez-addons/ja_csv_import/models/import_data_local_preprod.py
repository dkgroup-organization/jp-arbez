# -*- coding: utf-8 -*-

from import_data import SoloService
import os

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
Service.import_data('{}/../static/temp/vig_ - Tiers clients fournisseurs.csv'.format(os.path.dirname(os.path.realpath(__file__))))


