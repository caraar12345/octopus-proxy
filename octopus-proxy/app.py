import falcon
import sys

sys.path.append("octopus-proxy/")

app = application = falcon.App()

from rates import RatesResource

rates = RatesResource()
app.add_route("/get_rates", rates)
