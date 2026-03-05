---
project_name: 'BMad_Project'
user_name: 'Jenn'
date: '2026-03-05'
sections_completed: ['technology_stack', 'language_rules', 'framework_rules', 'testing_rules', 'quality_rules', 'workflow_rules', 'anti_patterns']
status: 'complete'
rule_count: 42
optimized_for_llm: true
---

# Project Context for AI Agents

_This file contains critical rules and patterns that AI agents must follow when implementing code in this project. Focus on unobvious details that agents might otherwise miss._

---

## Technology Stack & Versions

- Python 3.13
- Streamlit >= 1.32.0 (use `@st.cache_data`, NOT deprecated `@st.cache`)
- yfinance >= 0.2.0
- Plotly >= 5.0.0 (plotly.express for all charts)
- Pandas >= 2.0.0
- pytest >= 7.0.0
- Virtual environment: `.venv/` (Python 3.13)

## Critical Implementation Rules

### Language-Specific Rules (Python)

- Use `X | Y` union type syntax (not `Optional[X]`) — requires Python 3.10+
- Annotate return types on all public functions
- Absolute imports only; never use relative imports (`.module`)
- `config.py` is the single source of truth — import constants from it, never hardcode page paths or ticker strings inline
- Data layer functions return `None` on failure; never raise exceptions to callers
- Catch exceptions broadly in data layer with `except Exception as e`; log with `logger.warning()`
- No `print()` anywhere — use `logging.getLogger(__name__)` at module level in all non-UI files
- Log messages use structured key=value format: `logger.warning("fn_name: msg key=%s", value)`

### Framework-Specific Rules (Streamlit)

- All external API calls (yfinance) must use `@st.cache_data(ttl=3600)` — never call `yf.Ticker()` directly in a component
- Caching belongs in the data layer (`data/`), never in UI components or pages
- Page path constants live in `config.py`; use them via `st.switch_page(PAGE_CONSTANT)` — never hardcode path strings
- Inter-page state passes through `st.session_state`; always use `.get()` and guard against `None` before `st.stop()`
- Every button rendered in a loop needs a unique `key=f"btn_{identifier}"` — duplicate keys crash Streamlit
- `st.set_page_config()` must be the first Streamlit call in every page file
- Charts: always pass `use_container_width=True` to `st.plotly_chart()`
- Dashboard column count is dynamic: `st.columns(len(TICKERS))` — do not hardcode column count

### Testing Rules

- Test files live in `tests/`; named `test_{module}.py` mirroring the source module
- Group related tests in a class: `class TestFunctionName:`
- Mock at the consuming module's import path, not the source: `patch("data.fetcher.yf.Ticker")` not `patch("yfinance.Ticker")`
- Use factory helpers (e.g. `_make_ticker_mock()`) for reusable mock setup — don't inline identical mock construction
- Every data-layer function needs minimum 3 tests: happy path, empty/no-data, exception
- Assert exact column names with `list(result.columns) == [...]`, not just shape or dtype
- `@st.cache_data` wraps `get_history` — patch `yf.Ticker` before invoking, or call `get_history.clear()` in test teardown to avoid cache bleed between tests

### Code Quality & Style Rules

- File naming: `snake_case.py`; function naming: `snake_case`; constants: `UPPER_SNAKE_CASE`
- No business logic in `app.py` — entry point only; wire components, nothing else
- No Streamlit calls (`st.*`) allowed inside `data/` modules — data layer must be UI-agnostic
- `components/` functions are stateless render functions; accept `ticker: str` and `col` as parameters
- `config.py` holds constants only — no functions, no side effects, no conditional logic beyond env-var parsing
- Public functions get a single-line docstring: purpose, key args, return value
- Mark intentional deferred work with `# BACKLOG:` comments — do not remove existing ones; add new ones rather than leaving silent gaps

### Development Workflow Rules

- Run app: `streamlit run app.py` from project root with `.venv` active
- Run tests: `pytest` from project root (no config file; uses pytest defaults)
- Tickers are set via `STOCK_TICKERS` env var (comma-separated); fallback list is in `config.py`
- Adding a new page: (1) add path constant to `config.py`, (2) create `pages/{name}.py`, (3) reference via constant — never hardcode the path string at call sites
- No CI/CD pipeline exists — manual testing before commit
- Primary branch is `main`

### Critical Don't-Miss Rules

- NEVER call `yf.Ticker().history()` outside `data/fetcher.py` — always go through `get_history()`
- yfinance returns Date as the DataFrame index, NOT a column — always call `df.reset_index()` before selecting `["Date", "Close"]`
- Always guard `len(history) < 2` before computing price change — yfinance can return fewer than 2 rows, causing division by zero
- Data-layer functions return `None`; callers check for `None` — never add try/except in components, never raise from `data/`
- `st.session_state.get("selected_ticker")` returns `None` on direct page load — every page that reads session state must guard and `st.stop()`
- Prices display with `$` but yfinance returns native exchange currency — do not add currency logic without also fetching `ticker.info["currency"]` (BACKLOG)
- If a user-facing ticker input is ever added, validate against an alphanumeric whitelist before passing to yfinance (BACKLOG in `pages/stock_detail.py`)

---

## Usage Guidelines

**For AI Agents:**

- Read this file before implementing any code in this project
- Follow ALL rules exactly as documented
- When in doubt, prefer the more restrictive option
- Add `# BACKLOG:` comments for gaps rather than implementing partial solutions

**For Humans:**

- Keep this file lean and focused on agent needs
- Update when technology stack or patterns change
- Review periodically to remove rules that become obvious over time

Last Updated: 2026-03-05
