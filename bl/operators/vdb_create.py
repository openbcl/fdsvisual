import bpy
from bpy.types import Operator
import pyopenvdb as vdb
import time


class Object_OT_CreateVdbAll(Operator):
    """Export a VDB-Sequence for every single mesh in the FDS-Simulation"""
    bl_label = "Create all"
    bl_idname = "mesh.create_vdb_all"
    
    def execute(self, context):
        print("VDB: Create and export all VDBs")
        ## Get mesh data
        from .. import SimulationData
        meshes = SimulationData.meshes
        meshes_n = SimulationData.meshes_n
        
        ## Write and export VBD
        for n in range(meshes_n):
            mesh = meshes[n]
            Create_VDB(mesh, context)
        
        return {'FINISHED'}


class Object_OT_CreateVdbCustom(Operator):
    """Create VDB-Sequences for custom mesh"""
    bl_label = "Create custom"
    bl_idname = "mesh.create_vdb_custom"
    
    def execute(self, context):
        print("VDB: Create custom VDBs")
        ## Get mesh data
        from .. import SimulationData
        meshes = SimulationData.meshes

        ## Get custom mesh
        setup = context.scene.setup_tool
        n = int(setup.mesh_enum)

        ## Write and export VDB
        mesh = meshes[n]
        Create_VDB(mesh, context)
        
        return {'FINISHED'}



"""Helper Functions"""
def Create_VDB(mesh, context):
    import os

    from .. import SimulationData
    sim = SimulationData.sim
    chid = SimulationData.chid
    nframes_n = SimulationData.nframes_n
    
    ## Get some data from mesh
    id = mesh.id
    coordinates = mesh.coordinates
    dim_x = abs(coordinates['x'][1]-coordinates['x'][0])
    dim_y = abs(coordinates['y'][1]-coordinates['y'][0])
    dim_z = abs(coordinates['z'][1]-coordinates['z'][0])
    #If cells are unequal sized, use smallest dimension (==> for same dimensions in x,y,z)
    #Round flat values. Otherwise rounding errors occur from fds-input for unknown reason 
    dim = float(round(min(dim_x, dim_y, dim_z),3)) 
    
    ## Get data from smoke_3D
    print(f"VDB: Get Smoke3D Data for current mesh: '{id}'")
    smoke3d = sim.smoke_3d
    smoke = smoke3d.get_by_quantity("Soot Density")
    fire = smoke3d.get_by_quantity("HRRPUV")
    temp = smoke3d.get_by_quantity("Temperature")

    def current_time():
        t = time.strftime("%H:%M:%S", time.localtime())
        return t
    
    time_start = time.perf_counter()
    time_smoke = current_time()
    print(f"   ... Read Smoke Data at {time_smoke}")
    data_smoke = smoke[mesh].data

    time_fire = current_time()
    print(f"   ... Read Fire Data at {time_fire}")
    data_fire = fire[mesh].data

    time_temp = current_time()
    print(f"   ... Read Temp Data at {time_temp}")
    data_temp = temp[mesh].data

    time_end = time.perf_counter()
    print(f"   ... Parsing took {(time_end - time_start).__round__(3)}s")
    
    ## Define Path where to export VDS-Sequences
    setup = context.scene.setup_tool
    vdb_path = setup.vdb_path
    sim_path = setup.sim_path
    
    ## Check if folder VDB Sequences exists, if not create
    vdb_folder = f"VDB_Sequence {chid}"
    vdb_sequence = os.path.join(vdb_path, vdb_folder, id)
    print(f"VDB: VDB-Sequence will be exported to path: '{vdb_sequence}'")
    os.makedirs(vdb_sequence, exist_ok=True) #prevents error if path already exists

    for t in range(nframes_n):
        if t % 10 == 0:
            print(f"   ... Write and Export VDB for current timestep: {t+1} / {nframes_n}")
        
        ## Create grids with data
        data = data_smoke[t,:,:,:]
        
        density = vdb.FloatGrid() #empty vdb grid with single-precicion float-values
        density.name = "density" 
        density.copyFromArray(data)
        density.transform = vdb.createLinearTransform(voxelSize=dim)
        
        data = data_fire[t,:,:,:]
        flame = vdb.FloatGrid() #empty vdb grid with single-precicion float-values
        flame.name = "flame" 
        flame.copyFromArray(data)
        flame.transform = vdb.createLinearTransform(voxelSize=dim)
        
        data = data_temp[t,:,:,:]
        temperature = vdb.FloatGrid() #empty vdb grid with single-precicion float-values
        temperature.name = "temperature" 
        temperature.copyFromArray(data)
        temperature.transform = vdb.createLinearTransform(voxelSize=dim)
        
        ## Write VDB files
        vdb_file = f"{chid}-{id}-step={t+1}.vdb"
        
        os.chdir(vdb_sequence)
        vdb.write(vdb_file, grids=[density, flame, temperature])
        os.chdir(sim_path)
    
    time_finish = time.perf_counter()
    print(f"   ... VDB Export took {(time_finish - time_start).__round__(3)}s")


bl_classes = [Object_OT_CreateVdbAll, Object_OT_CreateVdbCustom]


def register():
    from bpy.utils import register_class

    for cls in bl_classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(bl_classes):
        unregister_class(cls)