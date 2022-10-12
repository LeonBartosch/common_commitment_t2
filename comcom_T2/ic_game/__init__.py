from otree.api import *
import csv

doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'ic_condition'
    PLAYERS_PER_GROUP = 4
    NUM_ROUNDS = 1
    ENDOWMENT = cu(800)
    MULTIPLIER = 2
    Eigenanteil = MULTIPLIER / 4 * 100
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
    sim_a_participation = models.IntegerField(choices=[[1, 'Ja'], [2, 'Nein'], ], blank=True)
    sim_b_participation = models.IntegerField(choices=[[1, 'Ja'], [2, 'Nein'], ], blank=True)
    sim_c_participation = models.IntegerField(choices=[[1, 'Ja'], [2, 'Nein'], ], blank=True)
    sim_d_participation = models.IntegerField(choices=[[1, 'Ja'], [2, 'Nein'], ], blank=True)
    sim_a_commitment = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    sim_b_commitment = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    sim_c_commitment = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    sim_d_commitment = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    sim_a_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    sim_b_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    sim_c_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
    sim_d_contribution = models.CurrencyField(min=0, max=C.ENDOWMENT, blank=True)
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
        label="Wie hoch sollte Ihr persönlicher Mindestbeitrag (in Cent) in der folgenden Verhandlung am Ende ausfallen? "
    )
    contribution = models.CurrencyField(min=0, max=C.ENDOWMENT,
                                        label="Bitte geben sie den Betrag (in Cent) an, den sie beisteuern wollen:"
                                        )
    contribution_check = models.BooleanField(
        initial=False
    )
    last_proposal = models.CurrencyField(
        max=C.ENDOWMENT, label="Dieser Wert ist mein Mindestbeitrag (in Cent):"
    )
    time_end = models.StringField()
    willingness = models.FloatField(min=0, max=100)
    teilnahme = models.BooleanField(
        choices=[[True, 'Ja'], [False, 'Nein'], ],
        label="Möchten Sie an der Verhandlung über einen gemeinsamen Mindestbeitrag teilnehmen?"
    )
    filler_motives = models.LongStringField(
        label='Bitte beschreiben Sie im hier, warum Sie sich gegen eine Teilnahme an der Verhandlung entschieden haben:',
        blank=True,
    )
    beliefs = models.IntegerField(choices=[-1, 0, 1, 2, 3], )

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

