# pylint: disable=missing-module-docstring, missing-class-docstring, missing-function-docstring

from app.models.storage.storage import Storage

if __name__ == "__main__":
    storage = Storage()
    print(storage.names)

    storage.event.append(
        [
            "6",
            "Torrua Dictionary Repair",
            "05/25/2019",
            "Repair of the dictionary by Torrua and Peter Hill",
            "Torrua Repair",
            "TDR",
        ]
    )

    item = ["13", "D-Prim", "Predicate", "", "", "JCB", "1991", "10", "cervu", "", "", ""]
    prepared_item = storage.word.convert_item_elements(item)

    for a, b in zip(storage.word.pattern, prepared_item):
        print(a, b)
    print(storage.word.is_proper_pattern(prepared_item))
