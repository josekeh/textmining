from odoo import models, fields, api

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

