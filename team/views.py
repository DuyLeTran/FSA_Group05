# team/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Member
from .forms import MemberForm
from import_export.formats.base_formats import XLSX, CSV
from django.http import HttpResponse
from django.contrib import messages
from .admin import MemberResource
from tablib import Dataset 
from django.db.models import Q
def team_list(request):
    query = request.GET.get('q', '')
    members = Member.objects.all()
    
    # Lọc danh sách thành viên dựa vào truy vấn
    if query:
        members = members.filter(Q(name__icontains=query))

    # Sắp xếp danh sách theo tên
    members = members.order_by('name')
    
    return render(request, 'team_list.html', {'members': members, 'query': query})

def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('team:team_list')
    else:
        form = MemberForm()
    return render(request, 'add_member.html', {'form': form})

def member_detail(request, pk):
    member = get_object_or_404(Member, pk=pk)
    return render(request, 'member_detail.html', {'member': member})

def edit_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            return redirect('team:team_list')
    else:
        form = MemberForm(instance=member)
    return render(request, 'edit_member.html', {'form': form})

def delete_member(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == 'POST':
        member.delete()
        return redirect('team:team_list')
    return render(request, 'confirm_delete.html', {'member': member})
def search_members(request):
    query = request.GET.get('query', '')
    if query:
        members = Member.objects.filter(name__icontains=query)  # Thay 'name' bằng trường bạn muốn tìm kiếm
    else:
        members = Member.objects.all()
    return render(request, 'team_list.html', {'members': members, 'query': query})
def export_members(request):
    member_resource = MemberResource()
    dataset = member_resource.export()
    response = HttpResponse(dataset.xlsx, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="members.xlsx"'
    return response

def import_members(request):
    if request.method == 'POST' and request.FILES['myfile']:
        member_resource = MemberResource()
        
        # Đọc file từ request
        uploaded_file = request.FILES['myfile']
        
        # Tạo dataset từ file tải lên
        dataset = Dataset()
        
        # Kiểm tra định dạng file (CSV, XLSX, ...)
        if uploaded_file.name.endswith('xlsx'):
            # Nếu file là XLSX
            dataset.load(uploaded_file.read(), format='xlsx')
        elif uploaded_file.name.endswith('csv'):
            # Nếu file là CSV
            dataset.load(uploaded_file.read().decode('utf-8'), format='csv')
        else:
            messages.error(request, "Unsupported file format. Please upload an XLSX or CSV file.")
            return redirect('team:team_list')

        # Kiểm tra lỗi trước khi thực sự nhập dữ liệu
        result = member_resource.import_data(dataset, dry_run=True)  # Kiểm tra lỗi
        
        if not result.has_errors():  # Nếu không có lỗi
            member_resource.import_data(dataset, dry_run=False)  # Nhập dữ liệu thực tế
            messages.success(request, "Members imported successfully.")
            return redirect('team:team_list')  # Chuyển hướng về danh sách thành viên
        else:
            messages.error(request, "There are errors in the uploaded file.")
            # Bạn có thể thêm logic để hiển thị các lỗi chi tiết nếu cần

    return render(request, 'import_members.html')