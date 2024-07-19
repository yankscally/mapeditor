#import bpy

# helper function to see properties anywhere in n panel. (without pinning the one in Item>Properties)



# PropertyList panel definition:

# class PropertyList(bpy.types.Panel):
#     bl_label = "Property List"
#     bl_idname = "VIEW3D_PT_property_panel"
#     bl_space_type = 'VIEW_3D'
#     bl_region_type = 'UI'
#     bl_category = 'Map'

#     def draw(self, context):
#         layout = self.layout
#         obj = context.object
        
#         if obj is None:
#             layout.label(text="No object selected")
#             return
        
#         # Inspect properties in the panel
#         property_names = [f'["{prop}"]' for prop in obj.keys()]
#         for name in property_names:
#             row = layout.row()
#             row.prop(obj, name)