{
    "name":"Sentiment Analyser",
    "category": "Website",
    "version": "1.0.0",
    "sequence": 1,
    "author": "José Keh",
    "license": "Other proprietary",
    "depends": ['mail', 'helpdesk'],
    'data':['views/mail_message_view.xml',
            'views/helpdesk_ticket_view.xml',
            ],
    "application": False,
    "installable": True,
    "auto_install": False,

    'external_dependencies': {
        'python': ['vaderSentiment', 'google-genai']
    },
}
