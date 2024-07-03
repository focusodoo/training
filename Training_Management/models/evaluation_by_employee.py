from odoo import api, fields, models, _


class Evaluation(models.Model):
    _name = "evaluation.management"
    _description = "Evaluation"
    _rec_name = "training_id"

    ######### Overall Satisfaction  ####################################################################

    question1 = fields.Selection([
        ('very_dissatisfied', 'Very Dissatisfied'), ('not_so_satisfied', 'Not so Satisfied'), ('somewhat_satisfied', 'Somewhat Satisfied'), ('satisfied', 'Satisfied'), ('very_satisfied', 'Very Satisfied')],
         string='What is your overall satisfaction?' )

    ######### Program and duration   ####################################################################

    question2 = fields.Selection([
         ('very_dissatisfied', 'Very Dissatisfied'), ('not_so_satisfied', 'Not so Satisfied'), ('somewhat_satisfied', 'Somewhat Satisfied'), ('satisfied', 'Satisfied'), ('very_satisfied', 'Very Satisfied')],
        string='How satisfied are you with the way the training was organized?')

    
    question3 = fields.Selection([
       ('very_dissatisfied', 'Very Dissatisfied'), ('not_so_satisfied', 'Not so Satisfied'), ('somewhat_satisfied', 'Somewhat Satisfied'), ('satisfied', 'Satisfied'), ('very_satisfied', 'Very Satisfied')],
         string='How satisfied were you with the training duration?')

    ######### Trainer competency and pedagogy ##################################################################""

    question4 = fields.Selection([
        ('very_dissatisfied', 'Very Dissatisfied'), ('not_so_satisfied', 'Not so Satisfied'), ('somewhat_satisfied', 'Somewhat Satisfied'), ('satisfied', 'Satisfied'), ('very_satisfied', 'Very Satisfied')],
         string="How satisfied are you with the trainer's skills?")
   
    question5 = fields.Selection([
        ('very_dissatisfied', 'Very Dissatisfied'), ('not_so_satisfied', 'Not so Satisfied'), ('somewhat_satisfied', 'Somewhat Satisfied'), ('satisfied', 'Satisfied'), ('very_satisfied', 'Very Satisfied')],
         string='You find the training methods to be effective?')
    
    ############ Content ####################################

    question6 = fields.Selection([
        ('strongly_disagree', 'Strongly Disagree'), ('disagree', 'Disagree'), ('neutral', 'Neutral'), ('agree', 'Agree'), ('strongly_agree', 'Strongly Agree')],
         string='You find the training content relevant and useful')
    
    question7 = fields.Selection([
        ('strongly_disagree', 'Strongly Disagree'), ('disagree', 'Disagree'), ('neutral', 'Neutral'), ('agree', 'Agree'), ('strongly_agree', 'Strongly Agree')],
         string='You find the training content adapted to your needs ?')
    
    ############ Recommendation ######################################
    
    question8 = fields.Selection([
        ('very_unlikely', 'Very Unlikely'), ('unlikely', 'Unlikely'),  ('neutral', 'Neutral'), ('somewhat_likely', 'Somewhat Likely'), ('very_likely', 'Very Likely')],
         string='How likely are you to (likely would be better in this context) recommend this training course?')
    
    ############ Comment ##################################################

    comment = fields.Char('Comment')

    #################################################################################################################



    training_id = fields.Many2one("hr.training", string="Training Name", store=True)
    employee_id = fields.Many2one("hr.employee", string="Employee", store=True)

    def write(self, vals):
        res = super(Evaluation, self).write(vals)
        trainee = self.env['hr.trainee'].search([('form_id_eval', '=', self.id)])
        trainee.evaluate_by_employee = True
        trainee.evaluation_submission_date = self.write_date
        return res
