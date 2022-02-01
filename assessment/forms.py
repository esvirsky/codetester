from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Button, Layout, Fieldset, ButtonHolder, Div, HTML
from django import forms
from django.forms import ModelForm

from assessment.examples import get_start_example, get_test_example, get_solution_example
from assessment.models import Question, Assessment
from general.models import Language

instruction_text = """
Write a function that takes a parameter and multiplies it by itself
"""


class AssessmentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AssessmentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'assessment-form'
        self.helper.add_input(Submit('submit', 'Update' if self.instance.id else 'Create', css_class="btn btn-primary"))

    class Meta:
        model = Assessment
        fields = ['name', 'language']


class QuestionForm(ModelForm):
    title = forms.CharField(required=True, label="<b>Title*</b>")
    instructions = forms.CharField(required=True, label="<b>Instructions*</b></br>Be as descriptive as possible", widget=forms.Textarea)
    starting_code = forms.CharField(required=True, label="""<b>Starting Code*</b></br>This will be the starting code that the test taker will see, 
                                                        should have a skeleton class or method""", widget=forms.Textarea)
    testing_code = forms.CharField(required=True, label="""<b>Testing Code*</b></br>This will call the code that the test taker creates. 
                                                        If the code has any mistakes output them to stderr. 
                                                        If stderr is null the test is passed.""",
                                                        widget=forms.Textarea)
    solution_code = forms.CharField(required=True, label="""<b>Solution Code*</b><br/>Use this field to test a solution and 
                                                            make sure that the testing code is working correctly""", widget=forms.Textarea)
    wrap_output = forms.BooleanField(required=False, label='''Wrap the solution code in an out(**kwargs) method that returns stdout''')

    results = forms.CharField(required=False, label="<b>Results</b>", widget=forms.Textarea, disabled=True)

    def __init__(self, *args, **kwargs):
        assessment = kwargs.pop("assessment")
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'question-form'
        self.helper.attrs = {'novalidate': 'novalidate'}
        self.helper.layout = Layout(
            Fieldset(
                '',
                Div(Div('title', css_class="col-sm-7"), css_class="row"),
                Div(
                    Div('instructions', css_class="col-sm-7"),
                    HTML("<div class='col-sm-5 pt-2 pb-4'><b>Example:</b><div class='pt-2'>%s</div></div>" % instruction_text),
                    css_class="row"
                ),
                Div(
                    Div('starting_code', css_class="col-sm-7"),
                    HTML("<div class='col-sm-5 pt-2'><b>Example:</b><div class='pt-2'>%s</div></div>" % get_start_example(assessment.language)),
                    css_class="row"
                ),
                Div(
                    Div('testing_code', css_class="col-sm-7"),
                    HTML("<div class='col-sm-5 pt-2'><b>Example:</b><div class='pt-2'>%s</div></div>" % get_test_example(assessment.language)),
                    css_class="row"
                ),
                Div(
                    Div('solution_code', css_class="col-sm-7"),
                    HTML("<div class='col-sm-5 pt-2'><b>Example:</b><div class='pt-2'>%s</div></div>" % get_solution_example(assessment.language)),
                    css_class="row"
                ),
                'wrap_output' if assessment.language == Language.PYTHON.value else HTML(''),
                Button("test", "Run"),
                HTML("<br/> Runs the testing code on the solution code"),
                'results'
            ),
            ButtonHolder(
                Submit('submit', 'Update' if self.instance.id else 'Create', css_class='btn btn-primary float-right')
            )
        )

    class Meta:
        model = Question
        fields = ['title', 'instructions', 'starting_code', 'testing_code', 'solution_code', 'wrap_output']


class StartAssessmentSelfForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)
    email = forms.EmailField(label='Your email', max_length=100)

    def __init__(self, *args, **kwargs):
        super(StartAssessmentSelfForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'start-assessment-self-form'
        self.helper.add_input(Submit('submit', 'Start Assessment', css_class="btn btn-primary"))