class Sim_IC(Page):
    form_model = 'player'
    form_fields = ['sim_a_participation', 'sim_b_participation', 'sim_c_participation', 'sim_d_participation',
                   'sim_a_commitment', 'sim_b_commitment', 'sim_c_commitment', 'sim_d_commitment',
                   'sim_a_contribution', 'sim_b_contribution', 'sim_c_contribution', 'sim_d_contribution']

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
        if player.ic_compr_a1 == 300 and player.ic_compr_a2 == 600 and player.ic_compr_a3 == 800 \
                and player.ic_compr_a4 == 500:
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
        if (values['ic_compr2_a1'] is None and player.ic_compr_a1 != 300) \
                or (values['ic_compr2_a2'] is None and player.ic_compr_a2 != 600) \
                or (values['ic_compr2_a3'] is None and player.ic_compr_a3 != 800) \
                or (values['ic_compr2_a4'] is None and player.ic_compr_a4 != 500):
            return 'Bitte füllen Sie alle Felder aus.'

    def before_next_page(player, timeout_happened):
        if (player.ic_compr_a1 == 300 or player.ic_compr2_a1 == 300) \
                and (player.ic_compr_a2 == 600 or player.ic_compr2_a2 == 600) \
                and (player.ic_compr_a3 == 800 or player.ic_compr2_a3 == 800) \
                and (player.ic_compr_a4 == 500 or player.ic_compr2_a4 == 500):
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
        if (values['ic_compr3_a1'] is None and player.ic_compr_a1 != 300 and player.ic_compr2_a1 != 300) \
                or (values['ic_compr3_a2'] is None and player.ic_compr_a2 != 600 and player.ic_compr2_a2 != 600) \
                or (values['ic_compr3_a3'] is None and player.ic_compr_a3 != 800 and player.ic_compr2_a3 != 800) \
                or (values['ic_compr3_a4'] is None and player.ic_compr_a4 != 500 and player.ic_compr2_a4 != 500):
            return 'Bitte füllen Sie alle Felder aus.'

    def before_next_page(player, timeout_happened):
        if (player.ic_compr_a1 == 300 or player.ic_compr2_a1 == 300 or player.ic_compr3_a1 == 300) \
                and (player.ic_compr_a2 == 600 or player.ic_compr2_a2 == 600 or player.ic_compr3_a2 == 600) \
                and (player.ic_compr_a3 == 800 or player.ic_compr2_a3 == 800 or player.ic_compr3_a3 == 800) \
                and (player.ic_compr_a4 == 500 or player.ic_compr2_a4 == 500 or player.ic_compr3_a4 == 500):
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
        if player.ic_compr_b1 == 600 and player.ic_compr_b2 == 0 and player.ic_compr_b3 == 800:
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
        if (values['ic_compr2_b1'] is None and player.ic_compr_b1 != 600) \
                or (values['ic_compr2_b2'] is None and player.ic_compr_b2 != 0) \
                or (values['ic_compr2_b3'] is None and player.ic_compr_b3 != 800):
            return 'Bitte füllen Sie alle Felder aus.'

    def before_next_page(player, timeout_happened):
        if (player.ic_compr_b1 == 600 or player.ic_compr2_b1 == 600) \
                and (player.ic_compr_b2 == 0 or player.ic_compr2_b2 == 0) \
                and (player.ic_compr_b3 == 800 or player.ic_compr2_b3 == 800):
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
        if (values['ic_compr3_b1'] is None and player.ic_compr_b1 != 600 and player.ic_compr2_b1 != 600) \
                or (values['ic_compr3_b2'] is None and player.ic_compr_b2 != 0 and player.ic_compr2_b2 != 0) \
                or (values['ic_compr3_b3'] is None and player.ic_compr_b3 != 800 and player.ic_compr2_b3 != 800):
            return 'Bitte füllen Sie alle Felder aus.'

    def before_next_page(player, timeout_happened):
        if (player.ic_compr_b1 == 600 or player.ic_compr2_b1 == 600 or player.ic_compr3_b1 == 600) \
                and (player.ic_compr_b2 == 0 or player.ic_compr2_b2 == 0 or player.ic_compr3_b2 == 0) \
                and (player.ic_compr_b3 == 800 or player.ic_compr2_b3 == 800 or player.ic_compr3_b3 == 800):
            player.ic_compr_check_b_pass = True
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


class IC_Verhandlungsziel(Page):
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

class IC_Chat(Page):
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
        with open('_static/chat/ic_chat.csv', mode='a') as csvfile:
            chat = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            chat.writerow(
                [player.session.code, player.group.id_in_subsession, player.id_in_group, player.participant.label,
                 datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"), bid])
        # with open('_static/chat/ic_chat.csv', mode='r+') as file:
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


class IC_One_neg(Page):
    def before_next_page(player, timeout_happened):
        import datetime
        player.participant.time_end = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    @staticmethod
    def is_displayed(player):
        return player.teilnahme == True and player.group.num_negotiators == 1


class No_neg(Page):
    @staticmethod
    def is_displayed(player):
        return player.group.num_negotiators == 0
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
        if values['last_proposal'] % 10 != 0:
            return 'Bitte geben Sie einen durch 10 teilbaren Betrag ein.'

    @staticmethod
    def is_displayed(player):
        return player.teilnahme == True and player.group.num_negotiators >= 2


class IC_Contribute(Page):
    form_model = 'player'
    form_fields = ['contribution']

    @staticmethod
    def error_message(player, values):
        if values['contribution'] is None:
            return 'Sie müssen Ihren Beitrag angeben.'
        if player.teilnahme and player.group.num_negotiators >= 2:
            if (values['contribution'] < player.last_proposal):
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
    template_name = 'ic_game/ResultsWaitPage.html'
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
                if row[0] == player.participant.label:
                    T1_payoff = cu(row[1]).to_real_world_currency(player.session)
        total_payoff = T1_payoff + player.participant.payoff_plus_participation_fee()
        return dict(
            others=player.get_others_in_group(),
            T1_payoff=T1_payoff,
            total_payoff=total_payoff
        )



page_sequence = [
    IC_instructions,IC_example,
    Sim_IC,
    IC_compr_check_a, IC_compr_check2_a, IC_compr_check3_a,
    IC_compr_check_b, IC_compr_check2_b, IC_compr_check3_b,
    Verhandlungsteilnahme, Beliefs,
    Verhandlungsziel_Waitpage, IC_Verhandlungsziel,
    Chat_Waitpage, IC_Chat, IC_One_neg, No_neg, IC_Last_proposal,
    IC_Contribute,
    Filler_task,
    ResultsWaitPage, Results]