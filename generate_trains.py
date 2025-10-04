import json

from draftsman.classes.blueprint import Blueprint
from draftsman.classes.blueprint_book import BlueprintBook
from draftsman.signatures import SignalID, Icon
from draftsman.utils import Vector
from draftsman.prototypes.locomotive import Locomotive
from draftsman.entity import new_entity, locomotives, cargo_wagons

TRAIN_LEN = 7
WAGON_TYPES = ["cargo-wagon", "fluid-wagon"]

def create_train_bp(variant):
    bps = []

    for wagon_type in WAGON_TYPES:
        with open("train_schedule_bp.json", "r") as f:
            train_schedule_bp_string = f.read()


        type_letter = "I" if wagon_type == "cargo-wagon" else "F"
        train_schedule_bp_string = ((train_schedule_bp_string
                                    .replace("[TRAIN_NAME]", variant["name"]))
                                    .replace("[TRAIN_TYPE]", type_letter))

        train_schedule_bp = json.loads(train_schedule_bp_string)

        current_x_pos = 0

        for i in range(len(variant["layout"])):
            if variant["layout"][i] == "locomotive" or variant["layout"][i] == "locomotive-reversed":
                train_schedule_bp["blueprint"]["entities"].append(
                    {
                        "entity_number": i+1,
                        "name": "locomotive",
                        "position": {
                            "x": current_x_pos,
                            "y": 0
                        },
                        "enable_logistics_while_moving": False,
                        "orientation": 0.25 if variant["layout"][i] == "locomotive" else 0.75,
                        "color": {
                            "r": 0,
                            "g": 0,
                            "b": 0,
                            "a": 1
                        },
                        "items": [
                            {
                                "id": {
                                    "name": "rocket-fuel"
                                },
                                "items": {
                                    "in_inventory": [
                                        {
                                            "inventory": 1,
                                            "stack": 0,
                                            "count": 5
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                )

                train_schedule_bp["blueprint"]["schedules"][0]["locomotives"].append(i+1)

                stock_connections = {
                    "stock": i+1
                }
                if i > 0:
                    stock_connections["front"] = i
                if len(variant["layout"]) > i+2:
                    stock_connections["back"] = i+2

                train_schedule_bp["blueprint"]["stock_connections"].append(stock_connections)

            if variant["layout"][i] == "wagon":
                train_schedule_bp["blueprint"]["entities"].append(
                    {
                        "entity_number": i+1,
                        "name": wagon_type,
                        "position": {
                            "x": current_x_pos,
                            "y": 0
                        },
                        "enable_logistics_while_moving": False,
                        "orientation": 0.75
                    },
                )

            current_x_pos -= TRAIN_LEN

        train_schedule_bp["blueprint"]["label"] = variant["name"] + (" Item" if wagon_type == "cargo-wagon" else " Fluid") + " DragonTrain"
        train_schedule_bp["blueprint"]["icons"] = [
                  {
                    "signal": {
                      "name": "locomotive"
                    },
                    "index": 1
                  },
                  {
                    "signal": {
                      "name": wagon_type
                    },
                    "index": 2
                  },
                  {
                    "signal": {
                      "type": "virtual",
                      "name": variant["signal"]
                    },
                    "index": 3
                  }
                ]

        # train_bp = Blueprint()
        # train_bp.label = variant["name"] + " DragonTrain"
        # train_bp.icons = [Icon(index=0, signal=SignalID("locomotive")), Icon(index=1, signal=SignalID(wagon_type))]
        # train_bp_dict = train_bp.to_dict()
        bps.append(train_schedule_bp)

    return bps




    # bp = BlueprintBook()
    #
    # for variant in variants_to_create:
    #     variant_schedule_bp = train_schedule_bp.replace("[]")
    #     train_bp = Blueprint.from_dict(json.loads(variant_schedule_bp))
    #     train_bp.label = variant["name"]
    #
    #     current_x_pos = 0
    #     for stock in variant["layout"]:
    #         if stock == "locomotive":
    #             locomotive = new_entity("locomotive")
    #             train_bp.entities.append(locomotive)
    #         elif stock == "wagon":
    #             wagon = new_entity("cargo-wagon")
    #             train_bp.entities.append(wagon)
    #
    #     bp.blueprints.append(train_bp)

    with open("trains_bp.txt", "w") as f:
        f.write(bp.to_string())

