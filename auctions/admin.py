from django.contrib import admin
from auctions.models import User, Listing, Bid, Watchlist, Comment
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    pass
class ListingAdmin(admin.ModelAdmin):
    pass
class BidAdmin(admin.ModelAdmin):
    pass

class WatchlistAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(Comment, CommentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Watchlist, WatchlistAdmin)