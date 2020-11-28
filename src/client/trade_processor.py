import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import client.constants as constants


class TradeProcessor:
    def __init__(self, window_short, window_long, z_threshold):
        self.window_short = window_short
        self.window_long = window_long
        self.z_threshold = z_threshold
        self.anchor_zscore = constants.ANCHOR_Z_SCORE

    def _calculate_mean(self, column):
        return column.mean()

    def _calculate_stdev(self, column):
        return np.std(column)

    def _generate_ma_column_label(self, window):
        return f"{str(window)}{constants.COLUMN_MA_ZSCORE}"

    def _extract_security_names(self, df_columns):
        securities = list(
            filter(lambda column_name: column_name != constants.COLUMN_DATE, df_columns)
        )

        if len(securities) == 2:
            return securities[0], securities[1]

    def calculate_statistics(self, pricing_df):

        # critical to maintain consistency as to what is security A vs B
        # this will define our spread and directly inform buy/sells in the strategy
        security_a, security_b = self._extract_security_names(
            df_columns=list(pricing_df.columns)
        )

        pricing_df[constants.COLUMN_SPREAD] = (
            pricing_df[security_a] / pricing_df[security_b]
        )

        spread_mean = self._calculate_mean(column=pricing_df[constants.COLUMN_SPREAD])
        spread_stdev = self._calculate_stdev(column=pricing_df[constants.COLUMN_SPREAD])

        pricing_df[constants.COLUMN_ZSCORE] = (
            pricing_df[constants.COLUMN_SPREAD] - spread_mean
        ) / spread_stdev

        pricing_df[self._generate_ma_column_label(window=self.window_short)] = (
            pricing_df[constants.COLUMN_ZSCORE].rolling(window=self.window_short).mean()
        )
        pricing_df[self._generate_ma_column_label(window=self.window_long)] = (
            pricing_df[constants.COLUMN_ZSCORE].rolling(window=self.window_long).mean()
        )

        return pricing_df

    def identify_historical_opportunities(self, pricing_df):

        pricing_df[constants.COLUMN_MOMENTUM] = np.where(
            pricing_df[self._generate_ma_column_label(window=self.window_short)]
            >= pricing_df[self._generate_ma_column_label(self.window_long)],
            1,
            -1,
        )

        # pricing_df[constants.]

        # save mean / std at z score entry, can calc a new z score for each new entry
        # this'll be used as the decision point w/ the threshold as to whether to hold or exit

        print(pricing_df.tail(30))

    def _add_horizontal_line(self, axis, y_value):
        axis.axhline(
            y=y_value,
            color=constants.HORIZONTAL_LINE_COLOR,
            ls=constants.HORIZONTAL_LINE_STYLE,
        )

    def visualize_relationship(self, pricing_df):

        current_axis = plt.gca()

        pricing_df.plot.line(
            x=constants.COLUMN_DATE, y=constants.COLUMN_ZSCORE, ax=current_axis
        )
        pricing_df.plot.line(
            x=constants.COLUMN_DATE,
            y=self._generate_ma_column_label(window=self.window_short),
            ax=current_axis,
        )
        pricing_df.plot.line(
            x=constants.COLUMN_DATE,
            y=self._generate_ma_column_label(window=self.window_long),
            ax=current_axis,
        )

        self._add_horizontal_line(
            axis=current_axis, y_value=self.anchor_zscore - self.z_threshold
        )
        self._add_horizontal_line(axis=current_axis, y_value=self.anchor_zscore)
        self._add_horizontal_line(
            axis=current_axis, y_value=self.anchor_zscore + self.z_threshold
        )

        plt.show()
