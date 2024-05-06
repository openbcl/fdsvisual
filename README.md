# FDSVisual repository

## About
*FDSVisual* is an open user interface for VR-Visualization of simulations from the [NIST Fire Dynamics Simulator (FDS)](https://pages.nist.gov/fds-smv/). It's main purpose is to read the simulated FDS-data and to facilitate the visualization of fire and smoke with volumetric data (VDB files) - especially when you are going to use Virtual Reality (VR) in the 3D graphic software *Blender*.


## Installation
### Blender installation
To install the addon, simply download the latest stable version of this repository as a zip file (Click on '<> Code' and then on 'Download ZIP').
Then go to Blender -> Edit -> Preferences and click onto the tab 'Add-ons' on the left hand side.
In the top-right corner you'll find the 'Install an add-on'-button. Select the path to the currently downloaded zip file and click on the 'Install Add-on'-button.


### Further required addons
For basic usage, no additional add-ons are required.
However, if an application for VR is planned, then the built-in add-on '3D View: VR Scene Inspection' is needed.
To activate this, follow the same steps as described earlier for accessing the 'Add-ons' menu.
Instead of clicking on 'Install Add-on'-button, type the name in the search bar.
Then simply activate the add-on by checking the box

## Panel Features
### Simulation Setup
**Define FDS Path:** To start the addon, you need to define a simulation path.
It is recommended to specify the path to the simulation folder.
Alternatively, the path to the Smokeview file in this folder can also be determined.

**Define VDB Path:** For the export and import of VDB sequences, another path needs to be provided.
The path must be identical for both export and import.
Within this path, the program searches for a folder named 'VDB_Sequence [CHID]'.
If this folder is not found during the export of the VDB files, the addon will create it along with additional subfolders for each mesh automatically. During import, the program also autonomously searches for this folder structure.

**Load simulation data:** In the next step, the simulation data needs to be loaded.
To do this, click on the 'Setup Simulation' button.
The program will then load all the important parameters of the simulation and configure the Blender scene settings.
To review the simulation parameters, a menu window will open below after the setup with the key parameters.

**[Elective] Select Mesh-ID for custom mesh operations:** If you don't want to work with the entire simulation data later on, but only with data from specific meshes, you can select the respective ID of the mesh from the dropdown list.
This will be queried by the program in subsequent functions.
For custom mesh operations, the respective operation is always performed for only one mesh at a time.
If you want to use it for multiple meshes, you need to perform the operation for each one individually.

### FDS geometry
**Import and delete FDS-Geometry:** In this menu, you can import the FDS geometry from the simulation or delete it from the Blender scene.
Both operators are available for the entire simulation data as well as custom operations.
During the import process, the program automatically creates a corresponding collection (either one for all objects or one for each mesh) and adds the relevant elements to it.

**RGBA Values:** If you have assigned a 'COLOR', 'RGB' or 'TRANSPARENCY' value directly to the obstacles (OBST) before the simulation, the program recognizes this and displays the objects as in your FDS simulation.
If you have assigned a Surf_Id with a corresponding 'COLOR', 'RGB' or 'TRANSPARENCY', the programm displays those objects as in your FDS simulation.

### VDBs
**Write and import VDB-Sequences:** The main function of this addon is the generation of volumetric data for visualizing fire and smoke.
You can both read the simulation data and export it as a VDB sequence, as well as import such sequences.
Similar to the geometry operators, there is the option to work with the simulation data from all meshes or only from each individual mesh.
When importing the VDB sequence, the program automatically creates its own collection, where each sequence for a mesh is located.

### Surface Materials
**Predefined materials:** For a partially higher-quality visualization, the program automatically creates some procedural materials (similar to Surf_IDs from FDS) during the simulation setup.
Currently, these include:
- Fire and Smoke
- Smokeview
- Glass
- Concrete
- Steel
- Wood Light
- Wood Dark
- Classical Bricks
- Sand-Lime Bricks
To assign such a material to an object, simply select the desired objects and then execute the operator.
This assigns the appropriate material to the elements.

If you want to remove an existing material from an object, you can use the 'Remove (unlink)' operator.
This removes the first assigned material for all selected objects.
It only deletes the link between them and does not remove the material itself.

***

The algorithms developed in this addon are based on the workflow outlined in the master's thesis titled [Entwicklung einer Schnittstelle zur Visualisierung von Brandsimulationen im virtuellen Raum](https://katalog.bib.htwk-leipzig.de/permalink/49LEIP_HTWK/1eq81pt/alma991023807002586).
