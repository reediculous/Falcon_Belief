def kwCheck1(kws, itemname):
    for kw in kws:
        if not kw in itemname:
            return False
    return True


def kwCheck(kwListList, itemName):
    for kwList in kwListList:
        if kwCheck1(kwList, itemName):
            return True
    return False

keywords = [["yeezy"],
            ["dunk"],
            ["nike", "ambush"],
            ["nike", "stussy"],
            ["air force", "para-noise"],
            ["sacai"],
            ["para-noise"],
            ]