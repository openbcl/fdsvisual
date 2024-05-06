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
        surfaces = SimulationData.surfaces

        coll_name = "Obstructions_All"
        collections = bpy.data.collections

        ## Check if collection is not created yet. Then create collection
        if coll_name not in collections:
            coll_new = collections.new(coll_name)
            bpy.context.scene.collection.children.link(coll_new)
        
            for n in range(obst_n):
                obj = obst[n]
                Import_Geometry(obj, coll_name, surfaces)
        
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

        ## Get obstruction data
        obst = meshes[n].obstructions
        obst_n = len(obst)
        surfaces = SimulationData.surfaces

        coll_name = f"Obstructions_{meshes[n].id}"
        collections = bpy.data.collections
        print(f"   Selected Mesh: {coll_name}")

        ## Check if collection is not created yet. Then create collection
        if coll_name not in collections:
            coll_new = collections.new(coll_name)
            bpy.context.scene.collection.children.link(coll_new)
        
            for n in range(obst_n):
                obj = obst[n]
                Import_Geometry(obj, coll_name, surfaces)
        
        return {'FINISHED'}



"""Helper Functions"""
def Import_Geometry(obj, coll_name, surfaces):
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

    ## Set RGBA to obj as material. Priority for each Obst: Color, then Surf_Id with Color, then default ('INERT' = 'Smokeview')
    rgba, color_index = get_rgba(obj)

    if color_index == -3: # Check if Color was assigned to Obst
        shader_name = "GeomImport"
        material_name = f"FDS_Color with {rgba}"
        create_material(shader_name, material_name, rgba)

        material = bpy.data.materials.get(material_name)
        mesh_obj.data.materials.append(material)

    elif color_index == -2:
        shader_name = "GeomImport"
        material_name = "Invisible"
        create_material(shader_name, material_name, rgba)

        material = bpy.data.materials.get(material_name)
        mesh_obj.data.materials.append(material)

    else: # Check if Surf_Id with Color was assigned - otherwise set default surface ('INERT' = 'Smokeview') as material
        sub_obst = obj[0] #Get the first Subobstruction, if you used 'SURF_IDS' or 'SURF_ID6' --> feature expansion is required.
        surf_name = sub_obst.side_surfaces[0].name #Take first element, because all six sid_surfaces have same surface name.
        if surf_name == "INERT":
            material = bpy.data.materials.get("Smokeview")
            mesh_obj.data.materials.append(material)
        else:
            for s in surfaces:
                if s.name == surf_name:
                    surface = s
                    break

            rgb = surface.rgb
            transparency = surface.transparency
            rgba = rgb + (transparency,) #Transform transparency into Tuple

            shader_name = "GeomImport"
            material_name = f"FDS_SurfId {surf_name} with {rgba}"
            create_material(shader_name, material_name, rgba)

            material = bpy.data.materials.get(material_name)
            mesh_obj.data.materials.append(material)



def get_rgba(obj):
        color_index = obj.color_index
        if color_index == -1:
            rgba = (1.0, 0.8, 0.4, 1.0) # -1 = default color
        elif color_index == -2:
            rgba = (1.0, 1.0, 1.0, 0.0) # -2 = invisible
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