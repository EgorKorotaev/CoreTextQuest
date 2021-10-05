from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import List, Union


from .common import DialogId


@dataclass
class DialogOption:
    next_dialog_id: str


class DialogError(Enum):
    option_does_not_exist = 'option_does_not_exist'


@dataclass
class Dialog:
    id: DialogId
    options: List[DialogOption]

    def get_option(self, index: int) -> Union[DialogOption, DialogError]:
        if index < 0 or index >= len(self.options):
            return DialogError.option_does_not_exist
        return self.options[index]
