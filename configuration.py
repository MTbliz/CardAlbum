import tomlkit


class DevConfig:

    with open("config.toml", "r", encoding="utf-8") as f:
        config = tomlkit.load(f)

    # local computer dev
    db_host = config["DATABASE"].get("host", None)
    port = config["DATABASE"].get("port", None)

    #docker dev
    #db_host = "postgres"
    #port = "5432"
    db_database = config["DATABASE"].get("database", None)
    db_user = config["DATABASE"].get("user", None)
    db_password = config["DATABASE"].get("password", None)

    #SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_password}@{db_host}:{port}/{db_database}"
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SECRET_KEY = config["SECRETS"].get("secret_key", None)


class ProdConfig:
    pass