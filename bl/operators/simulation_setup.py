import bpy
from bpy.types import Operator

import ctypes
import importlib.util
import site
import os
import subprocess
import sys


class WM_OT_ToggleSystemConsole(Operator):
    """Toggle the system console and update the property"""
    bl_label = "Toggle System Console on/off"
    bl_idname = "wm.toggle_console_property"
    
    def execute(self, context):
        ## Toggle system console
        bpy.ops.wm.console_toggle()

        ## Toggle the property
        setup = context.scene.setup_tool
        setup.console_toggle = not setup.console_toggle
        
        return {'FINISHED'}


class Development_OT_SimulationSetup(Operator):
    """Install python package 'fdsreader' and setup simulation data"""
    bl_label = "Setup Simulation"
    bl_idname = "wm.simulation_setup"
    
    def execute(self, context):
        print("Setup: Start Simulation Setup...")
        print("Setup: System Console toggled. To activate or deactivate go to 'Window' -> 'Toggle System Console'")
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
        surfaces = sim.surfaces
        print("SURFACES:", surfaces)
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
        SimulationData.surfaces = surfaces
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
    try:
        # Try to find the package in the current environment
        print(f"Setup: Attempting to import the module '{package_name}'.")
        import importlib.util
        spec = importlib.util.find_spec(package_name)
        
        if spec is not None:
            print(f"Setup: '{package_name}' is already installed and accessible.")
            return

        print("Setup: Module not found. Checking for potential package paths...")
        site_packages = []

        try:
            if hasattr(site, "getsitepackages"):
                site_packages.extend(site.getsitepackages())
            if hasattr(site, "getusersitepackages"):
                site_packages.append(site.getusersitepackages())
        except Exception as e:
            print(f"Setup: Failed to fetch site-packages paths: {e}")

        package_path = None
        for path in site_packages:
            potential_path = os.path.join(path, package_name)
            if os.path.exists(potential_path):
                package_path = path
                break

        if package_path:
            print(f"Setup: Found '{package_name}' in '{package_path}'. Adding it to sys.path.")
            if package_path not in sys.path:
                sys.path.append(package_path)
            print(f"Setup: Successfully added '{package_path}' to sys.path.")
            
            # Verify module import again
            print(f"Setup: Verifying the module '{package_name}' can now be imported...")
            spec = importlib.util.find_spec(package_name)
            if spec is not None:
                print(f"Setup: '{package_name}' is now accessible.")
                return

        # If module still cannot be imported, proceed to installation
        print(f"Setup: '{package_name}' is not installed. Preparing installation...")
        python_exe = sys.executable

        # Ensure pip is available and updated
        print("Setup: Ensuring pip is available and up to date...")
        import subprocess
        subprocess.run([python_exe, "-m", "ensurepip", "--upgrade"], check=True)
        subprocess.run([python_exe, "-m", "pip", "install", "--upgrade", "pip"], check=True)
        print("Setup: Pip setup and update completed.")

        # Install the requested package
        print(f"Setup: Installing the package '{package_name}'...")
        subprocess.run([python_exe, "-m", "pip", "install", package_name], check=True)
        print(f"Setup: Installation of '{package_name}' completed.")

        # Add the newly installed package path to sys.path
        print("Setup: Searching for the installed package path...")
        for path in site_packages:
            if os.path.exists(os.path.join(path, package_name)):
                package_path = path
                break

        if package_path:
            print(f"Setup: Found installed '{package_name}' in '{package_path}'. Adding to sys.path.")
            if package_path not in sys.path:
                sys.path.append(package_path)
            print(f"Setup: Successfully added '{package_path}' to sys.path.")
        else:
            raise ImportError(f"Setup: Failed to locate '{package_name}' after installation.")

        # Verify the module import again after installation
        print(f"Setup: Verifying the module '{package_name}' can now be imported...")
        spec = importlib.util.find_spec(package_name)
        if spec is None:
            raise ImportError(f"Setup: '{package_name}' is installed but cannot be imported.")

    except Exception as e:
        print(f"Setup: Failed to install '{package_name}': {e}")
        blender_python = sys.executable
        print("\nSetup: If manual installation is required, try running the following commands as administrator:")
        print(f'    "{blender_python}" -m ensurepip --upgrade')
        print(f'    "{blender_python}" -m pip install --upgrade pip')
        print(f'    "{blender_python}" -m pip install {package_name}')


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



bl_classes = [Development_OT_SimulationSetup, WM_OT_ToggleSystemConsole]


def register():
    from bpy.utils import register_class

    for cls in bl_classes:
        register_class(cls)


def unregister():
    from bpy.utils import unregister_class

    for cls in reversed(bl_classes):
        unregister_class(cls)