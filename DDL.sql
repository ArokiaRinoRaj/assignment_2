--stock_volatility
CREATE TABLE mydb.stock_volatility (
    ticker VARCHAR(20) PRIMARY KEY,
    volatility DECIMAL(10, 6)  -- standard deviation (not percentage)
);


--cumulative_returns
CREATE TABLE mydb.cumulative_returns (
    ticker VARCHAR(20) PRIMARY KEY,
    cumulative_return DECIMAL(10, 4)  -- can be negative or positive, in percentage
);


--sector_performance
CREATE TABLE mydb.sector_performance (
    sector VARCHAR(50),
    average_return DECIMAL(10, 4)  -- sector-wise average return in percentage
);


--daily_returns
CREATE TABLE mydb.daily_returns (
    date DATE,
    ticker VARCHAR(20),
    daily_return DECIMAL(10, 4),
    PRIMARY KEY (date, ticker)
);

--monthly_performance
CREATE TABLE mydb.monthly_performance (
    month DATE,
    ticker VARCHAR(20),
    monthly_return DECIMAL(10, 2),
    PRIMARY KEY (month, ticker)
);


