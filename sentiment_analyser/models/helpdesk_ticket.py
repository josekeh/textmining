from odoo import models, fields, api
from odoo.tools import html2plaintext
from odoo.exceptions import UserError
import os
# from transformers import pipeline
from google import genai


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    estado_felicidad = fields.Boolean(string="Cliente feliz", default=True, compute = '_compute_estado_felicidad')

    @api.depends('message_ids')
    def _compute_estado_felicidad(self):
        for ticket in self:
            # Filtramos los mensajes del cliente
            mensajes_cliente = ticket.message_ids.filtered(
                lambda m: m.author_id and not m.author_id.user_id.share
            )
            # import pdb; pdb.set_trace()

            ultimos = mensajes_cliente.sorted('date', reverse=True)[:3]

            hay_negativo = any(m.sentiment < 0
                for m in ultimos
            )

            ticket.estado_felicidad = not hay_negativo


    def action_create_summary(self):
        self.ensure_one()
        
        # get AI model

        # generator = pipeline(task="text-generation",model="datificate/gpt2-small-spanish",device=-1) 
        #generator = pipeline(task="text-generation",model="distilgpt2",device=-1)
        
        api_key = os.getenv("GENAI_API_KEY")
        if not api_key:
            raise ValueError("GENAI_API_KEY no está definido en el entorno")

        client = genai.Client(api_key=api_key)


        
        # init prompt
        prompt = "Summary:\n\n"

        # get messages
        mensajes = self.message_ids

        # Generate prompt

        for rec in mensajes:
            author = rec.author_id.name
            text = html2plaintext(rec.body)
            prompt += "Author: " + author +"\n" + text + "\n" + "--------------" + "\n"

        # Generate summary

        content = "Generá un resumen en castellano de la siguiente cadena de mensajes:\n\n" + prompt

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=content,
        )


        raise UserError(response.text)


        

        



    

