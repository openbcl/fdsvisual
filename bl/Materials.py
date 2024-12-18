import bpy


"""Shader for Fire and Smoke"""
def Create_Shader_Fire_n_Smoke():
    material = bpy.data.materials.new(name="Fire_n_Smoke")
    material.use_nodes = True
    
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    ## Referencing existing Nodes
    # For some reason blender sometimes creates Principled Volume instead of Principled BSDF
    # Thus it is necessary to delete the auto-created Principled-Node and create the one wanted until the problem is solved in a better way
    nodes.remove(nodes[0]) #Delete auto created Principled Node
    
    MaterialOutput = nodes.get('Material Output')
    MaterialOutput.location = (1100,200)
    
    ## Create new Nodes
    PrincipledVolume = nodes.new('ShaderNodeVolumePrincipled')
    PrincipledVolume.location = (800,200)
    PrincipledVolume.inputs[0].default_value = (0, 0, 0, 1)
    PrincipledVolume.inputs[9].default_value = (0.6, 0.12, 0, 1)
    
    ColorRampFire = nodes.new('ShaderNodeValToRGB')
    ColorRampFire.location = (0,0)
    ColorRampFire.color_ramp.elements.new(100)
    ColorRampFire.color_ramp.elements[0].position = 0
    ColorRampFire.color_ramp.elements[1].position = 0.5
    ColorRampFire.color_ramp.elements[2].position = 1
    ColorRampFire.color_ramp.elements[0].color = (1, 1, 1, 1)
    ColorRampFire.color_ramp.elements[1].color = (0.6, 0.12, 0, 1)
    ColorRampFire.color_ramp.elements[2].color = (0.5, 0.02, 0, 1)
    
    ColorRampSmoke = nodes.new('ShaderNodeValToRGB')
    ColorRampSmoke.location = (400,0)
    
    VolumeInfo = nodes.new('ShaderNodeVolumeInfo')
    VolumeInfo.location = (100,250)
    
    Divide = nodes.new('ShaderNodeMath')
    Divide.location = (400,300)
    Divide.operation = 'DIVIDE'
    Divide.inputs[1].default_value = 1
    
    ##Connect Nodes
    links.new(ColorRampFire.outputs[0], PrincipledVolume.inputs[7])
    
    links.new(VolumeInfo.outputs[1], PrincipledVolume.inputs[2])
    links.new(VolumeInfo.outputs[2], Divide.inputs[0])
    links.new(VolumeInfo.outputs[2], ColorRampSmoke.inputs[0])
    
    links.new(Divide.outputs[0], PrincipledVolume.inputs[6])
    links.new(ColorRampSmoke.outputs[0], PrincipledVolume.inputs[8])
    
    links.new(PrincipledVolume.outputs[0], MaterialOutput.inputs[1])



"""Shader for Materials"""
def Create_Shader_Smokeview():
    material = bpy.data.materials.new(name="Smokeview")
    material.use_nodes = True
    
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    ## Referencing existing Nodes
    # For some reason blender sometimes creates Principled Volume instead of Principled BSDF
    # Thus it is necessary to delete auto-created Principled-Node and create the one wanted until the problem is solved in a better way
    nodes.remove(nodes[0])
    
    MaterialOutput = nodes.get('Material Output')
    MaterialOutput.location = (550,0)
    
    ## Create new Nodes
    PrincipledBSDF = nodes.new('ShaderNodeBsdfPrincipled')
    PrincipledBSDF.location = (250,00)

    RGB = nodes.new('ShaderNodeRGB')
    RGB.location = (0,0)
    RGB.outputs[0].default_value = (1, 0.8, 0.4, 1)
    
    ##Connect Nodes
    links.new(RGB.outputs[0], PrincipledBSDF.inputs[0])
    links.new(PrincipledBSDF.outputs[0], MaterialOutput.inputs[0])



