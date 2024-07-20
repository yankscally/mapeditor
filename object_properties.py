import bpy
# TODO better name

# this is what happens when you select objects, you get the appropriate UI to setup the mesh properties,
# collisions, bodies, etc

class GameEngineProperties(bpy.types.PropertyGroup):
    
    body_types : bpy.props.EnumProperty(
        name="Body Types",
        description="enumerator",
        items=[
            ("1", "None", ""),
            ("2", "Static", ""),
            ("3", "Character", ""),
            ("4", "Rigid", ""),
               ],
        default="1") #type: ignore

    collision_types : bpy.props.EnumProperty(
        name="Collision Shape",
        description="enumerator",
        items=[
            ("1", "None", ""),
            ("2", "Convex", ""),
            ("3", "Concave", ""),
            ("4", "Shape", ""),
               ],
        default="1") #type: ignore

    collision_shapes : bpy.props.EnumProperty(
        name="Collision Shape",
        description="enumerator",
        items=[
            ("1", "Box", ""),
            ("2", "Sphere", ""),
            ("3", "Cylinder", ""),
            ("4", "Plane", ""),
               ],
        default="1"
        ) #type: ignore



# TODO think about props vs characters vs levels system.
#

class ObjectPanel(bpy.types.Panel):
    bl_label = "Object Panel"
    bl_idname = "VIEW3D_PT_object_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Map'

    def draw(self, context):
            layout = self.layout
            props = context.scene.object_properties
            obj = context.object

            if obj == None:
                 layout.label("No object selected.")

            row = layout.row()
            row.prop(props , "body_types")
            
            row = layout.row()
            row.prop(props , "collision_types")
            
            # if the collision is a shape, show the shapes enum
            if props.collision_types == "5":
                row = layout.row()
                row.prop(props , "collision_shapes")
