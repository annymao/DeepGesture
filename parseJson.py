import json

path = "deepgesture-export.json"
with open(path,encoding = 'utf8') as json_file: 
        
       data = json.load(json_file)
#for cellphone id in data
for cp in data:
    print(cp)
    # for user in data
    for d in data[cp]:
        print(d)
        #get user id and situation(save in name field)
        fileName = "Data/"+str(data[cp][d]["subject"]["id"])+"_"+data[cp][d]["subject"]["name"]+".json"
        print(fileName)
        with open(fileName, 'w') as f:
            json.dump(data[cp][d], f)
