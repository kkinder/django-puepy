from pathlib import Path

package_path = Path(__file__).parent.resolve()
static_path = (package_path / "static" / "django_puepy").resolve()

assert package_path.is_dir()
assert static_path.is_dir()

__all__ = ["package_path", "static_path"]
