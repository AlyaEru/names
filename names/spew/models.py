from django.db import models

#TODO: add adverb

class Word(models.Model):
    word = models.CharField(max_length=200)
    PART_OF_SPEECH = (
        ('no','Noun'),
        ('ad','Adjective'),
        ('na','Name'),
        ('se','Sentence'),
        ('av','Adverb'),
        ('s?','Interrogative'),
        ('pn','Plural Noun'),
    )
    partOfSpeech = models.CharField(
        max_length=2,
        choices=PART_OF_SPEECH
    )

    def __str__(self):
        return self.word
