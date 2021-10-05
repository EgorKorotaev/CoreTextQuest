from abc import ABC, abstractmethod
from dataclasses import dataclass

from dialog.domain.common import DialogId
from dialog.domain.dialog import Dialog, DialogError


@dataclass
class ChooseDialogOptionParams:
    dialog_id: str
    index: int


# input port
class ChooseDialogOption(ABC):
    @abstractmethod
    def run(self, params: ChooseDialogOptionParams):
        pass


# output port
class DialogIdPresenter(ABC):
    @abstractmethod
    def present(self, next_dialog_id: DialogId):
        pass


# data port
class DialogGateway(ABC):
    @abstractmethod
    def get_dialog_by_id(self, dialog_id: DialogId) -> Dialog:
        pass


# interactor (use_case)
@dataclass
class ChooseDialogOptionImpl(ChooseDialogOption):
    presenter: DialogIdPresenter
    dialog_gateway: DialogGateway

    def run(self, params: ChooseDialogOptionParams):
        current_dialog = self.dialog_gateway.get_dialog_by_id(params.dialog_id)
        option = current_dialog.get_option(index=params.index)
        if option == DialogError.option_does_not_exist:
            raise ValueError(f'unknown option with index {params.index}')
        next_dialog_id = option.next_dialog_id
        self.presenter.present(next_dialog_id)
