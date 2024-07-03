from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from lxml import etree

class EvaluationByManager(models.Model):
    _name = "evaluation.trainee"    
    _description = "Training's trainer"
    _rec_name = "employee_id"

    employee_id = fields.Many2one("hr.employee")
    status_form = fields.Char(string="status_form",default="not completed",store=True)
    training_id = fields.Many2one('hr.training', string="Training Name")

    ######### Overall Satisfaction  ####################################################################

    question1 = fields.Selection([
        ('very_dissatisfied', 'Very Dissatisfied'), ('not_so_satisfied', 'Not so Satisfied'), ('somewhat_satisfied', 'Somewhat Satisfied'), ('satisfied', 'Satisfied'), ('very_satisfied', 'Very Satisfied')],
        string='What is your overall satisfaction?' )
    
    ########## Productivity impact #######################################################################

    question2 = fields.Selection([
         ('strongly_disagree', 'Strongly Disagree'), ('disagree', 'Disagree'), ('neutral', 'Neutral'), ('agree', 'Agree'), ('strongly_agree', 'Strongly Agree')],
         string='This training improved the trainee’s productivity ?')

    
    question3 = fields.Selection([
       ('strongly_disagree', 'Strongly Disagree'), ('disagree', 'Disagree'), ('neutral', 'Neutral'), ('agree', 'Agree'), ('strongly_agree', 'Strongly Agree')],
         string='This training influenced the way of working or making decisions ?')

    ##########  Skills development  ###########################################################################

    question4 = fields.Selection([
       ('strongly_disagree', 'Strongly Disagree'), ('disagree', 'Disagree'), ('neutral', 'Neutral'), ('agree', 'Agree'), ('strongly_agree', 'Strongly Agree')],
        string="The trainee developed his/her skills through this training ?")
   
    question5 = fields.Selection([
       ('strongly_disagree', 'Strongly Disagree'), ('disagree', 'Disagree'), ('neutral', 'Neutral'), ('agree', 'Agree'), ('strongly_agree', 'Strongly Agree')],
         string='The skills development objectives set for this training been successfully achieved?')
    
    ############ Content ####################################

    question6 = fields.Selection([
        ('strongly_disagree', 'Strongly Disagree'), ('disagree', 'Disagree'), ('neutral', 'Neutral'), ('agree', 'Agree'), ('strongly_agree', 'Strongly Agree')],
        string='You find the training content to be relevant and useful ')
    
    question7 = fields.Selection([
        ('strongly_disagree', 'Strongly Disagree'), ('disagree', 'Disagree'), ('neutral', 'Neutral'), ('agree', 'Agree'), ('strongly_agree', 'Strongly Agree')],
         string='You find the training content to be adapted to project needs')
    
    ############## Comment #####################################

    comment = fields.Char('Comment')
    

    def write(self, vals):
        res = super(EvaluationByManager, self).write(vals)
        trainee = self.env['hr.trainee'].search([('form_id', '=',self.id )]) 
        trainee.evaluate_by_manager = True
        trainee.Status = "completed"
        trainee.Evaluation_Date_by_manager = self.write_date
        return res

