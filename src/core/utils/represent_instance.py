from sqlalchemy import inspect


def represent_instance(instance):
    attributes = ", ".join(
        f"{attribute}={getattr(instance, attribute)}"
        for attribute in inspect(instance).attrs.keys()
    )
    class_name = instance.__class__.__name__
    return f"<{class_name}({attributes})>"
