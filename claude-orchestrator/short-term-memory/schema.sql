-- Claude Orchestrator Short-term Memory Schema
-- SQLite database for session state management

-- Session state for continuity
CREATE TABLE IF NOT EXISTS session_state (
    session_id TEXT PRIMARY KEY,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    current_task TEXT,
    task_context TEXT,  -- Why we're doing it
    workflow TEXT,      -- Active workflow name
    context_tokens INTEGER DEFAULT 0,
    status TEXT DEFAULT 'active'  -- active, ended, crashed
);

-- Decisions made (audit trail)
CREATE TABLE IF NOT EXISTS decisions (
    decision_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    what_was_decided TEXT NOT NULL,
    reason TEXT,
    approved_by_user BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (session_id) REFERENCES session_state(session_id)
);

-- Issues/problems encountered
CREATE TABLE IF NOT EXISTS issues (
    issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    issue_description TEXT NOT NULL,
    resolution_attempted TEXT,
    resolved BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (session_id) REFERENCES session_state(session_id)
);

-- Checkpoints for session recovery
CREATE TABLE IF NOT EXISTS checkpoints (
    checkpoint_id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    trigger_type TEXT,  -- timer/major_step/user_approval/auto/session_end/context
    current_task TEXT,
    completed_items TEXT,  -- JSON array
    pending_decisions TEXT,  -- JSON array
    active_issues TEXT,  -- JSON array
    next_steps TEXT,
    context_usage_percent REAL,
    checkpoint_number INTEGER,
    FOREIGN KEY (session_id) REFERENCES session_state(session_id)
);

-- Checkpoint scheduling/reminders
CREATE TABLE IF NOT EXISTS checkpoint_schedule (
    session_id TEXT PRIMARY KEY,
    next_checkpoint_due TIMESTAMP,
    last_checkpoint_time TIMESTAMP,
    checkpoint_count INTEGER DEFAULT 0,
    timer_interval_minutes INTEGER DEFAULT 30,
    FOREIGN KEY (session_id) REFERENCES session_state(session_id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_decisions_session ON decisions(session_id);
CREATE INDEX IF NOT EXISTS idx_issues_session ON issues(session_id);
CREATE INDEX IF NOT EXISTS idx_checkpoints_session ON checkpoints(session_id);
CREATE INDEX IF NOT EXISTS idx_checkpoints_timestamp ON checkpoints(timestamp);
