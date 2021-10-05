from abc import ABC, abstractmethod
from dataclasses import dataclass

# -------------------------------- ENTITY --------------------------------
from dialog.domain.dialog import GameDialog
from dialog.domain.dialog_action import DialogAction



# -------------------------------- Use Case --------------------------------

# -------------------------------- Adapters (Controllers, Gateways) --------------------------------
class ConsoleDialogPresenter(DialogPresenter):  # presenter

    def __init__(self):
        pass

    def present(self, dialog: GameDialog):
        output_str = '********************************\n'
        output_str += f'Exposure: {dialog.exposure}\n--------------------------------\n'
        for action in dialog.actions:
            output_str += f'{action.action_order}: {action.action}\n'
        output_str += '********************************'
        print(output_str)


class HashMapDialogsGateway(ObjectsGateway):  # gateway

    def __init__(self):
        self.storage_dialog = {
            'd0': {"exposure": 'e0', "actions": [{'action': 'a1', 'next_dialog': 'd1'},
                                                 {'action': 'a2', 'next_dialog': 'd2'},
                                                 {'action': 'ar', 'next_dialog': 'd0'}
                                                 ]},
            'd1': {"exposure": 'e1', "actions": [{'action': 'a0', 'next_dialog': 'd0'},
                                                 {'action': 'a2', 'next_dialog': 'd2'},
                                                 {'action': 'ar', 'next_dialog': 'd1'}
                                                 ]},
            'd2': {"exposure": 'e2', "actions": [{'action': 'a0', 'next_dialog': 'd0'},
                                                 {'action': 'a1', 'next_dialog': 'd1'},
                                                 {'action': 'ar', 'next_dialog': 'd2'}
                                                 ]},
        }

        self.storage_exposure = {
            'e0': {"text": "Локация 0"},
            'e1': {"text": "Локация 1"},
            'e2': {"text": "Локация 2"},
        }

        self.storage_action = {
            "ar": {"text": "Где-где я?"},
            "a0": {"text": "Иду в 'Локацию 0'"},
            "a1": {"text": "Иду в 'Локацию 1'"},
            "a2": {"text": "Иду в 'Локацию 2'"},
        }

    def get_dialog_by_id(self, dialog_id: str) -> GameDialog:
        result_actions = []

        exposure = self.storage_exposure[self.storage_dialog[dialog_id]['exposure']]['text']
        actions = self.storage_dialog[dialog_id]['actions']
        for i in range(len(actions)):
            result_actions.append(DialogAction(action_order=i.__str__(),
                                               action_id=actions[i]['action'],
                                               action=self.storage_action[actions[i]['action']]['text'],
                                               next_dialog_id=actions[i]['next_dialog']))

        result = GameDialog(id=dialog_id,
                            exposure=exposure,
                            actions=result_actions)

        return result


class ConsoleDialogController:  # controller
    def __init__(self):
        presenter = ConsoleDialogPresenter()
        self.gateway = gateway = HashMapDialogsGateway()
        self.dialogs_use_case = DialogUseCaseImpl(dialogs_presenter=presenter, dialogs_gateway=gateway)
        self.last_dialog_id = ''

    def acceptAnswer(self, answer: int):
        dialog_id = self.gateway.storage_dialog[self.last_dialog_id]['actions'][answer]['next_dialog']
        self.dialogs(dialog_id)

    def dialogs(self, dialog_id):
        self.last_dialog_id = dialog_id
        params = DialogParams(dialog_id=dialog_id)
        self.dialogs_use_case.dialogs(params)


def play():
    controller = ConsoleDialogController()
    controller.dialogs('d0')
    while True:
        controller.acceptAnswer(int(input()))


if __name__ == '__main__':
    play()
