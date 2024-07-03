from odoo import api, fields, models, _
from datetime import datetime, time
from dateutil.relativedelta import relativedelta


class Training(models.Model):
    _inherit = "hr.training"

    @api.model
    def _cron_first_notification_employee_manager(self):
        today = fields.Datetime.now().date() 
        trainings = self.search([])
        list_training = []
        employees_trainings = []
        
        for training in trainings : 
            

            if training.end_date : 
                if  training.end_date <= today :
                    employees_trainings.append(training)

            if training.end_date and training.follow_up :
                if training.follow_up == 'one_year' :
                    follow_date = training.end_date + relativedelta(years=1)
                    if follow_date <= today :
                        list_training.append(training)
                elif training.follow_up == 'six_months' :
                    follow_date = training.end_date + relativedelta(months=6)
                    if follow_date <= today :
                        list_training.append(training)
        mans = []
        for training_selected in list_training :
            not_evaluated_trainings = self.env["hr.trainee"].search([("training","=",training_selected.id),("evaluate_by_manager","=",False)])
            #employees = training_selected.
            if not_evaluated_trainings :
                for emplo in not_evaluated_trainings.employee_trainee : 
                    if emplo.parent_id not in mans and emplo.state not in ["relieved", "terminate", "joined", "training", "withdrawn"]:
                        mans.append(emplo.parent_id)



        for manager in mans:
            if manager.user_id and manager.state not in ["relieved", "terminate", "joined", "training", "withdrawn"] : 
                # change the action to the training_em_id model 
                self._cron_training_send_reminder(
                        manager,
                        'training_notifications.mail_template_notification_notification',
                        'Training_Management.hr_training_action_not_evaluated_by_manager')

        ####################################################################################################
        emps = []
        for emp_training in employees_trainings :
    
            employees = []
            not_evaluated_trainings = self.env["hr.trainee"].search([("training","=",emp_training.id),("evaluate_by_employee","=",False)])
            if not_evaluated_trainings :
                for emplo in not_evaluated_trainings.employee_trainee : 
                    if emplo not in emps and emplo.state not in ["relieved", "terminate", "joined", "training", "withdrawn"]:
                        emps.append(emplo)
                #employees.append(not_evaluated_trainings.employee_trainee)
        for employee in emps : 
            if employee.user_id :
                # send email reminder if ot subited and the link to the form eval 
                self._cron_training_send_reminder(
                        employee,
                        'training_notifications.mail_template_notification_notification_employee',
                        'Training_Management.hr_training_action_not_evaluated',
                    )



    @api.model
    def _cron_training_send_reminder(self, employees, template_xmlid, action_xmlid):
        """ Send the email reminder to specified users
            :param user_ids : list of user identifier to send the reminder
            :param template_xmlid : xml id of the reminder mail template
        """
        action_url = '%s/web#menu_id=%s&action=%s' % (
            self.env['ir.config_parameter'].sudo().get_param('web.base.url'),
            self.env.ref('Training_Management.menu_training').id,
            self.env.ref(action_xmlid).id,
        )

        # send mail template to users having email address
        template = self.env.ref(template_xmlid)
        template_ctx = {'action_url': action_url}

        for employee in employees.filtered('user_id'):
            template.with_context(**template_ctx).send_mail(employee.id)


        