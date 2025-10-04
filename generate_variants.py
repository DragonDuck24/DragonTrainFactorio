import json

from draftsman import utils
from draftsman.blueprintable import BlueprintBook
from draftsman.classes.blueprint import Blueprint
from draftsman.signatures import Icon, SignalID

from generate_trains import create_train_bp
from switch_circuit_colors import switch_blueprint, swap_colors_in_description


# name: name of that type of train and station.
# wagons: number of wagons the train has.
# default_item_request: the default pre-populated value for item requests in bp parameterization. I recommend 4000*(number of wagons).
# default_fluid_request: the default pre-populated value for fluid requests in bp parameterization. I recommend 50000*(number of wagons).
# signal: the signal icon used in the train blueprints
# icons: the icons to use for the variant bp books
# layout options: locomotive, wagon, locomotive-reversed
# use locomotive_reversed to create a double-headed train
variants_to_create = [
    {
        "name": "1-1",
        "wagons": "1",
        "default_item_request": "4000",
        "default_fluid_request": "50000",
        "signal": "signal-1",
        "icons": [Icon(index=0, signal=SignalID("locomotive")), Icon(index=1, signal=SignalID("cargo-wagon")), Icon(index=2, signal=SignalID("signal-1"))],
        "layout": ["locomotive", "wagon"]
    },
    {
        "name": "1-2",
        "wagons": "2",
        "default_item_request": "8000",
        "default_fluid_request": "100000",
        "signal": "signal-2",
        "icons": [Icon(index=0, signal=SignalID("locomotive")), Icon(index=1, signal=SignalID("cargo-wagon")), Icon(index=2, signal=SignalID("signal-2"))],
        "layout": ["locomotive", "wagon", "wagon"]
    },
    {
        "name": "1-4",
        "wagons": "4",
        "default_item_request": "16000",
        "default_fluid_request": "200000",
        "signal": "signal-4",
        "icons": [Icon(index=0, signal=SignalID("locomotive")), Icon(index=1, signal=SignalID("cargo-wagon")), Icon(index=2, signal=SignalID("signal-4"))],
        "layout": ["locomotive", "wagon", "wagon", "wagon", "wagon"]
    },
    {
        "name": "1-1-1",
        "wagons": "1",
        "default_item_request": "4000",
        "default_fluid_request": "50000",
        "signal": "signal-D",
        "icons": [Icon(index=0, signal=SignalID("locomotive")), Icon(index=1, signal=SignalID("cargo-wagon")), Icon(index=2, signal=SignalID("signal-D"))],
        "layout": ["locomotive", "wagon", "locomotive-reversed"]
    },
]

# DO NOT MODIFY
# Sets the pre-existing names to find and replace in my BPs
starting_variant = {
    "name": "[TRAIN_NAME]",
    "wagons": "[WAGON_AMOUNT]",
    "default_item_request": "4189",
    "default_fluid_request": "49162",
    "color": "Red",
    "alt_color": "Green",
    "layout": ["locomotive", "wagon"]
}


def generate_variants(bp: str) -> dict:



    first_bp_book = BlueprintBook()
    first_bp_book.label = starting_variant["color"]
    first_bp_book.description = "DragonTrain station variants where the " + starting_variant["color"].lower() + " circuit wire is used to set requests on the network."
    first_bp_book.icons = [Icon(index=0, signal=SignalID(starting_variant["color"].lower() + "-wire"))]


    for variant in variants_to_create:
        variant_bp = BlueprintBook.from_dict(json.loads(bp.replace(starting_variant["name"], variant["name"])
                                                        .replace(starting_variant["wagons"], variant["wagons"])
                                                        .replace(starting_variant["default_item_request"], variant["default_item_request"])
                                                        .replace(starting_variant["default_fluid_request"], variant["default_fluid_request"])))
        variant_bp.icons = variant["icons"]
        first_bp_book.blueprints.append(variant_bp)
        # first_bp_book.blueprints.append(create_train_bp(variant, "cargo-wagon")) # Issues adding interrupts to bps, removing for now
        # first_bp_book.blueprints.append(create_train_bp(variant, "fluid-wagon"))

    converted_book = first_bp_book.to_dict()
    switch_blueprint(converted_book)
    swap_colors_in_description(converted_book)

    second_bp_book = BlueprintBook.from_dict(converted_book)
    second_bp_book.label = starting_variant["alt_color"]
    second_bp_book.description = "DragonTrain station variants where the " + starting_variant["alt_color"].lower() + " circuit wire is used to set requests on the network."
    second_bp_book.icons = [Icon(index=0, signal=SignalID(starting_variant["alt_color"].lower() + "-wire"))]


    variant_bp_book = BlueprintBook()
    variant_bp_book.label = "DragonTrain Variants"
    variant_bp_book.icons = [Icon(index=0, signal=SignalID("train-stop"))]
    variant_bp_book.blueprints.append(first_bp_book)
    variant_bp_book.blueprints.append(second_bp_book)

    train_bp_book = BlueprintBook()
    train_bp_book.label = "DragonTrains"
    train_bp_book.icons = [Icon(index=0, signal=SignalID("locomotive"))]
    train_bp_book.description = "There should be a train for every station type loaded in this blueprint. They request some rocket fuel to get to the depot, but can use coal, solid fuel, rocket fuel, and nuclear fuel to run, just create any refueler."


    main_bp_book = BlueprintBook()
    main_bp_book.label = "DragonTrain - Automatic Train Dispatching"
    main_bp_book.description = "Automatically provide and request items by train, in vanilla!\n\nSee https://factorioprints.com/view/-OE226mKZZTaEnA5TplU for usage instructions\nLast updated Oct 3, 2025"
    main_bp_book.icons = [Icon(index=0, signal=SignalID("locomotive")), Icon(index=1, signal=SignalID("passive-provider-chest")), Icon(index=2, signal=SignalID("requester-chest"))]
    main_bp_book.blueprints.append(variant_bp_book)
    with open ("rail_book_bp.txt", "r") as f:
        main_bp_book.blueprints.append(BlueprintBook.from_string(f.read()))
    main_bp_book.blueprints.append(train_bp_book)
    with open ("global_clock_bp.txt", "r") as f:
        main_bp_book.blueprints.append(Blueprint.from_string(f.read()))

    train_bps = []
    for variant in variants_to_create:
        for train in create_train_bp(variant):
            train_bps.append(train)


    main_dict = main_bp_book.to_dict()
    main_dict["blueprint_book"]["blueprints"][2]["blueprint_book"]["blueprints"] = train_bps

    return main_dict

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate variants for my DragonTrain blueprint")
    parser.add_argument("--output", help="Output filename (will be blueprint string or JSON)", default="all-variants.txt")
    parser.add_argument("--as-json", action="store_true", help="Treat input/output as raw JSON rather than string format")

    args = parser.parse_args()


    with open("station_bp.json", "r") as f:
        bp = json.load(f)

    string_bp = json.dumps(bp, separators=(",", ":"))

    print("Creating variants with names:")
    for variant in variants_to_create:
        print(variant["name"])
    print("\nFrom station_bp.json")

    generated = generate_variants(string_bp)


    if args.as_json:
        with open(args.output, "w") as f:
            json.dump(generated, f, separators=(",", ":"))

        print("Wrote JSON to", args.output)
    else:

        with open(args.output, "w") as f:
            f.write(utils.JSON_to_string(generated))
        print("Wrote blueprint string to", args.output)


