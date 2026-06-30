from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, Protocol

from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen.canvas import Canvas


class FormatoReciboProtocol(Protocol):
    def __init__(self, canvas: Canvas):
        ...

    def draw_background(self) -> None:
        ...

    def get_coordinates(self) -> dict:
        ...


class ReciboLayout(ABC):
    """Contract for recibo layout strategies."""

    @property
    @abstractmethod
    def pagesize(self):
        """Return the reportlab pagesize for this layout."""

    @abstractmethod
    def draw_background(self, canvas: Canvas) -> dict:
        """Draw static layout and return coordinate metadata."""

    @property
    def recibo_cls(self) -> type | None:
        """Return a ReciboSueldo subclass to use, or None for the default."""
        return None


@dataclass(frozen=True)
class LegacyFunctionLayout(ReciboLayout):
    """Adapter for existing function-based layouts (recibo_1/recibo_2)."""

    _pagesize: tuple[float, float]
    base_fn: Callable[[Canvas], dict]

    @property
    def pagesize(self):
        return self._pagesize

    def draw_background(self, canvas: Canvas) -> dict:
        return self.base_fn(canvas)


@dataclass(frozen=True)
class ClassBasedLayout(ReciboLayout):
    """Adapter for class-based layouts implementing FormatoReciboSueldo."""

    _pagesize: tuple[float, float]
    layout_cls: type[FormatoReciboProtocol]
    _recibo_cls: type | None = None

    @property
    def pagesize(self):
        return self._pagesize

    @property
    def recibo_cls(self) -> type | None:
        return self._recibo_cls

    def draw_background(self, canvas: Canvas) -> dict:
        layout = self.layout_cls(canvas)
        layout.draw_background()
        return layout.get_coordinates()


def get_layout_for_version(base_version: int) -> ReciboLayout:
    """Resolve layout strategy by version.

    Keeps legacy versions untouched and enables new class-based versions.
    """
    if base_version == 1:
        from py_arg_reports.reporters.recibo_sueldo.modelos.recibo_1 import my_base_recibo

        return LegacyFunctionLayout(_pagesize=landscape(A4), base_fn=my_base_recibo)

    if base_version == 2:
        from py_arg_reports.reporters.recibo_sueldo.modelos.recibo_2 import my_base_recibo

        return LegacyFunctionLayout(_pagesize=A4, base_fn=my_base_recibo)

    if base_version == 3:
        from py_arg_reports.reporters.recibo_sueldo.modelos.recibo_3 import FormatoRecibo3, ReciboSueldo3

        return ClassBasedLayout(_pagesize=A4, layout_cls=FormatoRecibo3, _recibo_cls=ReciboSueldo3)

    if base_version == 4:
        from py_arg_reports.reporters.recibo_sueldo.modelos.recibo_4 import FormatoRecibo4, ReciboSueldo4

        return ClassBasedLayout(_pagesize=A4, layout_cls=FormatoRecibo4, _recibo_cls=ReciboSueldo4)

    raise ValueError(f"base_version no soportada: {base_version}")
