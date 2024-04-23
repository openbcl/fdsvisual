import bpy
from bpy.types import Operator

class Object_OT_DelGeometryAll(Operator):
    """"Delete collection and every object"""
    bl_label = "Delete all"
    bl_idname = "mesh.del_geometry_all"
    
    def execute(self, context):
        print("Geometry: Delete all Obstructions")

        coll_name = "Obstructions_All"
        collections = bpy.data.collections

        if coll_name in collections:
            collection = collections[coll_name]
            
            ## Selecting only objects from collection
            bpy.ops.object.select_all(action='DESELECT')
            for obj in collection.all_objects:
                obj.select_set(True)
            
            obj = bpy.ops.object
            Delete_Geometry(obj, collection)
            
            ## Delete orphan data
            # bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=False) #Deletes unused material. Need to fix this
        
        return {'FINISHED'}


class Object_OT_DelGeometryCustom(Operator):
    """"Delete Collection and every object in it"""
    bl_label = "Delete custom"
    bl_idname = "mesh.del_geometry_custom"
    
    def execute(self, context):
        print("Geometry: Delete custom Obstructions")
        ## Get custom mesh
        setup = context.scene.setup_tool
        n = int(setup.mesh_enum)

        ## Get mesh data
        from .. import SimulationData
        meshes = SimulationData.meshes

        coll_name = f"Obstructions_{meshes[n].id}"
        collections = bpy.data.collections
        print(f"   Selected Mesh: {coll_name}")

        if coll_name in collections:
            collection = collections[coll_name]
            
            ## Select only objects from collection
            bpy.ops.object.select_all(action='DESELECT')
            for obj in collection.all_objects:
                obj.select_set(True)
            
            obj = bpy.ops.object
            Delete_Geometry(obj, collection)
            
            ## Delete orphan data
            # bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=False) #Deletes unused material. Need to fix this
        
        return {'FINISHED'}


"""Helper Functions"""
def Delete_Geometry(obj, collection):
    ## Delete objects and collection
    obj.delete()
    bpy.data.collections.remove(collection)
    

bl_classes = [Object_OT_DelGeometryAll, Object_OT_DelGeometryCustom]


def register():
    from bpy.utils import register_class

    for cls in bl_classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(bl_classes):
        unregister_class(cls)