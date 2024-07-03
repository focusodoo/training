from odoo import api, fields, models, _


class Technology(models.Model):
    _name = "training.technology"
    _description = "Training Technology"

    name = fields.Char(string="Technology Name")
    active = fields.Boolean(string="Active", default=True, invisible=1)


class TrainingObjective(models.Model):
    _name = "training.objective"
    _description = "Training Objective"
    _rec_name = 'training_obj'

    training_obj = fields.Char(string="Training Objective")
    active = fields.Boolean(string="Active", default=True, invisible=1)

