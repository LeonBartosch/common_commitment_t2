from os import environ


SESSION_CONFIGS = [
    dict(
        name='T2',
        display_name="T2",
        app_sequence=['cc_game'],
        num_demo_participants=4,
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.01, participation_fee=0.00, doc="", max_number_participants=1000
)

PARTICIPANT_FIELDS = [
    'time_start', 'time_end', 'treatment'
]
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'de'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True
POINTS_CUSTOM_NAME = 'Cent'

ROOMS = [
    dict(name="lab", display_name="Lab Experiment", participant_label_file='_rooms/lab.txt',),
]

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """
Here are some oTree games.
"""


SECRET_KEY = '5651370800674'

INSTALLED_APPS = ['otree']
