from __future__ import annotations

try:
	import tomllib as _toml
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11 fallback
	import tomli as _toml

TOMLDecodeError = _toml.TOMLDecodeError
load = _toml.load
loads = _toml.loads
