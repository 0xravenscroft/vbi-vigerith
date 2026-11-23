
import re

DIALECT = "https://json-schema.org/draft/2020-12/schema"
SUPPORTED_TYPES = {"object", "array", "string"}
SUPPORTED = {
    "$schema", "title", "description", "type", "required",
    "properties", "additionalProperties", "const", "enum",
    "minLength", "maxLength", "pattern", "format",
    "items", "uniqueItems",
}


def _walk_rules(rule: object, path: str) -> None:
    if not isinstance(rule, dict):
        raise ValueError(f"{path}: schema rule must be an object")

    unknown = set(rule) - SUPPORTED
    if unknown:
        raise NotImplementedError(
            f"{path}: unsupported schema keywords {sorted(unknown)}"
        )

    if "$schema" in rule and rule["$schema"] != DIALECT:
        raise ValueError(f"{path}: unsupported schema dialect")

    for field in ("title", "description"):
        if field in rule and not isinstance(rule[field], str):
            raise ValueError(f"{path}: {field} must be a string")

    if "type" in rule and (
        not isinstance(rule["type"], str)
        or rule["type"] not in SUPPORTED_TYPES
    ):
        raise NotImplementedError(f"{path}: unsupported schema type")

    if "required" in rule:
        names = rule["required"]
        if not isinstance(names, list) or any(
            not isinstance(name, str) for name in names
        ):
            raise ValueError(f"{path}: required must be a list of strings")
        if len(names) != len(set(names)):
            raise ValueError(f"{path}: required contains duplicate names")

    for field in ("minLength", "maxLength"):
        if field in rule and (
            type(rule[field]) is not int or rule[field] < 0
        ):
            raise ValueError(f"{path}: {field} must be a nonnegative integer")

    if "minLength" in rule and "maxLength" in rule:
        if rule["minLength"] > rule["maxLength"]:
            raise ValueError(f"{path}: minLength exceeds maxLength")

    if "pattern" in rule:
        if not isinstance(rule["pattern"], str):
            raise ValueError(f"{path}: pattern must be a string")
        try:
            re.compile(rule["pattern"])
        except re.error as exc:
            raise ValueError(f"{path}: invalid pattern") from exc

    if "format" in rule and rule["format"] != "date-time":
        raise NotImplementedError(f"{path}: unsupported format")

    if (
        "additionalProperties" in rule
        and rule["additionalProperties"] is not False
    ):
        raise NotImplementedError(
            f"{path}: additionalProperties must be false"
        )

    if "uniqueItems" in rule and type(rule["uniqueItems"]) is not bool:
        raise ValueError(f"{path}: uniqueItems must be a boolean")

    if "enum" in rule:
        values = rule["enum"]
        if not isinstance(values, list) or not values:
            raise ValueError(f"{path}: enum must be a nonempty list")
        if any(value in values[:index] for index, value in enumerate(values)):
            raise ValueError(f"{path}: enum contains duplicates")

    if "properties" in rule:
        properties = rule["properties"]
        if not isinstance(properties, dict):
            raise ValueError(f"{path}: properties must be an object")
        for name, child in properties.items():
            if not isinstance(name, str):
                raise ValueError(f"{path}: property names must be strings")
            _walk_rules(child, f"{path}.properties.{name}")

    if "items" in rule:
        _walk_rules(rule["items"], f"{path}.items")


def validate_schema_contract(schema: object) -> None:
    if not isinstance(schema, dict):
        raise ValueError("Schema root must be an object")
    if schema.get("$schema") != DIALECT:
        raise ValueError("Unsupported schema dialect")
    if schema.get("type") != "object":
        raise ValueError("Event root must declare type object")
    _walk_rules(schema, "$")
