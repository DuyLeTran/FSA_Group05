from django.contrib import admin
from .models import AIInsights, UserProgress,PerformanceAnalytics
# Register your models here.

admin.site.register(AIInsights)
admin.site.register(UserProgress)
admin.site.register(PerformanceAnalytics)
