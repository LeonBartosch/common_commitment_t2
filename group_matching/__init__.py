from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'group_matching'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# DEFS
def group_by_arrival_time_method(player, waiting_players):
    if len(waiting_players) >= 4:
        p1 = waiting_players[0]
        p2 = waiting_players[1]
        p3 = waiting_players[2]
        p4 = waiting_players[3]
        import random
        treatment = random.choice(['cc_game', 'ic_game'])
        p1.participant.treatment = treatment
        p2.participant.treatment = treatment
        p3.participant.treatment = treatment
        p4.participant.treatment = treatment
        return [p1, p2, p3, p4]


# PAGES


class GroupingWaitPage(WaitPage):
    group_by_arrival_time = True
    def vars_for_template(player):
        return {'body_text': 'Sobald drei weitere Personen eingetroffen sind, geht es los.',
                'title_text': 'Bitte warten Sie.'}

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.participant.treatment == 'ic_game':
            return "ic_game"



page_sequence = [GroupingWaitPage]
