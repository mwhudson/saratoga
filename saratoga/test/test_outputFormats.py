from twisted.trial.unittest import TestCase

from saratoga import api, outputFormats
from saratoga.test.test_api import APIImpl, APIDef

class SaratogaAcceptHeaderTests(TestCase):

    def setUp(self):

        def respJSON(status, data):
            return "JSON"

        def respYAML(status, data):
            return "YAML"

        o = outputFormats.OutputRegistry("application/json")
        o.register("application/yaml", respYAML)
        o.register("application/json", respJSON)
        o.register("application/debuggablejson",
                   outputFormats.DebuggableJSendJSONOutputFormat)

        self.api = api.SaratogaAPI(APIImpl, APIDef, outputRegistry = o)

    def test_noneGiven(self):

        def rendered(request):
            self.assertEqual(
                request.getWrittenData(),
                "JSON"
            )
            self.assertEqual(request.code, 200)

        return self.api.test("/v1/example").addCallback(rendered)

    def test_nonDefaultGiven(self):

        def rendered(request):
            self.assertEqual(
                request.getWrittenData(),
                "YAML"
            )
            self.assertEqual(request.code, 200)

        return self.api.test("/v1/example",
                             headers={"Accept": ["application/yaml"]}
                         ).addCallback(rendered)

    def test_unknownDefaultGiven(self):

        def rendered(request):
            self.assertEqual(
                request.getWrittenData(),
                "406 Not Acceptable, please use one of: application/yaml, appli"
                "cation/json, application/debuggablejson"
            )
            self.assertEqual(request.code, 406)

        return self.api.test("/v1/example",
                             headers={"Accept": ["application/whatever"]}
                         ).addCallback(rendered)

    def test_debuggableJSend(self):

        def rendered(request):
            self.assertEqual(
                request.getWrittenData(),
                '{\n    "data": {},\n    "status": "success"\n}'
            )
            self.assertEqual(request.code, 200)

        return self.api.test("/v1/example",
                             headers={"Accept": ["application/debuggablejson"]}
                         ).addCallback(rendered)

    def test_listDefaultGiven(self):

        def rendered(request):
            self.assertEqual(
                request.getWrittenData(),
                'JSON'
            )
            self.assertEqual(request.code, 200)

        return self.api.test("/v1/example",
                             headers={"Accept": ["text/html,application/xhtml+xm"
                                                 "l,application/xml;q=0.9,"
                                                 "*/*;q=0.8"]}
                         ).addCallback(rendered)

    def test_qualityPreferencesGiven(self):

        def rendered(request):
            self.assertEqual(
                request.getWrittenData(),
                'YAML'
            )
            self.assertEqual(request.code, 200)

        return self.api.test("/v1/example",
                             headers={"Accept": ["text/html,application/xhtml+xm"
                                                 "l,application/json;q=0.7,"
                                                 "application/yaml;q=0.8"]}
                         ).addCallback(rendered)
