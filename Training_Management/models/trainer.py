from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Trainer(models.Model):
    _name = "training.trainer"    
    _description = "Training's trainer"

    name = fields.Char(string="Trainer Name",required=True)

