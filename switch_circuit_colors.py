import json
from draftsman.blueprintable import Blueprint, BlueprintBook
from draftsman.data.entities import arithmetic_combinators
from draftsman.validators import ValidationMode
# from draftsman import prototypes
from draftsman import utils


def swap_colors_in_description(bp):
    if isinstance(bp, dict):
        for k, v in bp.items():
            if (k == "description" or k == "player_description") and isinstance(v, str):
                # temporary placeholder to avoid immediate overwriting
                swapped = v.replace("red", "__TEMP__").replace("green", "red").replace("__TEMP__", "green")
                bp[k] = swapped
                # print(swapped)
            elif isinstance(bp[k], dict) or isinstance(bp[k], list):
                swap_colors_in_description(bp[k])
    elif isinstance(bp, list):
        for i in range(len(bp)):
            swap_colors_in_description(bp[i])




def switch_blueprint(bp: dict):
    for key in bp.keys():
        if key == "blueprint_book":
            for i in range(len(bp["blueprint_book"]["blueprints"])):
                switch_blueprint(bp["blueprint_book"]["blueprints"][i])
        elif key == "blueprint":
            switch_wires(bp["blueprint"]["wires"])
            for e in bp["blueprint"]["entities"]:
                if e["name"] == "arithmetic-combinator":
                    switch_conditions(e["control_behavior"]["arithmetic_conditions"])
                elif e["name"] == "decider-combinator":
                    for condition in e["control_behavior"]["decider_conditions"]["conditions"]:
                        switch_conditions(condition)
                    for output in e["control_behavior"]["decider_conditions"]["outputs"]:
                        if output.keys().__contains__("networks"):
                            switch_signal_networks(output["networks"])
                        else:
                            # default is both true. If it doesn't exist, switch to both false
                            output["networks"] = { "red": False, "green": False }






def switch_wires(wires: dict):

    for wire in wires:
        first = wire[1]

        if first == 1:
            wire[1] = 2
        elif first == 2:
            wire[1] = 1
        elif first == 3:
            wire[1] = 4
        elif first == 4:
            wire[1] = 3

        second = wire[3]

        if second == 1:
            wire[3] = 2
        elif second == 2:
            wire[3] = 1
        elif second == 3:
            wire[3] = 4
        elif second == 4:
            wire[3] = 3



def switch_signal_networks(signal_networks: dict):

    if signal_networks.keys().__contains__("red"):
        red = signal_networks["red"]
    else:
        red = True
    if signal_networks.keys().__contains__("green"):
        green = signal_networks["green"]
    else:
        green = True

    signal_networks["red"] = green
    signal_networks["green"] = red

def switch_conditions(bp: dict):

    if bp.keys().__contains__("first_signal_networks"):
        switch_signal_networks(bp["first_signal_networks"])
    else:
        # default is both true. If it doesn't exist, switch to both false
        bp["first_signal_networks"] = { "red": False, "green": False }
    if bp.keys().__contains__("second_signal_networks"):
        switch_signal_networks(bp["second_signal_networks"])
    else:
        # default is both true. If it doesn't exist, switch to both false
        bp["second_signal_networks"] = { "red": False, "green": False }





if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Swap red/green wires in a Factorio blueprint (v2.0)")
    parser.add_argument("input", help="Input blueprint/book string or JSON file")
    parser.add_argument("output", help="Output filename (will be blueprint string or JSON)")
    parser.add_argument("--as-json", action="store_true", help="Treat input/output as raw JSON rather than string format")

    args = parser.parse_args()

    if args.as_json:

        with open(args.input, "r") as f:
            bp = json.load(f)

        switch_blueprint(bp)
        swap_colors_in_description(bp)

        with open(args.output, "w") as f:
            json.dump(bp, f, separators=(",", ":"))
        print("Wrote JSON to", args.output)
    else:
        # read blueprint string or text file containing it
        with open(args.input, "r") as f:
            bp = utils.string_to_JSON(f.read())
            print(bp)

        switch_blueprint(bp)
        swap_colors_in_description(bp)

        with open(args.output, "w") as f:
            f.write(utils.JSON_to_string(bp))
        print("Wrote blueprint string to", args.output)