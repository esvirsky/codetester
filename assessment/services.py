import json
from pprint import pprint

import requests
import base64
from django.conf import settings
from requests import RequestException

from general.models import Language

CodeMirrorMode = {
    Language.PYTHON.value: 'python',
    Language.JAVASCRIPT.value: 'javascript',
    Language.GO.value: 'go',
    Language.PHP.value: 'php',
    Language.RUBY.value: 'ruby',
    Language.JAVA.value: 'clike',
    Language.C.value: 'clike',
    Language.CPP.value: 'clike',
}


class Judge0(object):

    LanguageToIdDict = {
        Language.PYTHON.value: settings.JUDGE_LANGUAGE_PYTHON,
        Language.JAVASCRIPT.value: settings.JUDGE_LANGUAGE_JAVASCRIPT,
        Language.GO.value: settings.JUDGE_LANGUAGE_GO,
        Language.RUBY.value: settings.JUDGE_LANGUAGE_RUBY,
        Language.JAVA.value: settings.JUDGE_LANGUAGE_JAVA,
        Language.C.value: settings.JUDGE_LANGUAGE_C,
        Language.CPP.value: settings.JUDGE_LANGUAGE_CPP,
    }

    def submit_code(self, code, input, language):
        # Can raise a RequestException
        encoded_code = base64.b64encode(code.encode('utf-8'))
        data = {"source_code": encoded_code, "language_id": Judge0.LanguageToIdDict[language]}
        if input:
            data['stdin'] = base64.b64encode(input.encode('utf-8'))

        headers = {
            "X-Auth-Token": settings.JUDGE_AUTH_KEY
        }
        pprint(data)
        response = requests.post("%s/submissions/?base64_encoded=true&wait=false" % settings.JUDGE_API, data=data, headers=headers)
        if not response.ok:
            raise RequestException(response.text)

        return json.loads(response.text)["token"]

    def check_submission(self, token):
        # Can raise a RequestException
        headers = {
            "X-Auth-Token": settings.JUDGE_AUTH_KEY
        }
        response = requests.get("%s/submissions/%s?base64_encoded=true" % (settings.JUDGE_API, token), headers=headers)
        if not response.ok:
            raise RequestException(response.text)

        j = json.loads(response.text)
        for field in ['stdout', 'stderr', 'compile_output', 'message']:
            if field in j and j[field]:
                j[field] = base64.b64decode(j[field]).decode('utf-8')
        return j


class CodeMod(object):

    @staticmethod
    def wrap_code_in_method(code, language):
        if language == Language.PYTHON.value:
            all = "import io\n"
            all += "import sys\n"
            all += "from contextlib import redirect_stdout\n"
            all += "def out(**kwargs):\n"
            all += "\tfio = io.StringIO()\n"
            all += "\twith redirect_stdout(fio):\n\t\tpass\n\t\t"
            all += code.replace('\n', '\n\t\t') + "\n"
            all += "\toutput = fio.getvalue().strip()\n"
            all += "\treturn output"
            return all
        else:
            return code