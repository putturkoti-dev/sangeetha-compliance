from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from .models import Employee, DynamicColumn, Branch, BranchColumn, ComplianceTemplate
import pandas as pd
from datetime import datetime
import calendar as cal
import openpyxl


# =========================
# DASHBOARD
# =========================
def dashboard(request):
    return render(request, 'dashboard.html')


def logs(request):
    return render(request, 'logs.html')


# =========================
# EMPLOYEES
# =========================
def employees(request):

    month = request.GET.get('month')
    year = request.GET.get('year')

    if not month:
        month = str(datetime.now().month)

    if not year:
        year = str(datetime.now().year)

    data = Employee.objects.filter(month=month, year=year).order_by('-id')

    columns = DynamicColumn.objects.filter(
        month=month,
        year=year
    ).values_list('name', flat=True)

    if request.method == "POST":

        action = request.POST.get("action")

        # ADD COLUMN
        if action == "add_column":
            col = request.POST.get("new_column")
            if col:
                DynamicColumn.objects.get_or_create(
                    name=col,
                    month=month,
                    year=year
                )
            return redirect(request.get_full_path())

        # DELETE COLUMN
        if action == "delete_column":
            col = request.POST.get("column")
            DynamicColumn.objects.filter(
                name=col,
                month=month,
                year=year
            ).delete()
            return redirect(request.get_full_path())

        # ADD EMPLOYEE
        if action == "add_employee":

            dynamic_data = {
                k: v for k, v in request.POST.items()
                if k not in ['csrfmiddlewaretoken', 'action']
            }

            Employee.objects.create(
                dynamic_data=dynamic_data,
                month=month,
                year=year
            )

            return redirect(request.get_full_path())

        # IMPORT EXCEL
        if action == "import_excel":

            file = request.FILES.get("excel_file")

            if file:
                import pandas as pd

                df = pd.read_excel(file).fillna("")

                # create columns
                for col in df.columns:
                    DynamicColumn.objects.get_or_create(
                        name=str(col),
                        month=month,
                        year=year
                    )

                # rows insert
                for _, row in df.iterrows():

                    clean_data = {}

                    for col in df.columns:
                        val = row[col]

                        # convert everything to string
                        clean_data[str(col)] = str(val).strip()

                    Employee.objects.create(
                        dynamic_data=clean_data,
                        month=month,
                        year=year
                    )

            return redirect(request.get_full_path())

    return render(request, 'employees.html', {
        'data': data,
        'columns': columns,
        'month': month,
        'year': year
    })


def edit_employee(request, id):

    obj = Employee.objects.get(id=id)

    month = obj.month
    year = obj.year

    columns = DynamicColumn.objects.filter(
        month=month,
        year=year
    ).values_list('name', flat=True)

    if request.method == "POST":

        dynamic_data = {}

        for col in columns:
            dynamic_data[col] = request.POST.get(col, "")

        obj.dynamic_data = dynamic_data
        obj.save()

        return redirect('/employees/?month=' + month + '&year=' + year)

    return render(request, 'edit_employee.html', {
        'obj': obj,
        'columns': columns
    })


def delete_employee(request, id):

    obj = Employee.objects.get(id=id)

    month = obj.month
    year = obj.year

    obj.delete()

    return redirect('/employees/?month=' + month + '&year=' + year)


def export_employees(request):

    month = request.GET.get('month')
    year = request.GET.get('year')

    if not month:
        month = str(datetime.now().month)

    if not year:
        year = str(datetime.now().year)

    data = Employee.objects.filter(
        month=month,
        year=year
    ).order_by("id")

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Employees"

    columns = DynamicColumn.objects.filter(
        month=month,
        year=year
    ).values_list("name", flat=True)

    columns = list(columns)

    ws.append(columns)

    for row in data:

        line = []

        for col in columns:
            line.append(row.dynamic_data.get(col, ""))

        ws.append(line)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response['Content-Disposition'] = 'attachment; filename=employees.xlsx'

    wb.save(response)

    return response
