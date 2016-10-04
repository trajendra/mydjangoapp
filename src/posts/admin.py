from django.contrib import admin

# Register your models here.
from .models import Post,Category,SubCategory

class PostModelAdmin(admin.ModelAdmin):
	list_display = ["title", "updated", "timestamp"]
	list_display_links = ["updated"]
	list_editable = ["title"]
	list_filter = ["updated", "timestamp"]

	search_fields = ["title", "content"]
	class Meta:
		model = Post

class CategoryModelAdmin(admin.ModelAdmin):
	list_display = ["name", "is_active", "created_on"]
	list_display_links = ["name"]
	search_fields = ["name"]
	class Meta:
		model = Category

class SubCategoryModelAdmin(admin.ModelAdmin):
	list_display = ["category","name", "is_active", "created_on"]
	list_display_links = ["name"]
	list_filter = ["category"]

	search_fields = ["category", "name"]
	class Meta:
		model = SubCategory

admin.site.register(Post, PostModelAdmin)
admin.site.register(Category,CategoryModelAdmin)
admin.site.register(SubCategory,SubCategoryModelAdmin)


