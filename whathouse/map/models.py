from django.db import models

# Create your models here.
class real_price_deal(models.Model):
	date = models.IntegerField()
	area = models.CharField( max_length = 64)
	road = models.CharField( max_length = 256 )
	price = models.IntegerField()
	#longitude = models
	#latitude = models

	def __unicode__(self):
		return self.road


class real_price_rent(models.Model):
	date = models.IntegerField()
	area = models.CharField( max_length = 64)
	road = models.CharField( max_length = 256 )
	price =  models.IntegerField()
	#longitude = models
	#latitude = models

	def __unicode__(self):
		return self.road
