import os


TORTOISE_ORM = {
    "connections": {"default": "mysql://ikryty:ikryty123@localhost:3306/dbikryty"},
    #"connections": {"default": "mysql://civildefense:r8AbuAbu@147.229.177.177:3306/dbikryty"},
    "apps": {
        "models": {
            "models": [
                "src.database.models"
            ],
            "default_connection": "default"
        }
    }
}
