import getpass


def current_user_name() -> str:
    """Return current user name."""
    return getpass.getuser()
