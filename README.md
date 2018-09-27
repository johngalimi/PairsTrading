# PairsTrading

I designed a statistical arbitrage trading strategy commonly known as "Pairs Trading". My algorithm groups stocks in the S&P 500 by industry and applies multiple statistical tests (Cointegration Test & Augmented Dicky-Fuller (Stationarity) Test) to identify if a historical relationship exists between pairs of securities.

If a relationship exists, my program monitors the "spread" between the two stocks and generates trades when the spread widens too much (with the expectation that the pair's spread will revert to its historical mean). To exploit this, my algorithm signals a SELL of the outperforming stock and a BUY for the underperformer.


I maninly used pandas and numpy for the data analysis and matplotlib to handle the visualizations.
