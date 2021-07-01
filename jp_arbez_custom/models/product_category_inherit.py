from odoo import models, fields, api


class ProductCategoryInherit(models.Model):
    _inherit = "product.category"
    default_code = fields.Char("Référence")
    

