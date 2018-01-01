import os
import tempfile
from collections import OrderedDict
from zipfile import ZipFile

from django import forms
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from ..exporter import BaseExporter
from ..services.invoices import invoice_pdf_task
from ..signals import register_data_exporters


class InvoiceExporter(BaseExporter):
    identifier = 'invoices'
    verbose_name = _('All invoices')

    def render(self, form_data: dict):
        qs = self.event.invoices.all()

        if form_data.get('payment_provider'):
            qs = qs.filter(order__payment_provider=form_data.get('payment_provider'))

        if form_data.get('date_from'):
            qs = qs.filter(date__gte=form_data.get('date_from'))

        if form_data.get('date_to'):
            qs = qs.filter(date__lte=form_data.get('date_to'))

        with tempfile.TemporaryDirectory() as d:
            with ZipFile(os.path.join(d, 'tmp.zip'), 'w') as zipf:
                for i in qs:
                    if not i.file:
                        invoice_pdf_task.apply(args=(i.pk,))
                        i.refresh_from_db()
                    i.file.open('rb')
                    zipf.writestr('{}.pdf'.format(i.number), i.file.read())
                    i.file.close()

            with open(os.path.join(d, 'tmp.zip'), 'rb') as zipf:
                return '{}_invoices.zip'.format(self.event.slug), 'application/zip', zipf.read()

    @property
    def export_form_fields(self):
        return OrderedDict(
            [
                ('date_from',
                 forms.DateField(
                     label=_('Start date'),
                     widget=forms.DateInput(attrs={'class': 'datepickerfield'}),
                     required=False,
                     help_text=_('Only include invocies issued on or after this date. Note that the invoice date does '
                                 'not always correspond to the order or payment date.')
                 )),
                ('date_to',
                 forms.DateField(
                     label=_('End date'),
                     widget=forms.DateInput(attrs={'class': 'datepickerfield'}),
                     required=False,
                     help_text=_('Only include invocies issued on or before this date. Note that the invoice date '
                                 'does not always correspond to the order or payment date.')
                 )),
                ('payment_provider',
                 forms.ChoiceField(
                     label=_('Payment provider'),
                     choices=[
                         ('', _('All payment providers')),
                     ] + [
                         (k, v.verbose_name) for k, v in self.event.get_payment_providers().items()
                     ],
                     required=False,
                     help_text=_('Only include invocies for orders that are currently set to this payment provider. '
                                 'Note that this might include some invoices of other payment providers or misses '
                                 'some invoices if the payment provider of an order has been changed and a new order '
                                 'has been generated.')
                 )),
            ]
        )


@receiver(register_data_exporters, dispatch_uid="exporter_invoices")
def register_invoice_export(sender, **kwargs):
    return InvoiceExporter
