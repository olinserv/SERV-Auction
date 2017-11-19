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
    if affiliation == "Student":
        return ".".join(name.split()) + "@students.olin.edu"
    elif affiliation == "Alum":
        return ".".join(name.split()) + "@alumni.olin.edu"
    else:
        return ".".join(name.split()) + "@olin.edu"
