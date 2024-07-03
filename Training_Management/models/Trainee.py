from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Trainee(models.Model):
    _name = "hr.trainee"

    _description = "Trainee Evaluation"
    _rec_name = "employee_trainee"

    employee_trainee = fields.Many2one('hr.employee', string='Trainee')
    training = fields.Many2one('hr.training', string="Training Name")
    follow_date = fields.Date(string="follow Date ", related="training.follow_date", store=True)
    form_id = fields.Many2one('evaluation.trainee', string="form id")
    form_id_eval = fields.Many2one('evaluation.management', string="form id eval")
    evaluate_by_manager = fields.Boolean(default=False)
    evaluate_by_employee = fields.Boolean(default=False)
    evaluation_submission_date = fields.Datetime('Submission Eval Date', store=True)
    Status = fields.Char(string='status', default="not completed", store=True)
    Evaluation_Date_by_manager = fields.Datetime(string='Evaluation Date', store=True)
    active_status = fields.Boolean(default=False, store=True)
    date_from = fields.Date(related="training.start_date", string="Date From",store=True)
    date_to = fields.Date(related="training.end_date", string="Date To",store=True)

    def action_evaluate_by_manager(self):
        if self.form_id:
            return {
                "name": _('Follow Up Evaluation'),
                "type": "ir.actions.act_window",
                "res_model": "evaluation.trainee",
                "view_mode": "form",
                "res_id": self.form_id.id,
                "views": [[self.env.ref('Training_Management.hr_trainer_evaluation_form_view').id, "form"]],
                "target": "current",
                'context': {'form_view_initial_mode': 'edit', 'force_detailed_view': 'true'},

            }
        else:
            return {
                "name": _('Follow Up Evaluation'),
                "type": "ir.actions.act_window",
                "res_model": "evaluation.trainee",
                "view_mode": "form",
                "views": [[self.env.ref('Training_Management.hr_trainer_evaluation_form_view').id, "form"]],
                "target": "current",
                'context': {'form_view_initial_mode': 'edit', 'force_detailed_view': 'true'},
            }

    def action_evaluate_by_employee(self):
        context = {'form_view_initial_mode': 'edit', 'force_detailed_view': 'true'}
        if self.form_id_eval:
            return {
                "name": _('Employee Evaluation'),
                "type": "ir.actions.act_window",
                "res_model": "evaluation.management",
                "view_mode": "form",
                "res_id": self.form_id_eval.id,
                "views": [[self.env.ref('Training_Management.evaluation_by_employee_form_view').id, "form"]],
                "target": "current",
                "context": context,
            }
        else:
            return {
                "name": _('Employee Evaluation'),
                "type": "ir.actions.act_window",
                "res_model": "evaluation.management",
                "view_mode": "form",
                "views": [[self.env.ref('Training_Management.evaluation_by_employee_form_view').id, "form"]],
                "target": "current",
                "context": context,
            }

    def creation_trainee_eval_function(self):
        '''trainees = self.env['hr.training'].search([])
        for trainee in trainees:
            for rec in trainee['employees']:
                trainee_already_exist = self.env['hr.trainee'].search(
                    [('employee_trainee', '=', rec.id), ('training', '=', trainee.id), ('form_id_eval', '=', False)])
                if trainee_already_exist:
                    form = self.env['evaluation.trainee'].create({'employee_id': rec.id, 'training_id': trainee.id})
                    form_eval = self.env['evaluation.management'].create(
                        {'training_id': trainee.id, 'employee_id': rec.id})
                    trainee_already_exist.update({'form_id_eval': form_eval.id,'form_id': form.id})'''
        employee_id = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        domain = [('employee_trainee', '=', employee_id.id)]
        return {
            'name': _('My Evaluation'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.trainee',
            'view_mode': 'tree',
            'view_id': self.env.ref('Training_Management.evaluation_tree_view').id,
            "search_view_id": [self.env.ref('Training_Management.filter_training_in_my_evaluation').id, 'search'],

            "domain": domain,
        }

    def unlink(self):
        for rec in self:
            self.env['evaluation.management'].search(
                [('id', '=', rec.form_id_eval.id)]).unlink()
            self.env['evaluation.trainee'].search([('id', '=', rec.form_id.id)]).unlink()
        return super(Trainee, self).unlink()
