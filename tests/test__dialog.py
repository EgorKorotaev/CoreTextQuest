import unittest

from dialog.domain.dialog import Dialog, DialogOption, DialogError


class TestDialog(unittest.TestCase):
    def test__get_existing_option(self):
        # Given
        dialog_option = DialogOption('11')
        dialog = Dialog('1', [dialog_option])

        # When
        option = dialog.get_option(index=0)

        # Then
        self.assertEqual(dialog_option, option)

    def test__get_non_existing_option(self):
        # Given
        dialog_option = DialogOption('11')
        dialog = Dialog('1', [dialog_option])

        # When
        option = dialog.get_option(index=1000)

        # Then
        self.assertEqual(DialogError.option_does_not_exist, option)
