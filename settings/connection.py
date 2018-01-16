from db_connection.connection import get_session

sber_conn = get_session(
    'oracle+cx_oracle://sberbank_sys:1234@localhost:1521/ORCL')

forex_conn = get_session(
    'oracle+cx_oracle://forex_sys:1234@localhost:1521/ORCL')

alpha_conn = get_session(
    'oracle+cx_oracle://alpha_bank_sys:1234@localhost:1521/ORCL')

connection_dict = {
    '3': sber_conn,
    '4': forex_conn,
    '5': alpha_conn
}
