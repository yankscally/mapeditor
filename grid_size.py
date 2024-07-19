import bpy

# a grid panel, to half or double the grid with 2 buttons, and also set the size with a property.

# TODO not unit scale, but:
# bpy.context.space_data.overlay.grid_scale = 1
# resizing unit scale is not a good idea, can apparently effect export scaling?
# so change to grid scale for that 3D view.

# Define custom property for unit_size
bpy.types.Scene.unit_size = bpy.props.FloatProperty(
    name="Unit Size",
    description="Size of the grid units in meters",
    default=1.0,
    min=0.0625,
    max=1024.0,
    step=0.25,
    precision=2,
    update=lambda self, context: update_unit_scale(context, self.unit_size))


class GridPanel(bpy.types.Panel):
    bl_label = "Grid"
    bl_idname = "EDITOR_PT_grid"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Map"

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        layout.prop(scene, "unit_size", text="Unit Size (m)")
  
        # Change grid size..
        row = layout.row()
        row.operator("map_editor.double_unit_size", text="", icon="MESH_GRID")
        row.operator("map_editor.halve_unit_size", text="", icon="SNAP_GRID")
        row = layout.row()




# Update scale_length based on unit_size
def update_unit_scale(context, unit_size):
    if unit_size == 0:
        unit_size = 1
    context.scene.unit_settings.scale_length = 1.0 / unit_size

class GridDoubleOperator(bpy.types.Operator):
    bl_idname = "map_editor.double_unit_size"
    bl_label = "Double Unit Size"

    def execute(self, context):
        unit_size = context.scene.unit_size
        context.scene.unit_size = unit_size * 2
        update_unit_scale(context, unit_size * 2)
        return {'FINISHED'}

class GridHalfOperator(bpy.types.Operator):
    bl_idname = "map_editor.halve_unit_size"
    bl_label = "Halve Unit Size"

    def execute(self, context):
        unit_size = context.scene.unit_size
        context.scene.unit_size = unit_size / 2
        update_unit_scale(context, unit_size / 2)
        return {'FINISHED'}

# setup snapping, absolute off, clipping

def setup_snapping():
    pass
    # TODO set snapping rules:
    # snap to grid absolute OFF, so that a cube is in the center of a square.
    # mainly for drawing "brushes"
    # https://quakewiki.org/wiki/Getting_Started_Mapping#Brush:_Your_basic_building_block.21

def setup_far_clip():
    for a in bpy.context.screen.areas:
        if a.type == 'VIEW_3D':
            for s in a.spaces:
                if s.type == 'VIEW_3D':
                    s.clip_end = 32000 # 32k for now.