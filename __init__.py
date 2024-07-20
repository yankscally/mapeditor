bl_info = {
    "name" : "MapEditor", # for now I guess
    "author" : "ys", # sign your name lol!
    "description" : "",
    "blender" : (4, 1, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}
import bpy


import os
import importlib

# PLEASE READ!

# welcome to the beautiful mess that is developing a blender addon with multiple scripts.

# you will need:
# 1) fake bpy: https://github.com/nutti/fake-bpy-module
# 2) possibly the Blender Development addon in vscode extensions.
#


# some rules about this autoload:
# 1) there can only be 1 register/deregister function, and it must be in __init.py__ where bl_info is. do not register in other scripts!
# 2) panels and operators are autoloaded, but you must load property classes manually here, example at bottom.
# 3) if everything is setup correctly, reload the addon with F3>reload script (or TODO try make lazy reload button) 



# this is an old version which only loads panels and operators from _this_ directory.
## TODO update to new autoloader, which can dig through folders.


### thank you VERY MUCH to Valy Arhal for this autoload script and all the extra help! <3

#### AUTOLOADER
folder_blacklist = ["__pycache__"]
file_blacklist = ["__init__.py"]

addon_folders = list([__path__[0]])
addon_folders.extend( [os.path.join(__path__[0], folder_name) for folder_name in os.listdir(__path__[0]) if ( os.path.isdir( os.path.join(__path__[0], folder_name) ) ) and (folder_name not in folder_blacklist) ] )

addon_files = [[folder_path, file_name[0:-3]] for folder_path in addon_folders for file_name in os.listdir(folder_path) if (file_name not in file_blacklist) and (file_name.endswith(".py"))]

for folder_file_batch in addon_files:
    if (os.path.basename(folder_file_batch[0]) == os.path.basename(__path__[0])):
        file = folder_file_batch[1]

        if (file not in locals()):
            import_line = f"from . import {file}"
            exec(import_line)
        else:
            reload_line = f"{file} = importlib.reload({file})"
            exec(reload_line)
    
    else:
        if (os.path.basename(folder_file_batch[0]) != os.path.basename(__path__[0])):
            file = folder_file_batch[1]

            if (file not in locals()):
                import_line = f"from . {os.path.basename(folder_file_batch[0])} import {file}"
                exec(import_line)
            else:
                reload_line = f"{file} = importlib.reload({file})"
                exec(reload_line)


import inspect

class_blacklist = []

bpy_class_object_list = tuple(bpy_class[1] for bpy_class in inspect.getmembers(bpy.types, inspect.isclass) if (bpy_class not in class_blacklist))
_class_object_list = tuple(_class[1] for file_batch in addon_files for _class in inspect.getmembers(eval(file_batch[1]), inspect.isclass) if issubclass(_class[1], bpy_class_object_list) and (not issubclass(_class[1], bpy.types.WorkSpaceTool)))

ClassQueue = _class_object_list


def register_class_queue():
    for Class in ClassQueue:
        try:
            bpy.utils.register_class(Class)
        except:
            try:
                bpy.utils.unregister_class(Class)
                bpy.utils.register_class(Class)
            except:
                pass

def unregister_class_queue():
    for Class in ClassQueue:
        try:
            bpy.utils.unregister_class(Class)
        except:
            print("Can't Unregister", Class)
#### AUTOLOADER



## again, huge thanks Valy Arhal.







## TO LOAD PROPERTYS, you must do it here, manually. properties cannot be autoloaded.


# example:
# from . import panel_template
# (you will need a panel_template.py in the same dir as a module, that includes a MyProps class)


# inside /panel_template.py:

# class MyProps(bpy.types.PropertyGroup):
#     my_string : bpy.props.StringProperty(
#         name="string",
#         description="words and stuff") #type: ignore


# now register the properties!

from . import object_properties
from . import grid_size

def register_properties():
    # example:
    # bpy.types.Scene.my_prop = bpy.props.PointerProperty(type=panel_template.MyProps)
    bpy.types.Scene.object_properties = bpy.props.PointerProperty(type=object_properties.GameEngineProperties)
    bpy.types.Scene.grid_size = bpy.props.PointerProperty(type=grid_size.unit_size)
    pass

def unregister_properties():
    # example:
    # del bpy.types.Scene.my_prop
    del bpy.types.Scene.object_properties
    del bpy.types.Scene.grid_size
# ok! lets go!

def register():
    register_class_queue()
    register_properties()

def unregister():
    unregister_class_queue()
    unregister_properties()