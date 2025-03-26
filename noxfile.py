import nox
import nox_poetry
from nox import Session

package = "interpolation"
nox.options.sessions = "formatter", "pytest"
locations = ["interpolation"]

@nox_poetry.session(python="3.12")
def formatter(session: Session) -> None:
    """Run ruff code formatter."""
    args = session.posargs or locations
    session.install("ruff")
    session.run("ruff", "format", *args)

@nox_poetry.session(python="3.12")
def pytest(session: Session) -> None:
    """Run pytest."""
    args = session.posargs or ["--cov=interpolation"]
    session.install("pytest", "pytest-cov", "Pillow")
    session.run("pytest", *args)
