from .basemodels import DataModelAdmin


class DurationAdmin(DataModelAdmin):
    fields = [
        'is_current',
        'start_year',
        'end_year',
        'start_month',
        'end_month',
        'total_year',
        'total_month',
    ]
    list_display = [
        'is_current',
        'start_year',
        'end_year',
        'start_month',
        'end_month',
        'total_year',
        'total_month',
    ]
    list_filter = [
        'is_current',
        'start_month',
        'end_month',
    ]
    search_fields = [
    ]
    exclude = []
    raw_id_fields = [
    ]
    readonly_fields = [
        'total_year',
        'total_month',
    ]
    allowed_actions = []
    inlines = []

    def __init__(self, *args, **kwargs):
        parent_class = DataModelAdmin
        super(DurationAdmin, self).__init__(*args, **kwargs)

        self.fields = parent_class.fields + self.fields
        self.list_display = parent_class.list_display + self.list_display
        self.list_filter = parent_class.list_filter + self.list_filter
        self.search_fields = parent_class.search_fields + self.search_fields
        self.exclude = parent_class.exclude + self.exclude
        self.raw_id_fields = parent_class.raw_id_fields + self.raw_id_fields
        self.readonly_fields = parent_class.readonly_fields + self.readonly_fields
        self.inlines = parent_class.inlines + self.inlines
