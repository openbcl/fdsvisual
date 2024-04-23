import bpy
from bpy.types import Operator

class Shader_OT_Fire_n_SmokeAdd(Operator):
    """Creates Shader for a material to visualize fire and smoke"""
    bl_label = "Add Fire and Smoke"
    bl_idname = "shader.fire_n_smoke_operator"
    
    def execute(self, context):
        shader = "Fire_n_Smoke"
        Add_Material(shader)
        return {'FINISHED'}


class Shader_OT_SmokeviewAdd(Operator):
    """Creates Shader for a material that looks like in smokeview"""
    bl_label = "Add Smokeview"
    bl_idname = "shader.smv_operator"
    
    def execute(self, context):
        shader = "Smokeview"
        Add_Material(shader)
        return {'FINISHED'}


class Shader_OT_ConcreteAdd(Operator):
    """Creates Shader for a material that looks like concrete"""
    bl_label = "Add Concrete"
    bl_idname = "shader.concrete_operator"
    
    def execute(self, context):
        shader = "Concrete"
        Add_Material(shader)
        return {'FINISHED'}


class Shader_OT_WoodLightAdd(Operator):
    """Creates Shader for a material that looks like light wood"""
    bl_label = "Add Wood Light"
    bl_idname = "shader.woodlight_operator"
    
    def execute(self, context):
        shader = "Wood_Light"
        Add_Material(shader)
        return {'FINISHED'}


class Shader_OT_WoodDarkAdd(Operator):
    """Creates Shader for a material that looks like dark wood"""
    bl_label = "Add Wood Dark"
    bl_idname = "shader.wooddark_operator"
    
    def execute(self, context):
        shader = "Wood_Dark"
        Add_Material(shader)
        return {'FINISHED'}


class Shader_OT_BricksRedAdd(Operator):
    """Creates Shader for a material that looks like red small bricks"""
    bl_label = "Add Classical Bricks"
    bl_idname = "shader.bricksred_operator"
    
    def execute(self, context):
        shader = "Bricks_Red"
        Add_Material(shader)
        return {'FINISHED'}


class Shader_OT_BricksWhiteAdd(Operator):
    """Creates Shader for a material that looks like white bricks (sand-lime)"""
    bl_label = "Add Sand-Lime-Bricks"
    bl_idname = "shader.brickswhite_operator"
    
    def execute(self, context):
        shader = "Bricks_White"
        Add_Material(shader)
        return {'FINISHED'}


class Shader_OT_SteelAdd(Operator):
    """Creates Shader for a material that looks like steel"""
    bl_label = "Add Steel"
    bl_idname = "shader.steel_operator"
    
    def execute(self, context):
        shader = "Steel"
        Add_Material(shader)
        return {'FINISHED'}


class Shader_OT_GlassAdd(Operator):
    """Creates Shader for a material that looks like glass"""
    bl_label = "Add Glass"
    bl_idname = "shader.glass_operator"
    
    def execute(self, context):
        shader = "Glass"
        Add_Material(shader)
        return {'FINISHED'}


class Shader_OT_MatDelete(Operator):
    """Deletes first Shader of selected object(s)"""
    bl_label = "Remove (unlink)"
    bl_idname = "shader.materialdelete_operator"
    
    def execute(self, context):
        index_to_remove = 0
        Delete_Material(index_to_remove)
        return {'FINISHED'}



"""Helper Functions"""
def Add_Material(shader):
    obj_selection = bpy.context.selected_objects
    material = bpy.data.materials.get(shader)
    for obj in obj_selection:
        obj.data.materials.append(material)
    return {'FINISHED'}

def Delete_Material(index_to_remove):
    obj_selection = bpy.context.selected_objects
    for obj in obj_selection:
        obj.data.materials.pop(index = index_to_remove)
    return {'FINISHED'}



bl_classes = [Shader_OT_Fire_n_SmokeAdd,
              Shader_OT_SmokeviewAdd,
              Shader_OT_ConcreteAdd,
              Shader_OT_WoodLightAdd,
              Shader_OT_WoodDarkAdd,
              Shader_OT_BricksRedAdd,
              Shader_OT_BricksWhiteAdd,
              Shader_OT_SteelAdd,
              Shader_OT_GlassAdd,
              Shader_OT_MatDelete,
              ]


def register():
    from bpy.utils import register_class

    for cls in bl_classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(bl_classes):
        unregister_class(cls)