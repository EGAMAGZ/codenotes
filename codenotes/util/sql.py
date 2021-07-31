def add_conditions_sql(sql: str, condition: str, type_condition: str = None) -> str:
    """Adds where conditions to sql

    Parameters
    ----------
    sql : str
        SQL string that will be added the condition
    condition : str
        Condition added to SQL
    type_condition : str
        If 'WHERE' exists, will add the type of condition (AND/OR)

    Returns
    -------
    sql : str
        Returns the same SQL passed with the condition
    """
    if "where" in sql.lower():
        sql = sql + f" {type_condition} {condition}"
    else:
        sql = sql + f" WHERE {condition}"
    return sql
