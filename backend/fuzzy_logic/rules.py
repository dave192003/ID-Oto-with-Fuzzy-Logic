
RULES = [
    {
        "id": 1,
        "antecedents": [("brightness", "low")],
        "consequents": [("beta", "high")],
        "description": "IF Brightness is Low THEN Beta is High"
    },
    {
        "id": 2,
        "antecedents": [("brightness", "medium")],
        "consequents": [("beta", "normal")],
        "description": "IF Brightness is Medium THEN Beta is Normal"
    },
    {
        "id": 3,
        "antecedents": [("brightness", "high")],
        "consequents": [("beta", "low")],
        "description": "IF Brightness is High THEN Beta is Low"
    },
    {
        "id": 4,
        "antecedents": [("contrast", "low")],
        "consequents": [("alpha", "high")],
        "description": "IF Contrast is Low THEN Alpha is High"
    },
    {
        "id": 5,
        "antecedents": [("contrast", "medium")],
        "consequents": [("alpha", "normal")],
        "description": "IF Contrast is Medium THEN Alpha is Normal"
    },
    {
        "id": 6,
        "antecedents": [("contrast", "high")],
        "consequents": [("alpha", "low")],
        "description": "IF Contrast is High THEN Alpha is Low"
    },
    {
        "id": 7,
        "antecedents": [("sharpness", "low")],
        "consequents": [("sharpen", "high")],
        "description": "IF Sharpness is Low THEN Sharpen is High"
    },
    {
        "id": 8,
        "antecedents": [("sharpness", "medium")],
        "consequents": [("sharpen", "medium")],
        "description": "IF Sharpness is Medium THEN Sharpen is Medium"
    },
    {
        "id": 9,
        "antecedents": [("sharpness", "high")],
        "consequents": [("sharpen", "low")],
        "description": "IF Sharpness is High THEN Sharpen is Low"
    },
    {
        "id": 10,
        "antecedents": [("noise", "low")],
        "consequents": [("denoise", "low")],
        "description": "IF Noise is Low THEN Denoise is Low"
    },
    {
        "id": 11,
        "antecedents": [("noise", "medium")],
        "consequents": [("denoise", "medium")],
        "description": "IF Noise is Medium THEN Denoise is Medium"
    },
    {
        "id": 12,
        "antecedents": [("noise", "high")],
        "consequents": [("denoise", "high")],
        "description": "IF Noise is High THEN Denoise is High"
    },
    # Compound rules
    {
        "id": 13,
        "antecedents": [("brightness", "low"), ("contrast", "low")],
        "consequents": [("alpha", "high"), ("beta", "high")],
        "description": "IF Brightness is Low AND Contrast is Low THEN Alpha is High, Beta is High"
    },
    {
        "id": 14,
        "antecedents": [("brightness", "high"), ("contrast", "high")],
        "consequents": [("alpha", "low"), ("beta", "low")],
        "description": "IF Brightness is High AND Contrast is High THEN Alpha is Low, Beta is Low"
    },
    {
        "id": 15,
        "antecedents": [("sharpness", "low"), ("noise", "high")],
        "consequents": [("sharpen", "high"), ("denoise", "high")],
        "description": "IF Sharpness is Low AND Noise is High THEN Sharpen is High, Denoise is High"
    },
]


def evaluate_rules(fuzzified_inputs):
    # Initialize output accumulators
    outputs = {
        "alpha": {"low": 0.0, "normal": 0.0, "high": 0.0},
        "beta": {"low": 0.0, "normal": 0.0, "high": 0.0},
        "sharpen": {"low": 0.0, "medium": 0.0, "high": 0.0},
        "denoise": {"low": 0.0, "medium": 0.0, "high": 0.0},
    }

    fired_rules = []

    for rule in RULES:
        # Computing the rule activation strength 
        activation = 1.0
        for var_name, term in rule["antecedents"]:
            membership_value = fuzzified_inputs[var_name][term]
            activation = min(activation, membership_value)



        if activation > 0:
            fired_rules.append({
                "id": rule["id"],
                "description": rule["description"],
                "activation": round(activation, 4),
                "antecedents": rule["antecedents"],
                "consequents": rule["consequents"]
            })
            for output_var, output_term in rule["consequents"]:
                outputs[output_var][output_term] = max(
                    outputs[output_var][output_term],
                    activation
                )

    return {
        "outputs": outputs,
        "fired_rules": fired_rules
    }