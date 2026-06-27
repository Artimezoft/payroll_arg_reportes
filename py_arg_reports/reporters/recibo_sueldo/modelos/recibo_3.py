from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Mapping

from reportlab.lib.units import cm

from py_arg_reports.config import config_constants
from py_arg_reports.reporters.recibo_sueldo.base import EXCLUDED_CONCEPTS, FormatoReciboSueldo, ReciboSueldo
from py_arg_reports.tools.num_n_date_tools import float_to_format_currency

FONT_FAMILY = config_constants["FONT_FAMILY"]
FONT_FAMILY_BOLD = config_constants["FONT_FAMILY_BOLD"]
FONT_SIZE_MAIN = config_constants["FONT_SIZE_MAIN"]
FONT_SIZE_BODY = config_constants["FONT_SIZE_BODY"]


@dataclass(frozen=True)
class Recibo3LayoutConfig:
    """Configuracion parametrica para el layout de recibo_3.

    Todas las medidas en cm salvo corner_radius (puntos), y los campos *_share
    y *_ratio que son proporciones.
    """

    page_width_cm: float = 19.0
    page_height_cm: float = 29.7
    translate_x_cm: float = 1.0
    translate_y_cm: float = 1.0

    margin_x_cm: float = 0.4
    margin_y_cm: float = 0.3
    section_gap_cm: float = 0.2
    top_offset_cm: float = 0.9

    corner_radius: float = 7.0
    gray_fill: float = 0.93

    company_share: float = 0.07
    employee_share: float = 0.10
    conceptos_share: float = 0.46
    contribuciones_share: float = 0.24
    footer_share: float = 0.13

    company_width_ratio: float = 0.78
    liquidacion_gap_cm: float = 0.1

    conceptos_title_y_offset_cm: float = 0.3
    conceptos_title_left_x_offset_cm: float = 0.5
    conceptos_title_cant_ratio: float = 0.56
    conceptos_title_rem_ratio: float = 0.68
    conceptos_title_nr_ratio: float = 0.80
    conceptos_title_ap_ratio: float = 0.91
    conceptos_title_cant_label_offset_cm: float = 0.1
    conceptos_title_rem_label_offset_cm: float = 0.2
    conceptos_title_nr_label_offset_cm: float = 0.2
    conceptos_title_ap_label_offset_cm: float = 0.2

    totales_line_ratio_in_conceptos: float = 0.15
    totales_label_offset_cm: float = 0.5
    neto_label_y_offset_cm: float = 0.6
    neto_label_right_padding_cm: float = 5.2

    footer_extra_gap_cm: float = 0.25
    footer_height_scale: float = 1.1
    pie_pagina_y_offset_cm: float = 0.45
    footer_split_ratio: float = 0.5
    footer_split_offset_cm: float = 2.0

    @classmethod
    def from_mapping(cls, overrides: Mapping[str, float] | None = None) -> "Recibo3LayoutConfig":
        if not overrides:
            return cls()

        known_keys = set(cls.__dataclass_fields__.keys())
        filtered = {k: v for k, v in overrides.items() if k in known_keys}
        return cls(**filtered)

    def with_overrides(self, overrides: Mapping[str, float] | None = None) -> "Recibo3LayoutConfig":
        if not overrides:
            return self
        payload = asdict(self)
        for key, value in overrides.items():
            if key in payload:
                payload[key] = value
        return Recibo3LayoutConfig(**payload)


