from common.excel_templates.base import ExcelTemplate
from wells.excel_templates.abstract import AbstractTemporaryPeriodWorkSheet
from wells.excel_templates.config.description_sheets import (
    DescriptionHeadersTemporaryPeriod,
    DescriptionSheetsTemporaryPeriod,
)
from wells.excel_templates.config.temporary_period import WorkSheetHeaderTemporaryPeriod


class TemporaryPeriodSheetFirstWorkSheet(AbstractTemporaryPeriodWorkSheet):
    """
    Лист в перечнем всех скважин, находящихся в бездействии и ожидании освоения
    """

    title = "Фонд"
    worksheet_seal = AbstractTemporaryPeriodWorkSheet.create_worksheet_seal(
        DescriptionSheetsTemporaryPeriod.SHEET_1.value
    )


class TemporaryPeriodSheetSecondWorkSheet(AbstractTemporaryPeriodWorkSheet):
    """
    Лист с перечнем скважин, находящихся в бездействии и ожидании освоения 1 календарный месяц
    """

    title = "вр_приост_1"
    worksheet_seal = AbstractTemporaryPeriodWorkSheet.create_worksheet_seal(
        DescriptionSheetsTemporaryPeriod.SHEET_2.value
    )


class TemporaryPeriodSheetThirdWorkSheet(AbstractTemporaryPeriodWorkSheet):
    """
    Лист с перечнем временно приостановленных скважин, у которых проходит срок временной приостановки
    """

    title = "вр_приост_продление"
    worksheet_seal = AbstractTemporaryPeriodWorkSheet.create_worksheet_seal(
        DescriptionSheetsTemporaryPeriod.SHEET_3.value
    )


class TemporaryPeriodSheetFourthWorkSheet(AbstractTemporaryPeriodWorkSheet):
    """
    Лист с перечнем скважин, по которым не выполнена вовремя временная приостановка
    """

    title = "вр_приост_2"
    worksheet_seal = AbstractTemporaryPeriodWorkSheet.create_worksheet_seal(
        DescriptionSheetsTemporaryPeriod.SHEET_4.value
    )


class TemporaryPeriodSheetFifthWorkSheet(AbstractTemporaryPeriodWorkSheet):
    """
    Лист с перечнем скважин, которые были во временной приостановке, запущенные в отчетном месяце из бездействия или ожидания освоения
    """

    title = "вывод_из_вр_приост"
    header = WorkSheetHeaderTemporaryPeriod.get_filtered_headers(
        DescriptionHeadersTemporaryPeriod.BASE_HEADERS.value,
        DescriptionHeadersTemporaryPeriod.HEADERS_OUTPUT_TEMPORARY_PERIOD.value,
    )
    worksheet_seal = AbstractTemporaryPeriodWorkSheet.create_worksheet_seal(
        DescriptionSheetsTemporaryPeriod.SHEET_5.value
    )


class TemporaryPeriodTemplate(ExcelTemplate):
    """
    Шаблон отчета по временным приостановкам из ФОНДа ИНК
    """

    title = "Временные приостановки из ФОНДа ИНК"
    worksheet_list = [
        TemporaryPeriodSheetFirstWorkSheet,
        TemporaryPeriodSheetSecondWorkSheet,
        TemporaryPeriodSheetThirdWorkSheet,
        TemporaryPeriodSheetFourthWorkSheet,
        TemporaryPeriodSheetFifthWorkSheet,
    ]