def Create_Shader_Concrete():
    material = bpy.data.materials.new(name="Concrete")
    material.use_nodes = True
    
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    ## Referencing existing Nodes
    # For some reason blender sometimes creates Principled Volume instead of Principled BSDF
    # Thus it is necessary to delete auto-created Principled-Node and create the one wanted until the problem is solved in a better way
    nodes.remove(nodes[0])
    
    MaterialOutput = nodes.get('Material Output')
    MaterialOutput.location = (1700,300)
    
    ## Create new Nodes
    PrincipledBSDF = nodes.new('ShaderNodeBsdfPrincipled')
    PrincipledBSDF.location = (1400,300)
    
    TexCoord = nodes.new('ShaderNodeTexCoord')
    TexCoord.location = (0,0)
    
    NoiseTex1 = nodes.new('ShaderNodeTexNoise')
    NoiseTex1.location = (250,600)
    NoiseTex1.inputs[2].default_value = 2
    
    VoronoiTex = nodes.new('ShaderNodeTexVoronoi')
    VoronoiTex.location = (250,300)
    VoronoiTex.inputs[2].default_value = 2
    
    NoiseTex2 = nodes.new('ShaderNodeTexNoise')
    NoiseTex2.location = (250,-100)
    NoiseTex2.normalize = False
    NoiseTex2.inputs[2].default_value = 2
    NoiseTex2.inputs[3].default_value = 8
    NoiseTex2.inputs[4].default_value = 1
    
    Mix1 = nodes.new('ShaderNodeMix')
    Mix1.location = (500,0)
    Mix1.data_type= 'RGBA'
    Mix1.inputs[7].default_value = (0.25, 0.25, 0.25, 1)
    
    Mix2 = nodes.new('ShaderNodeMix')
    Mix2.location = (750,300)
    Mix2.data_type= 'RGBA'
    Mix2.blend_type = 'LIGHTEN'
    
    ColorRamp = nodes.new('ShaderNodeValToRGB')
    ColorRamp.location = (1000,300)
    ColorRamp.color_ramp.elements[0].color = (0.1, 0.1, 0.12, 1)
    ColorRamp.color_ramp.elements[1].color = (0.2, 0.2, 0.22, 1)
    
    ##Connect Nodes
    links.new(TexCoord.outputs[3], NoiseTex2.inputs[0])
    links.new(TexCoord.outputs[3], VoronoiTex.inputs[0])
    links.new(TexCoord.outputs[3], NoiseTex1.inputs[0])
    
    links.new(VoronoiTex.outputs[0], Mix1.inputs[0])
    links.new(NoiseTex2.outputs[0], Mix1.inputs[6])
    
    links.new(Mix1.outputs[2], Mix2.inputs[6])
    links.new(NoiseTex1.outputs[0], Mix2.inputs[7])
    
    links.new(Mix2.outputs[2], ColorRamp.inputs[0])
    
    links.new(ColorRamp.outputs[0], PrincipledBSDF.inputs[0])
    
    links.new(PrincipledBSDF.outputs[0], MaterialOutput.inputs[0])



