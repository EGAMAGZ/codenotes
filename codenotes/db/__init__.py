def add_conditions_sql(sql: str, condition: str, type_condition: str = None) -> str:
    if 'where' in sql.lower():
        sql = sql + f' {type_condition} {condition}'
    else:
        sql = sql + f' WHERE {condition}'
    return sql
