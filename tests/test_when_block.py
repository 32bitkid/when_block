from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..when_block import When

class TestClassify(NIOBlockTestCase):

    def test_static_subject(self):
        """Dyanmic when."""
        blk = When()
        self.configure_block(blk, {
            "subject": "nio",
            "cases": [
                {
                    "when": "{{ $hello }}",
                    "attributes": [
                        { "title": "goodbye", "formula": "world" }
                    ]
                }
            ]
        })
        blk.start()
        blk.process_signals([Signal({"hello": "nio"})])
        blk.stop()
        self.assert_num_signals_notified(1, blk, DEFAULT_TERMINAL)
        self.assert_num_signals_notified(0, blk, 'else')
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {"hello": "nio", "goodbye": "world"})

    def test_dynamic_subject(self):
        """Dyanmic subject."""
        blk = When()
        self.configure_block(blk, {
            "subject": "{{$hello}}",
            "cases": [
                {
                    "when": "nio",
                    "attributes": [
                        { "title": "goodbye", "formula": "world" }
                    ]
                }
            ]
        })
        blk.start()
        blk.process_signals([Signal({"hello": "nio"})])
        blk.stop()
        self.assert_num_signals_notified(1, blk, DEFAULT_TERMINAL)
        self.assert_num_signals_notified(0, blk, 'else')
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {"hello": "nio", "goodbye": "world"})

    def test_multiple_signals(self):
        """Multiple signals."""
        blk = When()
        self.configure_block(blk, {
            "subject": "{{$hello}}",
            "cases": [
                {
                    "when": "nio",
                    "attributes": [
                        { "title": "goodbye", "formula": "world" }
                    ]
                },
                {
                    "when": "mouse",
                    "attributes": [
                        { "title": "goodnight", "formula": "moon" }
                    ]
                }
            ],
        })
        blk.start()
        blk.process_signals([
            Signal({"hello": "nio"}),
            Signal({"hello": "mouse"})
        ])
        blk.stop()
        self.assert_num_signals_notified(2, blk, DEFAULT_TERMINAL)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {"hello": "nio", "goodbye": "world"})
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][1].to_dict(),
            {"hello": "mouse", "goodnight": "moon"})

    def test_else(self):
        """Else handling."""
        blk = When()
        self.configure_block(blk, {
            "subject": "{{$hello}}",
            "cases": [
                {
                    "when": "nio",
                    "attributes": [
                        { "title": "goodbye", "formula": "world" }
                    ]
                },
            ],
        })
        blk.start()
        blk.process_signals([
            Signal({"hello": "nio"}),
            Signal({"hello": "mouse"})
        ])
        blk.stop()
        self.assert_num_signals_notified(1, blk, DEFAULT_TERMINAL)
        self.assert_num_signals_notified(1, blk, 'else')

        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {"hello": "nio", "goodbye": "world"})
        self.assertDictEqual(
            self.last_notified['else'][0].to_dict(),
            {"hello": "mouse"})


    def test_multiple_conditions(self):
        """Multiple conditions in subject."""
        blk = When()
        self.configure_block(blk, {
            "subject": "{{($mode is 'greeting') and $who}}",
            "cases": [
                {
                    "when": "nio",
                    "attributes": [
                        { "title": "greeting", "formula": "hello there" },
                        { "title": "nickname", "formula": "niolabs" },
                    ],
                    "exclude": True,
                },
                {
                    "when": "mouse",
                    "attributes": [
                        { "title": "greeting", "formula": "yo yo yo" },
                        { "title": "nickname", "formula": "mousy" }
                    ],
                    "exclude": True,
                },
            ],
        })
        blk.start()
        blk.process_signals([
            Signal({"who": "nio", "mode": "greeting"}),
            Signal({"who": "mouse", "mode": "valediction"})
        ])
        blk.stop()
        self.assert_num_signals_notified(1, blk, DEFAULT_TERMINAL)
        self.assert_num_signals_notified(1, blk, 'else')

        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {"greeting": "hello there", "nickname": "niolabs"})

        self.assertDictEqual(
            self.last_notified['else'][0].to_dict(),
            {'mode': 'valediction', 'who': 'mouse'})


