import nox
import nox_poetry
from nox import Session

package = "interpolation"
nox.options.sessions = "linter", "formatter", "pytest", "documentation"
# nox.options.sessions = ["documentation"]
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


@nox_poetry.session(python="3.12")
def documentation(session: Session) -> None:
    """Generate documentation."""
    session.install("sphinx",
                    "sphinx_rtd_theme",
                    "sphinx_click",
                    "myst_parser",
                    "linkify-it-py")
    
    session.run("python", "-c", "import sys; sys.path.insert(0, '.')")
    session.run("sphinx-build", "-M", "html", "docs/source/", "docs/build/")