# Patchlets (Beta 0.5)

## Tools for extracting and manipulating patchlets from VCV Rack patches.

When using VCV Rack, I have sometimes wished that there was a way to copy some large combination of modules from another patch into the current patch I'm working on. Maybe I made a complicated LFO / sample&hold / quantized / transposed melody generator in another patch, and I'd like to use that in my current patch but don't want to bother building it again from scratch. Or maybe I have a complex, multi-module synth voice that I'd like to duplicate four times (assuming polyphony is not an option in this case).

The idea of **Patchlets** is to organize patches in rows, each row corresponding to some collection of modules and connected cables that could be repurposed in some other patch. A collection of patchlets can be like a toolbox of go-to solutions that can be combined in different ways to form new patches.

I've found these tools helpful for my Rack workflow and I hope some others may also benefit from them.

Currently Patchlets is implemented as two different python scripts:

- **extractPatchlets.py** takes a v1-compatible .vcv patch and splits it into multiple *patchlets*.

- **combinePatchlets.py** takes multiple v1-compatible patchlets and combines them to make a new patch. 

These python scripts can be run from any python environment, but standalone .exe files can easily be created with pyinstaller. The only packages they use are *os*, *random* and *re*. I've tested it on both MacOs and Windows, but not Linux. 

**Read the [Instructions](https://github.com/millxing/Patchlets/blob/master/Instructions.md) before using.**

### Plans for this project

- Clean up the code: I'm not an experienced python programmer. This is my first python project and I've been learning as I worked on it. The code is well-commented but does not follow standard python norms. The code can be made much more efficient, but it seems to work fine for these tasks. I do plan to improve the quality of the code.

- Testing: I've tested these scripts a bunch of times, but I'm sure I've missed some combination of conditions that could make these scripts fail.

- Add more tools: The logical one to add next would be **appendPatchlet**, so you could just add a patchlet to the bottom of an existing patch. Currently you can do the same thing by splitting the existing patch into patchlets with **extractPatchlets** and then recombining the patchlets and adding the new one with **combinePatchlets**.

- GUI: I've been playing with making a gui and a file browser dialog using Tkinter.

- Executables: I have standalone .exe versions available and will add them to this repository shortly.

- Known bugs: Crashes when two patchlets with Core Audio are combined.

- Partnership: If anyone wants to help with any of this, just let me know.
