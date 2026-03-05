import sys

import pytest


class TestConfig:
    def _reload_config(self):
        sys.modules.pop("config", None)
        import config
        return config

    def test_app_title_is_non_empty_string(self):
        import config
        assert isinstance(config.APP_TITLE, str)
        assert len(config.APP_TITLE) > 0

    def test_default_tickers_without_env(self, monkeypatch):
        monkeypatch.delenv("STOCK_TICKERS", raising=False)
        config = self._reload_config()
        assert config.TICKERS == ["META", "GOOGL", "MSFT"]

    def test_custom_tickers_from_env(self, monkeypatch):
        monkeypatch.setenv("STOCK_TICKERS", "AAPL,TSLA,AMZN")
        config = self._reload_config()
        assert config.TICKERS == ["AAPL", "TSLA", "AMZN"]

    def test_tickers_normalized_to_uppercase(self, monkeypatch):
        monkeypatch.setenv("STOCK_TICKERS", "aapl,tsla")
        config = self._reload_config()
        assert config.TICKERS == ["AAPL", "TSLA"]

    def test_tickers_strips_whitespace(self, monkeypatch):
        monkeypatch.setenv("STOCK_TICKERS", "AAPL, TSLA , AMZN")
        config = self._reload_config()
        assert config.TICKERS == ["AAPL", "TSLA", "AMZN"]

    def test_page_constants_are_strings(self):
        import config
        assert isinstance(config.PAGE_DASHBOARD, str)
        assert isinstance(config.PAGE_DETAIL, str)
