from typing import Dict, List, Optional
import yfinance as yf
import pandas as pd
from core.interfaces.market_data import MarketDataProvider, MarketDataAsset, MarketDataExchange
from core.domain.enums import AssetClass

class YFinanceMarketDataProvider(MarketDataProvider):
    def get_asset_details(self, ticker: str) -> Optional[MarketDataAsset]:
        try:
            ticker_obj = yf.Ticker(ticker)
            info = ticker_obj.info

            # yfinance info dict keys vary, we need to be defensive
            if not info or 'symbol' not in info:
                return None

            return self._map_to_asset_data(ticker, info)
        except Exception as e:
            # Log error ideally
            print(f"Error fetching data for {ticker}: {e}")
            return None

    def get_exchange_details(self, mic_code: str) -> Optional[MarketDataExchange]:
        # yfinance doesn't expose a direct "get exchange by mic" API easily.
        # We might need to infer this or return None if strictly relying on yf.
        # For now, we'll return None as YFinance is asset-centric.
        return None

    def get_assets_bulk(self, tickers: List[str]) -> Dict[str, Optional[MarketDataAsset]]:
        results = {}
        # YFinance download is for price data, Tickers is for info
        # For bulk info, it's actually slower with yf.Tickers if we access .info one by one
        # But let's try to use it.

        # Optimization: yfinance Tickers object
        tickers_obj = yf.Tickers(" ".join(tickers))

        for ticker_symbol in tickers:
            try:
                ticker_data = tickers_obj.tickers[ticker_symbol]
                # Note: Accessing .info triggers a request per ticker usually
                info = ticker_data.info
                if info and 'symbol' in info:
                    results[ticker_symbol] = self._map_to_asset_data(ticker_symbol, info)
                else:
                    results[ticker_symbol] = None
            except Exception as e:
                print(f"Error fetching bulk data for {ticker_symbol}: {e}")
                results[ticker_symbol] = None

        return results

    def _map_to_asset_data(self, ticker: str, info: dict) -> MarketDataAsset:
        # Map yfinance 'quoteType' to AssetClass
        # EQUITY, ETF, MUTUALFUND, CRYPTOCURRENCY, CURRENCY, INDEX, FUTURE, OPTION
        quote_type = info.get('quoteType', 'EQUITY').upper()

        asset_class_map = {
            'EQUITY': AssetClass.STOCK,
            'ETF': AssetClass.ETF,
            'CRYPTOCURRENCY': AssetClass.CRYPTO,
            # Default fallback
        }

        # If not in map, default to STOCK or handle error.
        # For this implementation, we default to STOCK if unknown, or we could be more strict.
        asset_class = asset_class_map.get(quote_type, AssetClass.STOCK)

        # Try to find ISIN
        isin = info.get('isin')

        # Currency
        currency = info.get('currency', 'USD')

        # Name
        name = info.get('longName') or info.get('shortName') or ticker

        # Exchange
        exchange = info.get('exchange') # This is usually the exchange code like 'NMS', 'NYQ'

        return MarketDataAsset(
            ticker=ticker,
            name=name,
            currency=currency,
            asset_class=asset_class.value, # Enum value string
            isin=isin,
            exchange_mic=exchange # Note: This is NOT a MIC code usually, but a YF exchange code. We need to map this later.
        )
