Factory Patter for DB

src/

 ├── domain/

 │    ├── models/

 │    │    └── user.py

 │    └── services/

 │         └── user_service.py

 │

 ├── application/

 │    ├── ports/

 │    │    └── db_port.py          # <-- Interface for DB operations <fetch,create,update,delete operation interface>

 │    └── use_cases/

 │         └── create_user_usecase.py

 │
 
 ├── infrastructure/

 │    ├── db/

 │    │    ├── factory/

 │    │    │    └── db_factory.py  # <-- Factory to get the right DB implementation <create and share correct DB instance. switch conditions>

 │    │    ├── base/

 │    │    │    └── db_instance.py # <-- Interface for DB config / base class <connect, get_session inteface>

 │    │    ├── implementations/

 │    │    │    └── pgsql.py       # <-- Concrete Postgres implementation <singelton instance for DB creation>

 │    │    └── config.py           # <-- Optional DB config loader

 │    └── logger/


 │         └── logger_adapter.py

 │
 └── presentation/

      └── api/

           └── routes/
           
                └── user_routes.py


[X]: DB Models Entities

[X] : DB_PORTS

[X]: DB_Factory

[X]: DB_Instance

[X]: implementation

    [X]: pgsql
    [X]: inMem