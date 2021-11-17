import datetime
from typing import Generic
from django.db import models
from django.utils import timezone
from django.contrib import admin
from taggit.managers import TaggableManager
from taggit.models import CommonGenericTaggedItemBase, TaggedItemBase

class GenericStringTaggedItem(CommonGenericTaggedItemBase, TaggedItemBase):
    object_id = models.CharField(max_length=50, verbose_name=_('Object id'), db_index=True)

class Question(models.Model):
    """Model for questions"""
    def __str__(self):
        return self.question_text
        
    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently?',
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    question_name = models.CharField(max_length=20, primary_key=True)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    tags = TaggableManager(through=GenericStringTaggedItem)
    
    

class Choice(models.Model):
    """Model for choices"""
    def __str__(self):
        return self.choice_text
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
