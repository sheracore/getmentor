from django.contrib import admin


class BaseAdmin(admin.ModelAdmin):
    fields = []
    list_filter = []
    list_display = []
    search_fields = []
    exclude = []
    raw_id_fields = []
    readonly_fields = []
    inlines = []


class DataModelAdmin(BaseAdmin):
    fields = [
        'pk',
        'is_active',
        'created_at',
        'update_at',
    ]
    list_display = [
        'pk',
        'is_active',
        'created_at',
        'update_at',
    ]
    list_filter = [
        'is_active',
        'created_at',
    ]
    search_fields = [
        'pk',
    ]
    exclude = []
    raw_id_fields = []
    readonly_fields = [
        'pk',
        'created_at',
        'update_at',
    ]
    allowed_actions = []
    inlines = []
    save_as = True

    def __init__(self, *args, **kwargs):
        parent_class = BaseAdmin
        super(DataModelAdmin, self).__init__(*args, **kwargs)

        self.fields = parent_class.fields + self.fields
        self.list_display = parent_class.list_display + self.list_display
        self.list_filter = parent_class.list_filter + self.list_filter
        self.search_fields = parent_class.search_fields + self.search_fields
        self.exclude = parent_class.exclude + self.exclude
        self.raw_id_fields = parent_class.raw_id_fields + self.raw_id_fields
        self.readonly_fields = parent_class.readonly_fields + self.readonly_fields
        self.inlines = parent_class.inlines + self.inlines


class UserDataModelAdmin(DataModelAdmin):
    fields = [
        'user',
    ]
    list_display = [
        'user',
    ]
    list_filter = []
    search_fields = ['user__username', 'user__pk']
    exclude = []
    raw_id_fields = [
        'user',
    ]
    dynamic_raw_id_fields = []
    readonly_fields = []
    inlines = []
    save_as = True

    def __init__(self, *args, **kwargs):
        parent_class = DataModelAdmin
        super(UserDataModelAdmin, self).__init__(*args, **kwargs)

        self.fields = parent_class.fields + self.fields
        self.list_display = parent_class.list_display + self.list_display
        self.list_filter = parent_class.list_filter + self.list_filter
        self.search_fields = parent_class.search_fields + self.search_fields
        self.exclude = parent_class.exclude + self.exclude
        self.raw_id_fields = parent_class.raw_id_fields + self.raw_id_fields
        self.readonly_fields = parent_class.readonly_fields + self.readonly_fields
        self.inlines = parent_class.inlines + self.inlines
