# Investment Analysis (Python)

A simple Python project for stock investment analysis using **pandas** and **matplotlib**.

## Features

- Read stock price data from CSV
- Calculate **daily return**
- Calculate **cumulative return**
- Calculate **annualized volatility**
- Plot **equity curve**
- Export analyzed data to CSV

## Project Structure

- `investment_analysis.py` – main analysis script
- `requirements.txt` – project dependencies

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Input CSV Format

The input CSV should include at least these columns:

- `Date`
- `Close`

Example:

```csv
Date,Close
2024-01-01,100
2024-01-02,101.5
2024-01-03,99.8
```

If your column names are different, use `--date-col` and `--price-col`.

## Usage

```bash
python investment_analysis.py path/to/stock_prices.csv --plot-file equity_curve.png
```

Optional arguments:

- `--output-csv` (default: `analysis_output.csv`) – path to save computed metrics
- `--plot-file` – if provided, saves the chart as an image instead of displaying it
- `--date-col` (default: `Date`) – input date column name
- `--price-col` (default: `Close`) – input close price column name

## Output

The script prints annualized volatility and writes an output CSV with:

- `Date`
- `Close`
- `Daily Return`
- `Cumulative Return`

It also shows or saves an equity curve where starting portfolio value is normalized to `1.0`.
