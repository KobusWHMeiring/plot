from django.contrib import admin
from .models import PilotInquiry

@admin.register(PilotInquiry)
class PilotInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'company_name', 'created_at')
    search_fields = ('name', 'email', 'company_name')
    readonly_fields = ('created_at',)
