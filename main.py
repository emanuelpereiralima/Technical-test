def ReadFile(fileName):
    file = open(fileName,"r")
    content = file.readlines()
    for i in range(len(content)):
      content[i] = content[i].replace("\n","").replace(".","")
      content[i] = content[i].split(' ')
    return content


def MoreThamOneLoot(loot):
  for list_itens in loot:
    value = " "
    for item in list_itens:
      if item.isdigit() == True:
        value += item
      if list_itens[1] == "a":
        list_itens = list_itens[2:]
    if value == " ":
      if list_itens not in keywords['Loot']:
        keywords['Loot'][(list_itens).strip()] = 1
      else:
        keywords['Loot'][list_itens.strip()] += 1
    else:
      list_itens = list_itens[3:]
      if list_itens not in keywords['Loot']:
        keywords['Loot'][list_itens.strip()] = int(value)
      else:
        keywords['Loot'][list_itens.strip()] += int(value)
        
  
def Output(keywords,output,len_output):
  if len_output == 0:
    return 1
  if len_output > 0:
    dict_list = list(keywords.values())
    print(output[len_output-1],dict_list[len_output-1],"\n")
    Output(keywords,output,len_output-1)
  

file = ReadFile("Server Log.txt")
output = ["Loot:","ExperienceGained:","ByCreatureKind:","DamageTaken:{\n Total:","HitpointsHealed:"]
keywords ={'Loot':{},'gained':0,'attack':{},'lose':0,'healed':0}
Unknown_count = 0

for phrase in file:
  temp_key = " "
  for word in phrase:
    if word in keywords.keys():
      temp_key = word
    if word.isdigit() == True and temp_key != " ":
      if temp_key != 'Loot' and temp_key != 'attack':
        keywords[temp_key] += int(word)
      if temp_key == 'lose' and 'attack' in phrase:
        if phrase[-2] not in keywords['attack']:
          keywords['attack'][phrase[-2].strip()] = int(word)
        else: 
          keywords['attack'][phrase[-2].strip()] += int(word)
      if temp_key == 'lose' and not 'attack' in phrase:
        Unknown_count += int(word)
      if temp_key == 'Loot' in phrase: 
        loot_name = " ".join(phrase[int(phrase.index(word) + 1):])
        if "," in loot_name:
          MoreThamOneLoot(loot_name.split(","))
          break
        if loot_name not in keywords['Loot']:
          keywords['Loot'][loot_name.strip()] = int(word)
        else: 
          keywords['Loot'][loot_name.strip()] += int(word)

Output(keywords,output,len(output))

print("Damage by Unknown Origins:",Unknown_count)