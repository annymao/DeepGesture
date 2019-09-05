import json

path = "deepgesture-export.json"
with open(path,encoding = 'utf8') as json_file: 
        
       data = json.load(json_file)

for cp in data:
    print(cp)
    for d in data[cp]:
        print(d)
        print(data[cp][d]["subject"]["id"])
        print(data[cp][d]["subject"]["name"])
        fileName = "Data/"+str(data[cp][d]["subject"]["id"])+"_"+data[cp][d]["subject"]["name"]+".json"
        with open(fileName, 'w') as f:
            json.dump(data, f)
