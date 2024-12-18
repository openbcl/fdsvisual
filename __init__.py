# SPDX-License-Identifier: GPL-3.0-or-later

# FDSVisual, an open tool for the NIST Fire Dynamics Simulator
# Copyright (C) 2024  Toni Nabrotzky
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


bl_info = { 
    #Equivalent of __init__ for python modules
    # Guideline: https://wiki.blender.org/wiki/Process/Addons/Guidelines/metainfo
    "name" : "FDSVisual main",
    "author" : "Toni Nabrotzky",
    "e-mail" : "t.nabrotzky@bcl-leipzig.de",
    "description" : "Visualization of FDS-Simulation results with VDB-files",
    "version" : (1,0,1),
    "blender" : (4, 1, 0),
    "location" : "View3d > Tool",
    "category" : "Import-Export", #https://docs.blender.org/manual/en/latest/addons/index.html
    "warning" : "", #used for warning icon and text in addons panel
    "support" : "COMMUNITY", #OFFICIAL, COMMUNITY, TESTING
    "github_url" : "",
}

## To view output: In Windows go to "Window -> Toggle System Console"

#Import built-in packages
import logging

#Import local packages
from . import bl


logging.basicConfig(level=logging.INFO) #Info or Debug
log = logging.getLogger(__name__)


# Automatic registering/deregistering of Blender entities
def register():
    log.info("Registering FDSVision...")
    bl.register()


def unregister():
    log.info("Unregistering FDSVision...")
    bl.unregister()