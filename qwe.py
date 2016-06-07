import urllib.request
import json
from pprint import pprint
import os
import pandas

def potovanje(mesto="LONDON",datum_zacetka = "2016-12-01", datum_konca = "2016-12-03", stevilo_zadetkov=50):
    ime_datoteke = mesto + ".txt"
    if os.path.isfile(ime_datoteke):
        print("Datoteke za to mesto so že shranjene!")

    else:
        url = "http://terminal2.expedia.com/x/mhotels/search?city={0}&checkInDate={1}&checkOutDate={2}&room1=2&resultsPerPage={3}&apikey=5nV9DnOkvYP0Ius05gpN9dHNAdYyF1F2".format(
                mesto, datum_zacetka, datum_konca, stevilo_zadetkov)
        slovar = get_slovar(url)
        with open(mesto + ".txt","w") as f:
            pprint(slovar, stream=f)
        csv = ""
        for i in range(stevilo_zadetkov):
            csv += slovar["hotelList"][i]["name"]+","
            csv += slovar["hotelList"][i]["proximityDistanceInKiloMeters"]+","
            csv += slovar["hotelList"][i]["lowRateInfo"]["priceToShowUsers"] + "\n"

        with open(mesto + ".csv","w") as f:
            f.write(csv)

        print("Poglej in se prepričaj!")

def get_slovar(url):

    """ V funkcijo vpisemo url, ki ga sestavimo iz danih podatkov (mesto, začetek in konec potovanja)"""

    response = urllib.request.urlopen(url)
    json_text = response.read()
    json_text = json_text.decode("utf-8")
    json_text.replace("\\r","")
    json_text.replace("\r","")
    return json.loads(json_text)