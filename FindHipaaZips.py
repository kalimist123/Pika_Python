import pandas as pd
import re
searchlist = []
with open("forbidden_zips.txt") as g:
    for line in g:
        searchlist.append(line.strip())

pattern = re.compile("|".join(searchlist))


df = pd.read_csv(r"file.xlsx .csv",encoding = 'unicode_escape')
rx = df[df['zip'].astype(str).str.contains(pattern)==True]
print(rx)
