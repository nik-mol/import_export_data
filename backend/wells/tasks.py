from datetime import date

from celery import current_task
from wells.export.temporary_period import ExportCalculationTemporaryPeriod

from backend import celery_app


@celery_app.task(bind=True)
def export_calculation_temporary_period(self, input_date: date) -> dict:
    """
    Выгрузка отчета по временным приостановкам из ФОНДа ИНК
    """

    workbook = ExportCalculationTemporaryPeriod._write_data_in_excel(input_date)
    filename = f"{current_task.request.id}.xlsx"
    workbook.save(filename=f"files/{filename}")

    return {"file": filename}
