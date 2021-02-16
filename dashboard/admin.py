from django.contrib import admin
from .models import Zip
from .models import Company
from .models import Client
from .models import Skill
from .models import Query
from .models import Job
from .models import Query_Job
from .models import Query_Skill


admin.site.register(Zip)
admin.site.register(Company)
admin.site.register(Client)
admin.site.register(Skill)
admin.site.register(Query)
admin.site.register(Job)
admin.site.register(Query_Job)
admin.site.register(Query_Skill)
