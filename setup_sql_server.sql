-- ============================================================
-- STEP 1: Create the database (run this first, alone)
-- ============================================================
CREATE DATABASE OI_Recorder;
GO

-- ============================================================
-- STEP 2: Switch to that database, then create the table
-- ============================================================
USE OI_Recorder;
GO

CREATE TABLE OI_Log (
    id              BIGINT IDENTITY(1,1) PRIMARY KEY,   -- auto row number
    log_time        DATETIME2 DEFAULT SYSDATETIME(),     -- when row was inserted (auto)
    ts_str          VARCHAR(20),                          -- your HH:MM:SS string
    spot            FLOAT,
    atm             FLOAT,
    ce_itm          FLOAT,
    ce_otm          FLOAT,
    tot_ce          FLOAT,
    pe_otm          FLOAT,
    pe_itm          FLOAT,
    tot_pe          FLOAT,
    pcr             FLOAT,
    net_bias        FLOAT,
    oi_imbalance    FLOAT,
    dce             FLOAT,
    dpe             FLOAT,
    dpcr            FLOAT,
    signal          VARCHAR(100),
    traded_val_5s   FLOAT,
    traded_val_pct  FLOAT,
    eq_traded_val_5s FLOAT,
    eq_traded_pct   FLOAT
);
GO

-- Index on ts_str so queries by time are fast later
CREATE INDEX idx_oi_log_time ON OI_Log (log_time);
GO

-- Quick test query to confirm it worked (should show 0 rows, no error)
SELECT TOP 10 * FROM OI_Log;
