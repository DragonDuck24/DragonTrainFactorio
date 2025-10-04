# DragonTrain - Automatic Train Dispatching

This is the project used to generate [my vanilla factorio LTN-like train dispatching system](https://factorioprints.com/view/-OE226mKZZTaEnA5TplU).
This repo was created to create different variants of stations and trains for the system.
Because of the design of the system, it is not inherently flexible with the train layouts you are able to use, and requires some decent modification to the BP.
This project allows for one master BP, and generates all variants from it.
It creates any train layout, and a version with a red and green cable attachment to the network.

Although my [Factorio Prints blueprint](https://factorioprints.com/view/-OE226mKZZTaEnA5TplU) includes some default layouts, you may want more, that's what this repo is for.

## Usage
1. Install [Python](https://www.python.org/downloads/).
2. Create a Python venv with `python -m venv .venv`
3. Activate the venv with `.venv\Scripts\activate.bat` on Windows cmd or `source .venv/bin/activate` on bash
4. Set the desired variants at the top of [generate_variants.py](generate_variants.py).
5. Run `python generate_variants.py`.
6. Import the contents of `all-variants.txt` into factorio.



The project uses [factorio-draftsman](https://github.com/redruin1/factorio-draftsman), however due to the nature of the project and encountering issues with it, I had to a lot of manual blueprint editing.
