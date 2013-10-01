from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

class Experiment(models.Model):
    code = models.CharField(max_length=64, blank=True, null=True)
    variant = models.CharField(max_length=64, blank=True, null=True)
    #fbposts = models.IntegerField(default=0, null=True, blank=True)
    pageviews = models.IntegerField(default=0, null=True, blank=True)
    #logins = models.IntegerField(default=0, null=True, blank=True)
    shares = models.IntegerField(default=0, null=True, blank=True)

    def pctshared(self):
        pct = 0.0
        if self.pageviews > 0:
            pct = (self.shares)/float(self.pageviews) * 100
        return '%2.1f' % pct

class ExperimentAdmin(admin.ModelAdmin):
    list_display = ['code', 'variant', 'pageviews', 'shares', 'pctshared']

admin.site.register(Experiment, ExperimentAdmin)
