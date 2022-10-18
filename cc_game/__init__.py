from otree.api import *
import csv
from otree.models import group


class C(BaseConstants):
    NAME_IN_URL = 'cc_condition'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 1
    ENDOWMENT = cu(800)
    MULTIPLIER = 2
    Eigenanteil = MULTIPLIER/4*100
    P1_ROLE = 'Person A'
    P2_ROLE = 'Person B'
    P3_ROLE = 'Person C'
    P4_ROLE = 'Person D'



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()
    public_good_total = models.CurrencyField()
    lowest_proposer = models.StringField()
    lowest_proposal = models.CurrencyField()
    num_negotiators = models.FloatField()
    num_contributed = models.FloatField()


class Player(BasePlayer):
    sim_a_participation = models.IntegerField(choices=[[1, 'Ja'], [2, 'Nein'], ])
    sim_b_participation = models.IntegerField(choices=[[1, 'Ja'], [2, 'Nein'], ])
    sim_c_participation = models.IntegerField(choices=[[1, 'Ja'], [2, 'Nein'], ])
    sim_d_participation = models.IntegerField(choices=[[1, 'Ja'], [2, 'Nein'], ])
    sim_a_commitment = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    sim_b_commitment = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    sim_c_commitment = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    sim_d_commitment = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    sim_a_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)
    sim_b_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)
    sim_c_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)
    sim_d_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT)
    compr_check_a_pass = models.BooleanField(
        initial=False)
    compr_a1 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr_a2 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr_a3 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr_a4 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr_a5 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr_a6 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr2_a1 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr2_a2 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr2_a3 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr2_a4 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr2_a5 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr2_a6 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr3_a1 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr3_a2 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr3_a3 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr3_a4 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr3_a5 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr3_a6 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr_check_b_pass = models.BooleanField(
        initial=False)
    compr_b1 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr_b2 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr_b3 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr_b4 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr2_b1 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr2_b2 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr2_b3 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr2_b4 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr3_b1 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr3_b2 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr3_b3 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    compr3_b4 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    verhandlungsziel = models.CurrencyField(
        min=0, max=C.ENDOWMENT,
        label="Wie hoch sollte der Mindestbeitrag (in Cent) in der folgenden Verhandlung am Ende ausfallen? "
    )
    contribution = models.CurrencyField(min=0, max=C.ENDOWMENT,
                                        label="Bitte geben sie den Betrag (in Cent) an, den sie beisteuern wollen:"
    )
    contribution_check = models.BooleanField(
        initial=False
    )
    last_proposal = models.CurrencyField(min=0,
        max=C.ENDOWMENT, label="Dieser Wert sollte der Mindestbeitrag (in Cent) für alle Verhandlungsteilnehmer*innen sein:"
    )
    teilnahme = models.BooleanField(
        choices=[[True, 'Ja'], [False, 'Nein'], ],
        label="Möchten Sie an der Verhandlung über einen gemeinsamen Mindestbeitrag teilnehmen?"
    )
    willingness = models.FloatField(min=0, max=100)
    time_end = models.StringField()
    filler_motives = models.LongStringField(
        label='Bitte beschreiben Sie hier, warum Sie sich gegen eine Teilnahme an der Verhandlung entschieden haben:',
        blank=True,
    )
    beliefs = models.IntegerField(choices=[-1, 0, 1, 2, 3],)
    T2_payoff = models.CurrencyField()
    T1_payoff = models.CurrencyField()


class Minimum(ExtraModel):
    player = models.Link(Player)
    amount = models.CurrencyField()
    time = models.StringField()


# FUNCTIONS
def group_by_arrival_time_method(player, waiting_players):
    if len(waiting_players) >= 4:
        p1 = waiting_players[0]
        p2 = waiting_players[1]
        p3 = waiting_players[2]
        p4 = waiting_players[3]
        return [p1, p2, p3, p4]

