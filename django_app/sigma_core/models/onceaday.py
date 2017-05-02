from django.db import models
from sigma_api.importer import load_ressource

GroupMember = load_ressource("GroupMember")

for mship in GroupMember.objects.all:
  if (mship.average_clicks_last_month!=0)
    mship.average_clicks_last_month = (mship.nb_clicks_today+29*mship.average_clicks_last_month)//30
  else
    mship.average_clicks_last_month = mship.nb_clicks_today//2
  mship.nb_clicks_today = 0
  mship.save()
