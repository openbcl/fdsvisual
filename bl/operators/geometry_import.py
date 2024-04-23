import bpy
from bpy.types import Operator


class Object_OT_ImportGeometryAll(Operator):
    """Create new collection and import all obstructions from FDS-simulation"""
    bl_label = "Import all"
    bl_idname = "mesh.import_geometry_all"
    
    def execute(self, context):
        print("Geometry: Import all Obstructions")
        ## Get obstruction data
        from .. import SimulationData
        obst = SimulationData.obst
        obst_n = SimulationData.obst_n

        coll_name = "Obstructions_All"
        collections = bpy.data.collections

        ## Check if collection is not created yet. Then create collection
        if coll_name not in collections:
            coll_new = collections.new(coll_name)
            bpy.context.scene.collection.children.link(coll_new)
        
            for n in range(obst_n):
                obj = obst[n]
                Import_Geometry(obj, coll_name)
        
        return {'FINISHED'}


class Object_OT_ImportGeometryCustom(Operator):
    """Create new collection and import obstructions from single mesh"""
    bl_label = "Import custom"
    bl_idname = "mesh.import_geometry_custom"
    
    def execute(self, context):
        print("Geometry: Import custom Obstructions")
        ## Get custom mesh
        setup = context.scene.setup_tool
        n = int(setup.mesh_enum)

        ## Get mesh data
        from .. import SimulationData
        meshes = SimulationData.meshes

        obst = meshes[n].obstructions
        obst_n = len(obst)

        coll_name = f"Obstructions_{meshes[n].id}"
        collections = bpy.data.collections
        print(f"   Selected Mesh: {coll_name}")

        ## Check if collection is not created yet. Then create collection
        if coll_name not in collections:
            coll_new = collections.new(coll_name)
            bpy.context.scene.collection.children.link(coll_new)
        
            for n in range(obst_n):
                obj = obst[n]
                Import_Geometry(obj, coll_name)
        
        return {'FINISHED'}



"""Helper Functions"""
def Import_Geometry(obj, coll_name):
    ## Get some geometry data
    id: str = obj.id

    obst_bound = obj.bounding_box
    x1 = obst_bound.x_start
    x2 = obst_bound.x_end
    y1 = obst_bound.y_start
    y2 = obst_bound.y_end
    z1 = obst_bound.z_start
    z2 = obst_bound.z_end
    
    ## Define all vertices and faces
    verts = [
    (x1, y1, z1),
    (x1, y2, z1),
    (x2, y2, z1),
    (x2, y1, z1),
    (x1, y1, z2),
    (x1, y2, z2),
    (x2, y2, z2),
    (x2, y1, z2),
    ]
    
    faces = [
    (0, 1, 2, 3),
    (7, 6, 5, 4),
    (5, 6, 2, 1),
    (6, 7, 3, 2),
    (7, 4, 0, 3),
    (4, 5, 1, 0),
    ]
    
    edges = []
    
    ## Create mesh 
    mesh_data = bpy.data.meshes.new(f"OBST_{id}")
    mesh_data.from_pydata(verts, edges, faces)

    ## Create new object and add to collection in outliner
    mesh_obj = bpy.data.objects.new(f"{id}", mesh_data)
    
    bpy.data.collections[coll_name].objects.link(mesh_obj)

    ## Check color_index of obj and set rgba-value as material
    rgba, color_index = get_rgba(obj)

    if color_index == -1:
        material = bpy.data.materials.get("Smokeview")
        mesh_obj.data.materials.append(material)
    elif color_index == -2:
        material_name = "Invisible" #später dann rgba
        shader_name = "GeomImport"
        create_material(shader_name, material_name, rgba)

        material = bpy.data.materials.get(material_name)
        mesh_obj.data.materials.append(material)
    else:
        material_name = f"FDS_Color with {rgba}"
        shader_name = "GeomImport"
        create_material(shader_name, material_name, rgba)

        material = bpy.data.materials.get(material_name)
        mesh_obj.data.materials.append(material)



def get_rgba(obj):
        color_index = obj.color_index
        if color_index == -1:
            rgba = (1, 0.8, 0.4, 1) # -1 = default color
        elif color_index == -2:
            rgba = (1, 1, 1, 0) # -2 = invisible
        else:
            rgba = obj.rgba # -3 = use red, green, blue and alpha (rgba attribute) n>0 - use n’th color table entry
        return rgba, color_index



def create_material(shader_name, material_name, rgba):
    from .. import Materials
    shaders = bpy.data.materials
    function_name = f"Create_Shader_{shader_name}"

    if material_name not in shaders:
        print(f"Geometry: {material_name} does not exist in blender file")
        if hasattr(Materials, function_name):
            print(f"   Create material shader: {material_name}")
            getattr(Materials, function_name)(material_name, rgba)



bl_classes = [Object_OT_ImportGeometryAll, Object_OT_ImportGeometryCustom]


def register():
    from bpy.utils import register_class

    for cls in bl_classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(bl_classes):
        unregister_class(cls)