def custom_export(players):
    # header row
    yield ['session', 'group', 'id_in_group', 'participant', 'amount', 'time']
    for p in players:
        GroupMinimum = Minimum.filter(player=p)
        participant = p.participant
        session = p.session
        group = p.group
        yield [session.code, group.code, p.id_in_group, participant.code, GroupMinimum.amount, GroupMinimum.time]

def set_minimum(group):
    players = group.get_players()
    group.lowest_proposal = 800
    group.lowest_proposer = ""
    for p in players:
        if p.teilnahme:
            if p.last_proposal < group.lowest_proposal:
                group.lowest_proposal = p.last_proposal
                if group.lowest_proposer== "":
                    group.lowest_proposer = "Person "+ str(p.id_in_group)
                else:
                    group.lowest_proposer += " und Person " + str(p.id_in_group)


def set_payoffs(group: Group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)
    group.public_good_total = (
        group.total_contribution * C.MULTIPLIER
    )
    group.individual_share = (
        group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP
    )
    for p in players:
        p.T2_payoff = C.ENDOWMENT - p.contribution + group.individual_share


def set_participants(group: Group):
    players = group.get_players()
    group.num_negotiators = 0
    for p in players:
        if p.teilnahme:
            group.num_negotiators += 1

def set_contributors(group: Group):
    players = group.get_players()
    group.num_contributed = 0
    for p in players:
        if p.contribution_check:
            group.num_contributed += 1


# PAGES
class CC_GroupingWaitPage(WaitPage):
    group_by_arrival_time = True
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

class CC_instructions(Page):
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class CC_example(Page):
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class Sim_CC(Page):
    form_model = 'player'
    form_fields = ['sim_a_participation', 'sim_b_participation', 'sim_c_participation', 'sim_d_participation',
                   'sim_a_commitment', 'sim_b_commitment', 'sim_c_commitment', 'sim_d_commitment',
                   'sim_a_contribution', 'sim_b_contribution', 'sim_c_contribution', 'sim_d_contribution']

    @staticmethod
    def error_message(player: Player, values):
        if values['sim_a_contribution'] % 10 != 0 or values['sim_b_contribution'] % 10 != 0 \
                or values['sim_c_contribution'] % 10 != 0 or values['sim_d_contribution'] % 10 != 0:
            return 'Bitte geben Sie durch 10 teilbare Beiträge an.'

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

