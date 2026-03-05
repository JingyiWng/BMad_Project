from unittest.mock import patch


def pytest_configure(config):
    """Patch st.cache_data to a no-op before any test module is imported."""
    patch("streamlit.cache_data", lambda **kwargs: (lambda f: f)).start()
