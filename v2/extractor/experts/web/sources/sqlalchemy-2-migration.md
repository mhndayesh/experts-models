# SQLAlchemy 1.x to 2.0 Migration (API changes)

## Connection and transaction management
`engine.execute(statement)` is removed; use `with engine.connect() as conn: conn.execute(statement)`.
Implicit "connectionless" execution and library-level autocommit are removed; use explicit transactions via `Connection.begin()` or `with engine.begin() as conn:`.
`.execution_options(autocommit=True)` is removed; use explicit transactions.
Bound metadata is removed: `MetaData(bind=engine)` then `stmt.execute()` no longer works; call `conn.execute(stmt)` and pass the engine explicitly to `metadata.create_all(engine)`.
`Connection.execute()` no longer accepts keyword bind parameters like `conn.execute(stmt, x=10, y=5)`; pass a dict `conn.execute(stmt, {"x": 10, "y": 5})`.
`Connection.execute()` no longer accepts a raw string; wrap textual SQL in `text()`: `conn.execute(text("SELECT * FROM table"))`.
Positional bind parameters are no longer accepted; use named parameters in a dict.

## Core SQL construction
`select([col1, col2])` with a list is removed; pass columns positionally: `select(col1, col2)`.
The `whereclause`, `from_obj`, and `order_by` keyword arguments to `select()` are removed; use generative methods `.where()`, `.select_from()`, `.order_by()`.
`insert(table, values={...})` is removed; use `insert(table).values(x=10)`.
`table.update(whereclause)` is removed; use `table.update().where(...)`.
`table.delete(whereclause)` is removed; use `table.delete().where(...)`.
`case([(cond, value)])` with a list is removed; pass positional tuples: `case((cond, value))`.

## ORM configuration
`from sqlalchemy.ext.declarative import declarative_base` is moved to `from sqlalchemy.orm import declarative_base`.
`from sqlalchemy.orm import mapper; mapper(SomeClass, table)` is removed; use `registry().map_imperatively(SomeClass, table)`.

## ORM querying
`session.query(User)` (the Query API) is superseded by `session.execute(select(User))`.
`session.query(User).get(5)` is moved to `session.get(User, 5)`.
`session.query(User).all()` becomes `session.execute(select(User)).scalars().all()`.
Joining by string like `session.query(User).join("addresses")` is removed; use `select(User).join(User.addresses)`.
Results with joined eager loads are no longer automatically uniquified; call `.unique()` on the result before `.all()`.
Row objects: `"col_name" in row` now returns `False`; use `row._mapping` or attribute access `row.col_name`.

## Session transaction control
`Session(autocommit=True)` is removed; use explicit `session.commit()` or `with session.begin():`.
`session.begin(subtransactions=True)` is removed; subtransactions are no longer supported.

## Python version
The minimum required Python is 3.7; Python 2 support is removed.
