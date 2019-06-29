import random
import os

print('')   
print("Current working directory is: " + os.getcwd())
print('') 

#os.chdir(path)

## Get name of new combined patch
fname = input("What is name of the new combined patch? ") 
print('') 

# Get names and contents of patchlets to combine
print("Input names of patchlets to combine (leave off '.vcv')")
print("Put all patchlets in the current directory or add the full path")
print("Hit [Enter] to finish")
print("")  

done = 0
pl = 0
patchlets = []
while done==0:   
    temp = input("Name of patchlet #" + str(pl+1) + " ")
    if temp=="": 
        done = 1
    else: 
        if os.path.exists(temp+".vcv"):
            patchlets.append(temp)        
            pl = pl + 1
        else:
            print("Error: file not found")

      
newPatch = []; newModules = []; newCables = []; modIdMap = []

# Loop through patchlets, adding modules to new module block and cables to new cable block
for k in range(0,len(patchlets)):   
    
    print(patchlets[k] + '.vcv')    
    
    # Read contents of patchlet
    f = open(patchlets[k] + '.vcv')
    A = []
    for line in f:
        A.append(line)
    f.close()       
    
    # Create the first 3 lines of a new patch ("{","version: #.#.#", "modules: ["})
    if k==0: 
        newPatch.append(A[0]) 
        newPatch.append(A[1])
        newPatch.append(A[2])
    
    # Extract the module block (moduleBlock)   
    openBracket = -99
    for i in range(0,len(A)):       
        if ('"modules":' in A[i]):
            moduleBlockStart = i+1
            openBracket = 1
        else:
            if ('[' in A[i]): openBracket = openBracket + 1                    
            if (']' in A[i]): openBracket = openBracket - 1   
        if openBracket==0:
            moduleBlockEnd = i
            openBracket=99
    moduleBlock = A[moduleBlockStart:moduleBlockEnd]    
    
    # Change the row to the patchlet number
    # Change the module id to a random number
    for i in range(0,len(moduleBlock)):  
        if (moduleBlock[i][:14] == '      "pos": ['):
            moduleBlock[i+2] = '        '+str(k)
        if (moduleBlock[i][:11]== '      "id":'):            
            temp = moduleBlock[i][12:]; temp = temp.split(","); idnum = int(temp[0])                        
            temp = random.randint(1,65536)
            moduleBlock[i] = ('      "id": ' + str(temp)+',\n')            
            modIdMap.append((idnum,temp,k))
                
    # Ensure that all the modules end with a comma
    if len(moduleBlock)>0:
        moduleBlock[-1] = '    },\n'      
        
    # Extract the cable block   
    openBracket = -99
    for i in range(moduleBlockEnd+1,len(A)):       
        if ('"cables":' in A[i]):
            cableBlockStart = i+1
            openBracket = 1
        else:
            if ('[' in A[i]): openBracket = openBracket + 1                    
            if (']' in A[i]): openBracket = openBracket - 1   
        if openBracket==0:
            cableBlockEnd = i
            openBracket=99
    cableBlock = A[cableBlockStart:cableBlockEnd]     
    
    # Ensure that all the cables end with a comma
    if len(cableBlock)>0:
        cableBlock[-1] = '    },\n'
    
    # Add this module block to newModules       
    for i in range(0,len(moduleBlock)):
        newModules.append(moduleBlock[i])
    
    # Add this cable block to newCables
    for i in range(0,len(cableBlock)):
        newCables.append(cableBlock[i])
       
# Ensure that there is no comma at the end of the new module and cable blocks
newModules[-1] = '    }\n'
if len(newCables)>0: 
    newCables[-1]  = '    }\n'

# Close module block with bracket and comma
newModules.append('  ],\n')              

# Close cable block with bracket (no comma)
newCables.append('  ]\n')
   
# Add the new module block to the new patch
for i in range(0,len(newModules)):
    newPatch.append(newModules[i])

# Add the new cable block to the new patch
newPatch.append('  "cables": [\n')       
for i in range(0,len(newCables)):
    newPatch.append(newCables[i])

# Close patch with brace    
newPatch.append('}\n')

    
# change the module ids in the cables to match the random module ids   
id = []    
for i in range(0,len(newPatch)):      
    if (newPatch[i][:11]== '      "id":'):
        temp = newPatch[i][12:]; temp = temp.split(","); 
        id.append(int(temp[0]))
for i in range(0,len(newPatch)): 
    if (newPatch[i][:22]== '      "rightModuleId":'):        
        #print("in  " + newPatch[i])
        temp = newPatch[i][23:]; temp = temp.split(","); idnum = int(temp[0])
        for j in range(0,len(modIdMap)):
            if modIdMap[j][0]==idnum: 
                newPatch[i] = ('      "rightModuleId" :'+ str(modIdMap[j][1]) + ',\n')                
                #print(str(modIdMap[j][0])+" "+str(modIdMap[j][1]))        
        #print(idnum)
        #print("out " + newPatch[i])        
    if (newPatch[i][:21]== '      "leftModuleId":'):    
        temp = newPatch[i][22:]; temp = temp.split(","); idnum = int(temp[0])         
        for j in range(0,len(modIdMap)):
            if modIdMap[j][0]==idnum: 
                newPatch[i] = ('      "leftModuleId": '+ str(modIdMap[j][1]) + ',\n')
    if (newPatch[i][:23]== '      "outputModuleId":'):    
        temp = newPatch[i][24:]; temp = temp.split(","); idnum = int(temp[0])        
        for j in range(0,len(modIdMap)):
            if modIdMap[j][0]==idnum: 
                newPatch[i] = ('      "outputModuleId": '+ str(modIdMap[j][1]) + ',\n')
    if (newPatch[i][:22]== '      "inputModuleId":'):        
        temp = newPatch[i][23:]; temp = temp.split(","); idnum = int(temp[0])        
        for j in range(0,len(modIdMap)):
            if modIdMap[j][0]==idnum: 
                newPatch[i] = ('      "inputModuleId": '+ str(modIdMap[j][1]) + ',\n')
     
        '      "rightModuleId": 269,'
        
# Write new patch to file    
f = open(fname+'.vcv','w')
for j in range(0,len(newPatch)):
    f.write(newPatch[j])
f.close()      
print("")   
print(fname + '.vcv created')
print("")   
print('Merge Completed')
    
# latest problem: when combining multiple copies of the same patch, the cables and left/right modules are messed up


