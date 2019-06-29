import re
import os

print('')   
print("Current working directory is: " + os.getcwd())
print('') 
print('') 
print('Which .vcv file would you like to create patchlets from?')
fname = input("? ")
print("")

# Read contents of patch
f = open(fname + '.vcv')
A = []
for line in f:
    A.append(line)
f.close()
original = A

# Extract the version of Rack (rackVersion)
temp = re.findall(r'\"(.+?)\"',A[1])
rackVersion = temp[1];

# Extract the module block (moduleBlock)   
openBracket = -99
for i in range(0,len(A)):       
    if (A[i]== '  "modules": [\n'):
        moduleBlockStart = i+1
        openBracket = 1
    else:
        if ('[' in A[i]): openBracket = openBracket + 1                    
        if (']' in A[i]): openBracket = openBracket - 1   
    if openBracket==0:
        moduleBlockEnd = i
        openBracket=99
moduleBlock = A[moduleBlockStart:moduleBlockEnd]        
            
# Extract the cable block (cableBlock)   
openBracket = -99
for i in range(moduleBlockEnd+1,len(A)):       
    if (A[i]== '  "cables": [\n'):
        cableBlockStart = i+1
        openBracket = 1
    else:
        if ('[' in A[i]): openBracket = openBracket + 1                    
        if (']' in A[i]): openBracket = openBracket - 1   
    if openBracket==0:
        cableBlockEnd = i
        openBracket=99
cableBlock = A[cableBlockStart:cableBlockEnd]     

# Create list of all the modules
modules = []; numModules = 0; openbracket = 0
for i in range(0,len(moduleBlock)):         
    if ('{' in moduleBlock[i]):
        if openbracket==0: cc = []
        openbracket = openbracket + 1        
    if openbracket>0:                
        cc.append(moduleBlock[i])      
    if ('}' in moduleBlock[i]): openbracket = openbracket - 1               
    if openbracket == 0:        
        numModules = numModules + 1
        modules.append(cc)
                         
# Create list of all the cables
cables = []; opencable = 0; numCables = 0
for i in range(0,len(cableBlock)):        
    if (cableBlock[i]== '    {\n'):        
        opencable = 1  
        cc = []
    if opencable == 1:                
        cc.append(cableBlock[i])    
    if ('    }' in cableBlock[i]):                
        opencable = 0        
        numCables = numCables + 1
        cables.append(cc)

# Create list of all module IDs, module rows, module columns
col = []; row = []; rowrow = []; colrow = []; id = []   
for i in range(0,numModules):     
    A = modules[i]
    for j in range(0,len(A)):         
        if (A[j][:11] == '      "id":'):            
            temp = re.findall(r'\d',A[j])
            temp = int("".join(list(map(str,temp))))
            id.append(temp)                     
        if A[j][:14] == '      "pos": [':
            temp = re.findall(r'\d',A[j+1])
            temp1 = int("".join(list(map(str,temp))))
            temp = re.findall(r'\d',A[j+2])
            temp2 = int("".join(list(map(str,temp))))
            col.append(temp1)            
            row.append(temp2)
            colrow.append(j+1) 
            rowrow.append(j+2)                                        
           
# Create list of all cable inputs and outputs
outMod = []; inMod = []; outId = []; inId = []       
for i in range(0,numCables):     
    A = cables[i]
    for j in range(0,len(A)):         
        if (('outputModuleId') in A[j]):            
            temp = re.findall(r'\d',A[j])
            temp = int("".join(list(map(str,temp))))
            outMod.append(temp)
        if (('inputModuleId') in A[j]):            
            temp = re.findall(r'\d',A[j])
            temp = int("".join(list(map(str,temp))))
            inMod.append(temp)
        if (('outputId') in A[j]):            
            temp = re.findall(r'\d',A[j])
            temp = int("".join(list(map(str,temp))))
            outId.append(temp)    
        if (('inputId') in A[j]):            
            temp = re.findall(r'\d',A[j])
            temp = int("".join(list(map(str,temp))))
            inId.append(temp)

# Create patchlets        
for k in range(0,max(row)+1):
    
    # Create the first 3 lines of a new patchlet ("{","version: #.#.#", "modules: ["})
    new_file = original[0:3]      
    
    # Find leftmost x-coordinate in the row
    mincol = 9999
    for u in range(0,len(modules)):
        if (row[u]==k):
            if col[u]<mincol: mincol = col[u]
    
    # Create new module block
    #   Change row to row 0
    #   Change x-coordinates so leftmost module is at 0
    new_modules = []
    for u in range(0,len(modules)):
        if (row[u]==k):
            modules[u][rowrow[u]] = "        "+str(0)+"\n"  
            modules[u][colrow[u]] = "        "+str(col[u]-mincol)+",\n" 
            new_modules.append(modules[u])    

    new_modules[-1][-1] =  '    }\n'       
    
    new_cables = []   
    # Create new cable block
    #   Add cables to new cable block only if they only connect to modules on this row
    for u in range(0,len(cables)):
        inx = -99; outx = -99; 
        for j in range(0,len(modules)):
            if inMod[u]==id[j]: inx = row[j]; 
            if outMod[u]==id[j]: outx = row[j]; 
        if inx==outx==k:
            new_cables.append(cables[u])  
    
    if len(new_cables)>0:       
        new_cables[-1][-1] =  '    }\n'   
        
    # Add module block to new patchlet 
    for u in range(0,len(new_modules)):
        for j in range(0,len(new_modules[u])):
            new_file.append(new_modules[u][j])                     
    # Close module block with bracket and comma
    new_file.append('  ],\n')  
           
    # Open cable block
    new_file.append('"cables": [\n')       
    for u in range(0,len(new_cables)):        
        for j in range(0,len(new_cables[u])):        
            new_file.append(new_cables[u][j])    
               
    # Close cable block with bracket (no comma)
    new_file.append(' ]\n')
        
    # Close patch with brace
    new_file.append('}\n')
         
    # Save each new patchlet
    plet_name = fname + "_" + str(k+1) + '.vcv'
    f = open(plet_name,'w')
    for j in range(0,len(new_file)):
        f.write(new_file[j])
    f.close()    
    print('Row ' + str(k+1) + " -> " + plet_name)              
            
print('Extraction Completed')           
            
            
            
            
                                
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        