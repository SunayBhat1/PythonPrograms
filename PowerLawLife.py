# https://betterprogramming.pub/how-to-send-push-notifications-to-your-phone-from-any-script-6b70e34748f6


from urllib import request
import numpy as np

key_Sunay = "Lmdwc3Ei4h0vfiIwLA4K0"
key_Matthew = "nHy_ScCt8nLNGZhaprZ9LSGQEV4CaNr8XSPmEzKdRU7"


# Fasting/Diet
if np.random.pareto(1.16,1)>50:
    message = 'Full_Fast_Day!!!'
elif np.random.pareto(1.16,1)>12:
    message = 'Dinner_Only_Day!!'
else:
    message = 'Normal_Day!'

request.urlopen("https://maker.ifttt.com/trigger/notify/with/key/%s?value1=%s" % (key_Sunay,message));
request.urlopen("https://maker.ifttt.com/trigger/notify/with/key/%s?value1=%s" % (key_Matthew,message));
