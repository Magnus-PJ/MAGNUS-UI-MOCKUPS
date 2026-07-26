"""Generation-time identity & palette normalizer (D-41). Sources stay frozen; every output runs through this."""
import re
REPLACES = [
 ("Meridian Diagnostics","Magnus Diagnostics"), ("meridian-diagnostics","magnus-diagnostics"), ("Meridian","Magnus"),
 ("MERIDIAN","MAGNUS"), ("meridian","magnus"), ("MERID","MAG"),
 ("Andheri West branch","North Paravoor"), ("Andheri West","North Paravoor"),
 ("Whitefield branch","Irinjalakuda"), ("Whitefield","Irinjalakuda"), ("Pune Camp","Pullur"),
 ("Bengaluru 560066","Ernakulam 683513"), ("Mumbai, Maharashtra 400005","Kochi, Kerala 682001"),
 ("Maharashtra 400053","Kerala 683513"), ("Lokhandwala, North Paravoor","Market Road, North Paravoor"),
 ("Mumbai","Kochi"), ("Maharashtra","Kerala"),
 ("Andheri W","North Paravoor"), ("Andheri","North Paravoor"), ("ANDHERI WEST","NORTH PARAVOOR"), ("ANDHERI","NORTH PARAVOOR"),
 ("Vashi","Irinjalakuda"), ("Colaba","Fort Kochi"), ("Powai","Aluva"), ("Borivali","Angamaly"), ("Thane","Thrissur"),
 ("US-AND-","US-NPV-"), ("INV/AND/","INV/NPV/"), ("RCP/AND/","RCP/NPV/"), ("CRN/AND/","CRN/NPV/"), ("EST/AND/","EST/NPV/"), ("CSH-AND-","CSH-NPV-"), ("AGX-AW-","AGX-NPV-"), ("AW-EDGE-","NPV-EDGE-"), ("MAG-AW","MAG-NPV"),
 ("27AAACM1234K1Z5","32AAACM1234K1Z7"), ("27AAACM5678P2Z1","32AAACM5678P2Z9"), ("MRD-PUN","MAG-IJK"), ("MRD-","MAG-"),
 ("VASHI","IJK"), ("US-THN","US-TSR"), ("andheri-west","north-paravoor"), ("andheri","npv"),
 ("CT-AND","CT-NPV"), ("MAG-AND","MAG-NPV"), ("-AND-","-NPV-"), ("-AW-","-NPV-"),
 ("Navi Kochi","Aluva"), ("POWAI","ALUVA"), ("Pune Aundh","Chalakudy"),
 ("Nashik camp unit","Guruvayur camp unit"), ("Nashik centre","Guruvayur centre"), ("Nashik camp","Guruvayur camp"),
 ("MH/PNDT/2019/4471","KL/PNDT/EKM/2019/4471"),
]
PALETTE_FIX = {  # rogue hex -> nearest token
 "#16A34A":"#15803D", "#DC2626":"#B91C1C", "#D97706":"#B45309", "#0EA5E9":"#0369A1",
 "#10B981":"#0F766E", "#EF4444":"#B91C1C", "#F97316":"#B45309", "#22C55E":"#15803D",
 "#2563EB":"#0369A1", "#7C3AED":"#6D28D9",
}
def normalize(text):
    for a,b in REPLACES: text = text.replace(a,b)
    for a,b in PALETTE_FIX.items():
        text = text.replace(a,b).replace(a.lower(),b)
    return text
