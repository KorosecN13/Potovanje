import urllib.request
import json
from pprint import pprint
import os
from datetime import date
from vikendi2017 import vikendi_get, datumi_vikendov_get
import unicodedata

mesta = ["LONDON", "PARIS", "MOSCOW", "BERLIN", "PRAGUE", "AMSTERDAM", "BERN"]

def potovanje(mesto="LONDON",datum_zacetka_obdobja = date(2017,2,1), datum_konca_obdobja = date(2017,12,31), stevilo_zadetkov=200):
    """Ta funkcija naredi datoteko, v kateri je shranjenih prvih nekaj (toliko kot je
       stevilo zadetkov) najugodnejsih ponudb za vikend nocitev za 2 odrasli osebi v
       izbranem kraju. Datoteka je sestavljena tako, da so vsi podatki za posamezen"""
    
    ime_datoteke = mesto + ".csv"
    if os.path.isfile(ime_datoteke):
        print("Podatki za to mesto so že shranjeni!")
    else:
        datumi_vikendov = datumi_vikendov_get(fromdate=datum_zacetka_obdobja, todate=datum_konca_obdobja)
        vikendi = vikendi_get(datum_zacetka_obdobja, datum_konca_obdobja)
        csv = ""
        stevec = 0
        hoteli = "hotelId,name,proximityDistance,guestRating,freeCancellation,shortDescription" + "\n"
        csv = ""
        print("Shranjujem ...")
        for datum_zacetka_vikenda, datum_konca_vikenda in vikendi:
            url = "http://terminal2.expedia.com/x/mhotels/search?city={0}&checkInDate={1}&checkOutDate={2}&room1=2&resultsPerPage={3}&apikey=5nV9DnOkvYP0Ius05gpN9dHNAdYyF1F2".format(
                mesto, str(datum_zacetka_vikenda), str(datum_konca_vikenda), stevilo_zadetkov)
            slovar = get_slovar(url)
            for j in range(stevilo_zadetkov):
                csv += str(datum_zacetka_vikenda) + ","
                csv += slovar["hotelList"][j]["hotelId"]+","
                dodatne_info = slovar["hotelList"][j]
                neki = dodatne_info['lowRateInfo']
                csv += neki["priceToShowUsers"]
                #csv += slovar["hotelList"][j]['lowRateInfo'].get("priceToShowUsers", "")
                csv += "\n"

                id = slovar["hotelList"][j]["hotelId"]
                if id in hoteli:
                    continue
                else:
                    hoteli += id + ","
                    c = slovar["hotelList"][j]["name"]
                    hoteli += " ".join(c.split(",")) + ","
                    a = slovar["hotelList"][j]["proximityDistanceInKiloMeters"]
                    hoteli += "%.2f" % round(float(a),2) + ","
                    hoteli += slovar["hotelList"][j]["hotelGuestRating"] + ","
                    hoteli += str(slovar["hotelList"][j]["hasFreeCancellation"]) + ","
                    b = slovar["hotelList"][j]["shortDescription"].strip()
                    hoteli += ";".join(b.split(","))  
                    hoteli += "\n"    
            stevec += 1

        with open(mesto + "_Hoteli.csv","w", encoding = 'utf-8') as f:
            f.write(hoteli)

        prva_vrstica = "friday,hotelId,price"
            
        with open(mesto + ".csv","w") as f:
            csv = prva_vrstica + "\n" + csv
            f.write(csv)
    print("Zaključeno!")

def get_slovar(url):

    """ V funkcijo vpisemo url, ki ga sestavimo iz danih
        podatkov (mesto, datum začetka in konca potovanja)"""

    response = urllib.request.urlopen(url)
    json_text = response.read()
    json_text = json_text.decode("utf-8")
    json_text.replace("\\r","")
    json_text.replace("\r","")
    return json.loads(json_text)
