import pandas as pd
import numpy as np
import src.client.constants as constants


class TradeProcessor:
    def _calculate_mean(self, column):
        return column.mean()

    def _calculate_stdev(self, column):
        return np.std(column)

    def _generate_ma_column_label(self, window):
        return f"{str(window)}{constants.COLUMN_MA_ZSCORE}"

    def calculate_statistics(self, pricing_df, window_short, window_long):
        spread_column = pricing_df[constants.COLUMN_SPREAD]

        spread_mean = self._calculate_mean(column=spread_column)
        spread_stdev = self._calculate_stdev(column=spread_column)

        pricing_df[constants.COLUMN_ZSCORE] = (
            pricing_df[constants.COLUMN_SPREAD] - spread_mean
        ) / spread_stdev

        pricing_df[self._generate_ma_column_label(window=window_short)] = pricing_df[constants.COLUMN_ZSCORE].rolling(window=window_short).mean()
        pricing_df[self._generate_ma_column_label(window=window_long)] = pricing_df[constants.COLUMN_ZSCORE].rolling(window=window_long).mean()

        return pricing_df
