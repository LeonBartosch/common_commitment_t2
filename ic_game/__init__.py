from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'ic_game'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 1
    ENDOWMENT = cu(100)
    MULTIPLIER = 2
    Eigenanteil = MULTIPLIER / 4 * 100
    P1_ROLE = 'Spieler*in A'
    P2_ROLE = 'Spieler*in B'
    P3_ROLE = 'Spieler*in C'
    P4_ROLE = 'Spieler*in D'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()
    public_good_total = models.CurrencyField()
    lowest_proposer = models.StringField()
    lowest_proposal = models.CurrencyField()
    ic_num_negotiators = models.FloatField()


class Player(BasePlayer):
    ic_compr_a1 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    ic_compr_a2 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    ic_compr_a3 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    ic_compr_a4 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    ic_compr2_a1 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    ic_compr2_a2 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    ic_compr2_a3 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    ic_compr2_a4 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    ic_compr3_a1 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    ic_compr3_a2 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    ic_compr3_a3 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    ic_compr3_a4 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    ic_compr_check_a_pass = models.BooleanField(
        initial=False)
    ic_compr_b1 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    ic_compr_b2 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    ic_compr_b3 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    ic_compr2_b1 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    ic_compr2_b2 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    ic_compr2_b3 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    ic_compr3_b1 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    ic_compr3_b2 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    ic_compr3_b3 = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    ic_compr_check_b_pass = models.BooleanField(
        initial=False)
    verhandlungsziel = models.CurrencyField(
        min=0, max=C.ENDOWMENT,
        label="Welchen Wert würden Sie gerne als persönlichen Mindestbeitrag in der folgenden Verhandlung erreichen?"
    )
    contribution = models.CurrencyField(min=0, max=C.ENDOWMENT,
                                        label="Bitte geben sie den Betrag an, den sie beisteuern wollen:"
                                        )
    last_proposal = models.CurrencyField(
        max=C.ENDOWMENT, label="Dieser Wert ist mein Mindestbeitrag:"
    )
    time_end = models.StringField()
    willingness = models.FloatField(min=0, max=100)
    teilnahme = models.BooleanField(
        choices=[[True, 'Ja'], [False, 'Nein'], ],
        label="Möchten Sie an der Verhandlung über einen gemeinsamen Mindestbeitrag teilnehmen?"
    )

class Minimum(ExtraModel):
    player = models.Link(Player)
    amount = models.CurrencyField()
    time = models.StringField()


# FUNCTIONS
def custom_export(players):
    # header row
    yield ['session', 'group', 'id_in_group', 'participant', 'amount', 'time']
    for p in players:
        GroupMinimum = Minimum.filter(player=p)
        participant = p.participant
        session = p.session
        group = p.group
        yield [session.code, group.code, p.id_in_group, participant.code, GroupMinimum.amount, GroupMinimum.time]


def set_participants(group: Group):
    players = group.get_players()
    group.ic_num_negotiators = 0
    for p in players:
        if p.teilnahme:
            group.ic_num_negotiators += 1


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
        p.payoff = C.ENDOWMENT - p.contribution + group.individual_share


