from django.contrib import admin
from .models import (
    Employee,
    DynamicColumn,
    Branch,
    BranchColumn,
    ComplianceTemplate
)

admin.site.register(Employee)
admin.site.register(DynamicColumn)
admin.site.register(Branch)
admin.site.register(BranchColumn)
admin.site.register(ComplianceTemplate)