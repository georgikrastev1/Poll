import os
from django.core.validators import FileExtensionValidator
from django.db import models
import datetime
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings


# Create your models here.
# def name_file(case, filename):
#     return  f'{case.author.username}/{case.date_posted.strftime("%Y-%m-%d_%H-%M-%S")}/{filename}'

def name_file(instance, filename):
    return f'main_images/{instance.author}/{filename}'

# def name_media_file(media, filename):
#     return  f'{media.case.author.username}/{media.case.date_posted.strftime("%Y-%m-%d_%H-%M-%S")}/{filename}'

def name_media_file(media, filename):
    return f'supplementary_files/case{media.case.id}/{filename}'
    
class Disease(models.Model):
    name = models.CharField(max_length=5000, null=True)
    description = models.CharField(max_length=10000, null=True)
    symptoms = models.CharField(max_length=5000, null=True)
    # https://www.datadictionary.nhs.uk/data_dictionary/attributes/e/end/ethnic_category_code_de.asp
    categories = (
        ('Alcohol and drug misuse', 'Alcohol and drug misuse'),
        ('Blood and lymph', 'Blood and lymph'),
        ('Brain, nerves and spinal cord', 'Brain, nerves and spinal cord'),
        ('Cancer', 'Cancer'),
        ('Diabetes', 'Diabetes'),
        ('Ears, nose and throat', 'Ears, nose and throat'),
        ('Eyes', 'Eyes'),
        ('Glands', 'Glands'),
        ('Heart and blood vessels', 'Heart and blood vessels'),
        ('Immune system', 'Immune system'),
        ('Infections and poisoning', 'Infections and poisoning'),
        ('Injuries', 'Injuries'),
        ('Kidneys, bladder and prostate', 'Kidneys, bladder and prostate'),
        ('Lungs and airways', 'Lungs and airways'),
        ('Mental health', 'Mental health'),
        ('Mouth', 'Mouth'),
        ('Muscle, bone and joints', 'Muscle, bone and joints'),
        ('Nutritional', 'Nutritional'),
        ('Pregnancy and childbirth', 'Pregnancy and childbirth'),
        ('Sexual and reproductive', 'Sexual and reproductive'),
        ('Stomach, liver and gastrointestinal tract', 'Stomach, liver and gastrointestinal tract'),
        ('Not Known', 'Not Known')

    )
    category = models.CharField(max_length=99, choices=categories, default='Other')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('disease-cases', kwargs={'disease_id': self.id})

    class Meta:
        ordering = ('name',)


class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

