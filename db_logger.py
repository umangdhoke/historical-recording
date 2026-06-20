"""
db_logger.py — drop this file in the same folder as oi_recorder_pro_equity.py

Handles all SQL Server saving. If SQL Server is down or slow, it will NOT
crash or freeze your recorder — it just prints a warning and skips that row.
"""

import pyodbc

# ── EDIT THIS to match your SQL Server setup ───────────────────────────────
SQL_CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"   # change if your server name is different
    "DATABASE=OI_Recorder;"
    "Trusted_Connection=yes;"          # uses your Windows login, no password needed
)

INSERT_SQL = """
INSERT INTO OI_Log (
    ts_str, spot, atm, ce_itm, ce_otm, tot_ce, pe_otm, pe_itm, tot_pe,
    pcr, net_bias, oi_imbalance, dce, dpe, dpcr, signal,
    traded_val_5s, traded_val_pct, eq_traded_val_5s, eq_traded_pct
) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
"""

_conn = None
_cursor = None


def connect():
    """Call this ONCE when your script starts."""
    global _conn, _cursor
    try:
        _conn = pyodbc.connect(SQL_CONN_STR, autocommit=True, timeout=5)
        _cursor = _conn.cursor()
        print("  [SQL] Connected to SQL Server OK")
        return True
    except Exception as e:
        print(f"  [SQL] Could NOT connect: {e}")
        print("  [SQL] Recorder will continue WITHOUT SQL logging.")
        _conn = None
        return False


def insert_row(ts_str, m):
    """
    Call this once per 5-second cycle, passing the same ts_str and the
    'm' dict (metrics) you already compute in your main loop.
    """
    if _cursor is None:
        return  # SQL not connected — silently skip, recorder keeps running

    try:
        _cursor.execute(INSERT_SQL, (
            ts_str,
            m["spot"], m["atm"],
            m["ce_itm"], m["ce_otm"], m["tot_ce"],
            m["pe_otm"], m["pe_itm"], m["tot_pe"],
            m["pcr"], m["net_bias"], m["oi_imbalance"],
            m["dce"], m["dpe"], m["dpcr"],
            m["signal"],
            m["traded_val_5s"], m["traded_val_pct"],
            m["eq_traded_val_5s"], m["eq_traded_pct"],
        ))
    except Exception as e:
        print(f"\n  [SQL] Insert failed: {e}")


def close():
    """Call this once when your script shuts down (Ctrl+C)."""
    if _conn is not None:
        try:
            _conn.close()
            print("  [SQL] Connection closed cleanly")
        except Exception:
            pass
