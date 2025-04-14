import nox
import nox_poetry
from nox import Session

package = "interpolation"
nox.options.sessions = "linter", "formatter", "pytest"
# nox.options.sessions = ["pytest"]
locations = "interpolation", "example", "docs", "tests"


@nox_poetry.session(python="3.12")
def formatter(session: Session) -> None:
    """Run ruff code formatter."""
    args = session.posargs or locations
    session.install("ruff")
    session.run("ruff", "format", *args)


@nox_poetry.session(python="3.12")
def linter(session: Session) -> None:
    """Run ruff code linter."""
    args = session.posargs or locations
    session.install("ruff")
    session.run("ruff", "check", "--fix", *args)


@nox_poetry.session(python="3.12")
def pytest(session: Session) -> None:
    """Run pytest."""
    args = session.posargs or ["--cov=interpolation"]
    session.install("pytest", "pytest-cov", "Pillow", "numpy")
    session.run("pytest", *args)
