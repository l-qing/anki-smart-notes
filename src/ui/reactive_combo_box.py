"""
 Copyright (C) 2024 Michael Piazza

 This file is part of Smart Notes.

 Smart Notes is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Smart Notes is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with Smart Notes.  If not, see <https://www.gnu.org/licenses/>.
"""

from typing import Any, Dict, Generic, List, TypeVar

from aqt import QComboBox, pyqtSignal

from .reactive_widget import ReactiveWidget
from .state_manager import StateManager

T = TypeVar("T")


class ReactiveComboBox(QComboBox, ReactiveWidget, Generic[T]):
    _fields_key: str
    _selected_key: str
    _state: StateManager[T]
    onChange = pyqtSignal(str)

    def __init__(self, state: StateManager[T], fields_key: str, selected_key: str):
        super().__init__()
        self._fields_key = fields_key
        self._selected_key = selected_key
        self._state = state
        self.currentTextChanged.connect(self.on_current_text_changed)
        state.bind(self)

    def update_from_state(self, updates: Dict[str, Any]) -> None:
        fields: List[str] = updates[self._fields_key]
        selected: str = updates[self._selected_key]
        assert fields and selected

        self.clear()
        self.addItems(fields)
        self.setCurrentText(selected)

    def on_current_text_changed(self, text: str) -> None:
        if self._state.updating:
            return

        self.onChange.emit(text)
