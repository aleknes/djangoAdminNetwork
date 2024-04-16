from django.contrib import admin

@admin.action(description='Do this on selected Routers')
def perform_some_action(self, request, queryset):
    for router in queryset:
        print(f'Doing something on {router.hostname}')