def Create_Shader_Wood_Light():
    material = bpy.data.materials.new(name="Wood_Light")
    material.use_nodes = True
    
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    ## Referencing existing Nodes
    # For some reason blender sometimes creates Principled Volume instead of Principled BSDF
    # Thus it is necessary to delete auto-created Principled-Node and create the one wanted until the problem is solved in a better way
    nodes.remove(nodes[0])
    
    MaterialOutput = nodes.get('Material Output')
    MaterialOutput.location = (2100,0)
    
    ## Create new Nodes
    PrincipledBSDF = nodes.new('ShaderNodeBsdfPrincipled')
    PrincipledBSDF.location = (1800,0)
        
    TexCoord = nodes.new('ShaderNodeTexCoord')
    TexCoord.location = (0,0)
    
    Mapping1 = nodes.new('ShaderNodeMapping')
    Mapping1.location = (200,0)
    
    Mapping2 = nodes.new('ShaderNodeMapping')
    Mapping2.location = (500,300)
    Mapping2.inputs[3].default_value[1] = -0.03
    Mapping2.inputs[3].default_value[2] = 0.25
    
    NoiseTex = nodes.new('ShaderNodeTexNoise')
    NoiseTex.location = (700,300)
    NoiseTex.inputs[2].default_value = 4
    NoiseTex.inputs[4].default_value = 0.8
    
    ColorRamp = nodes.new('ShaderNodeValToRGB')
    ColorRamp.location = (900,300)
    ColorRamp.color_ramp.elements[0].position = 0
    ColorRamp.color_ramp.elements[1].position = 0.1
    ColorRamp.color_ramp.elements.new(0.2)
    ColorRamp.color_ramp.elements.new(0.3)
    ColorRamp.color_ramp.elements.new(0.4)
    ColorRamp.color_ramp.elements.new(0.5)
    ColorRamp.color_ramp.elements.new(0.6)
    ColorRamp.color_ramp.elements.new(0.7)
    ColorRamp.color_ramp.elements.new(0.8)
    ColorRamp.color_ramp.elements.new(0.9)
    ColorRamp.color_ramp.elements.new(1)
    ColorRamp.color_ramp.elements[0].color = (0, 0, 0, 1)
    ColorRamp.color_ramp.elements[1].color = (1, 1, 1, 1)
    ColorRamp.color_ramp.elements[2].color = (0, 0, 0, 1)
    ColorRamp.color_ramp.elements[3].color = (1, 1, 1, 1)
    ColorRamp.color_ramp.elements[4].color = (0, 0, 0, 1)
    ColorRamp.color_ramp.elements[5].color = (1, 1, 1, 1)
    ColorRamp.color_ramp.elements[6].color = (0, 0, 0, 1)
    ColorRamp.color_ramp.elements[7].color = (1, 1, 1, 1)
    ColorRamp.color_ramp.elements[8].color = (0, 0, 0, 1)
    ColorRamp.color_ramp.elements[9].color = (1, 1, 1, 1)
    ColorRamp.color_ramp.elements[10].color = (0, 0, 0, 1)
    
    Mix1 = nodes.new('ShaderNodeMix')
    Mix1.location = (1200,300)
    Mix1.data_type= 'RGBA'
    Mix1.inputs[6].default_value = (0.6, 0.45, 0.3, 1)
    Mix1.inputs[7].default_value = (0.35, 0.15, 0.1, 1)
    
    
    Mapping3 = nodes.new('ShaderNodeMapping')
    Mapping3.location = (500,-100)
    Mapping3.inputs[3].default_value[1] = -0.15
    Mapping3.inputs[3].default_value[2] = -0.05
    
    WaveTex1 = nodes.new('ShaderNodeTexWave')
    WaveTex1.location = (500,-500)
    WaveTex1.bands_direction = 'Y'
    WaveTex1.inputs[1].default_value = 0.05
    WaveTex1.inputs[2].default_value = 3
    WaveTex1.inputs[3].default_value = 3
    WaveTex1.inputs[5].default_value = 0.75
    
    Mix2 = nodes.new('ShaderNodeMix')
    Mix2.location = (800,-300)
    Mix2.data_type= 'RGBA'
    Mix2.blend_type = 'LINEAR_LIGHT'
    Mix2.inputs[0].default_value = 0
    
    WaveTex2 = nodes.new('ShaderNodeTexWave')
    WaveTex2.location = (1000,-300)
    WaveTex2.wave_profile = 'SAW'
    WaveTex2.inputs[1].default_value = 3
    WaveTex2.inputs[2].default_value = 12
    WaveTex2.inputs[3].default_value = 9
    WaveTex2.inputs[4].default_value = 2
    WaveTex2.inputs[5].default_value = 0.9
    
    Mix3 = nodes.new('ShaderNodeMix')
    Mix3.location = (1500,0)
    Mix3.data_type= 'RGBA'
    Mix3.inputs[6].default_value = (0.15, 0.075, 0.025, 1)
    
    ##Connect Nodes
    links.new(TexCoord.outputs[3], Mapping1.inputs[0])
    
    links.new(Mapping1.outputs[0], Mapping2.inputs[0])
    links.new(Mapping1.outputs[0], Mapping3.inputs[0])
    links.new(Mapping1.outputs[0], WaveTex1.inputs[0])
    
    links.new(Mapping2.outputs[0], NoiseTex.inputs[0])
    
    links.new(NoiseTex.outputs[0], ColorRamp.inputs[0])

    links.new(ColorRamp.outputs[0], Mix1.inputs[0])
    
    links.new(Mapping3.outputs[0], Mix2.inputs[6])
    links.new(WaveTex1.outputs[0], Mix2.inputs[7])
    
    links.new(Mix2.outputs[2], WaveTex2.inputs[0])
    
    links.new(Mix1.outputs[2], Mix3.inputs[7])
    links.new(WaveTex2.outputs[0], Mix3.inputs[0])
    
    links.new(Mix3.outputs[2], PrincipledBSDF.inputs[0])
    
    links.new(PrincipledBSDF.outputs[0], MaterialOutput.inputs[0])



