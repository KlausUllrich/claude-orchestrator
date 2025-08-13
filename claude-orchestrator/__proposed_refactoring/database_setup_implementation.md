# Database Setup & Implementation Plan

## Database Architecture Decision

### Hybrid Approach: Central + Local Storage

```
Central SQLite DB (.agents-orchestrator/session.db)
├── session_state           # Current session info
├── agent_registry          # Available agents
├── cross_agent_messages    # Agent communications
└── session_history         # Session summaries

Local Agent Storage (per agent folder)
├── .agents/session-handover/data/handover.db
├── .agents/code-reviewer/data/reviews.db  
└── .agents/doc-checker/data/analysis.db
```

**Rationale:**
- **Central DB:** Cross-agent coordination, session state
- **Local DB:** Agent-specific data, templates, outputs
- **Performance:** No single bottleneck
- **Isolation:** Agents don't interfere with each other

## Central Database Schema

### File: `.agents-orchestrator/session.db`

```sql
-- Session management
CREATE TABLE sessions (
    id TEXT PRIMARY KEY,
    project_path TEXT NOT NULL,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP,
    status TEXT DEFAULT 'active', -- active, ended, archived
    main_agent_id TEXT,
    metadata JSON, -- user-defined session info
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Agent registry and status
CREATE TABLE agents (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL, -- handover, code-reviewer, doc-checker
    workspace_path TEXT NOT NULL,
    status TEXT DEFAULT 'inactive', -- inactive, active, busy, error
    pid INTEGER, -- Process ID if running
    mcp_port INTEGER, -- MCP server port
    capabilities JSON, -- What this agent can do
    config JSON, -- Agent configuration
    last_heartbeat TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cross-agent communication log
CREATE TABLE messages (
    id TEXT PRIMARY KEY,
    session_id TEXT,
    from_agent TEXT,
    to_agent TEXT,
    message_type TEXT, -- request, response, notification, error
    content TEXT,
    context JSON,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processed BOOLEAN DEFAULT FALSE,
    response_to TEXT, -- Reference to original message if this is a response
    FOREIGN KEY (session_id) REFERENCES sessions(id),
    FOREIGN KEY (from_agent) REFERENCES agents(id),
    FOREIGN KEY (to_agent) REFERENCES agents(id)
);

-- Session events and milestones
CREATE TABLE session_events (
    id TEXT PRIMARY KEY,
    session_id TEXT,
    event_type TEXT, -- agent_spawned, file_modified, check_completed, handover_created
    agent_id TEXT,
    event_data JSON,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(id),
    FOREIGN KEY (agent_id) REFERENCES agents(id)
);

-- Agent performance and metrics
CREATE TABLE agent_metrics (
    id TEXT PRIMARY KEY,
    agent_id TEXT,
    session_id TEXT,
    metric_name TEXT, -- response_time, success_rate, tasks_completed
    metric_value REAL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (agent_id) REFERENCES agents(id),
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

-- Indexes for performance
CREATE INDEX idx_messages_session ON messages(session_id, timestamp);
CREATE INDEX idx_messages_agents ON messages(from_agent, to_agent);
CREATE INDEX idx_events_session ON session_events(session_id, timestamp);
CREATE INDEX idx_agents_status ON agents(status, last_heartbeat);
```

## Local Agent Database Schema

### Example: Session Handover Agent DB
### File: `.agents/session-handover/data/handover.db`

