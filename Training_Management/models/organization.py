from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Trainer(models.Model):
    _name = "training.organization"    
    _description = "Training's organization"

    name = fields.Char(string="Organization Name")
    description = fields.Char(string="Description")