def Create_Shader_Wood_Dark():
    material = bpy.data.materials.new(name="Wood_Dark")
    material.use_nodes = True
    
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    ## Referencing existing Nodes
    # For some reason blender sometimes creates Principled Volume instead of Principled BSDF
    # Thus it is necessary to delete auto-created Principled-Node and create the one wanted until the problem is solved in a better way
    nodes.remove(nodes[0])
    
    MaterialOutput = nodes.get('Material Output')
    MaterialOutput.location = (2100,0)
    
    ## Create new Nodes
    PrincipledBSDF = nodes.new('ShaderNodeBsdfPrincipled')
    PrincipledBSDF.location = (1800,0)
        
    TexCoord = nodes.new('ShaderNodeTexCoord')
    TexCoord.location = (0,0)
    
    Mapping1 = nodes.new('ShaderNodeMapping')
    Mapping1.location = (200,0)
    
    Mapping2 = nodes.new('ShaderNodeMapping')
    Mapping2.location = (500,300)
    Mapping2.inputs[3].default_value[1] = -0.03
    Mapping2.inputs[3].default_value[2] = 0.25
    
    NoiseTex = nodes.new('ShaderNodeTexNoise')
    NoiseTex.location = (700,300)
    NoiseTex.inputs[2].default_value = 4
    NoiseTex.inputs[4].default_value = 0.8
    
    ColorRamp = nodes.new('ShaderNodeValToRGB')
    ColorRamp.location = (900,300)
    ColorRamp.color_ramp.elements[0].position = 0
    ColorRamp.color_ramp.elements[1].position = 0.1
    ColorRamp.color_ramp.elements.new(0.2)
    ColorRamp.color_ramp.elements.new(0.3)
    ColorRamp.color_ramp.elements.new(0.4)
    ColorRamp.color_ramp.elements.new(0.5)
    ColorRamp.color_ramp.elements.new(0.6)
    ColorRamp.color_ramp.elements.new(0.7)
    ColorRamp.color_ramp.elements.new(0.8)
    ColorRamp.color_ramp.elements.new(0.9)
    ColorRamp.color_ramp.elements.new(1)
    ColorRamp.color_ramp.elements[0].color = (0, 0, 0, 1)
    ColorRamp.color_ramp.elements[1].color = (1, 1, 1, 1)
    ColorRamp.color_ramp.elements[2].color = (0, 0, 0, 1)
    ColorRamp.color_ramp.elements[3].color = (1, 1, 1, 1)
    ColorRamp.color_ramp.elements[4].color = (0, 0, 0, 1)
    ColorRamp.color_ramp.elements[5].color = (1, 1, 1, 1)
    ColorRamp.color_ramp.elements[6].color = (0, 0, 0, 1)
    ColorRamp.color_ramp.elements[7].color = (1, 1, 1, 1)
    ColorRamp.color_ramp.elements[8].color = (0, 0, 0, 1)
    ColorRamp.color_ramp.elements[9].color = (1, 1, 1, 1)
    ColorRamp.color_ramp.elements[10].color = (0, 0, 0, 1)
    
    Mix1 = nodes.new('ShaderNodeMix')
    Mix1.location = (1200,300)
    Mix1.data_type= 'RGBA'
    Mix1.inputs[6].default_value = (0.2, 0.15, 0.1, 1)
    Mix1.inputs[7].default_value = (0.025, 0.01, 0.01, 1)
    
    
    Mapping3 = nodes.new('ShaderNodeMapping')
    Mapping3.location = (500,-100)
    Mapping3.inputs[3].default_value[1] = -0.15
    Mapping3.inputs[3].default_value[2] = -0.05
    
    WaveTex1 = nodes.new('ShaderNodeTexWave')
    WaveTex1.location = (500,-500)
    WaveTex1.bands_direction = 'Y'
    WaveTex1.inputs[1].default_value = 0.05
    WaveTex1.inputs[2].default_value = 3
    WaveTex1.inputs[3].default_value = 3
    WaveTex1.inputs[5].default_value = 0.75
    
    Mix2 = nodes.new('ShaderNodeMix')
    Mix2.location = (800,-300)
    Mix2.data_type= 'RGBA'
    Mix2.blend_type = 'LINEAR_LIGHT'
    Mix2.inputs[0].default_value = 0
    
    WaveTex2 = nodes.new('ShaderNodeTexWave')
    WaveTex2.location = (1000,-300)
    WaveTex2.wave_profile = 'SAW'
    WaveTex2.inputs[1].default_value = 3
    WaveTex2.inputs[2].default_value = 12
    WaveTex2.inputs[3].default_value = 9
    WaveTex2.inputs[4].default_value = 2
    WaveTex2.inputs[5].default_value = 0.9
    
    Mix3 = nodes.new('ShaderNodeMix')
    Mix3.location = (1500,0)
    Mix3.data_type= 'RGBA'
    Mix3.inputs[6].default_value = (0.06, 0.03, 0.01, 1)
    
    ##Connect Nodes
    links.new(TexCoord.outputs[3], Mapping1.inputs[0])
    
    links.new(Mapping1.outputs[0], Mapping2.inputs[0])
    links.new(Mapping1.outputs[0], Mapping3.inputs[0])
    links.new(Mapping1.outputs[0], WaveTex1.inputs[0])
    
    links.new(Mapping2.outputs[0], NoiseTex.inputs[0])
    
    links.new(NoiseTex.outputs[0], ColorRamp.inputs[0])

    links.new(ColorRamp.outputs[0], Mix1.inputs[0])
    
    links.new(Mapping3.outputs[0], Mix2.inputs[6])
    links.new(WaveTex1.outputs[0], Mix2.inputs[7])
    
    links.new(Mix2.outputs[2], WaveTex2.inputs[0])
    
    links.new(Mix1.outputs[2], Mix3.inputs[7])
    links.new(WaveTex2.outputs[0], Mix3.inputs[0])
    
    links.new(Mix3.outputs[2], PrincipledBSDF.inputs[0])
    
    links.new(PrincipledBSDF.outputs[0], MaterialOutput.inputs[0])



