from odoo import api, fields, models, _
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


class Training(models.Model):
    _name = "hr.training"
    _description = "Training"
    _rec_name = "combined_name"

    name = fields.Char(string="Name")
    combined_name = fields.Char(string="session",compute="_compute_session_name")
    organization = fields.Many2one("training.organization", string="Organization")
    trainer = fields.Many2one("training.trainer", string="Trainer")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    training_type = fields.Selection([
        ('Internal', 'Internal'),
        ('External', 'External'), ], string='Training Type')
    follow_up = fields.Selection([
        ('six_months', '6 Months'),
        ('one_year', '1 Year'), ],  string='Follow Up')
    follow_date = fields.Date(string="Follow Date", compute='_compute_follow_date')
    company_profile = fields.Many2one("res.company", string="Company")
    employees = fields.Many2many("hr.employee", string="Employees")
    number_of_participants = fields.Integer(string="Participants", compute='_compute_participants_number')
    status = fields.Selection([
        ('approved', 'Approved'), ], default='approved',  string='Training Status')
    active_status_training = fields.Boolean(default=False, store=True)
    cost = fields.Char(string="Cost")
    online_checkbox = fields.Boolean('Online', default=False)
    online = fields.Char(string="Online", compute='_compute_online')
    technology = fields.Many2many("training.technology", string="Technology")
    training_objective = fields.Many2one("training.objective", string="Training Objective")


    def _compute_online(self):
        for rec in self:
            if rec.online_checkbox:
                rec.online = "Online"
            else:
                rec.online = "In Person"

    @api.depends('follow_up', 'end_date')
    def _compute_follow_date(self):
        for training in self:
            if training.end_date and training.follow_up:
                if training.follow_up == 'one_year':
                    training.follow_date = training.end_date + relativedelta(years=1)
                elif training.follow_up == 'six_months':
                    training.follow_date = training.end_date + relativedelta(months=6)
                else:
                    training.follow_date = False
            else:
                training.follow_date = False

    @api.depends('employees')
    def _compute_participants_number(self):
        for training in self:
            training.number_of_participants = len(training.employees)

    @api.depends('name','start_date','end_date')
    def _compute_session_name(self):
        for training in self:
            training.combined_name = training.name +"  "+ training.start_date.strftime("%d/%m/%Y") +"  "+training.end_date.strftime("%d/%m/%Y")

    

    def action_on_spot_evaluation(self):
        employee_id = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)], limit=1)
        if not self.env.user.has_group('Training_Management.group_hr_training_admin_hr'):
            employee_with_trainee = self.env['hr.trainee'].search(
                [('training', '=', self.id), ('employee_trainee.parent_id', 'child_of', employee_id.id),('employee_trainee.id', '!=', employee_id.id)])
            
            domain = [('training', 'in', employee_with_trainee.training.ids),
                      ('employee_trainee', 'in', employee_with_trainee.employee_trainee.ids)]
        else:
            employee_with_trainee = self.env['hr.trainee'].search(
                [('training', '=', self.id)])
            domain = [('training', 'in', employee_with_trainee.training.ids)]
        return {
            'name': _('Follow Up Evaluation Page'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.trainee',
            'view_mode': 'tree',
            "domain": domain,
            'view_id': self.env.ref('Training_Management.hr_trainee_on_spot_tree_view').id,
            'context': {
                'search_default_evaluation_not_completed': True,
            }
        }
        """employee_id = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)], limit=1)
        if not self.env.user.has_group('Training_Management.group_hr_training_admin_hr'):
            employee_with_trainee = self.env['evaluation.management'].search(
                [('training_id', '=', self.id), ('employee_id.parent_id', 'child_of', employee_id.id)])
            domain = [('training_id', 'in', employee_with_trainee.training_id.ids),
                      ('employee_id', 'in', employee_with_trainee.employee_id.ids)]
        else:
            employee_with_trainee = self.env['evaluation.management'].search([('training_id', '=', self.id)])
            domain = [('training_id', 'in', employee_with_trainee.training_id.ids)]
        return {
            'name': _('Evaluation'),
            'type': 'ir.actions.act_window',
            'res_model': 'evaluation.management',
            'view_mode': 'tree',
            "domain": domain,
            'view_id': self.env.ref('Training_Management.spot_eval_tree_view').id,
        }"""

    def action_follow_evaluation(self):
        employee_id = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)], limit=1)
        if not self.env.user.has_group('Training_Management.group_hr_training_admin_hr'):
            employee_with_trainee = self.env['hr.trainee'].search(
                [('training', '=', self.id), ('employee_trainee.parent_id', 'child_of', employee_id.id),('employee_trainee.id', '!=', employee_id.id)])
            
            domain = [('training', 'in', employee_with_trainee.training.ids),
                      ('employee_trainee', 'in', employee_with_trainee.employee_trainee.ids)]
        else:
            employee_with_trainee = self.env['hr.trainee'].search(
                [('training', '=', self.id)])
            domain = [('training', 'in', employee_with_trainee.training.ids)]
        return {
            'name': _('Follow Up Evaluation Page'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.trainee',
            'view_mode': 'tree',
            "domain": domain,
            'view_id': self.env.ref('Training_Management.hr_trainee_tree_view').id,
            'context': {
                'search_default_evaluation_not_completed': True,
            }
        }

    # ---------------------------------------------------------------------------------------------------------

    @api.model
    def create(self, vals_list):
        all_training = self.env['hr.training'].search([])
        res = super(Training, self).create(vals_list)
        # for training in all_training:
        #     if training.name == res.name and training.organization == res.organization and training.trainer == res.trainer \
        #             and training.start_date == res.start_date and training.end_date == res.end_date and training.training_type == res.training_type\
        #             and training.follow_up == res.follow_up and training.company_profile == res.company_profile :
        #         raise ValidationError(_('This Training already exist.'))

        if 'employees' in vals_list:
            for rec in vals_list['employees'][0][2]:
                form = self.env['evaluation.trainee'].create({'employee_id': rec, 'training_id': res.id})
                form_eval = self.env['evaluation.management'].create(
                    {'training_id': res.id, 'employee_id': rec})
                self.env['hr.trainee'].create(
                    {'employee_trainee': rec, 'training': res.id, 'form_id_eval': form_eval.id,
                     'form_id': form.id})

        return res

    def write(self, vals_list):
        
        # for training in all_training:
        #     if training.name == self.name and training.organization == self.organization and training.trainer == self.trainer \
        #             and training.start_date == self.start_date and training.end_date == self.end_date and training.training_type == self.training_type\
        #             and training.follow_up == self.follow_up and training.company_profile == self.company_profile :
        #         raise ValidationError(_('This Training already exist.'))
        if 'employees' in vals_list and "migration" not in vals_list:
            res = super(Training, self).write(vals_list)
            all_training = self.env['hr.training'].search([('id', '!=', self.id)])
            trainees = list(self.env['hr.trainee'].search([('training', '=', self.id)]).employee_trainee.ids)
            main_list = list(set(trainees) - set(vals_list['employees'][0][2]))
            trainees_to_delete = self.env['hr.trainee'].search(
                [('employee_trainee', 'in', main_list), ('training', '=', self.id)])
            for trainee in trainees_to_delete:
                trainee.unlink()
                self.env['evaluation.management'].search([('employee_id', '=', trainee.id)]).unlink()
                self.env['evaluation.trainee'].search([('employee_id', '=', trainee.id)]).unlink()

            for rec in vals_list['employees'][0][2]:
                trainee_already_exist = self.env['hr.trainee'].search(
                    [('employee_trainee', '=', rec), ('training', '=', self.id)])
                if not trainee_already_exist:
                    form = self.env['evaluation.trainee'].create({'employee_id': rec, 'training_id': self.id})
                    form_eval = self.env['evaluation.management'].create(
                        {'training_id': self.id, 'employee_id': rec})
                    self.env['hr.trainee'].create(
                        {'employee_trainee': rec, 'training': self.id, 'form_id_eval': form_eval.id,
                         'form_id': form.id})

        elif 'employees' in vals_list and "migration" in vals_list:
            del vals_list["migration"]
            
            all_training = self.env['hr.training'].search([('id', '!=', self.id)])
            trainees = list(self.env['hr.trainee'].search([('training', '=', self.id)]).employee_trainee.ids)
            main_list = list(set(trainees) - set(vals_list['employees']))
            trainees_to_delete = self.env['hr.trainee'].search(
                [('employee_trainee', 'in', main_list), ('training', '=', self.id)])
            for trainee in trainees_to_delete:
                trainee.unlink()
                self.env['evaluation.management'].search([('employee_id', '=', trainee.id)]).unlink()
                self.env['evaluation.trainee'].search([('employee_id', '=', trainee.id)]).unlink()
            
            for rec in vals_list['employees']:
                trainee_already_exist = self.env['hr.trainee'].search(
                    [('employee_trainee', '=', rec), ('training', '=', self.id)])
                if not trainee_already_exist:
                    form = self.env['evaluation.trainee'].create({'employee_id': rec, 'training_id': self.id})
                    form_eval = self.env['evaluation.management'].create(
                        {'training_id': self.id, 'employee_id': rec})
                    self.env['hr.trainee'].create(
                        {'employee_trainee': rec, 'training': self.id, 'form_id_eval': form_eval.id,
                         'form_id': form.id})
            vals_list['employees'] = [(4,vals_list['employees'][0])]
            res = super(Training, self).write(vals_list)
        else :
            res = super(Training, self).write(vals_list)

        return res

    def unlink(self):
        for training in self:
            trainees = self.env['hr.trainee'].search([('training', '=', training.id)])
            dashboard = self.env['evaluation.report.by.training'].search([('training_id', '=', training.id)])
            for trainee in trainees:
                if trainee:
                    trainee.sudo().unlink()

            for dash in dashboard:
                if dash:
                    dash.sudo().unlink()
        return super(Training, self).unlink()

    def employee_evaluation(self):
        domain = []
        if not self.env.user.has_group('Training_Management.group_hr_training_admin_hr'):
            employee_id = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.user.id)], limit=1)
            domain = [('employees.parent_id', 'child_of', employee_id.id)]
        return {
            "name": _('Employee Evaluation'),
            "type": "ir.actions.act_window",
            "res_model": "hr.training",
            "view_mode": "tree",
            "views": [[self.env.ref('Training_Management.eval_tree_view').id, "tree"]],
            "target": "current",
            "domain": domain,
        }