```sql
-- Handover documents and versions
CREATE TABLE handover_documents (
    id TEXT PRIMARY KEY,
    session_id TEXT,
    template_name TEXT,
    version INTEGER DEFAULT 1,
    content TEXT,
    placeholders_remaining JSON, -- List of unfilled placeholders
    validation_status TEXT DEFAULT 'pending', -- pending, passed, failed
    validation_errors JSON,
    file_path TEXT, -- Where document was saved
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Session context analysis
CREATE TABLE session_analysis (
    id TEXT PRIMARY KEY,
    session_id TEXT,
    analysis_type TEXT, -- git_analysis, file_analysis, todo_analysis
    analysis_data JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Handover validation results
CREATE TABLE validation_results (
    id TEXT PRIMARY KEY,
    handover_id TEXT,
    rule_name TEXT,
    rule_type TEXT, -- mandatory_section, quality_check, validation_rule
    status TEXT, -- passed, failed, warning
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (handover_id) REFERENCES handover_documents(id)
);

-- User templates and rules (cached from files)
CREATE TABLE user_templates (
    id TEXT PRIMARY KEY,
    template_name TEXT UNIQUE,
    template_content TEXT,
    file_path TEXT,
    file_hash TEXT, -- To detect file changes
    last_modified TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE user_rules (
    id TEXT PRIMARY KEY,
    rule_name TEXT,
    rule_type TEXT,
    rule_content TEXT,
    file_path TEXT,
    file_hash TEXT,
    last_modified TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Next session recommendations
CREATE TABLE session_recommendations (
    id TEXT PRIMARY KEY,
    session_id TEXT,
    recommendation_type TEXT, -- files_to_read, priorities, notes
    recommendation_data JSON,
    confidence_score REAL, -- 0.0 to 1.0
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Database Implementation

### 1. Database Manager Class

```javascript
// .agents-orchestrator/database/DatabaseManager.js
import sqlite3 from 'sqlite3';
import { open } from 'sqlite';
import path from 'path';
import fs from 'fs/promises';

export class DatabaseManager {
    constructor(projectPath) {
        this.projectPath = projectPath;
        this.centralDbPath = path.join(projectPath, '.agents-orchestrator', 'session.db');
        this.centralDb = null;
        this.agentDbs = new Map(); // agent_id -> db connection
    }

    async initialize() {
        // Ensure directory exists
        await fs.mkdir(path.dirname(this.centralDbPath), { recursive: true });
        
        // Open central database
        this.centralDb = await open({
            filename: this.centralDbPath,
            driver: sqlite3.Database
        });

        // Create tables if they don't exist
        await this.createCentralTables();
        
        console.log('Central database initialized:', this.centralDbPath);
    }

    async createCentralTables() {
        const schema = await fs.readFile(
            path.join(__dirname, 'schemas', 'central-schema.sql'), 
            'utf8'
        );
        await this.centralDb.exec(schema);
    }

    // Session Management
    async createSession(sessionData) {
        const sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        
        await this.centralDb.run(`
            INSERT INTO sessions (id, project_path, main_agent_id, metadata)
            VALUES (?, ?, ?, ?)
        `, [sessionId, this.projectPath, sessionData.mainAgentId, JSON.stringify(sessionData.metadata || {})]);
        
        return sessionId;
    }

    async getActiveSession() {
        return await this.centralDb.get(`
            SELECT * FROM sessions 
            WHERE status = 'active' 
            ORDER BY start_time DESC 
            LIMIT 1
        `);
    }

    async endSession(sessionId, summary) {
        await this.centralDb.run(`
            UPDATE sessions 
            SET status = 'ended', end_time = CURRENT_TIMESTAMP, metadata = json_set(metadata, '$.summary', ?)
            WHERE id = ?
        `, [summary, sessionId]);
    }

    // Agent Management
    async registerAgent(agentData) {
        const agentId = `agent_${agentData.name}_${Date.now()}`;
        
        await this.centralDb.run(`
            INSERT INTO agents (id, name, type, workspace_path, capabilities, config)
            VALUES (?, ?, ?, ?, ?, ?)
        `, [
            agentId, 
            agentData.name, 
            agentData.type, 
            agentData.workspacePath,
            JSON.stringify(agentData.capabilities || []),
            JSON.stringify(agentData.config || {})
        ]);
        
        return agentId;
    }

    async updateAgentStatus(agentId, status, heartbeat = true) {
        const updates = { status };
        if (heartbeat) {
            updates.last_heartbeat = new Date().toISOString();
        }
        
        const setClause = Object.keys(updates).map(key => `${key} = ?`).join(', ');
        const values = Object.values(updates);
        
        await this.centralDb.run(`
            UPDATE agents SET ${setClause} WHERE id = ?
        `, [...values, agentId]);
    }

    async getActiveAgents() {
        return await this.centralDb.all(`
            SELECT * FROM agents 
            WHERE status IN ('active', 'busy') 
            AND last_heartbeat > datetime('now', '-5 minutes')
        `);
    }

