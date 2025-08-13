export class MessageBroker {
    constructor(db, registry) {
        this.db = db;
        this.registry = registry;
        this.outputWaiters = new Map(); // agent_id -> array of waiting promises
    }

    async sendMessage(fromAgent, toAgent, messageType, content, filePath = null) {
        // Verify both agents exist
        const sender = await this.db.getAgent(fromAgent);
        const receiver = await this.db.getAgent(toAgent);
        
        if (!sender) {
            throw new Error(`Sender agent '${fromAgent}' not registered`);
        }
        if (!receiver) {
            throw new Error(`Receiver agent '${toAgent}' not registered`);
        }
        
        // Store message in database
        const messageId = await this.db.addMessage(
            fromAgent,
            toAgent,
            messageType,
            content,
            filePath
        );
        
        // If this is an output notification, trigger any waiters
        if (messageType === 'output_ready' && filePath) {
            this.notifyOutputWaiters(fromAgent, filePath);
        }
        
        return messageId;
    }

    async getMessagesForAgent(agentId, markAsRead = true) {
        const messages = await this.db.getUnreadMessages(agentId);
        
        if (markAsRead && messages.length > 0) {
            const messageIds = messages.map(m => m.id);
            await this.db.markMessagesAsRead(messageIds);
        }
        
        return messages;
    }

    async notifyOutputReady(agentId, filePath) {
        // Check if any agents are waiting for output from this agent
        const waiters = this.outputWaiters.get(agentId);
        
        if (waiters && waiters.length > 0) {
            // Resolve all waiting promises
            waiters.forEach(waiter => {
                waiter.resolve({ agent_id: agentId, file_path: filePath });
            });
            
            // Clear the waiters
            this.outputWaiters.set(agentId, []);
        }
        
        // Also send a broadcast message to all agents
        const agents = await this.registry.getAllAgents();
        for (const agent of agents) {
            if (agent.id !== agentId) {
                await this.sendMessage(
                    agentId,
                    agent.id,
                    'notification',
                    `Output ready at: ${filePath}`,
                    filePath
                );
            }
        }
    }

    registerOutputWaiter(agentId, resolve, reject) {
        if (!this.outputWaiters.has(agentId)) {
            this.outputWaiters.set(agentId, []);
        }
        
        this.outputWaiters.get(agentId).push({ resolve, reject });
    }

    async waitForOutput(waitingAgent, fromAgent, timeoutMs = 30000) {
        return new Promise((resolve, reject) => {
            // Set up timeout
            const timeout = setTimeout(() => {
                // Remove from waiters
                const waiters = this.outputWaiters.get(fromAgent);
                if (waiters) {
                    const index = waiters.findIndex(w => w.resolve === resolve);
                    if (index !== -1) {
                        waiters.splice(index, 1);
                    }
                }
                
                reject(new Error(`Timeout waiting for output from ${fromAgent}`));
            }, timeoutMs);
            
            // Register as waiter
            this.registerOutputWaiter(fromAgent, (output) => {
                clearTimeout(timeout);
                resolve(output);
            }, reject);
        });
    }

    notifyOutputWaiters(agentId, filePath) {
        const waiters = this.outputWaiters.get(agentId);
        
        if (waiters && waiters.length > 0) {
            waiters.forEach(waiter => {
                waiter.resolve({ agent_id: agentId, file_path: filePath });
            });
            
            this.outputWaiters.set(agentId, []);
        }
    }
}