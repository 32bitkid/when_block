from enum import Enum

from nio.block import output
from nio.block.base import Block
from nio.signal.base import Signal
from nio.properties import BoolProperty, Property, ListProperty, PropertyHolder, \
    SelectProperty, VersionProperty

class SignalField(PropertyHolder):
    title = Property(default='', title='Attribute Name', order=0)
    formula = Property(default='',
                       title='Attribute Value',
                       allow_none=True,
                       order=1)

class Case(PropertyHolder):
    when = Property(default='',
                    title='When',
                    order=0)
    attributes = ListProperty(SignalField,
                              title="Attributes",
                              default=[],
                              order=2)
    exclude = BoolProperty(default=False,
                           title='Exclude existing attributes?',
                           order=1)

@output('else', label='Else')
@output('then', label='', default=True)
class When(Block):
    subject = Property(default=None,
                       title='Subject',
                       allow_none=True,
                       order=0)
    cases = ListProperty(Case,
                         title='Cases',
                         default=[],
                         order=1)
    version = VersionProperty('0.1.0')

    def process_signals(self, in_sigs):
        then_signals = []
        else_signals = []

        for signal in in_sigs:

            subject = self.subject(signal)
            for case in self.cases():
                if subject != case.when(signal):
                    continue

                sig = Signal() if case.exclude(signal) else signal

                for attr in case.attributes():
                    title = attr.title(signal)
                    value = attr.formula(signal)
                    setattr(sig, title, value)

                then_signals.append(sig)
                break
            else:
                else_signals.append(signal)

        if len(then_signals):
            self.notify_signals(then_signals, 'then')

        if len(else_signals):
            self.notify_signals(else_signals, 'else')
