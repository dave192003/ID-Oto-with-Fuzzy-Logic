
from .membership import fuzzify
from .membership import triangular
from .memberships import (
    BRIGHTNESS,
    CONTRAST,
    SHARPNESS,
    NOISE,
)
from .output_membership import (
    ALPHA,
    BETA,
    SHARPEN,
    DENOISE,
)
from .rules import evaluate_rules
from .defuzzification import centroid_defuzzify

def fuzzy_logic(features):
    #  Fuzzification
    fuzzified = {
        "brightness": fuzzify(features["brightness"], BRIGHTNESS),
        "contrast": fuzzify(features["contrast"], CONTRAST),
        "sharpness": fuzzify(features["sharpness"], SHARPNESS),
        "noise": fuzzify(features["noise"], NOISE),
    }

    print(" FUZZIFICATION ", flush=True)
    for var_name, values in fuzzified.items():
        print(f"{var_name.capitalize()}: {values}", flush=True)

    # Rule Evaluation + Aggregation
    result = evaluate_rules(fuzzified)
    outputs = result["outputs"]
    fired_rules = result["fired_rules"]

    print("RULE OUTPUTS ", flush=True)
    for var_name, values in outputs.items():
        print(f"{var_name}: {values}", flush=True)

    print("FIRED RULES ", flush=True)
    for rule in fired_rules:
        print(f"Rule {rule['id']}: {rule['description']} (activation: {rule['activation']})", flush=True)

    # Defuzzification (centroid method)
    parameters = {
        "alpha": centroid_defuzzify(outputs["alpha"], ALPHA),
        "beta": centroid_defuzzify(outputs["beta"], BETA),
        "sharpen": centroid_defuzzify(outputs["sharpen"], SHARPEN),
        "denoise": centroid_defuzzify(outputs["denoise"], DENOISE),
    }

    print(" DEFUZZIFIED PARAMETERS ", flush=True)
    print(parameters, flush=True)

    return {
        "parameters": parameters,
        "fuzzified": fuzzified,
        "fired_rules": fired_rules,
        "outputs": outputs,
    }