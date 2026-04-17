from django.db import models


# =========================
# EMPLOYEE
# =========================
class Employee(models.Model):
    dynamic_data = models.JSONField(default=dict)
    month = models.CharField(max_length=20, blank=True, null=True)
    year = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Employee {self.id}"


class DynamicColumn(models.Model):
    name = models.CharField(max_length=255)
    month = models.CharField(max_length=20)
    year = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# =========================
# BRANCH
# =========================
class Branch(models.Model):
    dynamic_data = models.JSONField(default=dict)
    month = models.CharField(max_length=20, blank=True, null=True)
    year = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Branch {self.id}"

class BranchColumn(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# =========================
# COMPLIANCE FORM TEMPLATES
# =========================
class ComplianceTemplate(models.Model):
    form_name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, blank=True, null=True)
    content = models.TextField()

    def __str__(self):
        return self.form_name