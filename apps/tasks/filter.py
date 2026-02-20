import django_filters
from django_filters.widgets import RangeWidget

from apps.tasks.models import Task


class TasksFilter(django_filters.FilterSet):
    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Completed", "Completed"),
    )

    status = django_filters.ChoiceFilter(
        choices=STATUS_CHOICES,
        empty_label="All",
        method="filter_status",
    )
    due_date = django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={"type": "date"}),
    )
    completed_date = django_filters.DateFromToRangeFilter(
        widget=RangeWidget(attrs={"type": "date"}),
    )
    show_archived = django_filters.BooleanFilter(
        method="filter_archived",
        label="Show Archived",
    )

    class Meta:
        model = Task
        fields = ["status", "due_date", "completed_date"]

    def filter_status(self, queryset, name, value):
        if value == "Pending":
            return queryset.filter(status=0)
        elif value == "Completed":
            return queryset.filter(status=1)
        return queryset

    def filter_archived(self, queryset, name, value):
        if value:
            return queryset
        return queryset.filter(archived=False)
