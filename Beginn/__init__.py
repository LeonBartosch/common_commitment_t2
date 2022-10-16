from otree.api import *
from string import digits
from string import ascii_letters

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Beginn'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
#    einverstaendnis = models.BooleanField(blank=True)
    time_end = models.StringField()
    code = models.StringField(label="")

# PAGES
class Begruessung(Page):
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class Informedconsent(Page):
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class Einwilligung(Page):
#    form_model = 'player'
#    form_fields = ['einverstaendnis']

    @staticmethod
#    def error_message(player, values):
#        if values['einverstaendnis'] is not True:
#            return 'Sie müssen die Teilnahmebedingungen akzeptieren, um an der Studie teilnehmen zu können.'
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        #with open('_static/Participated.txt', 'a') as file:
            #if(player.participant.label != "1234555"):
                #file.write('\n')
                #file.write(player.participant.label)


class Code_Eingabe(Page):
    form_model = 'player'
    form_fields = ['code']

    @staticmethod
    def error_message(player, values):
        if len(values['code']) !=6:
            return 'Ihr Code muss sechsstellig sein'
        with open('_static/Participated.txt', 'r') as file:
            txt = file.read()
        if (values['code'] not in txt and values['code'] != "123456"):
            return "Bitte überprüfen Sie Ihren Code und geben Sie den Code wie in Studienteil 1 an."

        if any([c not in digits for c in values['code'][4:6]]):
            return "Bitte geben Sie Ihren Code im korrekten Format an"

        if any([c not in ascii_letters for c in values['code'][0:4]]):
            return "Bitte geben Sie Ihren Code im korrekten Format an"

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        player.participant.personal_code = player.code


class Ueberleitung(Page):
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class Pgg_instructions(Page):
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class Pgg_scenario1(Page):
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class Pgg_scenario2(Page):
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class Pgg_scenario3(Page):
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")



page_sequence = [
#    Begruessung,
#    Informedconsent,
    Code_Eingabe,
#    Ueberleitung,
#    Pgg_instructions,
#    Pgg_scenario1,
#    Pgg_scenario2,
#    Pgg_scenario3
           ]
