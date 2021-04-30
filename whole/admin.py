from django.contrib import admin
from .models import Post #, Profile #Profile added


from .models import Search

admin.site.register(Post)


admin.site.register(Search)

