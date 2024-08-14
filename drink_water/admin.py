from django.contrib import admin

from drink_water.models import User, UserAction, UserDataHistory


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["name", "weight", "created_at"]
    search_fields = ["name"]

@admin.register(UserDataHistory)
class UserDataHistoryAdmin(admin.ModelAdmin):
    list_display = ["user", "weight", "created_at"]
    search_fields = ["user"]

@admin.register(UserAction)
class UserActionAdmin(admin.ModelAdmin):
    list_display = ["user", "action", "quantity", "created_at"]
    search_fields = ["user__name"]
