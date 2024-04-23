import bpy
from bpy.types import Operator

import importlib.util
import os
import platform
import subprocess
import sys


class Development_OT_SimulationSetup(Operator):
    """Install python package 'fdsreader' and setup simulation data"""
    bl_label = "Setup Simulation"
    bl_idname = "wm.simulation_setup"
    
    def execute(self, context):
        ## Open System Console
        bpy.ops.wm.console_toggle()

        print("Setup: Get Simulation Data...")
        ## Check if python module 'fdsreader' is installed, if not start installation
        install_python_package('fdsreader')
        import fdsreader as fds
        
        ## Read and Save Data from Simulation
        print("Setup: Read general Simulation Data...")
        setup = context.scene.setup_tool
        sim_path = setup.sim_path

        global sim, chid, timesteps, timesteps_n, sim_time, nframes, nframes_n, obst, obst_n, meshes, meshes_n, meshes_list
        sim = fds.Simulation(sim_path)
        chid = sim.chid
        timesteps = sim.steps['Simulation Time']    #in seconds 
            # key_args: 'Step Size' -> arrays in [s], 'Simulation Time' -> array in [s], 'CPU Time' -> array ins [s], 'Time Step' -> array in dtype=datetime64[ms]
        timesteps_n = len(timesteps)   #in seconds
        sim_time = timesteps[-1]
        nframes = sim.smoke_3d[0].times
        nframes_n = len(nframes)
        obst = sim.obstructions
        obst_n = len(obst)
        meshes = sim.meshes
        meshes_n = len(meshes)
        meshes_list = []
        set_meshes_list()
        
        from .. import SimulationData
        print("Setup: Save general Simulation Data...")
        SimulationData.sim = sim
        SimulationData.chid = chid
        SimulationData.timesteps = timesteps
        SimulationData.timesteps_n = timesteps_n 
        SimulationData.sim_time = sim_time
        """ Output frequency of 3D smoke data are written to .s3d-file every (T_END - T_BEGINN)/NFRAMES seconds. By default NFRAMES = 1000.
            Define 'DT_Smoke3D' to specify uniform time interval or 'RAMP_Smoke3D' to specify exactly which times to write out.
            For more information read user manual for FDS-Version 6.8.0 at page 292.
            Shape of Smoke3D-Array is independant of timesteps."""
        SimulationData.nframes = nframes
        SimulationData.nframes_n = nframes_n
        SimulationData.obst = obst
        SimulationData.obst_n = obst_n
        SimulationData.meshes = meshes
        SimulationData.meshes_n = meshes_n
        SimulationData.meshes_list = meshes_list
        
        ## Information about imported data (control of succesfull import)
        print(f"Setup: Imported Simulation:\n   -SimData: {sim}\n   -CHID: {chid}\n   -Simulation Time: {sim_time} s")
        # print(f"   -Timesteps: {timesteps}\n   -Timesteps_n: {timesteps_n}")
        # print(f"   -NFRAMES: {nframes}\n   -NFRAMES_n: {nframes_n}")
        # print(f"   -Obstructions: {obst}\n   -Obstructions_n: {obst_n}")
        # print(f"   -Meshes: {meshes}\n   -Meshes_n: {meshes_n}")
        
        ## Setup 3D Viewport
        bpy.context.scene.frame_end = nframes_n

        ## Create predefined materials
        material_names = ["Fire_n_Smoke", "Smokeview", "Concrete", "Wood_Light", "Wood_Dark", "Bricks_Red", "Bricks_White", "Steel", "Glass"]

        for material_name in material_names:
            create_material(material_name)
        
        return {'FINISHED'}



"""Helper Functions"""
def install_python_package(package_name):
    if package_name in sys.modules:
        print(f"{package_name!r} already in sys.modules")
    elif (spec := importlib.util.find_spec(package_name)) is not None:
        # If you choose to perform the actual import in BlenderPython
        def isWindows():
            return os.name == 'nt'
        def isMacOS():
            return os.name == 'posix' and platform.system() == "Darwin"

        def isLinux():
            return os.name == 'posix' and platform.system() == "Linux"

        def python_exec():
            
            if isWindows():
                return os.path.join(sys.prefix, 'bin', 'python.exe')
            elif isMacOS():
            
                try:
                    # 2.92 and older
                    path = bpy.app.binary_path_python
                except AttributeError:
                    # 2.93 and later
                    path = sys.executable
                return os.path.abspath(path)
            elif isLinux():
                return os.path.join(sys.prefix, 'sys.prefix/bin', 'python')
            else:
                print("sorry, still not implemented for ", os.name, " - ", platform.system)
        
        def installModule(packageName):
            python_exe = python_exec()

            try:
                subprocess.call([python_exe, "import ", packageName])
            except:
               # upgrade pip
                subprocess.call([python_exe, "-m", "ensurepip"])
                subprocess.call([python_exe, "-m", "pip", "install", "--upgrade", "pip"])
               # install required packages
                subprocess.call([python_exe, "-m", "pip", "install", packageName])
                
        installModule(package_name)
        
        
        print(f"{package_name!r} has been imported")
    else:
        print(f"can't find the {package_name!r} module")

        ## Use pip command to install fdsreader. Restart after installation required.
        #Need to check if previous function is still needed
        import pip
        pip.main(['install', 'fdsreader', '--user'])


def set_meshes_list():
    meshes_list.clear

    for n in range(meshes_n):
        variable = (f"{n}", meshes[n].id, "")
        meshes_list.append(variable)


def create_material(shader_name):
    from .. import Materials
    shaders = bpy.data.materials
    function_name = f"Create_Shader_{shader_name}"

    if shader_name not in shaders:
        print(f"Setup: {shader_name} does not exist in blender file")
        if hasattr(Materials, function_name):
            print(f"   Create predefined shader material: {shader_name}")
            getattr(Materials, function_name)()
        else:
            print(f"   Missing function for predefined shader material: {shader_name}")
    else:
        print(f"Setup: {shader_name} already created")



bl_classes = [Development_OT_SimulationSetup]


def register():
    from bpy.utils import register_class

    for cls in bl_classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(bl_classes):
        unregister_class(cls)