from odoo import models, fields, api


class ProductCategoryInherit(models.Model):
    _inherit = "product.category"
    default_code = fields.Char("Référence")
    

class ProductTemplateInherit(models.Model):
    _inherit = "product.template"
    barcode = fields.Char(compute="_compute_barcode")
    
    def _compute_barcode(self):
        for template in self:
            template.barcode = default_code