# PAGES
class IC_instructions(Page):
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class IC_example(Page):
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class IC_compr_check_a(Page):
    form_model = 'player'
    form_fields = ['ic_compr_a1', 'ic_compr_a2', 'ic_compr_a3', 'ic_compr_a4']

    @staticmethod
    def error_message(player, values):
        if values['ic_compr_a1'] is None or values['ic_compr_a2'] is None or values['ic_compr_a3'] is None \
                or values['ic_compr_a4'] is None:
            return 'Bitte füllen Sie alle Felder aus.'

    def before_next_page(player, timeout_happened):
        if player.ic_compr_a1 == 30 and player.ic_compr_a2 == 80 and player.ic_compr_a3 == 100 \
                and player.ic_compr_a4 == 50:
            player.ic_compr_check_a_pass = True
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class IC_compr_check2_a(Page):
    form_model = 'player'
    form_fields = ['ic_compr2_a1', 'ic_compr2_a2', 'ic_compr2_a3', 'ic_compr2_a4']

    @staticmethod
    def is_displayed(player):
        return player.ic_compr_check_a_pass == False

    def error_message(player, values):
        if (values['ic_compr2_a1'] is None and player.ic_compr_a1 != 30) \
                or (values['ic_compr2_a2'] is None and player.ic_compr_a2 != 80) \
                or (values['ic_compr2_a3'] is None and player.ic_compr_a3 != 100) \
                or (values['ic_compr2_a4'] is None and player.ic_compr_a4 != 50):
            return 'Bitte füllen Sie alle Felder aus.'

    def before_next_page(player, timeout_happened):
        if (player.ic_compr_a1 == 30 or player.ic_compr2_a1 == 30) \
                and (player.ic_compr_a2 == 80 or player.ic_compr2_a2 == 80) \
                and (player.ic_compr_a3 == 100 or player.ic_compr2_a3 == 100) \
                and (player.ic_compr_a4 == 50 or player.ic_compr2_a4 == 50):
            player.ic_compr_check_a_pass = True
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class IC_compr_check3_a(Page):
    form_model = 'player'
    form_fields = ['ic_compr3_a1', 'ic_compr3_a2', 'ic_compr3_a3', 'ic_compr3_a4']

    @staticmethod
    def is_displayed(player):
        return player.ic_compr_check_a_pass == False

    def error_message(player, values):
        if (values['ic_compr3_a1'] is None and player.ic_compr_a1 != 30 and player.ic_compr2_a1 != 30) \
                or (values['ic_compr3_a2'] is None and player.ic_compr_a2 != 80 and player.ic_compr2_a2 != 80) \
                or (values['ic_compr3_a3'] is None and player.ic_compr_a3 != 100 and player.ic_compr2_a3 != 100) \
                or (values['ic_compr3_a4'] is None and player.ic_compr_a4 != 50 and player.ic_compr2_a4 != 50):
            return 'Bitte füllen Sie alle Felder aus.'

    def before_next_page(player, timeout_happened):
        if (player.ic_compr_a1 == 30 or player.ic_compr2_a1 == 30 or player.ic_compr3_a1 == 30) \
                and (player.ic_compr_a2 == 80 or player.ic_compr2_a2 == 80 or player.ic_compr3_a2 == 80) \
                and (player.ic_compr_a3 == 100 or player.ic_compr2_a3 == 100 or player.ic_compr3_a3 == 100) \
                and (player.ic_compr_a4 == 50 or player.ic_compr2_a4 == 50 or player.ic_compr3_a4 == 50):
            player.ic_compr_check_a_pass = True
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class IC_compr_check_b(Page):
    form_model = 'player'
    form_fields = ['ic_compr_b1', 'ic_compr_b2', 'ic_compr_b3']

    @staticmethod
    def error_message(player, values):
        if values['ic_compr_b1'] is None or values['ic_compr_b2'] is None or values['ic_compr_b3'] is None:
            return 'Bitte füllen Sie alle Felder aus.'

    def before_next_page(player, timeout_happened):
        if player.ic_compr_b1 == 80 and player.ic_compr_b2 == 0 and player.ic_compr_b3 == 100:
            player.ic_compr_check_b_pass = True
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class IC_compr_check2_b(Page):
    form_model = 'player'
    form_fields = ['ic_compr2_b1', 'ic_compr2_b2', 'ic_compr2_b3']

    @staticmethod
    def is_displayed(player):
        return player.ic_compr_check_b_pass == False

    def error_message(player, values):
        if (values['ic_compr2_b1'] is None and player.ic_compr_b1 != 80) \
                or (values['ic_compr2_b2'] is None and player.ic_compr_b2 != 0) \
                or (values['ic_compr2_b3'] is None and player.ic_compr_b3 != 100):
            return 'Bitte füllen Sie alle Felder aus.'

    def before_next_page(player, timeout_happened):
        if (player.ic_compr_b1 == 80 or player.ic_compr2_b1 == 80) \
                and (player.ic_compr_b2 == 0 or player.ic_compr2_b2 == 0) \
                and (player.ic_compr_b3 == 100 or player.ic_compr2_b3 == 100):
            player.ic_compr_check_b_pass = True
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class IC_compr_check3_b(Page):
    form_model = 'player'
    form_fields = ['ic_compr3_b1', 'ic_compr3_b2', 'ic_compr3_b3']

    @staticmethod
    def is_displayed(player):
        return player.ic_compr_check_b_pass == False

    def error_message(player, values):
        if (values['ic_compr3_b1'] is None and player.ic_compr_b1 != 80 and player.ic_compr2_b1 != 80) \
                or (values['ic_compr3_b2'] is None and player.ic_compr_b2 != 0 and player.ic_compr2_b2 != 0) \
                or (values['ic_compr3_b3'] is None and player.ic_compr_b3 != 100 and player.ic_compr2_b3 != 100):
            return 'Bitte füllen Sie alle Felder aus.'

    def before_next_page(player, timeout_happened):
        if (player.ic_compr_b1 == 80 or player.ic_compr2_b1 == 80 or player.ic_compr3_b1 == 80) \
                and (player.ic_compr_b2 == 0 or player.ic_compr2_b2 == 0 or player.ic_compr3_b2 == 0) \
                and (player.ic_compr_b3 == 100 or player.ic_compr2_b3 == 100 or player.ic_compr3_b3 == 100):
            player.ic_compr_check_b_pass = True
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class Verhandlungsteilnahme(Page):
    form_model = 'player'
    form_fields = ['teilnahme', 'willingness']
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class Verhandlungsziel_Waitpage(WaitPage):
    after_all_players_arrive = set_participants
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class IC_Verhandlungsziel(Page):
    form_model = 'player'
    form_fields =['verhandlungsziel']

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    @staticmethod
    def is_displayed(player):
        return player.teilnahme == True and player.group.ic_num_negotiators >= 2
    @staticmethod
    def error_message(player, values):
        if values['verhandlungsziel'] is None:
            return 'Sie müssen Ihr Verhandlungsziel angeben.'
        if values['verhandlungsziel'] % 2 != 0:
            return 'Bitte geben Sie einen geraden Betrag ein.'



