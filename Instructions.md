# Instructions for using **extractPatchlets**

**extractPatchlets** takes a v1-compatible .vcv patch and splits it into multiple *patchlets*.<br/>

- When prompted, enter the name of the original patch.<br/>

- Do not include a .vcv extension.<br/>

- Include the full path of the .vcv file if it is different from the current working directory.<br/>

- There will be one patchlet for each row in the original patch.<br/>

- Each patchlet will contain all the modules in the corresponding row of the original patch.<br/>

- Any cables connecting modules in the same row will remain connected in the patchlet. Others will be discarded. <br/>

- Patchlets will be created in the current working directory.<br/>

- Patchlets will have the same name as the original patch, but with a suffix corresponding to the row in the original patch. <br/>

- The original patch will be unchanged.<br/>

- Example: If the original patch is named "X.vcv" and has 3 rows, then **extractPatchlets** will create 3 patchlets named "X_0.vcv", "X_1.vcv" and "X_2.vcv".<br/>


# Instructions for using **combinePatchlets**

**combinePatchlets** takes multiple v1-compatible patchlets and combines them to make a new patch. <br/>

- When prompted, enter the name of the new patch to be created. <br/>

- Do not include a .vcv extension.<br/>

- When prompted, enter the name of the patchlets to be combined. <br/>

- Include the full path if it is different from the current working directory.<br/>

- Do not include .vcv extensions.<br/>

- Hit [Enter] to finish entering patchlets.<br/>

- The patchlets will be comnbined into a single patch, one on each row of the new patch.<br/> 

- The new patch will be created in the current working directory. <br/>

- There will be no cable connections between rows, but cables connecting modules within each patchlet will remain connected.<br/>

- The same patchlet can be entered multiple times.<br/>

- Important: Do NOT enter more than one patchlet containing the *Core Audio-8 or Audio-16 modules*. VCV Rack will crash if you try to open the combined patch.


