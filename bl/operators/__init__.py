from . import (
    geometry_del,
    geometry_import,
    material_add,
    simulation_setup,
    vdb_create,
    vdb_import
)

ms_to_register = (
    geometry_import,
    geometry_del,
    material_add,
    simulation_setup,
    vdb_create,
    vdb_import
)


def register():
    for m in ms_to_register:
        m.register()


def unregister():
    for m in reversed(ms_to_register):
        m.unregister()