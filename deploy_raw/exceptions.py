from __future__ import annotations


class ValidationError(ValueError):
	pass


class ServiceNotFoundError(Exception):
	pass


class MixinMissingAttributesError(Exception):
	pass