def Create_Shader_Bricks_Red():
    material = bpy.data.materials.new(name="Bricks_Red")
    material.use_nodes = True
    
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    ## Referencing existing Nodes
    # For some reason blender sometimes creates Principled Volume instead of Principled BSDF
    # Thus it is necessary to delete auto-created Principled-Node and create the one wanted until the problem is solved in a better way
    nodes.remove(nodes[0])
    
    MaterialOutput = nodes.get('Material Output')
    MaterialOutput.location = (1500,0)
    
    ## Create new Nodes
    PrincipledBSDF = nodes.new('ShaderNodeBsdfPrincipled')
    PrincipledBSDF.location = (1200,0)
    PrincipledBSDF.inputs[2].default_value = 1
    
    TexCoord = nodes.new('ShaderNodeTexCoord')
    TexCoord.location = (0,0)
    
    Mapping = nodes.new('ShaderNodeMapping')
    Mapping.location = (200,0)
    
    NoiseTex = nodes.new('ShaderNodeTexNoise')
    NoiseTex.location = (400,100)
    NoiseTex.inputs[2].default_value = 100
    
    Mix = nodes.new('ShaderNodeMix')
    Mix.location = (600,0)
    Mix.data_type= 'RGBA'
    Mix.inputs[0].default_value = 0.003
    
    BrickTex = nodes.new('ShaderNodeTexBrick')
    BrickTex.location = (800,0)
    BrickTex.inputs[1].default_value = (0.5, 0.2, 0.1, 1)
    BrickTex.inputs[2].default_value = (0.45, 0.1, 0.05, 1)
    BrickTex.inputs[3].default_value = (0.1, 0.1, 0.1, 1)
    BrickTex.inputs[4].default_value = 5
    BrickTex.inputs[5].default_value = 0.02
    BrickTex.inputs[6].default_value = 0.6
    
    Bump = nodes.new('ShaderNodeBump')
    Bump.location = (1000,0)
    Bump.inputs[0].default_value = 0.3
    
    ##Connect Nodes
    links.new(TexCoord.outputs[2], Mapping.inputs[0])
    
    links.new(Mapping.outputs[0], NoiseTex.inputs[0])
    links.new(Mapping.outputs[0], Mix.inputs[6])
    
    links.new(NoiseTex.outputs[0], Mix.inputs[7])
    
    links.new(Mix.outputs[2], BrickTex.inputs[0])
        
    links.new(BrickTex.outputs[0], PrincipledBSDF.inputs[0])
    links.new(BrickTex.outputs[0], Bump.inputs[2])
    
    links.new(Bump.outputs[0], PrincipledBSDF.inputs[5])
    
    links.new(PrincipledBSDF.outputs[0], MaterialOutput.inputs[0])



