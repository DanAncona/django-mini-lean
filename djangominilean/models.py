from django.db import models
from django.contrib import admin

class Experiment(models.Model):
    code = models.CharField(max_length=64, blank=True, null=True)
    variant = models.CharField(max_length=64, blank=True, null=True)
    fbposts = models.IntegerField(default=0, null=True, blank=True)
    pageviews = models.IntegerField(default=0, null=True, blank=True)
    logins = models.IntegerField(default=0, null=True, blank=True)
    shares = models.IntegerField(default=0, null=True, blank=True)

    def pctfbtopage(self):
        pct = 0.0
        if self.fbposts > 0:
            pct = (self.pageviews)/float(self.fbposts) * 100
        return '%2.1f' % pct

    def pctpagetologin(self):
        pct = 0.0
        if self.logins > 0:
            pct = (self.logins)/float(self.pageviews) * 100
        return '%2.1f' % pct

class ExperimentAdmin(admin.ModelAdmin):
    list_display = ['code', 'variant', 'fbposts', 'pctfbtopage', 'pageviews', 'pctpagetologin', 'shares']

admin.site.register(Experiment, ExperimentAdmin)