2024 04 23
Panel update: Name changed to FDSVisual

2024 05 06
Feature added: RGBA values for geometry (OBST) are now derived from Surf_Id, if available and no direct color is assigned.

2024 12 18
Material Update: The "Concrete" and "Steel" materials previously used the Musgrave texture, which has been removed in Blender 4.1 and whose functionalities are now integrated into the Noise Texture Node. The materials have been updated accordingly.

Material update: The "Glass" material used BSDF Input = 1 for channel [17], which has been updated to [18].

Feature Update: The installation and import of 'fdsreader' into the Blender-Python environment have been optimized and should now work reliably across all systems. A detailed log is now output in the system console.

Panel Update: If no simulation is set, the mesh list will now be displayed as empty.

Feature Added: A button is now available in the panel to enable and disable the system console, providing detailed traceability of executed steps.