class CC_compr_check_a(Page):
    form_model = 'player'
    form_fields = ['compr_a1', 'compr_a2', 'compr_a3', 'compr_a4', 'compr_a5', 'compr_a6']

    @staticmethod
    def error_message(player, values):
        if values['compr_a1'] is None or values['compr_a2'] is None or values['compr_a3'] is None \
                or values['compr_a4'] is None or values['compr_a5'] is None or values['compr_a6'] is None:
            return 'Bitte füllen Sie alle Felder aus.'

    def before_next_page(player, timeout_happened):
        if player.compr_a1 == 300 and player.compr_a2 == 300 and player.compr_a3 == 800 and player.compr_a4 == 300 \
                and player.compr_a5 == 100 and player.compr_a6 == 500:
            player.compr_check_a_pass = True
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class CC_compr_check2_a(Page):
    form_model = 'player'
    form_fields = ['compr2_a1', 'compr2_a2', 'compr2_a3', 'compr2_a4', 'compr2_a5', 'compr2_a6']

    @staticmethod
    def is_displayed(player):
        return player.compr_check_a_pass == False

    def error_message(player, values):
        if (values['compr2_a1'] is None and player.compr_a1 != 300) \
                or (values['compr2_a2'] is None and player.compr_a2 != 300) \
                or (values['compr2_a3'] is None and player.compr_a3 != 800) \
                or (values['compr2_a4'] is None and player.compr_a4 != 300) \
                or (values['compr2_a5'] is None and player.compr_a5 != 100) \
                or (values['compr2_a6'] is None and player.compr_a6 != 500):
            return 'Bitte füllen Sie alle Felder aus.'

    def before_next_page(player, timeout_happened):
        if (player.compr_a1 == 300 or player.compr2_a1 == 300) \
                and (player.compr_a2 == 300 or player.compr2_a2 == 300) \
                and (player.compr_a3 == 800 or player.compr2_a3 == 800) \
                and (player.compr_a4 == 300 or player.compr2_a4 == 300) \
                and (player.compr_a5 == 100 or player.compr2_a5 == 100) \
                and (player.compr_a6 == 500 or player.compr2_a6 == 500):
            player.compr_check_a_pass = True
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class CC_compr_check3_a(Page):
    form_model = 'player'
    form_fields = ['compr3_a1', 'compr3_a2', 'compr3_a3', 'compr3_a4', 'compr3_a5', 'compr3_a6']

    @staticmethod
    def is_displayed(player):
        return player.compr_check_a_pass == False

    def error_message(player, values):
        if (values['compr3_a1'] is None and player.compr_a1 != 300 and player.compr2_a1 != 300) \
                or (values['compr3_a2'] is None and player.compr_a2 != 300 and player.compr2_a2 != 300) \
                or (values['compr3_a3'] is None and player.compr_a3 != 800 and player.compr2_a3 != 800) \
                or (values['compr3_a4'] is None and player.compr_a4 != 300 and player.compr2_a4 != 300) \
                or (values['compr3_a5'] is None and player.compr_a5 != 100 and player.compr2_a5 != 100) \
                or (values['compr3_a6'] is None and player.compr_a6 != 500 and player.compr2_a6 != 500):
            return 'Bitte füllen Sie alle Felder aus.'

    def before_next_page(player, timeout_happened):
        if (player.compr_a1 == 300 or player.compr2_a1 == 300 or player.compr3_a1 == 300) \
                and (player.compr_a2 == 300 or player.compr2_a2 == 300 or player.compr3_a2 == 300) \
                and (player.compr_a3 == 800 or player.compr2_a3 == 800 or player.compr3_a3 == 800) \
                and (player.compr_a4 == 300 or player.compr2_a4 == 300 or player.compr3_a4 == 300) \
                and (player.compr_a5 == 100 or player.compr2_a5 == 100 or player.compr3_a5 == 100) \
                and (player.compr_a6 == 500 or player.compr2_a6 == 500 or player.compr3_a6 == 500):
            player.compr_check_a_pass = True
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

