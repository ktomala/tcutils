import pwd
import os


def current_user_name() -> str:
    """Return current user name."""
    return pwd.getpwuid(os.getuid())[0]
