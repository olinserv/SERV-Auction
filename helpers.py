def addDollarSign(amt):
    if amt[:2] == '\\$':
        return amt
    else:
        return '\\$'+amt


def handleLatexChars(s):
    return (
        s.replace("$","\\$")
        .replace("&","\\&")
        .replace("#","\\#")
        .replace("^","\\^")
        .replace("_","\\_")
        .replace("\^\^","^^")
        .replace("%","\\%")
        .replace(">", "\\textgreater ")
        .replace("<", "\\textless ")
    )


def parse_email(name, affiliation):
    name = name.split(',')[0].split(';')[0] # pull out the first name if there are several
    if affiliation == "Alum":
        return ".".join(name.split()) + "@alumni.olin.edu" # first.last@alumni.olin.edu
    else:
        return "".join(name.split()[0][0], *name.split()[1:]) + "@olin.edu" # flast@olin.edu
