from . import operators, Panels


ms_to_register = (
    operators,
    Panels,
)


def register():
    for m in ms_to_register:
        m.register()


def unregister():
    for m in (ms_to_register):
        m.unregister()