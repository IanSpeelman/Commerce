from django.contrib import admin
from auctions.models import User, Listing
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    pass
class ListingAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)