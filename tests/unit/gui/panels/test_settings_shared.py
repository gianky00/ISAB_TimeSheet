"""Unit tests for Settings Shared utilities."""

from PySide6.QtWidgets import QLineEdit, QPushButton, QSpinBox

from src.gui.panels.settings.shared import (
    create_group_box,
    list_style,
    style_button,
    style_input,
    style_mini_button,
)


def test_create_group_box(qtbot):
    group = create_group_box("Test Group")
    assert group.title() == "Test Group"
    assert "border: 1px solid" in group.styleSheet()


def test_list_style():
    style = list_style()
    assert "QListWidget" in style
    assert "border: 1px solid" in style


def test_style_input(qtbot):
    edit = QLineEdit()
    style_input(edit)
    assert "QLineEdit" in edit.styleSheet()

    spin = QSpinBox()
    style_input(spin)
    assert "QSpinBox" in spin.styleSheet()


def test_style_button(qtbot):
    btn = QPushButton("Click Me")
    style_button(btn)
    assert "QPushButton" in btn.styleSheet()
    assert "font-weight: bold" in btn.styleSheet()


def test_style_mini_button(qtbot):
    btn = QPushButton()
    style_mini_button(btn, "#ff0000")
    # Usa width() e height() invece di fixedSize()
    assert btn.width() == 32
    assert btn.height() == 32
    assert "border-color: #ff0000" in btn.styleSheet()