class Chat_Waitpage(WaitPage):
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class IC_Chat(Page):
    timeout_seconds = 60
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
        return player.teilnahme == True and player.group.ic_num_negotiators >= 2

    @staticmethod
    def live_method(player, bid):
        my_id = player.id_in_group
        response = dict(id_in_group=my_id, bid=bid)
        import datetime
        time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        Minimum.create(player=player, amount=bid, time=time)
        return {0: response}

    @staticmethod
    def js_vars(player: Player):
        return dict(
            player_id=player.id_in_group
        )


class IC_One_neg(Page):
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    @staticmethod
    def is_displayed(player):
        return player.group.ic_num_negotiators == 1


class No_neg(Page):
    @staticmethod
    def is_displayed(player):
        return player.group.ic_num_negotiators == 0
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class IC_Last_proposal(Page):
    form_model = 'player'
    form_fields = ['last_proposal']

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    def error_message(player, values):
        if values['last_proposal'] is None:
            return 'Sie müssen einen Betrag angeben.'
        if values['last_proposal'] % 2 != 0:
            return 'Bitte geben Sie einen geraden Betrag ein.'

    @staticmethod
    def is_displayed(player):
        return player.teilnahme == True and player.group.ic_num_negotiators >= 2


class IC_Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    @staticmethod
    def error_message(player, values):
        if values['contribution'] is None:
            return 'Sie müssen Ihren Beitrag angeben.'
        if player.teilnahme:
            if (values['contribution'] < player.last_proposal):
                return 'Sie dürfen nicht weniger als den Mindestbeitrag angeben.'
        if values['contribution'] % 2 != 0:
            return 'Bitte geben Sie einen geraden Betrag ein.'

    @staticmethod
    def vars_for_template(player: Player):
        return dict(
            p1_participated=player.group.get_player_by_id(1).ic_teilnahme,
            p2_participated=player.group.get_player_by_id(2).ic_teilnahme,
            p3_participated=player.group.get_player_by_id(3).ic_teilnahme,
            p4_participated=player.group.get_player_by_id(4).ic_teilnahme
        )


class Filler_task(Page):
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    @staticmethod
    def is_displayed(player):
        return player.teilnahme == False and player.group.ic_num_negotiators >= 2


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs

    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")


class Results(Page):
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    @staticmethod
    def vars_for_template(player: Player):
        return dict(others=player.get_others_in_group())



page_sequence = [Verhandlungsteilnahme, Chat_Waitpage, IC_Chat, IC_One_neg, No_neg,
                 IC_Last_proposal, IC_Contribute, Filler_task, ResultsWaitPage, Results]