class CC_compr_check_b(Page):
    form_model = 'player'
    form_fields = ['compr_b1', 'compr_b2', 'compr_b3', 'compr_b4']

    @staticmethod
    def error_message(player, values):
        if values ['compr_b1'] is None or values ['compr_b2'] is None or values ['compr_b3'] is None \
                or values ['compr_b4'] is None:
            return 'Bitte füllen Sie alle Felder aus'
    def before_next_page(player, timeout_happened):
        if player.compr_b1 == 200 and player.compr_b2 == 0 and player.compr_b3 == 800 and player.compr_b4 == 100:
            player.compr_check_b_pass = True
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class CC_compr_check2_b(Page):
    form_model = 'player'
    form_fields = ['compr2_b1', 'compr2_b2', 'compr2_b3', 'compr2_b4']

    @staticmethod
    def is_displayed(player):
        return player.compr_check_b_pass == False
    def error_message(player, values):
        if (values ['compr2_b1'] is None and player.compr_b1 != 200)\
                or (values ['compr2_b2'] is None and player.compr_b2 != 0) \
                or (values ['compr2_b3'] is None and player.compr_b3 != 800) \
                or (values ['compr2_b4'] is None and player.compr_b4 != 100):
            return 'Bitte füllen Sie alle Felder aus'
    def before_next_page(player, timeout_happened):
        if (player.compr_b1 == 200 or player.compr2_b1 == 200) and (player.compr_b2 == 0 or player.compr2_b2 == 0) \
                and (player.compr_b3 == 800 or player.compr2_b3 == 800) and (player.compr_b4 == 100 or player.compr2_b4 == 100):
            player.compr_check_b_pass = True
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class CC_compr_check3_b(Page):
    form_model = 'player'
    form_fields = ['compr3_b1', 'compr3_b2', 'compr3_b3', 'compr3_b4']

    @staticmethod
    def is_displayed(player):
        return player.compr_check_b_pass == False
    def error_message(player, values):
        if (values ['compr3_b1'] is None and player.compr_b1 != 200 and player.compr2_b1 != 200)\
                or (values ['compr3_b2'] is None and player.compr_b2 != 0 and player.compr2_b2 != 0) \
                or (values ['compr3_b3'] is None and player.compr_b3 != 800 and player.compr2_b3 != 800) \
                or (values ['compr3_b4'] is None and player.compr_b4 != 100 and player.compr2_b4 != 100):
            return 'Bitte füllen Sie alle Felder aus'
    def before_next_page(player, timeout_happened):
        if (player.compr_b1 == 200 or player.compr2_b1 == 200 or player.compr3_b1 == 200)\
                and (player.compr_b2 == 0 or player.compr2_b2 == 0 or player.compr3_b2 == 0) \
                and (player.compr_b3 == 800 or player.compr2_b3 == 800 or player.compr3_b3 == 800) \
                and (player.compr_b4 == 100 or player.compr2_b4 == 100 or player.compr3_b4 == 100):
            player.compr_check_b_pass = True
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class Verhandlungsteilnahme(Page):
    form_model = 'player'
    form_fields = ['teilnahme', 'willingness']
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

class Beliefs(Page):
    form_model = 'player'
    form_fields = ['beliefs']
    def error_message(player: Player, values):
        if values['beliefs'] == -1:
            return "Bitte wählen Sie eine Anzahl zwischen 0 und 3 Personen aus"
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

class Verhandlungsziel_Waitpage(WaitPage):
    after_all_players_arrive = set_participants
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class CC_Verhandlungsziel(Page):
    form_model = 'player'
    form_fields =['verhandlungsziel']

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    @staticmethod
    def is_displayed(player):
        return player.teilnahme == True and player.group.num_negotiators >= 2
    @staticmethod
    def error_message(player, values):
        if values['verhandlungsziel'] is None:
            return 'Sie müssen Ihr Verhandlungsziel angeben.'
        if values['verhandlungsziel'] % 10 != 0:
            return 'Bitte geben Sie einen durch 10 teilbaren Betrag ein.'


class Chat_Waitpage(WaitPage):
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    @staticmethod
    def is_displayed(player):
        return player.teilnahme == True and player.group.num_negotiators >= 2

