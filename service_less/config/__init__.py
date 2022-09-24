import importlib


_LOCAL_ATTRS = "service_less.config.constants"


"""TODO: Keep track of the loaded
         modules creating a manifest 
"""


def get_module_attr(module: str, attr: str):

    """ Import a module and get an attribute value by name """

    try:
        imported_module = importlib.import_module(module)
        return getattr(imported_module, attr.upper())
    except Exception as e:
        return None


def config_attr(attr: str, local: bool=True):
    """ Get a config attribute from local or user defined source

    Args:
        attr (str): Description
        local (bool, optional): Description

    Returns:
        Config attribute value
    """
    attribute = get_module_attr("config", attr)

    if not bool(attribute) and local:
        attribute = get_module_attr(_LOCAL_ATTRS, attr)

    return attribute