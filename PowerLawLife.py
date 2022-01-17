from urllib import request
import numpy as np

key = "Lmdwc3Ei4h0vfiIwLA4K0"


# Fasting/Diet
if np.random.pareto(1.16,1)>75:
    message = 'Full_Fast_Day!!!'
elif np.random.pareto(1.16,1)>15:
    message = 'Dinner_Only_Day!!'
else:
    message = 'Normal_Day!'

request.urlopen("https://maker.ifttt.com/trigger/notify/with/key/%s?value1=%s" % (key,message));
