def fix_id(element):
    """Convierte el _id de MongoDB a id y lo convierte a string."""
    if element:
        element["id"] = str(element["_id"])
        del element["_id"]
    return element