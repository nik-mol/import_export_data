import polars as pl
from django.db import models
from django.db.models.functions import Lower, Trim


class HandbookLoader:
    """
    Класс для выгрузки данных по Газовому обслуживанию
    """

    @staticmethod
    def get_handbook(model: models.Model) -> pl.DataFrame:
        """
        Выгрузка справочников

        Args:
            data (QuerySet): сам queryset из джанги

        Returns:
            pl.Dataframe: датафрейм со справочником
        """

        queryset = model.objects.values("id").annotate(name=Trim(Lower("name")))

        if queryset.count() == 0:
            dataframe = pl.DataFrame(schema={"id": pl.Int64, "name": pl.String})

        else:
            dataframe = pl.from_records(list(queryset))

        return dataframe
