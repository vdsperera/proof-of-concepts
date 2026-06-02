class BaseModelAdmin:
    def get_readonly_fields(self):
        print("BaseModelAdmin called")
        return ["base_model_id", "created"]


class ModelAdmin(BaseModelAdmin):
    def get_readonly_fields(self):
        print("ModelAdmin called")
        fields = super().get_readonly_fields()
        fields.append("model_admin_id")
        return fields


class SubModelAdmin(ModelAdmin):
    def get_readonly_fields(self):
        print("SubModelAdmin called")
        fields = super().get_readonly_fields()
        fields.append("sub_model_admin_id")
        return fields


admin = SubModelAdmin()
result = admin.get_readonly_fields()

print("\nFINAL RESULT:", result)

print("\nMRO ORDER:")
for cls in SubModelAdmin.__mro__:
    print(cls.__name__)