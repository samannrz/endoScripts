dict = {'nicolas.bourdel': 0, 'Jean-Luc.Pouly': 1, 'giuseppe.giacomello': 2, 'filippo.ferrari': 3
    , 'Ervin.Kallfa': 4,'ebbe.thinggaard': 5}# , 'incision.consensus': 4
for annotator in list(dict.keys()):
    with open("IncisionDataFolderCreation_V2.py") as f:
        exec(f.read())
