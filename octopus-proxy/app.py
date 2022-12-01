import falcon
import sys

sys.path.append('octopus-proxy/')
from main import GetRates


app = application = falcon.App()
get_rates = GetRates()
app.add_route('/get_rates', get_rates)