# =========================
# BRANCHES
# =========================
# =========================
# BRANCHES
# =========================
def branches(request):

    month = request.GET.get('month')
    year = request.GET.get('year')

    if not month:
        month = str(datetime.now().month)

    if not year:
        year = str(datetime.now().year)

    data = Branch.objects.filter(month=month, year=year).order_by('-id')

    columns = DynamicColumn.objects.filter(
        month=month,
        year=year
    ).values_list('name', flat=True)

    if request.method == "POST":

        action = request.POST.get("action")

        # ADD COLUMN
        if action == "add_column":
            col = request.POST.get("new_column")
            if col:
                DynamicColumn.objects.get_or_create(
                    name=col,
                    month=month,
                    year=year
                )
            return redirect(request.get_full_path())

        # DELETE COLUMN
        if action == "delete_column":
            col = request.POST.get("column")
            DynamicColumn.objects.filter(
                name=col,
                month=month,
                year=year
            ).delete()
            return redirect(request.get_full_path())

        # ADD EMPLOYEE
        if action == "add_branch":

            dynamic_data = {
                k: v for k, v in request.POST.items()
                if k not in ['csrfmiddlewaretoken', 'action']
            }

            Branch.objects.create(
                dynamic_data=dynamic_data,
                month=month,
                year=year
            )

            return redirect(request.get_full_path())

        # IMPORT EXCEL
        if action == "import_excel":

            file = request.FILES.get("excel_file")

            if file:
                import pandas as pd

                df = pd.read_excel(file).fillna("")

                # create columns
                for col in df.columns:
                    DynamicColumn.objects.get_or_create(
                        name=str(col),
                        month=month,
                        year=year
                    )

                # rows insert
                for _, row in df.iterrows():

                    clean_data = {}

                    for col in df.columns:
                        val = row[col]

                        # convert everything to string
                        clean_data[str(col)] = str(val).strip()

                    Branch.objects.create(
                        dynamic_data=clean_data,
                        month=month,
                        year=year
                    )

            return redirect(request.get_full_path())

    return render(request, 'branches.html', {
        'data': data,
        'columns': columns,
        'month': month,
        'year': year
    })

# =========================
# BRANCH EXCEL UPLOAD
# =========================
def upload_branches_excel(request):

    if request.method == "POST":

        file = request.FILES.get("excel_file")

        if file:
            df = pd.read_excel(file)

            for _, row in df.iterrows():
                Branch.objects.create(
                    dynamic_data=row.to_dict()
                )

    return redirect('branches')


# =========================
# BRANCH EXPORT
# =========================
def export_branches(request):

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Branches"

    data = Branch.objects.all().order_by("id")

    if not data.exists():
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response['Content-Disposition'] = 'attachment; filename=branches.xlsx'
        wb.save(response)
        return response

    columns = []

    for row in data:
        for key in row.dynamic_data.keys():
            if key not in columns:
                columns.append(key)

    ws.append(columns)

    for row in data:
        line = []
        for col in columns:
            line.append(row.dynamic_data.get(col, ""))
        ws.append(line)

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    response['Content-Disposition'] = 'attachment; filename=branches.xlsx'

    wb.save(response)
    return response

# =========================
# DELETE BRANCH
# =========================
def delete_branch(request, id):
    Branch.objects.get(id=id).delete()
    return redirect('branches')

def delete_all_branches(request):
    Branch.objects.all().delete()
    return redirect('branches')
def delete_all_employees(request):
    month = request.GET.get('month')
    year = request.GET.get('year')

    Employee.objects.filter(
        month=month,
        year=year
    ).delete()

    return redirect('/employees/?month=' + month + '&year=' + year)
from .models import DynamicColumn
from django.shortcuts import redirect

from django.shortcuts import redirect
def delete_all_columns(request):
    from .models import DynamicColumn, BranchColumn, Branch, Employee

    page = request.GET.get("page")

    if page == "branches":

        BranchColumn.objects.all().delete()

        for b in Branch.objects.all():
            b.dynamic_data = {}
            b.save()

        return redirect("/branches/")

    else:

        DynamicColumn.objects.all().delete()

        for e in Employee.objects.all():
            e.dynamic_data = {}
            e.save()

        return redirect("/employees/")

