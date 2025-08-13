import sqlite3 from 'sqlite3';
import { open } from 'sqlite';
import path from 'path';
import fs from 'fs/promises';

export class DatabaseManager {
    constructor(dbPath) {
        this.dbPath = dbPath;
        this.db = null;
    }

    async initialize() {
        // Ensure directory exists
        await fs.mkdir(path.dirname(this.dbPath), { recursive: true });
        
        // Open database connection
        this.db = await open({
            filename: this.dbPath,
            driver: sqlite3.Database
        });

        // Create tables
        await this.createTables();
        
        console.error('Database initialized at:', this.dbPath);
    }

    async createTables() {
        // Agents table
        await this.db.exec(`
            CREATE TABLE IF NOT EXISTS agents (
                id TEXT PRIMARY KEY,
                workspace_path TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                details TEXT,
                capabilities TEXT,
                last_heartbeat TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        `);

        // Messages table
        await this.db.exec(`
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_agent TEXT NOT NULL,
                to_agent TEXT NOT NULL,
                message_type TEXT NOT NULL,
                content TEXT NOT NULL,
                file_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                read_at TIMESTAMP,
                FOREIGN KEY (from_agent) REFERENCES agents(id),
                FOREIGN KEY (to_agent) REFERENCES agents(id)
            )
        `);

        // Outputs table
        await this.db.exec(`
            CREATE TABLE IF NOT EXISTS outputs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_id TEXT NOT NULL,
                file_path TEXT NOT NULL,
                metadata TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (agent_id) REFERENCES agents(id)
            )
        `);

        // Create indexes for performance
        await this.db.exec(`
            CREATE INDEX IF NOT EXISTS idx_messages_to_agent ON messages(to_agent, read_at);
            CREATE INDEX IF NOT EXISTS idx_outputs_agent ON outputs(agent_id, created_at);
        `);
    }

    // Agent operations
    async registerAgent(agentId, workspacePath, capabilities = []) {
        await this.db.run(
            `INSERT OR REPLACE INTO agents (id, workspace_path, capabilities, status, last_heartbeat) 
             VALUES (?, ?, ?, 'active', CURRENT_TIMESTAMP)`,
            [agentId, workspacePath, JSON.stringify(capabilities)]
        );
    }

    async updateAgentStatus(agentId, status, details = null) {
        await this.db.run(
            `UPDATE agents SET status = ?, details = ?, last_heartbeat = CURRENT_TIMESTAMP 
             WHERE id = ?`,
            [status, details, agentId]
        );
    }

    async getAgent(agentId) {
        return await this.db.get('SELECT * FROM agents WHERE id = ?', [agentId]);
    }

    async getAllAgents() {
        return await this.db.all('SELECT * FROM agents ORDER BY created_at DESC');
    }

    // Message operations
    async addMessage(fromAgent, toAgent, messageType, content, filePath = null) {
        const result = await this.db.run(
            `INSERT INTO messages (from_agent, to_agent, message_type, content, file_path) 
             VALUES (?, ?, ?, ?, ?)`,
            [fromAgent, toAgent, messageType, content, filePath]
        );
        return result.lastID;
    }

    async getUnreadMessages(agentId) {
        return await this.db.all(
            `SELECT * FROM messages 
             WHERE to_agent = ? AND read_at IS NULL 
             ORDER BY created_at ASC`,
            [agentId]
        );
    }

    async markMessageAsRead(messageId) {
        await this.db.run(
            'UPDATE messages SET read_at = CURRENT_TIMESTAMP WHERE id = ?',
            [messageId]
        );
    }

    async markMessagesAsRead(messageIds) {
        if (messageIds.length === 0) return;
        
        const placeholders = messageIds.map(() => '?').join(',');
        await this.db.run(
            `UPDATE messages SET read_at = CURRENT_TIMESTAMP WHERE id IN (${placeholders})`,
            messageIds
        );
    }

    // Output operations
    async addOutput(agentId, filePath, metadata = {}) {
        await this.db.run(
            `INSERT INTO outputs (agent_id, file_path, metadata) VALUES (?, ?, ?)`,
            [agentId, filePath, JSON.stringify(metadata)]
        );
    }

    async getLatestOutput(agentId) {
        return await this.db.get(
            `SELECT * FROM outputs 
             WHERE agent_id = ? 
             ORDER BY created_at DESC 
             LIMIT 1`,
            [agentId]
        );
    }

    async getOutputsSince(timestamp) {
        return await this.db.all(
            'SELECT * FROM outputs WHERE created_at > ? ORDER BY created_at DESC',
            [timestamp]
        );
    }

    // Cleanup operations
    async cleanup() {
        if (this.db) {
            await this.db.close();
        }
    }

    async clearOldMessages(daysOld = 7) {
        await this.db.run(
            `DELETE FROM messages 
             WHERE created_at < datetime('now', '-${daysOld} days')`,
        );
    }
}