from odoo import fields, models, Command, tools, api
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from odoo.tools import html2plaintext
from googletrans import Translator

# pip install googletrans==3.1.0a0
# pip install vaderSentiment

class MailMessage(models.Model):
    _inherit = 'mail.message'

    sentiment = fields.Float(default = False, compute= '_compute_sentiment')

    def _compute_sentiment(self):
        analyser = SentimentIntensityAnalyzer()
        translator = Translator()
        for rec in self:
            # detectar idioma y transformar
            if not rec.author_id.user_id.share and rec.author_id.company_type == 'person':
            
                if rec.body:
                    text = html2plaintext(rec.body)
                    text_lang = translator.detect(text)
                    if text_lang.lang != 'en':
                        trans_text = translator.translate(text)
                        text = trans_text.text

                    text = html2plaintext(rec.body or "")
                    score = analyser.polarity_scores(text)

                    rec.sentiment = score['compound']
                else:
                    rec.sentiment = False
            else:
                rec.sentiment = False

