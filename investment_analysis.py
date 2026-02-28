"""Simple investment analysis script.

Reads stock price data from CSV and calculates:
- Daily return
- Cumulative return
- Volatility (annualized)
- Equity curve plot
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


TRADING_DAYS_PER_YEAR = 252


def load_price_data(csv_path: Path, date_col: str = "Date", price_col: str = "Close") -> pd.DataFrame:
    """Load and validate stock price data from CSV."""
    df = pd.read_csv(csv_path)

    missing_cols = [col for col in (date_col, price_col) if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required column(s): {', '.join(missing_cols)}")

    df = df[[date_col, price_col]].copy()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df[price_col] = pd.to_numeric(df[price_col], errors="coerce")
    df = df.dropna(subset=[date_col, price_col]).sort_values(by=date_col)

    if df.empty:
        raise ValueError("No valid rows found after parsing Date and Close columns")

    df = df.rename(columns={date_col: "Date", price_col: "Close"})
    return df


def calculate_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate daily return and cumulative return."""
    result = df.copy()
    result["Daily Return"] = result["Close"].pct_change()
    result["Cumulative Return"] = (1 + result["Daily Return"].fillna(0)).cumprod() - 1
    return result


def annualized_volatility(daily_returns: pd.Series) -> float:
    """Calculate annualized volatility from daily returns."""
    clean_returns = daily_returns.dropna()
    if clean_returns.empty:
        return 0.0
    return clean_returns.std() * (TRADING_DAYS_PER_YEAR**0.5)


def plot_equity_curve(df: pd.DataFrame, output_path: Path | None = None) -> None:
    """Plot cumulative return as equity curve."""
    plt.figure(figsize=(10, 5))
    plt.plot(df["Date"], 1 + df["Cumulative Return"], label="Equity Curve")
    plt.title("Equity Curve")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value (Start = 1.0)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    if output_path:
        plt.savefig(output_path, dpi=150)
        print(f"Saved equity curve to {output_path}")
    else:
        plt.show()



def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze stock price data from a CSV file.")
    parser.add_argument("csv_file", type=Path, help="Path to CSV file with Date and Close columns")
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("analysis_output.csv"),
        help="Where to save calculated metrics (default: analysis_output.csv)",
    )
    parser.add_argument(
        "--plot-file",
        type=Path,
        default=None,
        help="Optional path to save equity curve image (e.g. equity_curve.png)",
    )
    parser.add_argument("--date-col", default="Date", help="Name of date column in input CSV")
    parser.add_argument("--price-col", default="Close", help="Name of price column in input CSV")
    return parser.parse_args()



def main() -> None:
    args = parse_args()

    data = load_price_data(args.csv_file, date_col=args.date_col, price_col=args.price_col)
    analyzed = calculate_metrics(data)
    vol = annualized_volatility(analyzed["Daily Return"])

    analyzed.to_csv(args.output_csv, index=False)
    print(f"Saved analysis results to {args.output_csv}")
    print(f"Annualized volatility: {vol:.2%}")

    plot_equity_curve(analyzed, args.plot_file)


if __name__ == "__main__":
    main()
