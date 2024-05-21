from django.contrib import admin

from users.models import User, EmailVerification


admin.site.register(User)


@admin.register(EmailVerification)
class AdminEmailVerification(admin.ModelAdmin):
    list_display = ('id', 'user', 'key', 'created_at', 'expiration',)
    list_filter = ('expiration',)
