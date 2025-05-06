from django.contrib import admin
from .models import Contact,Enrollment,Trainer,MembershipPlan,Feedback


# Register your models here.
admin.site.register(Contact)
admin.site.register(Enrollment)
admin.site.register(Trainer)
admin.site.register(MembershipPlan)
admin.site.register(Feedback)