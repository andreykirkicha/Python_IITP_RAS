import nox
import nox_poetry
from nox import Session

package = "interpolation"
nox.options.sessions = "linter", "formatter", "pytest", "documentation"
# nox.options.sessions = ["performance"]
locations = "interpolation", "example", "docs", "tests", "plots"


@nox_poetry.session(python="3.12")
def formatter(session: Session) -> None:
    """Run ruff code formatter."""
    args = locations
    session.install("ruff")
    session.run("ruff", "format", *args)


@nox_poetry.session(python="3.12")
def linter(session: Session) -> None:
    """Run ruff code linter."""
    args = locations
    session.install("ruff")
    session.run("ruff", "check", "--fix", *args)


@nox_poetry.session(python="3.12")
def pytest(session: Session) -> None:
    """Run pytest."""
    args = ["--cov=interpolation"]
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

@nox_poetry.session(python="3.12")
def performance(session: Session) -> None:
    """Build performance plots."""
    args = locations
    session.install("Pillow", "matplotlib")
    session.install(".")
    session.run("python", "plots/performance.py", *args)
    session.run("rm", "-r", "dist", external=True)
