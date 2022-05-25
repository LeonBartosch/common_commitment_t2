from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Ende'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    time_end = models.StringField()
    effort = models.IntegerField(
        choices=[
            [1, 'fast keine'],
            [2, 'sehr wenig'],
            [3, 'etwas'],
            [4, 'ziemlich viel'],
            [5, 'sehr viel'],
        ],
        widget=widgets.RadioSelect
    )
    attention = models.IntegerField(
        choices=[
            [1, 'fast keine'],
            [2, 'sehr wenig meiner'],
            [3, 'etwas meiner'],
            [4, 'die meiste meiner'],
            [5, 'meine volle'],
        ],
        widget=widgets.RadioSelect
    )
    use_data = models.BooleanField(
        choices=[
            [True, 'Ja'],
            [False, 'Nein'],
        ]
    )
    comments = models.LongStringField(
        label='',
        blank=True
    )
    study_completed = models.BooleanField(initial=False)
    srsn_check_pass = models.BooleanField(initial=False)


# PAGES
class Seriousness_check(Page):
    form_model = 'player'
    form_fields = ['effort', 'attention', 'use_data']

    def before_next_page(player, timeout_happened):
        player.study_completed = True
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        if player.effort == 5 and player.attention == 5 and player.use_data:
            player.srsn_check_pass = True
        with open('LabIds/CountParticipation.txt', 'r') as file:
            txt = int(file.read())
            print(txt)
            txt += 1
            print(txt)
        if (player.participant.label != "1234555"):
            if player.srsn_check_pass & player.use_data:
                with open('LabIds/CountParticipation.txt', 'w') as file:
                    file.write(str(txt))


class Debriefing(Page):
    form_model = 'player'
    form_fields = ['comments']
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class Endpage(Page):
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


page_sequence = [Seriousness_check, Debriefing, Endpage]