class CC_Chat(Page):
    timeout_seconds = 180
    timer_text = 'Verbleibende Verhandlungs-Zeit:'
    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            p1_participated = player.group.get_player_by_id(1).teilnahme,
            p2_participated = player.group.get_player_by_id(2).teilnahme,
            p3_participated = player.group.get_player_by_id(3).teilnahme,
            p4_participated = player.group.get_player_by_id(4).teilnahme
        )

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    @staticmethod
    def is_displayed(player):
        return player.teilnahme == True and player.group.num_negotiators >= 2

    @staticmethod
    def live_method(player, bid):
        import datetime
        import csv
        with open('_static/chat/cc_chat.csv', mode='a') as csvfile:
            chat = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            chat.writerow(
                [player.session.code, player.group.id_in_subsession, player.id_in_group,
                 player.participant.personal_code,
                 datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"), bid]
            )
        # with open('_static/chat/cc_chat.csv', mode='r+') as file:
        # lines = file.readlines()
        # file.seek(0)
        # file.truncate()
        # file.writelines(lines[:-1])
        my_id = player.id_in_group
        response = dict(id_in_group=my_id, bid=bid)
        time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        Minimum.create(player=player, amount=bid, time=time)
        return {0: response}

    @staticmethod
    def js_vars(player: Player):
        return dict(
            player_id=player.id_in_group
        )


class One_neg(Page):
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    @staticmethod
    def is_displayed(player):
        return player.group.num_negotiators == 1


class No_neg(Page):
    @staticmethod
    def is_displayed(player):
        return player.group.num_negotiators == 0
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class Last_proposal(Page):
    form_model = 'player'
    form_fields = ['last_proposal']

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    def error_message(player, values):
        if values['last_proposal'] is None:
            return 'Sie müssen einen Betrag angeben.'
        if values['last_proposal'] % 10 != 0:
            return 'Bitte geben Sie einen durch 10 teilbaren Betrag ein.'

    @staticmethod
    def is_displayed(player):
        return player.teilnahme == True and player.group.num_negotiators >= 2


class Proposal_waitpage(WaitPage):
    after_all_players_arrive = set_minimum

    @staticmethod
    def is_displayed(player):
        return player.teilnahme == True and player.group.num_negotiators >= 2

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']

    @staticmethod
    def error_message(player, values):
        if values['contribution'] is None:
            return 'Sie müssen Ihren Beitrag angeben.'
        if player.teilnahme and player.group.num_negotiators >= 2:
            if (values['contribution'] < player.group.lowest_proposal):
                return 'Sie dürfen nicht weniger als den Mindestbeitrag angeben.'
        if values['contribution'] % 10 != 0:
            return 'Bitte geben Sie einen durch 10 teilbaren Betrag ein.'

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            p1_participated=player.group.get_player_by_id(1).teilnahme,
            p2_participated=player.group.get_player_by_id(2).teilnahme,
            p3_participated=player.group.get_player_by_id(3).teilnahme,
            p4_participated=player.group.get_player_by_id(4).teilnahme
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.contribution != None:
            player.contribution_check = True
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        set_contributors(player.group)


class Filler_task(Page):
    form_model = 'player'
    form_fields = ['filler_motives']

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    @staticmethod
    def is_displayed(player):
        return player.teilnahme == False and player.group.num_negotiators >= 2


class ResultsWaitPage(WaitPage):
    template_name = 'cc_game/ResultsWaitPage.html'
    #after_all_players_arrive = set_payoffs

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    @staticmethod
    def is_displayed(player):
        return player.group.num_contributed < 4


class Results(Page):
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    @staticmethod
    def vars_for_template(player: Player):
        set_payoffs(player.group)
        with open('payoffs_T1.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                if row[0] == player.participant.personal_code:
                    T1_payoff = cu(row[1])
                    T1_payoff_euro = cu(row[1]).to_real_world_currency(player.session)
                    T2_payoff_euro = cu(player.T2_payoff).to_real_world_currency(player.session)
        player.participant.payoff = T1_payoff + player.T2_payoff
        player.T1_payoff = T1_payoff
        return dict(
            others=player.get_others_in_group(),
            T1_payoff_euro=T1_payoff_euro,
            T2_payoff_euro = T2_payoff_euro
        )

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.participant.treatment == 'cc_game':
            return "Ende"


page_sequence = [
    CC_GroupingWaitPage,
    CC_instructions,
    CC_example,
    Sim_CC,
    CC_compr_check_a,
    CC_compr_check2_a,
    CC_compr_check3_a,
    CC_compr_check_b,
    CC_compr_check2_b,
    CC_compr_check3_b,
    Verhandlungsteilnahme,
    Beliefs,
    Verhandlungsziel_Waitpage,
    CC_Verhandlungsziel,
    Chat_Waitpage,
    CC_Chat,
    One_neg,
    No_neg,
    Last_proposal,
    Proposal_waitpage,
    Contribute,
    Filler_task,
    ResultsWaitPage,
    Results
]

