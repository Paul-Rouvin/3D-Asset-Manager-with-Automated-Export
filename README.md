# 3D-Asset-Manager-with-Automated-Export

A collection of **pipeline tools for Autodesk Maya** designed to streamline asset management, versioning, and scene setup.

This project provides a **lightweight asset pipeline** for individual artists or small teams, inspired by production workflows used in VFX and game studios.

The goal is to simplify:

- Asset versioning
- Asset browsing with thumbnails
- Fast mesh iteration between software
- Lighting setup referencing
- Automatic export and publishing

---

## Future Direction

This project currently focuses on a **Maya-based asset pipeline**, but it also serves as a foundation for a more **software-agnostic asset manager**.

In the future, I plan to develop a similar asset management system centered around **Blender**, using **OBJ files as a universal geometry format**. The goal is to create a more **portable asset library structure** that can easily move between different DCC applications such as Blender, Maya, Houdini, and real-time engines.

---

# Features

## Asset Browser
A graphical asset browser inside Maya allowing artists to:

- Browse assets by **category**
- View **automatic thumbnails**
- Import assets directly into the scene
- Choose between **normal import or reference**

Assets automatically display the **latest version** available.

---

## Asset Version Exporter
Publish assets directly from Maya with automatic versioning.

Features:

- Choose or create an **asset category**
- Automatically creates **asset folders**
- Detects existing versions and increments automatically
- Exports as **Maya ASCII (.ma)**
- Automatically generates a **thumbnail screenshot**

Example output:

Assets_Maya/
Props/
Sword/
Sword_v001.ma
Sword_v001.png
Sword_v002.ma
Sword_v002.png

---

## Fast Mesh Export
Quickly export the currently selected mesh as **OBJ** for fast iteration with external tools such as:

- ZBrush
- Houdini
- Blender
- Substance

Exports are timestamped to avoid overwriting.

Example:

Sword_20260406_143512.obj

---

## Latest Mesh Import
Automatically imports the **most recently modified mesh file** from a transition folder.

Supported formats:

- `.obj`
- `.fbx`
- `.ma`
- `.mb`

This allows a very fast workflow between Maya and external tools.

---

## Lighting Setup Import
Import a lighting setup as a **reference** while automatically configuring render settings.

Features:

- References a lighting setup scene
- Automatically connects **Arnold atmosphere volumes**
- Copies render settings from the reference scene
- Ensures compatibility with `defaultArnoldRenderOptions`

This allows reusable lighting setups across multiple scenes.

---

# Folder Structure

Assets are stored in a structured library:

Assets_Maya/
Characters/
Knight/
Knight_v001.ma
Knight_v001.png
Knight_v002.ma
Knight_v002.png

Props/
Sword/
Sword_v001.ma
Sword_v001.png

Each asset:

- Lives inside its own folder
- Uses versioned filenames
- Has an associated thumbnail

---

# Scripts Included

| Script | Purpose |
|------|------|
| `MayaAsset_Database.py` | Asset browser with thumbnails |
| `ExportMesh.py` | Quick export of selected mesh to OBJ |
| `ImportMesh.py` | Import the most recent mesh file |
| `export_asset_version.py` | Publish versioned Maya assets with thumbnails |
| `import_lighting_setup.py` | Import lighting setups with Arnold render settings |

---

# Requirements

- Autodesk **Maya**
- Python (Maya embedded Python)
- Arnold renderer (for lighting setup features)

---

# Installation

1. Clone the repository:

git clone https://github.com/yourusername/maya-asset-manager.git

2. Place the scripts somewhere in your Maya scripts directory or pipeline folder.

Example:

Documents/maya/scripts/

3. Update the **asset root directory** in the scripts if needed:

EXPORT_ROOT_DIRECTORY = "D:/Ressources/Maya/Assets_Maya"

---

# Usage

## Asset Browser

Run Inside Maya

import MayaAsset_Database MayaAsset_Database.main()

------------------------------------------------------------------------

Publish Asset Version

Run:

import export_asset_version export_asset_version.export_asset_version()

This will:

-   Ask for an asset category
-   Create folders if necessary
-   Save a new version
-   Generate a thumbnail

------------------------------------------------------------------------

Export Selected Mesh

import ExportMesh ExportMesh.export_selected_mesh_obj()

------------------------------------------------------------------------

Import Latest Mesh

import ImportMesh
ImportMesh.import_last_modified_mesh(“D:/Ressources/Msh_Transition”)

------------------------------------------------------------------------

Import Lighting Setup

import import_lighting_setup
import_lighting_setup.import_lighting_setup_with_render_settings(“path/to/light_setup.mb”)

------------------------------------------------------------------------

Example Workflow

Asset Publishing

Model asset ↓ Run export_asset_version ↓ Asset_v001.ma created
Asset_v001.png created

------------------------------------------------------------------------

Asset Usage

Open Asset Browser ↓ Choose category ↓ Import asset or reference it

------------------------------------------------------------------------

External Tool Iteration

Export selected mesh ↓ Edit in ZBrush / Houdini ↓ Import latest mesh
automatically

------------------------------------------------------------------------

Goals of the Project

This project explores how a simple asset pipeline can be built using
only Python and Maya commands.

It demonstrates core technical art concepts:

-   Versioned asset publishing
-   Asset libraries
-   Thumbnail generation
-   Scene referencing
-   Tool automation

------------------------------------------------------------------------

Possible Future Improvements

-   Search bar for assets
-   Tag system
-   Turntable preview generation
-   Drag and drop import
-   Asset metadata system
-   Integration with USD pipelines

------------------------------------------------------------------------

License

MIT License