def Create_Shader_Bricks_White():
    material = bpy.data.materials.new(name="Bricks_White")
    material.use_nodes = True
    
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    ## Referencing existing Nodes
    # For some reason blender sometimes creates Principled Volume instead of Principled BSDF
    # Thus it is necessary to delete auto-created Principled-Node and create the one wanted until the problem is solved in a better way
    nodes.remove(nodes[0])
    
    MaterialOutput = nodes.get('Material Output')
    MaterialOutput.location = (1500,0)
    
    ## Create new Nodes
    PrincipledBSDF = nodes.new('ShaderNodeBsdfPrincipled')
    PrincipledBSDF.location = (1200,0)
    PrincipledBSDF.inputs[2].default_value = 1
    
    TexCoord = nodes.new('ShaderNodeTexCoord')
    TexCoord.location = (0,0)
    
    Mapping = nodes.new('ShaderNodeMapping')
    Mapping.location = (200,0)
    
    NoiseTex = nodes.new('ShaderNodeTexNoise')
    NoiseTex.location = (400,100)
    NoiseTex.inputs[2].default_value = 100
    
    Mix = nodes.new('ShaderNodeMix')
    Mix.location = (600,0)
    Mix.data_type= 'RGBA'
    Mix.inputs[0].default_value = 0.003
    
    BrickTex = nodes.new('ShaderNodeTexBrick')
    BrickTex.location = (800,0)
    BrickTex.inputs[1].default_value = (0.8, 0.8, 0.8, 1)
    BrickTex.inputs[2].default_value = (0.6, 0.6, 0.6, 1)
    BrickTex.inputs[3].default_value = (0.2, 0.2, 0.2, 1)
    BrickTex.inputs[4].default_value = 2
    BrickTex.inputs[5].default_value = 0.01
    BrickTex.inputs[6].default_value = 0.6
    
    Bump = nodes.new('ShaderNodeBump')
    Bump.location = (1000,0)
    Bump.inputs[0].default_value = 0.3
    
    ##Connect Nodes
    links.new(TexCoord.outputs[2], Mapping.inputs[0])
    
    links.new(Mapping.outputs[0], NoiseTex.inputs[0])
    links.new(Mapping.outputs[0], Mix.inputs[6])
    
    links.new(NoiseTex.outputs[0], Mix.inputs[7])
    
    links.new(Mix.outputs[2], BrickTex.inputs[0])
        
    links.new(BrickTex.outputs[0], PrincipledBSDF.inputs[0])
    links.new(BrickTex.outputs[0], Bump.inputs[2])
    
    links.new(Bump.outputs[0], PrincipledBSDF.inputs[5])
    
    links.new(PrincipledBSDF.outputs[0], MaterialOutput.inputs[0])



def Create_Shader_Steel():
    material = bpy.data.materials.new(name="Steel")
    material.use_nodes = True
    
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    ## Referencing existing Nodes
    # For some reason blender sometimes creates Principled Volume instead of Principled BSDF
    # Thus it is necessary to delete auto-created Principled-Node and create the one wanted until the problem is solved in a better way
    nodes.remove(nodes[0])
    
    MaterialOutput = nodes.get('Material Output')
    MaterialOutput.location = (1200,100)
    
    ## Create new Nodes
    PrincipledBSDF = nodes.new('ShaderNodeBsdfPrincipled')
    PrincipledBSDF.location = (900,100)
    PrincipledBSDF.inputs[1].default_value = 1    
    
    TexCoord = nodes.new('ShaderNodeTexCoord')
    TexCoord.location = (0,0)
    
    NoiseTex1 = nodes.new('ShaderNodeTexNoise')
    NoiseTex1.location = (250,0)
    NoiseTex1.inputs[2].default_value = 3
    NoiseTex1.inputs[3].default_value = 8
    NoiseTex1.inputs[4].default_value = 1
    NoiseTex1.inputs[5].default_value = 3
    NoiseTex1.noise_type = 'MULTIFRACTAL'
    
    NoiseTex2 = nodes.new('ShaderNodeTexNoise')
    NoiseTex2.location = (250,-300)
    NoiseTex2.inputs[2].default_value = 9
    NoiseTex2.inputs[3].default_value = 9
    NoiseTex2.inputs[4].default_value = 0.8
    
    Mix = nodes.new('ShaderNodeMix')
    Mix.location = (500,-300)
    Mix.data_type= 'RGBA'
    Mix.inputs[0].default_value = (1)
    
    ColorRamp = nodes.new('ShaderNodeValToRGB')
    ColorRamp.location = (500,0)
    ColorRamp.color_ramp.elements[0].color = (0.4, 0.35, 0.35, 1)
    ColorRamp.color_ramp.elements[1].color = (0.5, 0.5, 0.5, 1)

    ##Connect Nodes
    links.new(TexCoord.outputs[3], NoiseTex1.inputs[0])
    links.new(TexCoord.outputs[3], NoiseTex2.inputs[0])
    
    links.new(NoiseTex1.outputs[0], ColorRamp.inputs[0])
    
    links.new(NoiseTex1.outputs[0], Mix.inputs[6])
    links.new(NoiseTex2.outputs[0], Mix.inputs[7])
    
    links.new(ColorRamp.outputs[0], PrincipledBSDF.inputs[0])
    links.new(Mix.outputs[2], PrincipledBSDF.inputs[2])
    
    links.new(PrincipledBSDF.outputs[0], MaterialOutput.inputs[0])



