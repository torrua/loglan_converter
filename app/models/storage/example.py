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

    storage.word.append(
        ["13", "D-Prim", "Predicate", "", "", "JCB", "1991", "10+", "cervu", "", "", ""]
    )

    from pprint import pprint

    pprint(storage)
