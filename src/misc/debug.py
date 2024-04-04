from os import getenv

# Перевод DEBUG_MODE в bool
is_debug = bool(getenv('DEBUG_MODE', False))