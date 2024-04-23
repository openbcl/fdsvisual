import bpy
from bpy.types import Operator
import pyopenvdb as vdb


class Object_OT_ImportVDBAll(Operator):
    """Import a VDB-Sequence for every single mesh in the FDS-Simulation"""
    bl_label = "Import all VDBs"
    bl_idname = "mesh.import_vdb_all"
    
    def execute(self, context):
        print("VDB: Import all")
        ## Get mesh data
        from .. import SimulationData
        meshes = SimulationData.meshes
        meshes_n = SimulationData.meshes_n
        
        ## Import VBD sequence
        for n in range(meshes_n):
            mesh = meshes[n]
            Import_VDB(mesh, context)
        
        return {'FINISHED'}


class Object_OT_ImportVDBCustom(Operator):
    """Import VDB-Sequences for custom mesh"""
    bl_label = "Import custom"
    bl_idname = "mesh.import_vdb_custom"
    
    def execute(self, context):
        print("VDB: Import custom VDBs")
        ## Get mesh data
        from .. import SimulationData
        meshes = SimulationData.meshes

        ## Get custom mesh
        setup = context.scene.setup_tool
        n = int(setup.mesh_enum)

        ## Import VDB sequence
        mesh = meshes[n]
        Import_VDB(mesh, context)
        
        return {'FINISHED'}


"""Helper Functions"""
def Import_VDB(mesh, context):
    import os

    from .. import SimulationData
    chid = SimulationData.chid
    nframes_n = SimulationData.nframes_n
    id = mesh.id
    t = 1
    
    ## Define paths and file names
    setup = context.scene.setup_tool
    vdb_path = setup.vdb_path

    vdb_name = f"{chid}-{id}-step={t}"
    vdb_file = f"{vdb_name}.vdb"

    vdb_folder = f"VDB_Sequence {chid}"
    vdb_sequence = os.path.join(vdb_path, vdb_folder, id)
    vdb_filepath = os.path.join(vdb_sequence, vdb_file)

    ## Check if Collection 'VDB' is already created.
    coll_name= "VDBs"
    collections = bpy.data.collections

    if coll_name not in collections:
        coll_new = collections.new(name=coll_name)
        bpy.context.scene.collection.children.link(coll_new)
    
    coll_SceneColl = bpy.context.scene.collection
    coll_Collection = bpy.data.collections.get('Collection')
    coll_VDB = bpy.data.collections.get(coll_name)

    ## Check if VDB is already imported
    print(f"VDB: Import VDB-Sequence '{vdb_name}'")
    objects = bpy.context.scene.objects

    for obj in objects:
        vdb_data_filepath = os.path.join("//", vdb_folder, id, vdb_file)
        # print(vdb_data_filepath) #Development purposes
        # print(obj.data.filepath) #Development purposes
        if obj.type == 'VOLUME' and obj.data.filepath == vdb_data_filepath:
            print(f"   '{vdb_name}' is already imported.")
            return  # Exit the function if the VDB is already imported
    
    ## Get parameters
    vdb_extent = mesh.extent
    x1 = vdb_extent[1][0]
    y1 = vdb_extent[2][0]
    z1 = vdb_extent[0][0]
    
    ## Import VDB
    bpy.ops.object.volume_import(
        filepath = vdb_filepath,
        directory = vdb_sequence,
        files =[{"name":vdb_file}],
        check_existing = True,
        align ='WORLD',
        location = (x1, y1, z1),
        scale = (1, 1, 1)
        )
    bpy.context.object.data.is_sequence = True
    bpy.context.object.data.frame_duration = nframes_n

    ## Find imported VDB and move it to specific collection
    for obj in bpy.context.scene.objects:
        if obj.type == 'VOLUME':
            if coll_VDB:
                coll_VDB.objects.link(obj)
                # Check builtin 'Collection'
                if coll_Collection is not None:
                    for obj in coll_Collection.objects:
                        if obj.type == 'VOLUME':
                            coll_Collection.objects.unlink(obj)
                # Check builtin 'Scene Collection'
                for obj in coll_SceneColl.objects:
                    if obj.type == 'VOLUME':
                        coll_SceneColl.objects.unlink(obj)
            break


bl_classes = [Object_OT_ImportVDBAll, Object_OT_ImportVDBCustom]


def register():
    from bpy.utils import register_class

    for cls in bl_classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(bl_classes):
        unregister_class(cls)