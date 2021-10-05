import unittest
from dataclasses import dataclass

from dialog.domain.common import DialogId
from dialog.domain.dialog import Dialog, DialogOption
from dialog.use_case.choose_dialog_option import DialogIdPresenter, ChooseDialogOptionParams, ChooseDialogOptionImpl, \
    DialogGateway


class TestChooseDialogOption(unittest.TestCase):
    #  Я как "игрок" хочу "выбрать вариант на `экране диалога`"
    def test__choose_dialog_option(self):
        # Given
        dialog_id = '1'
        expected_dialog_id = '42'
        presenter = TestDialogIdPresenter()
        dialog_gateway = TestDialogGateway(
            {dialog_id: Dialog(dialog_id, [DialogOption('a'), DialogOption('b'), DialogOption(expected_dialog_id)])}
        )
        use_case = ChooseDialogOptionImpl(presenter=presenter, dialog_gateway=dialog_gateway)

        # When
        use_case.run(ChooseDialogOptionParams(dialog_id=dialog_id, index=2))

        # Then
        next_dialog_id = presenter.result
        self.assertEqual(expected_dialog_id, next_dialog_id)

    def test__not_existing_choose_dialog_option(self):
        # Given
        dialog_id = '1'
        presenter = TestDialogIdPresenter()
        dialog_gateway = TestDialogGateway(
            {dialog_id: Dialog(dialog_id, [])}
        )
        use_case = ChooseDialogOptionImpl(presenter=presenter, dialog_gateway=dialog_gateway)

        # When
        self.assertRaises(ValueError, use_case.run, ChooseDialogOptionParams(dialog_id=dialog_id, index=1000))


@dataclass
class TestDialogIdPresenter(DialogIdPresenter):
    result: str = ''

    def present(self, next_dialog_id: DialogId):
        self.result = next_dialog_id


@dataclass
class TestDialogGateway(DialogGateway):
    dialog: dict[DialogId, Dialog]

    def get_dialog_by_id(self, dialog_id: DialogId) -> Dialog:
        return self.dialog[dialog_id]


if __name__ == '__main__':
    unittest.main()
