import importlib


_LOCAL_ATTRS = "core.conf.vars"


def get_module_attr(module: str, attr: str):

	""" Import a module and get an attribute value by name """

    try:
        imported_module = importlib.import_module(module)
        return getattr(imported_module, attr.upper())
    except Exception:
        return None


def config_attr(attr: str, local: bool=True):
    """ Get a config attribute from local or user defined source

    Args:
        attr (str): Description
        local (bool, optional): Description

    Returns:
        Config attribute value
    """
    attribute = get_module_attr(attr, "config")

    if not bool(attribute) and local:
        attribute = get_module_attr(attr, _LOCAL_ATTRS)

    return attribute