from django.contrib import admin

from .models import Comment, Genre, Review, Title

admin.site.register(Review)
admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Comment)
