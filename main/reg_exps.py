"""
    List of regular expressions that will be
    used to search for specific data in text
"""
# List of dates
dates = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi",
         "dimanche", "janvier", "fevrier", "mars", "avril", "mai",
         "juin", "juillet", "aout", "septembre", "octobre", "novembre",
         "décembre", "demain", "aujoud'hui", "hier", "midi", "minuit", "soir"]

# List of regexp
regexp_hours = r"\b[0-9]{1,2}( )*[h:]( )*[0-9]{0,2}\b"
regexp_money = r"""\b[0-9]+( )*(euros|e|eur|euro|dollar|dollars|
                    boul|patate|boule|boules)\b"""
regexp_currency = r"(€|\$)"
regexp_email = r"\b[a-z]*@[a-z]*[.]\b"
regexp_tel = r"(?:(?:\+|00)33|0)\s*[1-9](?:[\s.-]*\d{2}){4}"
