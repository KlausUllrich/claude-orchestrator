export class AgentRegistry {
    constructor(db) {
        this.db = db;
        this.agents = new Map(); // agent_id -> agent info
    }

    async register(agentId, workspacePath, capabilities = []) {
        // Store in database
        await this.db.registerAgent(agentId, workspacePath, capabilities);
        
        // Cache in memory
        this.agents.set(agentId, {
            id: agentId,
            workspace_path: workspacePath,
            capabilities: capabilities,
            status: 'active',
            registered_at: new Date()
        });
        
        console.error(`Agent registered: ${agentId} at ${workspacePath}`);
        
        return agentId;
    }

    async updateStatus(agentId, status, details = null) {
        // Update database
        await this.db.updateAgentStatus(agentId, status, details);
        
        // Update cache
        const agent = this.agents.get(agentId);
        if (agent) {
            agent.status = status;
            agent.details = details;
            agent.last_update = new Date();
        }
        
        console.error(`Agent ${agentId} status: ${status}${details ? ` (${details})` : ''}`);
    }

    async getAgent(agentId) {
        // Try cache first
        if (this.agents.has(agentId)) {
            return this.agents.get(agentId);
        }
        
        // Fall back to database
        const agent = await this.db.getAgent(agentId);
        if (agent) {
            // Update cache
            this.agents.set(agentId, agent);
        }
        
        return agent;
    }

    async getAllAgents() {
        // Get from database to ensure we have latest
        const agents = await this.db.getAllAgents();
        
        // Update cache
        for (const agent of agents) {
            this.agents.set(agent.id, agent);
        }
        
        return agents;
    }

    isRegistered(agentId) {
        return this.agents.has(agentId);
    }

    getActiveAgents() {
        const active = [];
        for (const agent of this.agents.values()) {
            if (agent.status === 'active' || agent.status === 'busy') {
                active.push(agent);
            }
        }
        return active;
    }
}