def Create_Shader_Glass():
    material = bpy.data.materials.new(name="Glass")
    material.use_nodes = True
    
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    ## Editing some material and scene setting
    material = bpy.data.materials[material.name]
    # material.use_screen_refraction = True
    # material.blend_method = 'HASHED'
    # material.shadow_method = 'HASHED'
        
    # bpy.data.scenes["Scene"].eevee.use_ssr = True
    # bpy.data.scenes["Scene"].eevee.use_ssr_refraction = True
    # bpy.data.scenes["Scene"].eevee.taa_render_samples = 132
    # bpy.data.scenes["Scene"].eevee.taa_samples = 64
    # bpy.data.scenes["Scene"].eevee.use_gtao = True
    # bpy.data.scenes["Scene"].eevee.gtao_distance = 5
    
    ## Referencing existing Nodes
    # For some reason blender sometimes creates Principled Volume instead of Principled BSDF
    # Thus it is necessary to delete auto-created Principled-Node and create the one wanted until the problem is solved in a better way
    nodes.remove(nodes[0])
    
    MaterialOutput = nodes.get('Material Output')
    MaterialOutput.location = (900,100)
    
    ## Create new Nodes
    PrincipledBSDF = nodes.new('ShaderNodeBsdfPrincipled')
    PrincipledBSDF.location = (0,0)
    PrincipledBSDF.inputs[2].default_value = 0
    PrincipledBSDF.inputs[18].default_value = 1
    
    TransparentBSDF = nodes.new('ShaderNodeBsdfTransparent')
    TransparentBSDF.location = (0,100)
    
    Fresnel = nodes.new('ShaderNodeFresnel')
    Fresnel.location = (0,200)
    
    ColorRamp = nodes.new('ShaderNodeValToRGB')
    ColorRamp.location = (300,300)
    ColorRamp.color_ramp.elements[0].color = (0.6, 0.6, 0.6, 1)
    
    MixShader = nodes.new('ShaderNodeMixShader')
    MixShader.location = (600,100)
    
    ##Connect Nodes
    links.new(Fresnel.outputs[0], ColorRamp.inputs[0])
    
    links.new(ColorRamp.outputs[0], MixShader.inputs[0])
    links.new(PrincipledBSDF.outputs[0], MixShader.inputs[1])
    links.new(TransparentBSDF.outputs[0], MixShader.inputs[2])
    
    links.new(MixShader.outputs[0], MaterialOutput.inputs[0])



"""Shader for Geometry import"""
def Create_Shader_GeomImport(name, rgba):
    material = bpy.data.materials.new(name = name)
    material.use_nodes = True
    
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    
    ## Referencing existing Nodes
    # For some reason blender sometimes creates Principled Volume instead of Principled BSDF
    # Thus it is necessary to delete auto-created Principled-Node and create the one wanted until the problem is solved in a better way
    nodes.remove(nodes[0])
    
    MaterialOutput = nodes.get('Material Output')
    MaterialOutput.location = (550,0)
    
    ## Create new Nodes
    PrincipledBSDF = nodes.new('ShaderNodeBsdfPrincipled')
    PrincipledBSDF.location = (250,00)

    RGB = nodes.new('ShaderNodeRGB')
    RGB.location = (0,0)
    RGB.outputs[0].default_value = rgba
    
    ##Connect Nodes
    links.new(RGB.outputs[0], PrincipledBSDF.inputs[0])
    links.new(PrincipledBSDF.outputs[0], MaterialOutput.inputs[0])
