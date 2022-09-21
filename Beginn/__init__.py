from otree.api import *


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
    einverstaendnis = models.BooleanField(blank=True)
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
    form_model = 'player'
    form_fields = ['einverstaendnis']

    @staticmethod
    def error_message(player, values):
        if values['einverstaendnis'] is not True:
            return 'Sie müssen die Teilnahmebedingungen akzeptieren, um an der Studie teilnehmen zu können.'
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        #with open('LabIds/Participated.txt', 'a') as file:
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

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


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



page_sequence = [Begruessung, Informedconsent, Einwilligung, Code_Eingabe, Ueberleitung,
                 Pgg_scenario1, Pgg_scenario2, Pgg_scenario3]