def edit_branch(request, id):

    obj = Branch.objects.get(id=id)
    columns = BranchColumn.objects.all().values_list('name', flat=True)

    if request.method == "POST":

        dynamic_data = {}

        for col in columns:
            dynamic_data[col] = request.POST.get(col, "")

        obj.dynamic_data = dynamic_data
        obj.save()

        return redirect('branches')

    return render(request, 'edit_branch.html', {
        'obj': obj,
        'columns': columns
    })

# =========================
# CALENDAR
# =========================
def calendar(request):

    month = int(request.GET.get('month', datetime.today().month))
    year = int(request.GET.get('year', datetime.today().year))

    cal_obj = cal.monthcalendar(year, month)

    return render(request, 'calendar.html', {
        'calendar': cal_obj,
        'month': month,
        'year': year,
        'month_name': cal.month_name[month],
    })


# =========================
# OTHER PAGES
# =========================
def notice(request):
    return render(request, 'notice.html')



def compliance(request):

    branches = Branch.objects.all().order_by("id")
    forms = ComplianceTemplate.objects.all()

    result = None

    if request.method == "POST":

        branch_id = request.POST.get("branch")
        form_id = request.POST.get("form")

        branch = Branch.objects.get(id=branch_id)
        form = ComplianceTemplate.objects.get(id=form_id)

        # employee count
        emp_count = Employee.objects.count()

        text = form.content

        text = text.replace("{{branch}}", branch.dynamic_data.get("Branch", ""))
        text = text.replace("{{address}}", branch.dynamic_data.get("Address", ""))
        text = text.replace("{{state}}", branch.dynamic_data.get("State", ""))
        text = text.replace("{{district}}", branch.dynamic_data.get("District", ""))
        text = text.replace("{{employees}}", str(emp_count))

        result = text

    return render(request, "compliance.html", {
        "branches": branches,
        "forms": forms,
        "result": result
    })

def compliance_form(request):

    step = int(request.GET.get("step", 1))

    state = request.GET.get("state", "")
    district = request.GET.get("district", "")
    branch_name = request.GET.get("branch", "")
    form_id = request.GET.get("form", "")

    data = Branch.objects.all()

    # STEP 1
    states = sorted(set(
        x.dynamic_data.get("State", "")
        for x in data if x.dynamic_data.get("State", "")
    ))

    # STEP 2
    districts = sorted(set(
        x.dynamic_data.get("District", "")
        for x in data
        if x.dynamic_data.get("State", "") == state
    ))

    # STEP 3
    branches = sorted(set(
        x.dynamic_data.get("Branch", "")
        for x in data
        if x.dynamic_data.get("State", "") == state
        and x.dynamic_data.get("District", "") == district
    ))

    # STEP 4 (Admin Forms)
    forms = ComplianceTemplate.objects.all()

    result = None

    # STEP 5 Generate
    if step == 5 and form_id:

        branch = Branch.objects.filter(
            dynamic_data__Branch=branch_name
        ).first()

        form = ComplianceTemplate.objects.get(id=form_id)

        emp_count = Employee.objects.count()

        text = form.content

        if branch:
            text = text.replace("{{branch}}", branch.dynamic_data.get("Branch", ""))
            text = text.replace("{{address}}", branch.dynamic_data.get("Address", ""))
            text = text.replace("{{state}}", branch.dynamic_data.get("State", ""))
            text = text.replace("{{district}}", branch.dynamic_data.get("District", ""))

        text = text.replace("{{employees}}", str(emp_count))

        result = text

    return render(request, "compliance_form.html", {
        "step": step,
        "state": state,
        "district": district,
        "branch": branch_name,
        "states": states,
        "districts": districts,
        "branches": branches,
        "forms": forms,
        "result": result
    })

def forms(request):
    return render(request, 'form_generator.html')


def convert(request):
    return render(request, 'docx_to_pdf.html')