    // Message Management
    async logMessage(messageData) {
        const messageId = `msg_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        
        await this.centralDb.run(`
            INSERT INTO messages (id, session_id, from_agent, to_agent, message_type, content, context, response_to)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        `, [
            messageId,
            messageData.sessionId,
            messageData.fromAgent,
            messageData.toAgent,
            messageData.messageType,
            messageData.content,
            JSON.stringify(messageData.context || {}),
            messageData.responseTo || null
        ]);
        
        return messageId;
    }

    async getConversation(agentA, agentB, limit = 50) {
        return await this.centralDb.all(`
            SELECT * FROM messages 
            WHERE (from_agent = ? AND to_agent = ?) OR (from_agent = ? AND to_agent = ?)
            ORDER BY timestamp DESC 
            LIMIT ?
        `, [agentA, agentB, agentB, agentA, limit]);
    }

    // Event Logging
    async logEvent(eventData) {
        const eventId = `event_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        
        await this.centralDb.run(`
            INSERT INTO session_events (id, session_id, event_type, agent_id, event_data)
            VALUES (?, ?, ?, ?, ?)
        `, [
            eventId,
            eventData.sessionId,
            eventData.eventType,
            eventData.agentId,
            JSON.stringify(eventData.eventData || {})
        ]);
        
        return eventId;
    }

    // Agent-specific database connections
    async getAgentDb(agentId, agentWorkspace) {
        if (this.agentDbs.has(agentId)) {
            return this.agentDbs.get(agentId);
        }
        
        const dbPath = path.join(agentWorkspace, 'data', 'agent.db');
        await fs.mkdir(path.dirname(dbPath), { recursive: true });
        
        const db = await open({
            filename: dbPath,
            driver: sqlite3.Database
        });
        
        // Create agent-specific tables based on agent type
        await this.createAgentTables(db, agentId);
        
        this.agentDbs.set(agentId, db);
        return db;
    }

    async createAgentTables(db, agentId) {
        // Load schema based on agent type
        const agent = await this.centralDb.get('SELECT type FROM agents WHERE id = ?', [agentId]);
        
        if (agent) {
            const schemaFile = path.join(__dirname, 'schemas', `${agent.type}-schema.sql`);
            try {
                const schema = await fs.readFile(schemaFile, 'utf8');
                await db.exec(schema);
            } catch (error) {
                console.warn(`No specific schema found for agent type: ${agent.type}`);
                // Use default schema
                const defaultSchema = await fs.readFile(
                    path.join(__dirname, 'schemas', 'default-agent-schema.sql'), 
                    'utf8'
                );
                await db.exec(defaultSchema);
            }
        }
    }

    // Cleanup and maintenance
    async cleanup() {
        // Close all agent database connections
        for (const [agentId, db] of this.agentDbs) {
            await db.close();
        }
        this.agentDbs.clear();
        
        // Close central database
        if (this.centralDb) {
            await this.centralDb.close();
        }
    }

    async archiveOldSessions(daysOld = 30) {
        await this.centralDb.run(`
            UPDATE sessions 
            SET status = 'archived' 
            WHERE status = 'ended' 
            AND start_time < datetime('now', '-${daysOld} days')
        `);
    }
}
```

### 2. Agent Database Helper

```javascript
// .agents-orchestrator/database/AgentDbHelper.js
export class AgentDbHelper {
    constructor(dbManager, agentId, agentWorkspace) {
        this.dbManager = dbManager;
        this.agentId = agentId;
        this.agentWorkspace = agentWorkspace;
        this.db = null;
    }

    async initialize() {
        this.db = await this.dbManager.getAgentDb(this.agentId, this.agentWorkspace);
    }

    // Generic methods for all agents
    async storeAnalysis(analysisType, data) {
        const sessionId = await this.getCurrentSessionId();
        
        await this.db.run(`
            INSERT INTO session_analysis (session_id, analysis_type, analysis_data)
            VALUES (?, ?, ?)
        `, [sessionId, analysisType, JSON.stringify(data)]);
    }

    async getLatestAnalysis(analysisType) {
        return await this.db.get(`
            SELECT * FROM session_analysis 
            WHERE analysis_type = ? 
            ORDER BY created_at DESC 
            LIMIT 1
        `, [analysisType]);
    }