class FormatoRecibo3(FormatoReciboSueldo):
    """Layout class-based con coordenadas configurables.

    Mantiene el contrato de salida esperado por ReciboDownloader.get_coordinates_for_recibo.
    Soporta configuracion via config_constants['RECIBO_3_LAYOUT'] y via argumento explicito.
    """

    _default_config = Recibo3LayoutConfig()

    def __init__(self, canvas, config_overrides: Mapping[str, float] | None = None):
        super().__init__(canvas)
        constants_overrides = config_constants.get("RECIBO_3_LAYOUT", {})
        self.config = self._default_config.with_overrides(constants_overrides).with_overrides(config_overrides)

    @classmethod
    def configure_defaults(cls, overrides: Mapping[str, float] | None = None) -> None:
        """Permite ajustar defaults en runtime para nuevos layouts/versiones."""
        cls._default_config = cls._default_config.with_overrides(overrides)

    def _get_section_heights(self, available_height: float) -> dict[str, float]:
        cfg = self.config
        shares = {
            "company": max(cfg.company_share, 0),
            "employee": max(cfg.employee_share, 0),
            "conceptos": max(cfg.conceptos_share, 0),
            "contribuciones": max(cfg.contribuciones_share, 0),
            "footer": max(cfg.footer_share, 0),
        }
        total_share = sum(shares.values()) or 1.0
        return {
            name: available_height * (share / total_share) - cfg.section_gap_cm * cm
            for name, share in shares.items()
        }

    def draw_background(self):
        c = self.canvas
        cfg = self.config

        tot_x = cfg.page_width_cm * cm
        tot_y = cfg.page_height_cm * cm
        margin_x = cfg.margin_x_cm * cm
        margin_y = cfg.margin_y_cm * cm
        section_gap = cfg.section_gap_cm * cm

        self.coordinates = {
            "tot_x": tot_x,
            "tot_y": tot_y,
            "margin_between_lines": section_gap,
            "margin_x": margin_x,
            "has_duplicate": False,
        }

        available_height = tot_y - 2 * margin_y
        available_width = tot_x - 2 * margin_x
        section_heights = self._get_section_heights(available_height)

        c.translate(cfg.translate_x_cm * cm, cfg.translate_y_cm * cm)
        c.setFillColorRGB(cfg.gray_fill, cfg.gray_fill, cfg.gray_fill)

        company_height = section_heights["company"]
        company_width = available_width * cfg.company_width_ratio
        y = tot_y - margin_y - company_height - cfg.top_offset_cm * cm

        self.coordinates["company_info_y"] = y
        self.coordinates["company_info_height"] = company_height

        c.roundRect(
            margin_x,
            y,
            company_width,
            company_height,
            radius=cfg.corner_radius,
            stroke=1,
            fill=1,
        )

        liquidacion_x = margin_x + company_width + cfg.liquidacion_gap_cm * cm
        liquidacion_width = available_width - company_width - cfg.liquidacion_gap_cm * cm
        self.coordinates["liquidacion_info_x"] = liquidacion_x
        self.coordinates["liquidacion_info_width"] = liquidacion_width

        c.roundRect(
            liquidacion_x,
            y,
            liquidacion_width,
            company_height,
            radius=cfg.corner_radius,
            stroke=1,
            fill=0,
        )
        c.line(
            liquidacion_x,
            y + company_height / 2,
            liquidacion_x + liquidacion_width,
            y + company_height / 2,
        )

        y -= section_heights["employee"] + section_gap
        employee_width = available_width
        self.coordinates["employee_info_y"] = y
        self.coordinates["employee_info_height"] = section_heights["employee"]
        self.coordinates["employee_info_width"] = employee_width

        c.roundRect(
            margin_x,
            y,
            employee_width,
            section_heights["employee"],
            radius=cfg.corner_radius,
            stroke=1,
            fill=0,
        )

        y -= section_heights["conceptos"] + section_gap
        conceptos_width = employee_width
        self.coordinates["conceptos_y"] = y + section_heights["conceptos"]
        self.coordinates["conceptos_height"] = section_heights["conceptos"]

        c.roundRect(
            margin_x,
            y,
            conceptos_width,
            section_heights["conceptos"],
            radius=cfg.corner_radius,
            stroke=1,
            fill=0,
        )

        c.setFont(FONT_FAMILY_BOLD, FONT_SIZE_MAIN)
        c.setFillColorRGB(0, 0, 0)

        conceptos_titles_y = self.coordinates["conceptos_y"] - cfg.conceptos_title_y_offset_cm * cm
        concepto_titles_x_cant = margin_x + conceptos_width * cfg.conceptos_title_cant_ratio
        concepto_titles_x_rem = margin_x + conceptos_width * cfg.conceptos_title_rem_ratio
        concepto_titles_x_nr = margin_x + conceptos_width * cfg.conceptos_title_nr_ratio
        concepto_titles_x_ap = margin_x + conceptos_width * cfg.conceptos_title_ap_ratio

        self.coordinates["conceptos_titles_y"] = conceptos_titles_y
        self.coordinates["concepto_titles_x_cant"] = concepto_titles_x_cant
        self.coordinates["concepto_titles_x_rem"] = concepto_titles_x_rem
        self.coordinates["concepto_titles_x_nr"] = concepto_titles_x_nr
        self.coordinates["concepto_titles_x_ap"] = concepto_titles_x_ap

        c.drawString(margin_x + cfg.conceptos_title_left_x_offset_cm * cm, conceptos_titles_y, "Conceptos")
        c.drawString(
            concepto_titles_x_cant + cfg.conceptos_title_cant_label_offset_cm * cm,
            conceptos_titles_y,
            "Cant.",
        )
        c.drawString(
            concepto_titles_x_rem + cfg.conceptos_title_rem_label_offset_cm * cm,
            conceptos_titles_y,
            "Remun.",
        )
        c.drawString(
            concepto_titles_x_nr + cfg.conceptos_title_nr_label_offset_cm * cm,
            conceptos_titles_y,
            "No Rem.",
        )
        c.drawString(
            concepto_titles_x_ap + cfg.conceptos_title_ap_label_offset_cm * cm,
            conceptos_titles_y,
            "Retenc.",
        )

        starting_y_totales = y + section_heights["conceptos"] * cfg.totales_line_ratio_in_conceptos
        starting_y_totales_text = starting_y_totales - cfg.totales_label_offset_cm * cm
        starting_y_totales_neto = y + cfg.neto_label_y_offset_cm * cm

        self.coordinates["starting_y_totales"] = starting_y_totales_text
        self.coordinates["starting_y_totales_neto"] = starting_y_totales_neto

        c.line(
            margin_x,
            starting_y_totales,
            margin_x + conceptos_width,
            starting_y_totales,
        )
        c.drawString(margin_x + cfg.conceptos_title_left_x_offset_cm * cm, starting_y_totales_text, "Totales:")
        c.drawString(
            margin_x + conceptos_width - cfg.neto_label_right_padding_cm * cm,
            starting_y_totales_neto,
            "Neto a Pagar:",
        )

        y -= section_heights["contribuciones"] + section_gap
        self.coordinates["contribuciones_y"] = y + section_heights["contribuciones"]
        self.coordinates["contribuciones_height"] = section_heights["contribuciones"]

        c.roundRect(
            margin_x,
            y,
            employee_width,
            section_heights["contribuciones"],
            radius=cfg.corner_radius,
            stroke=1,
            fill=0,
        )

        c.setFont(FONT_FAMILY_BOLD, FONT_SIZE_MAIN)
        c.setFillColorRGB(0, 0, 0)

        contribuciones_titles_y = self.coordinates["contribuciones_y"] - cfg.conceptos_title_y_offset_cm * cm
        self.coordinates["contribuciones_titles_y"] = contribuciones_titles_y
        c.drawString(margin_x + cfg.conceptos_title_left_x_offset_cm * cm, contribuciones_titles_y, "Contribuciones Empleador")

        y -= section_heights["footer"] + section_gap + cfg.footer_extra_gap_cm * cm
        footer_height = section_heights["footer"] * cfg.footer_height_scale

        self.coordinates["pie_pagina_y"] = y + footer_height - cfg.pie_pagina_y_offset_cm * cm
        self.coordinates["pie_pagina_height"] = footer_height
        self.coordinates["pie_pagina_width"] = conceptos_width

        c.roundRect(
            margin_x,
            y,
            conceptos_width,
            footer_height,
            radius=cfg.corner_radius,
            stroke=1,
            fill=0,
        )

        split_x = margin_x + conceptos_width * cfg.footer_split_ratio + cfg.footer_split_offset_cm * cm
        c.line(split_x, y, split_x, y + footer_height)

        c.setFont(FONT_FAMILY, FONT_SIZE_BODY)
        self.coordinates["canvas"] = c


