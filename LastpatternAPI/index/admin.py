from django.contrib import admin

from .models import StartPredictionScheduler, PredictionModel


@admin.register(StartPredictionScheduler)
class PredictionModelAdmin(admin.ModelAdmin):
    actions = ("start_workers",)

    def start_workers(self, request, queryset):
        from .scheduler import start
        start()


@admin.register(PredictionModel)
class PredictionModelA(admin.ModelAdmin):
    list_display = ("symbol", "interval", "symbolClosePrice", "nextClosePrice",
                    "patternPredictionIsSuccess", "indicatorPredictionIsSuccess", "summaryPredictionIsSuccess")
    ordering = ("-createdTime",)
    list_per_page = 50
