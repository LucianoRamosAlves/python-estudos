intens = (1, 2, 3, 4, 5)

for intem in (intens):
    print(f"round {intem}")

# eu posso também usar em texto
files = [' Cse.TXT ', ' Data.doc ', 'FN.TXT']

for file in files:
    file = file.strip().lower().replace(".doc", ".txt")
    print(file) 