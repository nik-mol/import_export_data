from datetime import date

from wells.models import (
    CharacteristicBaseFund,
    District,
    Field,
    Pad,
    Well,
    WellsBaseFund,
    WellsStatus,
    WellsStatuses,
)


class CalculationTemporaryPeriodLoader:
    """
    Класс для выгрузки данных для отчета по временным приостановкам из ФОНДа ИНК
    """

    need_statuses: tuple[str, str, str, str] = (
        "В ож.освоения",
        "Бездействие текущего года",
        "Бездействие прошлых лет",
        "Бездействующая",
    )
    statuses_work_simple: tuple[str, str] = (
        "В работе",
        "Простой",
    )

    @classmethod
    def get_wells(cls, sheet_number: float = 1) -> str:
        """
        Выгрузка скважин для отчета по временным приостановкам из ФОНДа ИНК

        Args:
            sheet_number (int): номер листа

        Returns:
                str: сформированный SQL-запрос
        """

        delay_conditions = {
            2: "cbf.delay_start = lwbf.latest_date",
            3: "lwbf.latest_date = cbf.delay_period - INTERVAL '1 month'",
            4.1: "cbf.delay_period <= lwbf.latest_date",
            4.2: "cbf.delay_start < lwbf.latest_date AND cbf.delay_period IS NULL",
        }

        delay_condition = delay_conditions.get(sheet_number, "")
        if delay_condition:
            delay_condition = delay_condition + " AND"

        return f"""
            WITH LatestWellsBaseFund AS (
                SELECT
                    well_id,
                    MAX(date) AS latest_date
                FROM {WellsBaseFund._meta.db_table}
                GROUP BY well_id
            )
            SELECT
                d.short_name as license_name,
                f.short_name as field_name,
                SPLIT_PART(w.name, '_', 2) AS well_number,
                w.name,
                p.name as pad_name,
                ws.name as status_name,
                cbf.building_end_date AS end_date,
                cbf.delay_period AS delay_period,
                cbf.delay_start AS delay_start
            FROM {WellsBaseFund._meta.db_table} wbf
            JOIN {Well._meta.db_table} w ON wbf.well_id = w.id
            JOIN {Pad._meta.db_table} p ON w.wellpad_id = p.id
            JOIN {Field._meta.db_table} f ON p.field_id = f.id
            JOIN {District._meta.db_table} d ON p.license_id = d.id
            JOIN {WellsStatus._meta.db_table} ws ON wbf.status_id = ws.id
            JOIN {WellsStatuses._meta.db_table} wss ON ws.status_id = wss.id
            JOIN {CharacteristicBaseFund._meta.db_table} cbf ON wbf.well_id = cbf.well_id
            JOIN LatestWellsBaseFund lwbf ON wbf.well_id = lwbf.well_id AND wbf.date = lwbf.latest_date
            WHERE
                {delay_condition}
                wss.name IN {cls.need_statuses}
        """

    @classmethod
    def get_wells_output_temporary_period(cls, input_date: date) -> str:
        """
        Выгрузка скважин которые были во временной приостановке, запущенные в отчетном месяце из бездействия или ожидания освоения

        Args:
            input_date (date): дата на которую сформировать отчет

        Returns:
                str: сформированный SQL-запрос
        """

        if input_date:
            formatted_input_date = input_date.strftime("'%Y-%m-%d'")
            filter_latest_well = f"si.date = {formatted_input_date}"
            select_previous_well = "si.status_fund AS previous_status"
            filter_previous_well = f"""
                FROM StatusInfo si
                WHERE
                    si.date + INTERVAL '1 month' = {formatted_input_date}
            """
        else:
            filter_latest_well = f"""(si.well_id, si.date) IN (
                                        SELECT
                                            well_id,
                                            MAX(date) AS latest_date
                                        FROM
                                            {WellsBaseFund._meta.db_table}
                                        GROUP BY
                                            well_id
                                    )"""
            select_previous_well = "si.previous_status"
            filter_previous_well = """
                FROM (
                    SELECT
                        well_id,
                        ROW_NUMBER() OVER (PARTITION BY well_id ORDER BY date DESC) AS rank,
                        status_name,
                        status_fund AS previous_status
                    FROM
                        StatusInfo
                ) si
                WHERE
                    si.rank = 2
            """

        return f"""
            WITH StatusInfo AS (
                SELECT
                    wbf.well_id,
                    wbf.date,
                    wss.name AS status_name,
                    ws.name AS status_fund
                FROM {WellsBaseFund._meta.db_table} wbf
                JOIN {WellsStatus._meta.db_table} ws ON wbf.status_id = ws.id
                JOIN {WellsStatuses._meta.db_table} wss ON ws.status_id = wss.id
            ),
            LatestWellsBaseFund AS (
                SELECT
                    si.well_id,
                    si.status_fund AS last_status
                FROM StatusInfo si
                WHERE
                    {filter_latest_well}
                    AND si.status_name IN {cls.statuses_work_simple}
            ),
            PreviousWellsBaseFund AS (
                SELECT
                    si.well_id,
                    {select_previous_well}
                {filter_previous_well}
                AND si.status_name IN {cls.need_statuses}
            )
            SELECT
                d.short_name as license_name,
                f.short_name as field_name,
                SPLIT_PART(w.name, '_', 2) AS well_number,
                w.name as well_name,
                p.name as pad_name,
                pwbf.previous_status,
                lwdf.last_status
            FROM LatestWellsBaseFund lwdf
            JOIN PreviousWellsBaseFund pwbf ON lwdf.well_id = pwbf.well_id
            JOIN {Well._meta.db_table} w ON lwdf.well_id = w.id
            JOIN {Pad._meta.db_table} p ON w.wellpad_id = p.id
            JOIN {Field._meta.db_table} f ON p.field_id = f.id
            JOIN {District._meta.db_table} d ON p.license_id = d.id
            JOIN {CharacteristicBaseFund._meta.db_table} cbf ON lwdf.well_id = cbf.well_id
            WHERE
                cbf.delay_period IS NOT NULL
        """
