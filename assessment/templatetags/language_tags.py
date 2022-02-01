from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static

from assessment.services import CodeMirrorMode
from general.models import Language

register = template.Library()




pretty_print_dict = {
    Language.PYTHON.value: "lang-py",
    Language.JAVASCRIPT.value: "lang-js",
    Language.GO.value: "",
    Language.RUBY.value: "lang-rb",
    Language.JAVA.value: "lang-java",
}


@register.simple_tag
def codemirror_mode_javascript(language):
    return static('js/mode/%s.js' % CodeMirrorMode[language])


@register.simple_tag
def codemirror_mode(language):
    return CodeMirrorMode[language]


@register.simple_tag
def pretty_print_language(language):
    return pretty_print_dict[language]
