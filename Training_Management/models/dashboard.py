from odoo import api, fields, models, _
from odoo.exceptions import ValidationError



class EvaluationReportByTraining(models.Model):
    _name = "evaluation.report.by.training"
    _description = "Evaluation Report by Training"
    _rec_name = "training_id"

    training_id = fields.Many2one('hr.training')
    percentage_evaluate_trainee = fields.Float('Evaluate Trainee Percentage')
    type = fields.Char('Training analysis')
    effective = fields.Float('Percentage of an effective training')
    type_effective = fields.Char('type  effectivenees')
    
    ################################################################
    response = fields.Char('over all satisfaction responses')
    percentage_on_spot_eval_overall_satisfaction = fields.Float('Evaluate over all satisfaction Percentage')
    ################################################################

    response2 = fields.Char('program and duration')
    percentage_program_and_duration = fields.Float('program and duration Percentage')

    #################################################################
    response3 = fields.Char('Content')
    percentage_content = fields.Float('Content Percentage')

    ######################################################################

    response4 = fields.Char('Trainer Skills')
    percentage_trainer_skills = fields.Float('Trainer Skills')

    ######################################################################

    response5 = fields.Char('Trainer Skills')
    percentage_training_methods = fields.Float('Trainer Skills')

    ######################################################################


    response6 = fields.Char('Recommandations')
    percentage_training_recommandation = fields.Float('Recommandations')

    ######################################################################

    response7 = fields.Char('Recommandations')
    percentage_training_overall_satisfaction_follow_up = fields.Float('Recommandations')

    ######################################################################

    response8 = fields.Char('Responses')
    section = fields.Char('Section')
    percentage_training_other_follow_up = fields.Float('Percentage')
    

    


    active_status = fields.Boolean(default=False, store=True)



    def pie_percentage_evalaution_trainee_function(self,training_id):
        training = self.env['hr.training'].search([('id', '=', training_id)])
        
        if training :
            nb_trainee_by_training = self.env['hr.trainee'].search_count([('training', '=', training_id)])       
            nb_trainee_evaluated= self.env['hr.trainee'].search_count(
                [('training', '=', training_id),('Status', "=" ,"completed")])
            percentage_evaluated_trainee = self.env['evaluation.report.by.training'].search(
                            [('training_id', '=', training_id), ('type', '=', 'evaluated')])
            percentage_not_evaluated_trainee = self.env['evaluation.report.by.training'].search(
                            [('training_id', '=', training_id), ('type', '=', 'not evaluated')])
            resultat = 0
            if nb_trainee_evaluated :
                resultat = (nb_trainee_evaluated * 100 ) / nb_trainee_by_training
            if not percentage_evaluated_trainee:
                self.env['evaluation.report.by.training'].create(
                                {'training_id': training_id, 'percentage_evaluate_trainee': resultat, 'type': 'evaluated', 'active_status': True})
            else:
                percentage_evaluated_trainee.write({'percentage_evaluate_trainee': resultat, 'type': 'evaluated' , 'active_status': True})
            if not (percentage_not_evaluated_trainee):
                self.env['evaluation.report.by.training'].create(
                                    {'training_id': training_id, 'percentage_evaluate_trainee': 100 - resultat, 'type': 'not evaluated', 'active_status': True})
            else :
                percentage_not_evaluated_trainee.write({'percentage_evaluate_trainee': 100 - resultat, 'type': 'not evaluated', 'active_status': True})
            percentage_evaluated_trainee.active_status = True
            
      
    def pie_chart_of_Training_effective(self,training_id):
            nbre_yes_in_question1 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question1','=','yes'),('status_form', '=', 'completed')])
            nbre_yes_perfectly_in_question2 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question2','=','Yes_Perfectly'),('question1','=','yes'),('status_form', '=', 'completed')]) * 1
            nbre_yes_partially_in_question2 =  self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question2','=','Yes_Partially'),('question1','=','yes'),('status_form', '=', 'completed')]) * 0.75    
            percentage_evaluated_trainee = self.env['evaluation.report.by.training'].search(
                                [('training_id', '=', training_id), ('type', '=', 'evaluated')])
            percentage_not_evaluated_trainee = self.env['evaluation.report.by.training'].search(
                                [('training_id', '=', training_id), ('type', '=', 'not evaluated')])

            effective= 0
            if nbre_yes_in_question1 :
                    effective  = ( nbre_yes_perfectly_in_question2 +  nbre_yes_partially_in_question2 ) / nbre_yes_in_question1 * 100
            if percentage_evaluated_trainee:
                    percentage_evaluated_trainee.write({'effective': effective, 'type_effective': 'effective'})
            if percentage_not_evaluated_trainee:
                    percentage_not_evaluated_trainee.write({'effective': 100 - effective, 'type_effective': 'not effective'})

    def training_pie_action_onspot_overall_satisfaction(self,training_id):
        
        ########### calculate percentage ###############################################
        #
        nbr_total_question1 = self.env['hr.training'].search([('id', '=', training_id)]).number_of_participants
        nbr_very_dissatisfied_in_question1 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question1','=','very_dissatisfied')])
        nbr_not_so_satisfied_in_question1 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question1','=','not_so_satisfied')])
        nbr_somewhat_satisfied_in_question1 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question1','=','somewhat_satisfied')])
        nbr_satisfied_in_question1 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question1','=','satisfied')])
        nbr_very_satisfied_in_question1 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question1','=','very_satisfied')])
        # 

        #
        
        # ##############################################################################
        if nbr_total_question1 !=  0 :
            percentage_not_evaluated_trainee_very_dissatisfied = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response', '=', 'very_dissatisfied')])
            if not percentage_not_evaluated_trainee_very_dissatisfied : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_on_spot_eval_overall_satisfaction':(nbr_very_dissatisfied_in_question1/nbr_total_question1)*100 , 'response': 'very_dissatisfied', 'active_status': True})
            else :
                percentage_not_evaluated_trainee_very_dissatisfied.write({'response': 'very_dissatisfied', 'percentage_on_spot_eval_overall_satisfaction': (nbr_very_dissatisfied_in_question1/nbr_total_question1)*100})
            ########################################################################################
            percentage_not_evaluated_trainee_not_so_satisfied = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response', '=', 'not_so_satisfied')])
            if not percentage_not_evaluated_trainee_not_so_satisfied : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_on_spot_eval_overall_satisfaction': (nbr_not_so_satisfied_in_question1/nbr_total_question1)*100, 'response': 'not_so_satisfied', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_not_so_satisfied.write({'response': 'not_so_satisfied', 'percentage_on_spot_eval_overall_satisfaction': (nbr_not_so_satisfied_in_question1/nbr_total_question1)*100})

            ##############################################################################################
            percentage_not_evaluated_trainee_somewhat_satisfied = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response', '=', 'somewhat_satisfied')])
            if not percentage_not_evaluated_trainee_somewhat_satisfied : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_on_spot_eval_overall_satisfaction': (nbr_somewhat_satisfied_in_question1/nbr_total_question1)*100, 'response': 'somewhat_satisfied', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_somewhat_satisfied.write({'response': 'not_so_satisfied', 'percentage_on_spot_eval_overall_satisfaction':  (nbr_somewhat_satisfied_in_question1/nbr_total_question1)*100})

            ###################################################################################################
            percentage_not_evaluated_trainee_satisfied = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response', '=', 'satisfied')])
            if not percentage_not_evaluated_trainee_satisfied : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_on_spot_eval_overall_satisfaction':  (nbr_satisfied_in_question1/nbr_total_question1)*100, 'response': 'satisfied', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_satisfied.write({'response': 'satisfied', 'percentage_on_spot_eval_overall_satisfaction':  (nbr_satisfied_in_question1/nbr_total_question1)*100})

            ####################################################################################################
            percentage_not_evaluated_trainee_very_satisfied = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response', '=', 'very_satisfied')])
            
            if not percentage_not_evaluated_trainee_very_satisfied : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_on_spot_eval_overall_satisfaction': (nbr_very_satisfied_in_question1/nbr_total_question1)*100, 'response': 'very_satisfied', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_very_satisfied.write({'response': 'very_satisfied', 'percentage_on_spot_eval_overall_satisfaction':  (nbr_very_satisfied_in_question1/nbr_total_question1)*100})

        else :
            raise ValidationError(_('There are no completed evel for this training.'))
        

    def training_pie_action_onspot_program_and_duration(self,training_id):
        
        ########### calculate percentage ###############################################
        #
        nbr_total_question1 = self.env['hr.training'].search([('id', '=', training_id)]).number_of_participants
        nbr_strongly_disagree_in_question2 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question2','=','very_dissatisfied')])
        nbr_disagree_in_question2 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question2','=','not_so_satisfied')])
        nbr_neutral_in_question2 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question2','=','somewhat_satisfied')])
        nbr_agree_in_question2 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question2','=','satisfied')])
        nbr_strongly_agree_in_question2 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question2','=','very_satisfied')])
        # 

        #
        
        # ##############################################################################
        if nbr_total_question1 !=  0 :
            percentage_not_evaluated_trainee_strongly_disagree = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response2', '=', 'very_dissatisfied')])
            if not percentage_not_evaluated_trainee_strongly_disagree : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_program_and_duration':(nbr_strongly_disagree_in_question2/nbr_total_question1)*100 , 'response2': 'very_dissatisfied', 'active_status': True})
            else :
                percentage_not_evaluated_trainee_strongly_disagree.write({'response2': 'very_dissatisfied', 'percentage_program_and_duration': (nbr_strongly_disagree_in_question2/nbr_total_question1)*100})
            ########################################################################################
            percentage_not_evaluated_trainee_disagree = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response2', '=', 'not_so_satisfied')])
            if not percentage_not_evaluated_trainee_disagree : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_program_and_duration': (nbr_disagree_in_question2/nbr_total_question1)*100, 'response2': 'not_so_satisfied', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_disagree.write({'response2': 'not_so_satisfied', 'percentage_program_and_duration': (nbr_disagree_in_question2/nbr_total_question1)*100})

            ##############################################################################################
            percentage_not_evaluated_trainee_neutral = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response2', '=', 'somewhat_satisfied')])
            if not percentage_not_evaluated_trainee_neutral : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_program_and_duration': (nbr_neutral_in_question2/nbr_total_question1)*100, 'response2': 'somewhat_satisfied', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_neutral.write({'response2': 'somewhat_satisfied', 'percentage_program_and_duration':  (nbr_neutral_in_question2/nbr_total_question1)*100})

            ###################################################################################################
            percentage_not_evaluated_trainee_agree = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response2', '=', 'satisfied')])
            if not percentage_not_evaluated_trainee_agree : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_program_and_duration':  (nbr_agree_in_question2/nbr_total_question1)*100, 'response2': 'satisfied', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_agree.write({'response2': 'satisfied', 'percentage_program_and_duration':  (nbr_agree_in_question2/nbr_total_question1)*100})

            ####################################################################################################
            percentage_not_evaluated_trainee_strongly_agree = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response2', '=', 'very_satisfied')])
            
            if not percentage_not_evaluated_trainee_strongly_agree : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_program_and_duration': (nbr_strongly_agree_in_question2/nbr_total_question1)*100, 'response2': 'very_satisfied', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_strongly_agree.write({'response2': 'very_satisfied', 'percentage_program_and_duration':  (nbr_strongly_agree_in_question2/nbr_total_question1)*100})

        else :
            raise ValidationError(_('There are no completed evel for this training.'))
        

    def training_pie_action_content(self,training_id):
        
        ########### calculate percentage ###############################################
        #

        nbr_total_question1 = self.env['hr.training'].search([('id', '=', training_id)]).number_of_participants

        nbr_strongly_disagree_in_question6 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question6','=','strongly_disagree')])
        nbr_disagree_in_question6 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question6','=','disagree')])
        nbr_neutral_in_question6 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question6','=','neutral')])
        nbr_agree_in_question6 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question6','=','agree')])
        nbr_strongly_agree_in_question6 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question6','=','strongly_agree')])


        nbr_strongly_disagree_in_question7 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question7','=','strongly_disagree')])
        nbr_disagree_in_question7 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question7','=','disagree')])
        nbr_neutral_in_question7 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question7','=','neutral')])
        nbr_agree_in_question7 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question7','=','agree')])
        nbr_strongly_agree_in_question7 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question7','=','strongly_agree')])

        #
        # ##############################################################################
        if nbr_total_question1 !=  0 :
            percentage_not_evaluated_trainee_strongly_disagree = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response3', '=', 'strongly_disagree')])
            if not percentage_not_evaluated_trainee_strongly_disagree : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_content':(nbr_strongly_disagree_in_question6 + nbr_strongly_disagree_in_question7 /nbr_total_question1)*100 , 'response3': 'strongly_disagree', 'active_status': True})
            else :
                percentage_not_evaluated_trainee_strongly_disagree.write({'response3': 'strongly_disagree', 'percentage_content': (nbr_strongly_disagree_in_question6 + nbr_strongly_disagree_in_question7/nbr_total_question1)*100})
            ########################################################################################
            percentage_not_evaluated_trainee_disagree = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response3', '=', 'disagree')])
            if not percentage_not_evaluated_trainee_disagree : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_content': (nbr_disagree_in_question6 + nbr_disagree_in_question7 /nbr_total_question1)*100, 'response3': 'disagree', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_disagree.write({'response3': 'disagree', 'percentage_content': (nbr_disagree_in_question6 + nbr_disagree_in_question7/nbr_total_question1)*100})

            ##############################################################################################
            percentage_not_evaluated_trainee_neutral = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response3', '=', 'neutral')])
            if not percentage_not_evaluated_trainee_neutral : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_content': (nbr_neutral_in_question6 + nbr_neutral_in_question7 / nbr_total_question1)*100, 'response3': 'neutral', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_neutral.write({'response3': 'neutral', 'percentage_content':  (nbr_neutral_in_question6 + nbr_neutral_in_question7 / nbr_total_question1)*100})

            ###################################################################################################
            percentage_not_evaluated_trainee_agree = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response3', '=', 'agree')])
            if not percentage_not_evaluated_trainee_agree : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_content':  (nbr_agree_in_question6 + nbr_agree_in_question7 / nbr_total_question1)*100, 'response3': 'agree', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_agree.write({'response3': 'agree', 'percentage_content':  (nbr_agree_in_question6 + nbr_agree_in_question7 / nbr_total_question1)*100})

            ####################################################################################################
            percentage_not_evaluated_trainee_strongly_agree = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response3', '=', 'strongly_agree')])
            
            if not percentage_not_evaluated_trainee_strongly_agree : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_content': (nbr_strongly_agree_in_question6 + nbr_strongly_agree_in_question7 /nbr_total_question1)*100, 'response3': 'strongly_agree', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_strongly_agree.write({'response3': 'strongly_agree', 'percentage_content':  (nbr_strongly_agree_in_question6 + nbr_strongly_agree_in_question7 /nbr_total_question1)*100})

        else :
            raise ValidationError(_('There are no completed evel for this training.'))
        
    def training_pie_action_trainer_skills(self,training_id):

       
        ########### calculate percentage ###############################################
        #
        nbr_total_question1 = self.env['hr.training'].search([('id', '=', training_id)]).number_of_participants
        nbr_very_dissatisfied_in_question4 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question4','=','very_dissatisfied')])
        nbr_not_so_satisfied_in_question4 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question4','=','not_so_satisfied')])
        nbr_somewhat_satisfied_in_question4 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question4','=','somewhat_satisfied')])
        nbr_satisfied_in_question4 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question4','=','satisfied')])
        nbr_very_satisfied_in_question4 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question4','=','very_satisfied')])
        # 

        #
        
        # ##############################################################################
        if nbr_total_question1 !=  0 :
            percentage_not_evaluated_trainee_very_dissatisfied = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response4', '=', 'very_dissatisfied')])
            if not percentage_not_evaluated_trainee_very_dissatisfied : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_trainer_skills':(nbr_very_dissatisfied_in_question4/nbr_total_question1)*100 , 'response4': 'very_dissatisfied', 'active_status': True})
            else :
                percentage_not_evaluated_trainee_very_dissatisfied.write({'response4': 'very_dissatisfied', 'percentage_trainer_skills': (nbr_very_dissatisfied_in_question4/nbr_total_question1)*100})
            ########################################################################################
            percentage_not_evaluated_trainee_not_so_satisfied = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response4', '=', 'not_so_satisfied')])
            if not percentage_not_evaluated_trainee_not_so_satisfied : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_trainer_skills': (nbr_not_so_satisfied_in_question4/nbr_total_question1)*100, 'response4': 'not_so_satisfied', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_not_so_satisfied.write({'response4': 'not_so_satisfied', 'percentage_trainer_skills': (nbr_not_so_satisfied_in_question4/nbr_total_question1)*100})

            ##############################################################################################
            percentage_not_evaluated_trainee_somewhat_satisfied = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response4', '=', 'somewhat_satisfied')])
            if not percentage_not_evaluated_trainee_somewhat_satisfied : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_trainer_skills': (nbr_somewhat_satisfied_in_question4/nbr_total_question1)*100, 'response4': 'somewhat_satisfied', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_somewhat_satisfied.write({'response4': 'not_so_satisfied', 'percentage_trainer_skills':  (nbr_somewhat_satisfied_in_question4/nbr_total_question1)*100})

            ###################################################################################################
            percentage_not_evaluated_trainee_satisfied = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response4', '=', 'satisfied')])
            if not percentage_not_evaluated_trainee_satisfied : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_trainer_skills':  (nbr_satisfied_in_question4/nbr_total_question1)*100, 'response4': 'satisfied', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_satisfied.write({'response4': 'satisfied', 'percentage_trainer_skills':  (nbr_satisfied_in_question4/nbr_total_question1)*100})

            ####################################################################################################
            percentage_not_evaluated_trainee_very_satisfied = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response4', '=', 'very_satisfied')])
            
            if not percentage_not_evaluated_trainee_very_satisfied : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_trainer_skills': (nbr_very_satisfied_in_question4/nbr_total_question1)*100, 'response4': 'very_satisfied', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_very_satisfied.write({'response4': 'very_satisfied', 'percentage_trainer_skills':  (nbr_very_satisfied_in_question4/nbr_total_question1)*100})

        else :
            raise ValidationError(_('There are no completed evel for this training.'))
        

    def training_pie_action_trainer_methods(self,training_id):

        
        ########### calculate percentage ###############################################
        #
        nbr_total_question1 = self.env['hr.training'].search([('id', '=', training_id)]).number_of_participants
        nbr_very_dissatisfied_in_question5 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question5','=','very_dissatisfied')])
        nbr_not_so_satisfied_in_question5 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question5','=','not_so_satisfied')])
        nbr_somewhat_satisfied_in_question5 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question5','=','somewhat_satisfied')])
        nbr_satisfied_in_question5 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question5','=','satisfied')])
        nbr_very_satisfied_in_question5 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question5','=','very_satisfied')])
        # 

        #
        
        # ##############################################################################
        if nbr_total_question1 !=  0 :
            percentage_not_evaluated_trainee_very_dissatisfied = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response5', '=', 'very_dissatisfied')])
            if not percentage_not_evaluated_trainee_very_dissatisfied : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_training_methods':(nbr_very_dissatisfied_in_question5/nbr_total_question1)*100 , 'response5': 'very_dissatisfied', 'active_status': True})
            else :
                percentage_not_evaluated_trainee_very_dissatisfied.write({'response5': 'very_dissatisfied', 'percentage_training_methods': (nbr_very_dissatisfied_in_question5/nbr_total_question1)*100})
            ########################################################################################
            percentage_not_evaluated_trainee_not_so_satisfied = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response5', '=', 'not_so_satisfied')])
            if not percentage_not_evaluated_trainee_not_so_satisfied : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_training_methods': (nbr_not_so_satisfied_in_question5/nbr_total_question1)*100, 'response5': 'not_so_satisfied', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_not_so_satisfied.write({'response5': 'not_so_satisfied', 'percentage_training_methods': (nbr_not_so_satisfied_in_question5/nbr_total_question1)*100})

            ##############################################################################################
            percentage_not_evaluated_trainee_somewhat_satisfied = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response5', '=', 'somewhat_satisfied')])
            if not percentage_not_evaluated_trainee_somewhat_satisfied : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_training_methods': (nbr_somewhat_satisfied_in_question5/nbr_total_question1)*100, 'response5': 'somewhat_satisfied', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_somewhat_satisfied.write({'response5': 'not_so_satisfied', 'percentage_training_methods':  (nbr_somewhat_satisfied_in_question5/nbr_total_question1)*100})

            ###################################################################################################
            percentage_not_evaluated_trainee_satisfied = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response5', '=', 'satisfied')])
            if not percentage_not_evaluated_trainee_satisfied : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_training_methods':  (nbr_satisfied_in_question5/nbr_total_question1)*100, 'response5': 'satisfied', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_satisfied.write({'response5': 'satisfied', 'percentage_training_methods':  (nbr_satisfied_in_question5/nbr_total_question1)*100})

            ####################################################################################################
            percentage_not_evaluated_trainee_very_satisfied = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response5', '=', 'very_satisfied')])
            
            if not percentage_not_evaluated_trainee_very_satisfied : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_training_methods': (nbr_very_satisfied_in_question5/nbr_total_question1)*100, 'response5': 'very_satisfied', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_very_satisfied.write({'response5': 'very_satisfied', 'percentage_training_methods':  (nbr_very_satisfied_in_question5/nbr_total_question1)*100})

        else :
            raise ValidationError(_('There are no completed evel for this training.'))



    def training_pie_action_recommandations(self,training_id):
        
        ########### calculate percentage ###############################################
        #
        nbr_total_question1 = self.env['hr.training'].search([('id', '=', training_id)]).number_of_participants
        nbr_very_unlikely_in_question8 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question8','=','very_unlikely')])
        nbr_unlikely_in_question8 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question8','=','unlikely')])
        nbr_neutral_in_question8 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question8','=','neutral')])
        nbr_somewhat_likely_in_question8 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question8','=','somewhat_likely')])
        nbr_very_likely_in_question8 = self.env['evaluation.management'].search_count([('training_id', '=', training_id),('question8','=','very_likely')])
        # 

        #
        
        # ##############################################################################
        if nbr_total_question1 !=  0 :
            percentage_not_evaluated_trainee_very_dissatisfied = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response6', '=', 'very_unlikely')])
            if not percentage_not_evaluated_trainee_very_dissatisfied : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_training_recommandation':(nbr_very_unlikely_in_question8/nbr_total_question1)*100 , 'response6': 'very_unlikely', 'active_status': True})
            else :
                percentage_not_evaluated_trainee_very_dissatisfied.write({'response6': 'very_unlikely', 'percentage_training_recommandation': (nbr_very_unlikely_in_question8/nbr_total_question1)*100})
            ########################################################################################
            percentage_not_evaluated_trainee_not_so_satisfied = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response6', '=', 'unlikely')])
            if not percentage_not_evaluated_trainee_not_so_satisfied : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_training_recommandation': (nbr_unlikely_in_question8/nbr_total_question1)*100, 'response6': 'unlikely', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_not_so_satisfied.write({'response6': 'unlikely', 'percentage_training_recommandation': (nbr_unlikely_in_question8/nbr_total_question1)*100})

            ##############################################################################################
            percentage_not_evaluated_trainee_somewhat_satisfied = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response6', '=', 'neutral')])
            if not percentage_not_evaluated_trainee_somewhat_satisfied : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_training_recommandation': (nbr_neutral_in_question8/nbr_total_question1)*100, 'response6': 'neutral', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_somewhat_satisfied.write({'response6': 'neutral', 'percentage_training_recommandation':  (nbr_neutral_in_question8/nbr_total_question1)*100})

            ###################################################################################################
            percentage_not_evaluated_trainee_satisfied = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response6', '=', 'somewhat_likely')])
            if not percentage_not_evaluated_trainee_satisfied : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_training_recommandation':  (nbr_somewhat_likely_in_question8/nbr_total_question1)*100, 'response6': 'somewhat_likely', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_satisfied.write({'response6': 'somewhat_likely', 'percentage_training_recommandation':  (nbr_somewhat_likely_in_question8/nbr_total_question1)*100})

            ####################################################################################################
            percentage_not_evaluated_trainee_very_satisfied = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response6', '=', 'very_likely')])
            
            if not percentage_not_evaluated_trainee_very_satisfied : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_training_recommandation': (nbr_very_likely_in_question8/nbr_total_question1)*100, 'response6': 'very_likely', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_very_satisfied.write({'response6': 'very_likely', 'percentage_training_recommandation':  (nbr_very_likely_in_question8/nbr_total_question1)*100})

        else :
            raise ValidationError(_('There are no completed evel for this training.'))
        

    def training_pie_action_follow_up_satisfaction(self,training_id):
        
        ########### calculate percentage ###############################################
        #

        nbr_total_question1 = self.env['hr.training'].search([('id', '=', training_id)]).number_of_participants

        nbr_very_dissatisfied_in_question1 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question1','=','very_dissatisfied'),('status_form', '=', 'completed')])
        nbr_not_so_satisfied_in_question1 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question1','=','not_so_satisfied'),('status_form', '=', 'completed')])
        nbr_somewhat_satisfied_in_question1 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question1','=','somewhat_satisfied'),('status_form', '=', 'completed')])
        nbr_satisfied_in_question1 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question1','=','satisfied'),('status_form', '=', 'completed')])
        nbr_very_satisfied_in_question1 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question1','=','very_satisfied'),('status_form', '=', 'completed')])

        # 

        #
        
        # ##############################################################################
        if nbr_total_question1 !=  0 :
            percentage_not_evaluated_trainee_very_dissatisfied = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response7', '=', 'very_dissatisfied')])
            if not percentage_not_evaluated_trainee_very_dissatisfied : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_training_overall_satisfaction_follow_up':(nbr_very_dissatisfied_in_question1/nbr_total_question1)*100 , 'response7': 'very_dissatisfied', 'active_status': True})
            else :
                percentage_not_evaluated_trainee_very_dissatisfied.write({'response7': 'very_dissatisfied', 'percentage_training_overall_satisfaction_follow_up': (nbr_very_dissatisfied_in_question1/nbr_total_question1)*100})
            ########################################################################################
            percentage_not_evaluated_trainee_not_so_satisfied = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response7', '=', 'not_so_satisfied')])
            if not percentage_not_evaluated_trainee_not_so_satisfied : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_training_overall_satisfaction_follow_up': (nbr_not_so_satisfied_in_question1/nbr_total_question1)*100, 'response7': 'not_so_satisfied', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_not_so_satisfied.write({'response7': 'not_so_satisfied', 'percentage_training_overall_satisfaction_follow_up': (nbr_not_so_satisfied_in_question1/nbr_total_question1)*100})

            ##############################################################################################
            percentage_not_evaluated_trainee_somewhat_satisfied = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response7', '=', 'somewhat_satisfied')])
            if not percentage_not_evaluated_trainee_somewhat_satisfied : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_training_overall_satisfaction_follow_up': (nbr_somewhat_satisfied_in_question1/nbr_total_question1)*100, 'response7': 'somewhat_satisfied', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_somewhat_satisfied.write({'response7': 'not_so_satisfied', 'percentage_training_overall_satisfaction_follow_up':  (nbr_somewhat_satisfied_in_question1/nbr_total_question1)*100})

            ###################################################################################################
            percentage_not_evaluated_trainee_satisfied = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response7', '=', 'satisfied')])
            if not percentage_not_evaluated_trainee_satisfied : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_training_overall_satisfaction_follow_up':  (nbr_satisfied_in_question1/nbr_total_question1)*100, 'response7': 'satisfied', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_satisfied.write({'response7': 'satisfied', 'percentage_training_overall_satisfaction_follow_up':  (nbr_satisfied_in_question1/nbr_total_question1)*100})

            ####################################################################################################
            percentage_not_evaluated_trainee_very_satisfied = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response7', '=', 'very_satisfied')])
            
            if not percentage_not_evaluated_trainee_very_satisfied : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'percentage_training_overall_satisfaction_follow_up': (nbr_very_satisfied_in_question1/nbr_total_question1)*100, 'response7': 'very_satisfied', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_very_satisfied.write({'response7': 'very_satisfied', 'percentage_training_overall_satisfaction_follow_up':  (nbr_very_satisfied_in_question1/nbr_total_question1)*100})

        else :
            raise ValidationError(_('There are no completed evel for this training.'))
        
        
    def training_histogram_action_follow_up_other(self,training_id):
        ########### calculate percentage ###############################################
        #

        nbr_total_question1 = self.env['hr.training'].search([('id', '=', training_id)]).number_of_participants

        nbr_strongly_disagree_in_question2 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question2','=','strongly_disagree'),('status_form', '=', 'completed')])
        nbr_disagree_in_question2 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question2','=','disagree'),('status_form', '=', 'completed')])
        nbr_neutral_in_question2 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question2','=','neutral'),('status_form', '=', 'completed')])
        nbr_agree_in_question2 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question2','=','agree'),('status_form', '=', 'completed')])
        nbr_strongly_agree_in_question2 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question2','=','strongly_agree'),('status_form', '=', 'completed')])


        nbr_strongly_disagree_in_question3 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question3','=','strongly_disagree'),('status_form', '=', 'completed')])
        nbr_disagree_in_question3 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question3','=','disagree'),('status_form', '=', 'completed')])
        nbr_neutral_in_question3 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question3','=','neutral'),('status_form', '=', 'completed')])
        nbr_agree_in_question3 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question3','=','agree'),('status_form', '=', 'completed')])
        nbr_strongly_agree_in_question3 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question3','=','strongly_agree'),('status_form', '=', 'completed')])

        nbr_strongly_disagree_in_question4 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question4','=','strongly_disagree'),('status_form', '=', 'completed')])
        nbr_disagree_in_question4 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question4','=','disagree'),('status_form', '=', 'completed')])
        nbr_neutral_in_question4 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question4','=','neutral'),('status_form', '=', 'completed')])
        nbr_agree_in_question4 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question4','=','agree'),('status_form', '=', 'completed')])
        nbr_strongly_agree_in_question4 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question4','=','strongly_agree'),('status_form', '=', 'completed')])


        nbr_strongly_disagree_in_question5 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question5','=','strongly_disagree'),('status_form', '=', 'completed')])
        nbr_disagree_in_question5 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question5','=','disagree'),('status_form', '=', 'completed')])
        nbr_neutral_in_question5 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question5','=','neutral'),('status_form', '=', 'completed')])
        nbr_agree_in_question5 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question5','=','agree'),('status_form', '=', 'completed')])
        nbr_strongly_agree_in_question5 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question5','=','strongly_agree'),('status_form', '=', 'completed')])

        nbr_strongly_disagree_in_question6 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question6','=','strongly_disagree'),('status_form', '=', 'completed')])
        nbr_disagree_in_question6 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question6','=','disagree'),('status_form', '=', 'completed')])
        nbr_neutral_in_question6 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question6','=','neutral'),('status_form', '=', 'completed')])
        nbr_agree_in_question6 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question6','=','agree'),('status_form', '=', 'completed')])
        nbr_strongly_agree_in_question6 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question6','=','strongly_agree'),('status_form', '=', 'completed')])


        nbr_strongly_disagree_in_question7 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question7','=','strongly_disagree'),('status_form', '=', 'completed')])
        nbr_disagree_in_question7 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question7','=','disagree'),('status_form', '=', 'completed')])
        nbr_neutral_in_question7 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question7','=','neutral'),('status_form', '=', 'completed')])
        nbr_agree_in_question7 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question7','=','agree'),('status_form', '=', 'completed')])
        nbr_strongly_agree_in_question7 = self.env['evaluation.trainee'].search_count([('training_id', '=', training_id),('question7','=','strongly_agree'),('status_form', '=', 'completed')])

        # 

        #
        
        #
        if nbr_total_question1 !=  0 :

                        #                  ################################################ Productivity impact #############################################################################################################""

            percentage_not_evaluated_trainee_strongly_disagree1 = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response8', '=', 'strongly_disagree'), ('section', '=', 'Productivity impact')])
            if not percentage_not_evaluated_trainee_strongly_disagree1 : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'section':'Productivity impact','percentage_training_other_follow_up':(nbr_strongly_disagree_in_question2 + nbr_strongly_disagree_in_question3 /nbr_total_question1)*100 , 'response8': 'strongly_disagree', 'active_status': True})
            else :
                percentage_not_evaluated_trainee_strongly_disagree1.write({'response8': 'strongly_disagree','section':'Productivity impact', 'percentage_training_other_follow_up': (nbr_strongly_disagree_in_question2 + nbr_strongly_disagree_in_question3 /nbr_total_question1)*100})
            ########################################################################################
            percentage_not_evaluated_trainee_disagree1 = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response8', '=', 'disagree'),('section', '=', 'Productivity impact')])
            if not percentage_not_evaluated_trainee_disagree1 : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'section':'Productivity impact','percentage_training_other_follow_up': (nbr_disagree_in_question2 + nbr_disagree_in_question3 /nbr_total_question1)*100, 'response8': 'disagree', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_disagree1.write({'response8': 'disagree', 'section':'Productivity impact','percentage_training_other_follow_up': (nbr_disagree_in_question2 + nbr_disagree_in_question3 /nbr_total_question1)*100})

            ##############################################################################################
            percentage_not_evaluated_trainee_neutral1 = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response8', '=', 'neutral'),('section', '=', 'Productivity impact')])
            if not percentage_not_evaluated_trainee_neutral1 : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'section':'Productivity impact','percentage_training_other_follow_up': (nbr_neutral_in_question2 + nbr_neutral_in_question3 / nbr_total_question1)*100, 'response8': 'neutral', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_neutral1.write({'response8': 'neutral', 'section':'Productivity impact','percentage_training_other_follow_up':  (nbr_neutral_in_question2 + nbr_neutral_in_question3 / nbr_total_question1)*100})

            ###################################################################################################
            percentage_not_evaluated_trainee_agree1 = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response8', '=', 'agree'),('section', '=', 'Productivity impact')])
            if not percentage_not_evaluated_trainee_agree1 : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'section':'Productivity impact','percentage_training_other_follow_up':  (nbr_agree_in_question2 + nbr_agree_in_question3 / nbr_total_question1)*100, 'response8': 'agree', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_agree1.write({'response8': 'agree','section':'Productivity impact', 'percentage_training_other_follow_up':  (nbr_agree_in_question2 + nbr_agree_in_question3 / nbr_total_question1)*100})

            ####################################################################################################
            percentage_not_evaluated_trainee_strongly_agree1 = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response8', '=', 'strongly_agree'),('section', '=', 'Productivity impact')])
            
            if not percentage_not_evaluated_trainee_strongly_agree1 : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'section':'Productivity impact','percentage_training_other_follow_up': (nbr_strongly_agree_in_question2 + nbr_strongly_agree_in_question3 /nbr_total_question1)*100, 'response8': 'strongly_agree', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_strongly_agree1.write({'response8': 'strongly_agree', 'section':'Productivity impact','percentage_training_other_follow_up':  (nbr_strongly_agree_in_question2 + nbr_strongly_agree_in_question3 /nbr_total_question1)*100})

            #                  ################################################ Skills development #############################################################################################################""

            percentage_not_evaluated_trainee_strongly_disagree2 = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response8', '=', 'strongly_disagree'),('section', '=', 'Skills development')])
            if not percentage_not_evaluated_trainee_strongly_disagree2 : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'section':'Skills development','percentage_training_other_follow_up':(nbr_strongly_disagree_in_question4 + nbr_strongly_disagree_in_question5 /nbr_total_question1)*100 , 'response8': 'strongly_disagree', 'active_status': True})
            else :
                percentage_not_evaluated_trainee_strongly_disagree2.write({'response8': 'strongly_disagree','section':'Skills development', 'percentage_training_other_follow_up': (nbr_strongly_disagree_in_question4 + nbr_strongly_disagree_in_question5 /nbr_total_question1)*100})
            ########################################################################################
            percentage_not_evaluated_trainee_disagree2 = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response8', '=', 'disagree'),('section', '=', 'Skills development')])
            if not percentage_not_evaluated_trainee_disagree2 : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'section':'Skills development','percentage_training_other_follow_up': (nbr_disagree_in_question4 + nbr_disagree_in_question5 /nbr_total_question1)*100, 'response8': 'disagree', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_disagree2.write({'response8': 'disagree', 'section':'Skills development','percentage_training_other_follow_up': (nbr_disagree_in_question4 + nbr_disagree_in_question5/nbr_total_question1)*100})

            ##############################################################################################
            percentage_not_evaluated_trainee_neutral2 = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response8', '=', 'neutral'),('section', '=', 'Skills development')])
            if not percentage_not_evaluated_trainee_neutral2 : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'section':'Skills development','percentage_training_other_follow_up': (nbr_neutral_in_question4 + nbr_neutral_in_question5 / nbr_total_question1)*100, 'response8': 'neutral', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_neutral2.write({'response8': 'neutral', 'section':'Skills development','percentage_training_other_follow_up':  (nbr_neutral_in_question4 + nbr_neutral_in_question5 / nbr_total_question1)*100})

            ###################################################################################################
            percentage_not_evaluated_trainee_agree2 = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response8', '=', 'agree'),('section', '=', 'Skills development')])
            if not percentage_not_evaluated_trainee_agree2 : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'section':'Skills development','percentage_training_other_follow_up':  (nbr_agree_in_question4 + nbr_agree_in_question5 / nbr_total_question1)*100, 'response8': 'agree', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_agree2.write({'response8': 'agree','section':'Skills development', 'percentage_training_other_follow_up':  (nbr_agree_in_question4 + nbr_agree_in_question5 / nbr_total_question1)*100})

            ####################################################################################################
            percentage_not_evaluated_trainee_strongly_agree2 = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response8', '=', 'strongly_agree'),('section', '=', 'Skills development')])
            
            if not percentage_not_evaluated_trainee_strongly_agree2 : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'section':'Skills development','percentage_training_other_follow_up': (nbr_strongly_agree_in_question4 + nbr_strongly_agree_in_question5 /nbr_total_question1)*100, 'response8': 'strongly_agree', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_strongly_agree2.write({'response8': 'strongly_agree', 'section':'Skills development','percentage_training_other_follow_up':  (nbr_strongly_agree_in_question4 + nbr_strongly_agree_in_question5 /nbr_total_question1)*100})

            #                ################################################ CONTENT #############################################################################################################""

            percentage_not_evaluated_trainee_strongly_disagree3 = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response8', '=', 'strongly_disagree'), ('section', '=', 'Content')])
            if not percentage_not_evaluated_trainee_strongly_disagree3 : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'section':'Content','percentage_training_other_follow_up':(nbr_strongly_disagree_in_question6 + nbr_strongly_disagree_in_question7 /nbr_total_question1)*100 , 'response8': 'strongly_disagree', 'active_status': True})
            else :
                percentage_not_evaluated_trainee_strongly_disagree3.write({'response8': 'strongly_disagree','section':'Content', 'percentage_training_other_follow_up': (nbr_strongly_disagree_in_question6 + nbr_strongly_disagree_in_question7/nbr_total_question1)*100})
            ########################################################################################
            percentage_not_evaluated_trainee_disagree3 = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response8', '=', 'disagree'),('section', '=', 'Content')])
            if not percentage_not_evaluated_trainee_disagree3 : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'section':'Content','percentage_training_other_follow_up': (nbr_disagree_in_question6 + nbr_disagree_in_question7 /nbr_total_question1)*100, 'response8': 'disagree', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_disagree3.write({'response8': 'disagree', 'section':'Content','percentage_training_other_follow_up': (nbr_disagree_in_question6 + nbr_disagree_in_question7/nbr_total_question1)*100})

            ##############################################################################################
            percentage_not_evaluated_trainee_neutral3 = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response8', '=', 'neutral'),('section', '=', 'Content')])
            if not percentage_not_evaluated_trainee_neutral3 : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'section':'Content','percentage_training_other_follow_up': (nbr_neutral_in_question6 + nbr_neutral_in_question7 / nbr_total_question1)*100, 'response8': 'neutral', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_neutral3.write({'response8': 'neutral', 'section':'Content','percentage_training_other_follow_up':  (nbr_neutral_in_question6 + nbr_neutral_in_question7 / nbr_total_question1)*100})

            ###################################################################################################
            percentage_not_evaluated_trainee_agree3 = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response8', '=', 'agree'),('section', '=', 'Content')])
            if not percentage_not_evaluated_trainee_agree3 : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'section':'Content','percentage_training_other_follow_up':  (nbr_agree_in_question6 + nbr_agree_in_question7 / nbr_total_question1)*100, 'response8': 'agree', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_agree3.write({'response8': 'agree','section':'Content', 'percentage_training_other_follow_up':  (nbr_agree_in_question6 + nbr_agree_in_question7 / nbr_total_question1)*100})

            ####################################################################################################
            percentage_not_evaluated_trainee_strongly_agree3 = self.env['evaluation.report.by.training'].search(
                                    [('training_id', '=', training_id), ('response8', '=', 'strongly_agree'),('section', '=', 'Content')])
            
            if not percentage_not_evaluated_trainee_strongly_agree3 : 
                self.env['evaluation.report.by.training'].create(
                                        {'training_id': training_id, 'section':'Content','percentage_training_other_follow_up': (nbr_strongly_agree_in_question6 + nbr_strongly_agree_in_question7 /nbr_total_question1)*100, 'response8': 'strongly_agree', 'active_status': True})
            else:
                percentage_not_evaluated_trainee_strongly_agree3.write({'response8': 'strongly_agree', 'section':'Content','percentage_training_other_follow_up':  (nbr_strongly_agree_in_question6 + nbr_strongly_agree_in_question7 /nbr_total_question1)*100})

        else :
            raise ValidationError(_('There are no completed evel for this training.'))
                

      
    
    def update_status_question_form(self,training_id):
        trainee_evaluated = self.env['hr.trainee'].search([('training',"=",training_id),('Status', '=', 'completed')])
        trainees = self.env['evaluation.trainee'].search([('employee_id', 'in', trainee_evaluated.employee_trainee.ids)])
        for rec in trainees:
            rec.update({'status_form': "completed"})

    def search_training(self):
        training_id = self.training_id
        self.env['hr.trainee'].search([( 'training' , '=', self.training_id.id)]).update({'active_status': True})
        self.env['hr.trainee'].search([( 'training' , '!=', self.training_id.id)]).update({'active_status': False})
        self.env['hr.training'].search([( 'id' , '=', self.training_id.id)]).update({'active_status_training': True})
        self.env['hr.training'].search([( 'id' , '!=', self.training_id.id)]).update({'active_status_training': False})
        self.env['evaluation.report.by.training'].search([( 'training_id' , '!=', self.training_id.id)]).update({'active_status': False}) 
        if training_id :
           self.search([('training_id', '=', training_id.id)]).sudo().unlink()
        self.update_status_question_form(training_id.id)
        self.pie_percentage_evalaution_trainee_function(training_id.id)
        self.pie_chart_of_Training_effective(training_id.id)
        self.training_pie_action_onspot_overall_satisfaction(training_id.id)
        self.training_pie_action_onspot_program_and_duration(training_id.id)
        self.training_pie_action_content(training_id.id)
        self.training_pie_action_trainer_skills(training_id.id)
        self.training_pie_action_trainer_methods(training_id.id)
        self.training_pie_action_recommandations(training_id.id)
        self.training_pie_action_follow_up_satisfaction(training_id.id)
        self.training_histogram_action_follow_up_other(training_id.id)


        return {
                'name': _('Training Dashboard'),
                'type': 'ir.actions.act_window',
                'res_model': 'board.board',
                'view_mode': 'form',
                "views": [[self.env.ref('Training_Management.board_training_dash_view').id, "form"]],     
            }
    