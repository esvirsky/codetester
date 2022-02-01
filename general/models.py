from enum import Enum

from django.db import models


class Language(Enum):
    PYTHON = "python"
    RUBY = "ruby"
    JAVASCRIPT = "javascript"
    PHP = "php"
    JAVA = "java"
    C = "c"
    CPP = "cpp"
    GO = "go"


class BaseCreatedModifiedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
