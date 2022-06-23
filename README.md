# BlenderGDSII
If you want to have presentable 3D images of your microfabrication layout use this!
This is a GUI for opening GDSII files in Blender. 

What can it do?
- convert your layout to STL files
  - these can be deselected and selected for Blender
- open the stl files in Blender
  - add selected materials
  - add selected thickness
  - produce proper eevee-render settings
- save sessions
- load sessions
- delete saved sessions

Works with most GDSII files produced in KLayout,L-Edit or similar software.

This GUI uses the gdsiistl built by Daniel Teal:
https://github.com/dteal/gdsiistl

The beautiful tkinter GUI was customized by Tom Schimansky:
https://github.com/TomSchimansky/CustomTkinter

All the code was integrated by Niels Burghoorn in this package:
https://github.com/SwaggerNiels/BlenderGDSII

## Interface
This is the example layout that can be loaded directly:
![afbeelding](https://user-images.githubusercontent.com/58084010/175263631-d1f0d351-61b3-4c20-9620-e9c35d0a012e.png)

## Pictures
![afbeelding](https://user-images.githubusercontent.com/58084010/174489455-4d0cfcf6-16e2-4670-b9b5-32f207a9b131.png)