    async getCurrentSessionId() {
        const session = await this.dbManager.getActiveSession();
        return session ? session.id : null;
    }

    // Template management (for agents that use templates)
    async cacheTemplate(templateName, content, filePath) {
        const fileHash = await this.calculateFileHash(filePath);
        
        await this.db.run(`
            INSERT OR REPLACE INTO user_templates 
            (template_name, template_content, file_path, file_hash, last_modified)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        `, [templateName, content, filePath, fileHash]);
    }

    async getTemplate(templateName) {
        return await this.db.get(`
            SELECT * FROM user_templates WHERE template_name = ?
        `, [templateName]);
    }

    async isTemplateUpToDate(templateName, filePath) {
        const cached = await this.getTemplate(templateName);
        if (!cached) return false;
        
        const currentHash = await this.calculateFileHash(filePath);
        return cached.file_hash === currentHash;
    }

    async calculateFileHash(filePath) {
        const crypto = await import('crypto');
        const fs = await import('fs/promises');
        
        try {
            const content = await fs.readFile(filePath, 'utf8');
            return crypto.createHash('md5').update(content).digest('hex');
        } catch (error) {
            return null;
        }
    }
}
```

## Implementation Roadmap

### Phase 1: Core Database Setup (Week 1)
- [ ] **Day 1-2:** Create DatabaseManager class with central DB
- [ ] **Day 3:** Implement session management (create, get, end)
- [ ] **Day 4:** Implement agent registration and status tracking
- [ ] **Day 5:** Add message logging and basic queries
- [ ] **Day 6-7:** Testing and error handling

### Phase 2: Agent Database Integration (Week 2)
- [ ] **Day 1-2:** Create AgentDbHelper class
- [ ] **Day 3:** Implement template caching system
- [ ] **Day 4:** Add session analysis storage
- [ ] **Day 5:** Create handover-specific schema and methods
- [ ] **Day 6-7:** Integration testing with MCP server

### Phase 3: Advanced Features (Week 3)
- [ ] **Day 1-2:** Add event logging and metrics collection
- [ ] **Day 3:** Implement conversation tracking between agents
- [ ] **Day 4:** Add database maintenance and archiving
- [ ] **Day 5:** Performance optimization and indexing
- [ ] **Day 6-7:** Comprehensive testing and documentation

### Phase 4: Production Readiness (Week 4)
- [ ] **Day 1-2:** Error handling and recovery mechanisms
- [ ] **Day 3:** Database migration system for schema updates
- [ ] **Day 4:** Backup and restore functionality
- [ ] **Day 5:** Performance monitoring and alerting
- [ ] **Day 6-7:** Final testing and deployment preparation

## Database Configuration

### Environment Variables
```bash
# .agents-orchestrator/.env
DB_PATH=".agents-orchestrator/session.db"
DB_BACKUP_INTERVAL=3600  # 1 hour
DB_ARCHIVE_DAYS=30       # Archive sessions older than 30 days
DB_MAX_CONNECTIONS=10
DB_QUERY_TIMEOUT=5000    # 5 seconds
```

### Configuration File
```json
// .agents-orchestrator/config/database.json
{
  "central": {
    "path": ".agents-orchestrator/session.db",
    "backup": {
      "enabled": true,
      "interval": 3600,
      "maxBackups": 24
    },
    "maintenance": {
      "archiveDays": 30,
      "vacuumInterval": 86400
    }
  },
  "agents": {
    "defaultSchema": "default-agent-schema.sql",
    "schemas": {
      "session-handover": "handover-schema.sql",
      "code-reviewer": "reviewer-schema.sql",
      "doc-checker": "doc-checker-schema.sql"
    }
  },
  "performance": {
    "maxConnections": 10,
    "queryTimeout": 5000,
    "cacheSize": 1000
  }
}
```

## Testing Strategy

### Unit Tests
```javascript
// tests/database/DatabaseManager.test.js
describe('DatabaseManager', () => {
    let dbManager;
    let tempDir;

    beforeEach(async () => {
        tempDir = await fs.mkdtemp(path.join(os.tmpdir(), 'agent-test-'));
        dbManager = new DatabaseManager(tempDir);
        await dbManager.initialize();
    });

    afterEach(async () => {
        await dbManager.cleanup();
        await fs.rm(tempDir, { recursive: true });
    });

    describe('Session Management', () => {
        test('should create and retrieve session', async () => {
            const sessionData = {
                mainAgentId: 'test-agent',
                metadata: { purpose: 'test session' }
            };
            
            const sessionId = await dbManager.createSession(sessionData);
            expect(sessionId).toMatch(/^session_\d+_/);
            
            const session = await dbManager.getActiveSession();
            expect(session.id).toBe(sessionId);
            expect(session.status).toBe('active');
        });

        test('should end session with summary', async () => {
            const sessionId = await dbManager.createSession({ mainAgentId: 'test' });
            await dbManager.endSession(sessionId, 'Test completed successfully');
            
            const session = await dbManager.centralDb.get('SELECT * FROM sessions WHERE id = ?', [sessionId]);
            expect(session.status).toBe('ended');
            expect(session.end_time).toBeTruthy();
        });
    });

    describe('Agent Management', () => {
        test('should register and track agent status', async () => {
            const agentData = {
                name: 'test-handover',
                type: 'session-handover',
                workspacePath: path.join(tempDir, '.agents', 'test-handover'),
                capabilities: ['analyze_session', 'generate_handover']
            };
            
            const agentId = await dbManager.registerAgent(agentData);
            expect(agentId).toMatch(/^agent_test-handover_/);
            
            await dbManager.updateAgentStatus(agentId, 'active');
            
            const activeAgents = await dbManager.getActiveAgents();
            expect(activeAgents).toHaveLength(1);
            expect(activeAgents[0].id).toBe(agentId);
        });
    });

    describe('Message Logging', () => {
        test('should log and retrieve conversation', async () => {
            const sessionId = await dbManager.createSession({ mainAgentId: 'main' });
            const agent1 = await dbManager.registerAgent({ name: 'agent1', type: 'test', workspacePath: '/tmp' });
            const agent2 = await dbManager.registerAgent({ name: 'agent2', type: 'test', workspacePath: '/tmp' });
            
            await dbManager.logMessage({
                sessionId,
                fromAgent: agent1,
                toAgent: agent2,
                messageType: 'request',
                content: 'Please analyze session',
                context: { priority: 'high' }
            });
            
            const conversation = await dbManager.getConversation(agent1, agent2);
            expect(conversation).toHaveLength(1);
            expect(conversation[0].content).toBe('Please analyze session');
        });
    });
});
```

### Integration Tests
```javascript
// tests/integration/DatabaseIntegration.test.js
describe('Database Integration', () => {
    test('should handle complete session lifecycle', async () => {
        // Create session
        const sessionId = await dbManager.createSession({
            mainAgentId: 'main-agent',
            metadata: { project: 'test-project' }
        });

        // Register agents
        const handoverAgent = await dbManager.registerAgent({
            name: 'handover',
            type: 'session-handover',
            workspacePath: path.join(tempDir, '.agents', 'handover')
        });

        // Log some activity
        await dbManager.logMessage({
            sessionId,
            fromAgent: 'main-agent',
            toAgent: handoverAgent,
            messageType: 'request',
            content: 'Create handover document'
        });

        await dbManager.logEvent({
            sessionId,
            eventType: 'handover_created',
            agentId: handoverAgent,
            eventData: { documentPath: '/path/to/handover.md' }
        });

        // End session
        await dbManager.endSession(sessionId, 'Session completed successfully');

        // Verify everything was stored correctly
        const session = await dbManager.centralDb.get('SELECT * FROM sessions WHERE id = ?', [sessionId]);
        expect(session.status).toBe('ended');

        const messages = await dbManager.centralDb.all('SELECT * FROM messages WHERE session_id = ?', [sessionId]);
        expect(messages).toHaveLength(1);

        const events = await dbManager.centralDb.all('SELECT * FROM session_events WHERE session_id = ?', [sessionId]);
        expect(events).toHaveLength(1);
    });
});
```

This database setup provides a robust foundation for agent coordination while maintaining clear separation between central orchestration and agent-specific data.