class ReciboSueldo3(ReciboSueldo):
    """Version-3-specific drawing overrides for ReciboSueldo."""

    def draw_contribuciones(self) -> None:
        """Column format matching conceptos_part: name | cant | importe right-aligned."""
        coords = self.coordinates
        conceptos_liquidados = self.info_recibo['conceptos_liquidados'][self.legajo]
        self.total_contribuciones = 0.0

        this_y = coords['starting_y_contribuciones']
        for concepto in conceptos_liquidados:
            code = concepto['code']
            name = concepto['name']
            tipo_concepto = concepto['tipo_concepto']
            cantidad = f"{concepto['cantidad']:.2f}" if concepto['cantidad'] != 0.0 else ''
            importe = concepto['importe']

            if code in EXCLUDED_CONCEPTS or tipo_concepto != 4 or importe == 0.0:
                continue

            self.total_contribuciones += importe
            self._set_font(bold=False, size=self.font_size_body)
            self.c.drawString(coords['conceptos_x'], this_y, name)
            self.c.drawString(coords['concepto_titles_x_cant'], this_y, str(cantidad))
            self.draw_text_with_end_coordinate(
                self.c,
                coords['concepto_titles_x_ap_ends'],
                this_y,
                float_to_format_currency(importe, include_currency=False),
            )
            this_y -= 0.4 * cm

        # Separator line + total anchored to the bottom of the contribuciones section box
        section_bottom = coords['contribuciones_section_bottom_y']
        section_left = coords['conceptos_x'] - 0.2 * cm   # = margin_x, matches box edge
        section_right = section_left + coords['pie_de_pagina_width']
        line_y = section_bottom + 0.7 * cm
        total_label_y = section_bottom + 0.25 * cm
        self.c.line(section_left, line_y, section_right, line_y)
        self._set_font(bold=True, size=self.font_size_main)
        self.c.drawString(coords['conceptos_x'] + 0.5 * cm, total_label_y, "Total Contribuciones Empleador:")
        self.draw_text_with_end_coordinate(
            self.c,
            coords['concepto_titles_x_ap_ends'] - 0.3 * cm,
            total_label_y,
            float_to_format_currency(self.total_contribuciones),
        )
        self._set_font(bold=False, size=self.font_size_body)

    def draw_composition_salario(self) -> None:
        """Detalle de la Composición Salarial: title, two-column breakdown, pie chart."""
        coords = self.coordinates
        pie_de_pagina_x = coords['pie_de_pagina_x']
        pie_de_pagina_y = coords['pie_de_pagina_y']
        pie_linea_4_y = pie_de_pagina_y - self.base_line_between * 3

        # ── Title ─────────────────────────────────────────────────────────────
        self._set_font(bold=True, size=self.font_size_body)
        self.c.drawString(
            pie_de_pagina_x + 0.3 * cm,
            pie_de_pagina_y,
            "Detalle de la Composición Salarial",
        )

        # ── Pie chart (unchanged) ──────────────────────────────────────────────
        pie_size = 1.8 * cm
        pie_x = pie_de_pagina_x + coords['pie_de_pagina_width'] * 0.42 + 0.5 * cm - 1.0 * cm + 3.0 * cm
        pie_y = max(0.2 * cm, pie_linea_4_y + 0.2 * cm)
        self.draw_pie_chart(
            pie_x,
            pie_y,
            pie_size,
            self.info_recibo['totales_liquidacion'][self.legajo],
            self.info_recibo['conceptos_liquidados'][self.legajo],
            font_delta=2,
        )

        # ── Two-column breakdown (hardcoded labels — values wired later) ───────
        ROW_H = 0.32 * cm
        GAP_H = 0.19 * cm
        col1_x = pie_de_pagina_x + 0.3 * cm
        col2_x = pie_de_pagina_x + 5.5 * cm
        start_y = pie_de_pagina_y - 0.4 * cm

        COL1 = [
            ("Total Costo Sindical", True),
            ("Empleador", False),
            ("Trabajador", False),
            None,
            ("Total Seguridad Social", True),
            ("Empleador", False),
            ("Trabajador", False),
            None,
            ("Total Obra Social", True),
            ("Empleador", False),
            ("Trabajador", False),
        ]
        COL2 = [
            ("Total INSSJP (PAMI)", True),
            ("Empleador", False),
            ("Trabajador", False),
            None,
            ("Total ART", True),
            ("Empleador", False),
            None,
            ("Total Seguro Vida (SCVO)", True),
            ("Empleador", False),
        ]

        for col_x, items in ((col1_x, COL1), (col2_x, COL2)):
            cur_y = start_y
            for entry in items:
                if entry is None:
                    cur_y -= GAP_H
                    continue
                label, bold = entry
                self._set_font(bold=bold, size=self.font_size_small)
                self.c.drawString(col_x, cur_y, label)
                cur_y -= ROW_H

        self._set_font(bold=False, size=self.font_size_body)
