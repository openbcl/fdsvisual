from bpy.types import Panel, PropertyGroup, Scene
from bpy.props import BoolProperty, EnumProperty, PointerProperty, StringProperty


"""Panels in 3D Viewport"""
## User Input of path to FDS-Simulation
# With a PropertyGroup and a PointerProperty you can register all your properties in the scene.
# They are then accessible by panels or operators under the name you've chosen.
# The StringProperty allows you to set the subtype to FILE_PATH which creates a text field with a file selector.
# Once clicked this triggers Blender's file browser and the user can select a file. The path to the file is then stored in the property.

class SimulationSetup(PropertyGroup):
    sim_path: StringProperty(
        name = "FDS Path",
        default = "",
        description = "Define path to FDS-Simulation. Neccessary for Simulation Setup.",
        subtype = "FILE_PATH"
    )
    
    vdb_path: StringProperty(
        name = "VDB Path",
        default = "",
        description = "Define path for operations with VDBs. At this location subfolders are created for VDB-Export. For VDB-Import those subfolders are automatically detected.",
        subtype = "FILE_PATH"
    )

    def get_items(self, context):
        items = []

        from . import SimulationData
        try:
            list = SimulationData.meshes_list
            for item in list:
                items.append(item)
        except:
            return [("NONE", "No Meshes Found", "")]
        return items

    mesh_enum: EnumProperty(
        name = "Custom Mesh",
        description = "Select mesh for custom operators",
        items = get_items
    )

    console_toggle : BoolProperty(
        name = "Toggled System Console",
        description = "Toggle system console on/off",
        default = False
    )



class VIEW3D_PT_FDSVisual(Panel):
    bl_label = "Simulation Setup"     #name in layout
    bl_idname = "VIEW3D_PT_FDSVisual"       #identifier (PT=PanelType)
    bl_space_type = 'VIEW_3D'       #location where to put addon
    bl_region_type = 'UI'           #specification of location
    bl_category = 'FDS Visual'  #create new tab with this name
    
    def draw(self, context):
        layout = self.layout
        setup = context.scene.setup_tool

        layout.prop(setup, "console_toggle")
        layout.operator("wm.toggle_console_property", icon="CONSOLE")
        
        layout.label(text="Path to FDS-Simulation:")
        layout.prop(setup, "sim_path")

        layout.operator("wm.simulation_setup", icon = "SYSTEM")
        
        layout.label(text="Mesh for custom operators:")
        layout.prop(setup, "mesh_enum")
        


class VIEW3D_PT_SimulationData(Panel):
    bl_label = "Simulation Data:"
    bl_idname = "VIEW3D_PT_SimulationData"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'FDS Visual'
    bl_parent_id = "VIEW3D_PT_FDSVisual"
    
    def draw(self, context):
        layout = self.layout
        
        from . import operators
        sim_data = operators.simulation_setup
        try:
            row = layout.row()
            row.label(text=f"{sim_data.chid}", icon = "INFO")
            row = layout.row()
            row.label(text=f"simtime = {sim_data.sim_time} s", icon = "TIME")
            row = layout.row()
            row.label(text=f"timesteps = {sim_data.timesteps_n}", icon = "PREVIEW_RANGE")
            row = layout.row()
            row.label(text=f"nframes = {sim_data.nframes_n} | {sim_data.sim_time/(sim_data.nframes_n-1)} s", icon = "MOD_TIME")
            row = layout.row()
            row.label(text=f"obstructions = {sim_data.obst_n}", icon = "MESH_CUBE")
            row = layout.row()
            row.label(text=f"meshes = {sim_data.meshes_n}", icon = "MESH_GRID")
        except:
            pass


class VIEW3D_PT_Geometry(Panel):
    bl_label = "FDS Geometry"
    bl_idname = "VIEW3D_PT_Geometry"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'FDS Visual'
    # bl_parent_id = "VIEW3D_PT_FDSVisual"
    # bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.label(text="All Meshes Operators")
        row = layout.row()
        row.operator("mesh.import_geometry_all", icon = "SNAP_VOLUME")
        # row = layout.row()
        row.operator("mesh.del_geometry_all", icon = "BRUSHES_ALL")
        
        row = layout.row()
        row.label(text="Custom Mesh Operators")
        row = layout.row()
        row.operator("mesh.import_geometry_custom", icon = "MESH_CUBE")
        # row = layout.row()
        row.operator("mesh.del_geometry_custom", icon = "BRUSH_DATA")


class VIEW3D_PT_VDB(Panel):
    bl_label = "VDBs"
    bl_idname = "VIEW3D_PT_VDB"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'FDS Visual'
    # bl_parent_id = "VIEW3D_PT_FDSVisual"
    # bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        setup = context.scene.setup_tool

        layout.label(text="Path to VDB-Sequences:")
        layout.prop(setup, "vdb_path")
        
        row = layout.row()
        row.label(text="All Meshes Operators") 
        row = layout.row() 
        row.operator("mesh.create_vdb_all", icon = "EXPORT") #OUTLINER_OB_VOLUME
        row.operator("mesh.import_vdb_all", icon = "IMPORT")
        
        row = layout.row()
        row.label(text="Custom Mesh Operators")
        row = layout.row()
        row.operator("mesh.create_vdb_custom", icon = "SORT_DESC")
        row.operator("mesh.import_vdb_custom", icon = "SORT_ASC")


class VIEW3D_PT_Materials(Panel):
    bl_label = "Surface Materials"
    bl_idname = "VIEW3D_PT_Materials"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'FDS Visual'
    # bl_parent_id = "VIEW3D_PT_FDSVisual"
    bl_options = {'DEFAULT_CLOSED'}
    
    def draw(self, context):
        layout = self.layout
        
        row = layout.row()
        row.operator("shader.materialdelete_operator", icon = "TRASH")
        row = layout.row()
        row.operator("shader.fire_n_smoke_operator", icon = "BRUSH_DATA") 
        row = layout.row()
        row.operator("shader.smv_operator", icon = "SEQUENCE_COLOR_03")
        row = layout.row()
        row.operator("shader.glass_operator", icon = "COLORSET_08_VEC")
        row = layout.row()
        row.operator("shader.concrete_operator", icon = "SEQUENCE_COLOR_09")
        row = layout.row()
        row.operator("shader.steel_operator", icon = "COLORSET_13_VEC")
        row = layout.row()
        row.operator("shader.woodlight_operator", icon = "SEQUENCE_COLOR_08")
        row = layout.row()
        row.operator("shader.wooddark_operator", icon = "SEQUENCE_COLOR_08")
        row = layout.row()
        row.operator("shader.bricksred_operator", icon = "SEQUENCE_COLOR_01")
        row = layout.row()
        row.operator("shader.brickswhite_operator", icon = "TEXTURE_DATA")
        

bl_classes = [
    SimulationSetup,
    VIEW3D_PT_FDSVisual,
    VIEW3D_PT_SimulationData,
    VIEW3D_PT_Geometry,
    VIEW3D_PT_VDB,
    VIEW3D_PT_Materials,
]


def register():
    from bpy.utils import register_class

    for cls in bl_classes:
        register_class(cls)
    
    Scene.setup_tool = PointerProperty(type=SimulationSetup)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(bl_classes):
        unregister_class(cls)
    
    del Scene.setup_tool