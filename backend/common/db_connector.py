import connectorx as cx
import numpy as np
from django.db import connections


class ConnectorManager:
    @classmethod
    def __create_db_url(cls) -> str:
        """
        Возвращает урлу подключения к бд
        """
        default_settings = connections["default"].settings_dict
        return "".join(
            [
                default_settings["ENGINE"].split(".")[
                    -1
                ],  # чтобы был postgresql а не django.backends...
                "://",
                default_settings["USER"],
                ":",
                default_settings["PASSWORD"],
                "@",
                default_settings["HOST"],
                ":",
                str(default_settings["PORT"]),
                "/",
                default_settings["NAME"],
            ]
        )

    @classmethod
    def get_raw_data(
        cls,
        query: str,
    ) -> np.ndarray:
        """
        Метод отдающий np.array через connectorx
        """

        url = cls.__create_db_url()

        return cx.read_sql(
            conn=url,
            query=query,
            return_type="polars",
        ).to_numpy()
