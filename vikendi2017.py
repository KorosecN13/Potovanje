from datetime import date, timedelta, datetime

def vikendi_get(fromdate=date(2017,1,1), todate=date(2017,1,31)):
    delta = timedelta(days = 1)
    d = fromdate
    vikendi = []
    """Funkcija vrne seznam dvojic petkov in nedelj"""
    while d <= todate:
        if d.weekday() == 4:
            vikendi.append((str(d), str(d+2*delta)))
        d+=delta
    return vikendi


def datumi_vikendov_get(fromdate=date(2017,1,1), todate=date(2017,12,31)):
    datumi = []
    for vikend in vikendi_get(fromdate, todate):
        m, n = vikend
        datumi.append(m[8:10] + ".-" + n[8:10] + "." + n[5:7])
    return datumi
