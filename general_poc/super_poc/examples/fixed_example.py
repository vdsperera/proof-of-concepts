class BaseModelAdmin:
    readonly_fields = ('base_model_id','created')

    def get_readonly_fields(self):
        return list(self.readonly_fields)

class ModelAdmin(BaseModelAdmin):
    
    def get_readonly_fields(self):
        readonly_fields = list(super().get_readonly_fields())
        readonly_fields.append('model_admin_id')
        return readonly_fields

class SubModelAdmin(ModelAdmin):

    def get_readonly_fields(self):
        readonly_fields = list(super().get_readonly_fields())
        readonly_fields.append('sub_model_admin_id')
        print(readonly_fields)
        return readonly_fields

submodel_admin = SubModelAdmin()
submodel_admin.get_readonly_fields()