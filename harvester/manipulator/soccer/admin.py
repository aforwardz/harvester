from django.contrib import admin
from soccer import models

# Register your models here.


class AwardAdmin(admin.ModelAdmin):
    list_display = ['id', 'award_name', 'award_grade', 'award_season', 'award_date']
    ordering = ('-create_time',)
    search_fields = ('award_name', )

    class Meta:
        model = models.Award


class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'nation']
    ordering = ('-create_time',)
    search_fields = ('name',)

    class Meta:
        model = models.Competition


class ClubAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'nation']
    ordering = ('-create_time',)
    search_fields = ('name', )

    class Meta:
        model = models.Club


class NationTeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'nation']
    ordering = ('-create_time',)
    search_fields = ('name', )

    class Meta:
        model = models.NationTeam


class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'en_name', 'birth', 'age', 'nationality']
    ordering = ('-create_time',)
    search_fields = ('name', )

    class Meta:
        model = models.Player


class PlayRecordAdmin(admin.ModelAdmin):
    list_display = ['id', ]
    ordering = ('-create_time',)
    # search_fields = ()

    class Meta:
        model = models.PlayRecord


class CoachAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'en_name', 'birth', 'age', 'nationality']
    ordering = ('-create_time',)
    search_fields = ('name', )

    class Meta:
        model = models.Coach


class CoachRecordAdmin(admin.ModelAdmin):
    list_display = ['id']
    ordering = ('-create_time',)
    # search_fields = ('award_name', )

    class Meta:
        model = models.CoachRecord


class MatchAdmin(admin.ModelAdmin):
    list_display = ['id']
    ordering = ('-create_time',)
    # search_fields = ('award_name', )

    class Meta:
        model = models.Match


class PlayerPerformanceAdmin(admin.ModelAdmin):
    list_display = ['id']
    ordering = ('-create_time',)
    # search_fields = ('award_name', )

    class Meta:
        model = models.PlayerPerformance


class CompetitionDataAdmin(admin.ModelAdmin):
    list_display = ['id']
    ordering = ('-create_time',)
    # search_fields = ('award_name', )

    class Meta:
        model = models.CompetitionData


admin.site.register(models.Award, AwardAdmin)
admin.site.register(models.Competition, CompetitionAdmin)
admin.site.register(models.Club, ClubAdmin)
admin.site.register(models.NationTeam, NationTeamAdmin)
admin.site.register(models.Player, PlayerAdmin)
admin.site.register(models.PlayRecord, PlayRecordAdmin)
admin.site.register(models.Coach, CoachAdmin)
admin.site.register(models.CoachRecord, CoachRecordAdmin)
admin.site.register(models.Match, MatchAdmin)
admin.site.register(models.PlayerPerformance, PlayerPerformanceAdmin)
admin.site.register(models.CompetitionData, CompetitionDataAdmin)
