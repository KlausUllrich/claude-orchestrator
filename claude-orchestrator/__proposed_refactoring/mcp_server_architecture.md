# MCP Server Architecture & Implementation

## Architecture Decision: Central Orchestrator + Specialized Agent MCPs

### Hybrid MCP Architecture
```
Main Agent (Claude Code)
├── Central MCP Server (Port 3001)
│   ├── Cross-Agent Communication
│   ├── Session Management  
│   ├── Agent Lifecycle
│   └── Event Coordination
│
└── Agent-Specific MCP Servers
    ├── Handover MCP (Port 3002)
    │   ├── Template Management
    │   ├── Document Generation
    │   ├── Validation Rules
    │   └── Context Analysis
    │
    ├── Code Review MCP (Port 3003)
    │   ├── Style Checking
    │   ├── Security Analysis
    │   ├── Pattern Validation
    │   └── Report Generation
    │
    └── Doc Checker MCP (Port 3004)
        ├── Documentation Analysis
        ├── Consistency Checking
        ├── Update Suggestions
        └── Structure Validation
```

**Rationale:**
- **Central MCP:** Agent coordination, session state, communication
- **Specialized MCPs:** Domain-specific tools, isolated concerns
- **Scalability:** Add new agent types without affecting existing ones
- **Maintenance:** Each MCP is focused and manageable

## Central MCP Server Implementation

### Features & Responsibilities
1. **Agent Lifecycle Management** - Spawn, monitor, terminate agents
2. **Cross-Agent Communication** - Message routing and delivery
3. **Session State Management** - Track session progress and context
4. **Event Coordination** - Broadcast events to relevant agents
5. **Health Monitoring** - Agent heartbeats and error detection

### File: `.agents-orchestrator/central-mcp-server.js`

```javascript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { DatabaseManager } from './database/DatabaseManager.js';
import { AgentManager } from './agents/AgentManager.js';
import { EventBus } from './events/EventBus.js';
import { MessageRouter } from './communication/MessageRouter.js';

export class CentralMCPServer {
    constructor(projectPath) {
        this.server = new Server(
            { name: 'enhanced-session-orchestrator', version: '1.0.0' },
            { capabilities: { tools: {} } }
        );
        
        this.projectPath = projectPath;
        this.dbManager = new DatabaseManager(projectPath);
        this.agentManager = new AgentManager(this.dbManager);
        this.eventBus = new EventBus();
        this.messageRouter = new MessageRouter(this.dbManager, this.eventBus);
        
        this.setupTools();
        this.setupEventHandlers();
    }

    setupTools() {
        // Session Management Tools
        this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
            tools: [
                {
                    name: 'create_enhanced_session',
                    description: 'Initialize an enhanced Claude session with support agents',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            sessionName: { type: 'string', description: 'Name for this session' },
                            agents: { 
                                type: 'array', 
                                items: { type: 'string' },
                                description: 'List of agent types to spawn (handover, code-reviewer, doc-checker)'
                            },
                            metadata: { type: 'object', description: 'Additional session metadata' }
                        },
                        required: ['sessionName']
                    }
                },
                {
                    name: 'send_to_agent',
                    description: 'Send a message to a specific agent',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            agentType: { 
                                type: 'string', 
                                enum: ['handover', 'code-reviewer', 'doc-checker'],
                                description: 'Type of agent to send message to'
                            },
                            message: { type: 'string', description: 'Message content' },
                            context: { type: 'object', description: 'Additional context' },
                            priority: { 
                                type: 'string', 
                                enum: ['low', 'normal', 'high', 'urgent'],
                                default: 'normal'
                            }
                        },
                        required: ['agentType', 'message']
                    }
                },
                {
                    name: 'get_session_state',
                    description: 'Get current session state and agent status',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            includeMetrics: { type: 'boolean', default: false },
                            includeMessages: { type: 'boolean', default: false }
                        }
                    }
                },
                {
                    name: 'broadcast_event',
                    description: 'Broadcast an event to all active agents',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            eventType: { type: 'string', description: 'Type of event' },
                            eventData: { type: 'object', description: 'Event payload' },
                            targetAgents: { 
                                type: 'array', 
                                items: { type: 'string' },
                                description: 'Specific agents to notify (empty = all)'
                            }
                        },
                        required: ['eventType']
                    }
                },
                {
                    name: 'end_session',
                    description: 'End the current session and cleanup',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            summary: { type: 'string', description: 'Session summary' },
                            createHandover: { type: 'boolean', default: true },
                            cleanupAgents: { type: 'boolean', default: true }
                        }
                    }
                }
            ]
        }));

        this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
            const { name, arguments: args } = request.params;

            try {
                switch (name) {
                    case 'create_enhanced_session':
                        return await this.createEnhancedSession(args);
                    case 'send_to_agent':
                        return await this.sendToAgent(args);
                    case 'get_session_state':
                        return await this.getSessionState(args);
                    case 'broadcast_event':
                        return await this.broadcastEvent(args);
                    case 'end_session':
                        return await this.endSession(args);
                    default:
                        throw new Error(`Unknown tool: ${name}`);
                }
            } catch (error) {
                return {
                    content: [{ 
                        type: 'text', 
                        text: `Error executing ${name}: ${error.message}` 
                    }],
                    isError: true
                };
            }
        });
    }

    async createEnhancedSession(args) {
        const { sessionName, agents = ['handover'], metadata = {} } = args;
        
        // Create session in database
        const sessionId = await this.dbManager.createSession({
            name: sessionName,
            mainAgentId: 'main-claude',
            metadata
        });

        // Spawn requested agents
        const spawnedAgents = [];
        for (const agentType of agents) {
            try {
                const agentId = await this.agentManager.spawnAgent(agentType, sessionId);
                spawnedAgents.push({ type: agentType, id: agentId, status: 'spawning' });
                
                // Log agent spawn event
                await this.dbManager.logEvent({
                    sessionId,
                    eventType: 'agent_spawned',
                    agentId,
                    eventData: { agentType }
                });
            } catch (error) {
                console.error(`Failed to spawn ${agentType} agent:`, error);
                spawnedAgents.push({ type: agentType, error: error.message });
            }
        }

        // Broadcast session start event
        await this.eventBus.emit('session_started', {
            sessionId,
            sessionName,
            agents: spawnedAgents
        });

        return {
            content: [{
                type: 'text',
                text: `Enhanced session created successfully!

Session ID: ${sessionId}
Session Name: ${sessionName}
Spawned Agents: ${spawnedAgents.filter(a => !a.error).length}/${agents.length}

Active Agents:
${spawnedAgents.map(a => 
    a.error 
        ? `❌ ${a.type}: ${a.error}`
        : `✅ ${a.type}: Ready (${a.id})`
).join('\n')}

You can now communicate with agents using the send_to_agent tool.`
            }]
        };
    }

    async sendToAgent(args) {
        const { agentType, message, context = {}, priority = 'normal' } = args;
        
        // Get current session
        const session = await this.dbManager.getActiveSession();
        if (!session) {
            throw new Error('No active session found');
        }

        // Find target agent
        const agents = await this.dbManager.getActiveAgents();
        const targetAgent = agents.find(a => a.type === agentType);
        
        if (!targetAgent) {
            throw new Error(`No active ${agentType} agent found`);
        }

        // Route message to agent
        const messageId = await this.messageRouter.routeMessage({
            sessionId: session.id,
            fromAgent: 'main-claude',
            toAgent: targetAgent.id,
            messageType: 'request',
            content: message,
            context: { ...context, priority }
        });

        // Wait for response (with timeout)
        const response = await this.messageRouter.waitForResponse(messageId, 30000);

        return {
            content: [{
                type: 'text',
                text: response ? response.content : `Message sent to ${agentType} agent. Response may be available via get_session_state.`
            }]
        };
    }

    async getSessionState(args) {
        const { includeMetrics = false, includeMessages = false } = args;
        
        const session = await this.dbManager.getActiveSession();
        if (!session) {
            return {
                content: [{ type: 'text', text: 'No active session found' }]
            };
        }

        const agents = await this.dbManager.getActiveAgents();
        const state = {
            session: {
                id: session.id,
                name: session.metadata?.name || 'Unnamed Session',
                startTime: session.start_time,
                status: session.status
            },
            agents: agents.map(a => ({
                id: a.id,
                type: a.type,
                status: a.status,
                lastHeartbeat: a.last_heartbeat
            }))
        };

        if (includeMessages) {
            state.recentMessages = await this.dbManager.centralDb.all(`
                SELECT from_agent, to_agent, message_type, content, timestamp 
                FROM messages 
                WHERE session_id = ? 
                ORDER BY timestamp DESC 
                LIMIT 10
            `, [session.id]);
        }

        if (includeMetrics) {
            state.metrics = await this.dbManager.centralDb.all(`
                SELECT agent_id, metric_name, metric_value, timestamp
                FROM agent_metrics 
                WHERE session_id = ?
                ORDER BY timestamp DESC 
                LIMIT 50
            `, [session.id]);
        }

        return {
            content: [{
                type: 'text',
                text: `Session State:

📊 Session: ${state.session.name} (${state.session.id})
⏰ Started: ${new Date(state.session.startTime).toLocaleString()}
📈 Status: ${state.session.status}

👥 Active Agents (${state.agents.length}):
${state.agents.map(a => 
    `${getAgentEmoji(a.type)} ${a.type}: ${a.status} (Last seen: ${getTimeAgo(a.lastHeartbeat)})`
).join('\n')}

${includeMessages && state.recentMessages?.length > 0 ? `
💬 Recent Messages:
${state.recentMessages.slice(0, 5).map(m => 
    `${m.from_agent} → ${m.to_agent}: ${m.content.substring(0, 50)}...`
).join('\n')}
` : ''}

${includeMetrics && state.metrics?.length > 0 ? `
📈 Recent Metrics:
${state.metrics.slice(0, 5).map(m => 
    `${m.agent_id}: ${m.metric_name} = ${m.metric_value}`
).join('\n')}
` : ''}`
            }]
        };
    }

    async broadcastEvent(args) {
        const { eventType, eventData = {}, targetAgents = [] } = args;
        
        const session = await this.dbManager.getActiveSession();
        if (!session) {
            throw new Error('No active session found');
        }

        // Get target agents
        const agents = await this.dbManager.getActiveAgents();
        const targets = targetAgents.length > 0 
            ? agents.filter(a => targetAgents.includes(a.type))
            : agents;

        // Broadcast to each target
        const results = [];
        for (const agent of targets) {
            try {
                await this.messageRouter.routeMessage({
                    sessionId: session.id,
                    fromAgent: 'orchestrator',
                    toAgent: agent.id,
                    messageType: 'notification',
                    content: `Event: ${eventType}`,
                    context: eventData
                });
                
                results.push({ agentId: agent.id, status: 'sent' });
            } catch (error) {
                results.push({ agentId: agent.id, status: 'failed', error: error.message });
            }
        }

        // Log broadcast event
        await this.dbManager.logEvent({
            sessionId: session.id,
            eventType: 'broadcast_event',
            agentId: 'orchestrator',
            eventData: { originalEventType: eventType, targets: targets.map(t => t.id) }
        });

        return {
            content: [{
                type: 'text',
                text: `Event "${eventType}" broadcast to ${targets.length} agents:

${results.map(r => 
    r.status === 'sent' 
        ? `✅ ${r.agentId}: Delivered`
        : `❌ ${r.agentId}: Failed (${r.error})`
).join('\n')}`
            }]
        };
    }

    async endSession(args) {
        const { summary = '', createHandover = true, cleanupAgents = true } = args;
        
        const session = await this.dbManager.getActiveSession();
        if (!session) {
            throw new Error('No active session found');
        }

        let handoverResult = null;
        
        // Create handover if requested
        if (createHandover) {
            try {
                const handoverAgent = await this.dbManager.centralDb.get(`
                    SELECT * FROM agents 
                    WHERE type = 'handover' AND status IN ('active', 'busy')
                    LIMIT 1
                `);
                
                if (handoverAgent) {
                    const messageId = await this.messageRouter.routeMessage({
                        sessionId: session.id,
                        fromAgent: 'main-claude',
                        toAgent: handoverAgent.id,
                        messageType: 'request',
                        content: 'Create final session handover document',
                        context: { summary, sessionEnd: true }
                    });
                    
                    handoverResult = await this.messageRouter.waitForResponse(messageId, 60000);
                }
            } catch (error) {
                console.error('Failed to create handover:', error);
            }
        }

        // Cleanup agents if requested
        if (cleanupAgents) {
            const agents = await this.dbManager.getActiveAgents();
            for (const agent of agents) {
                try {
                    await this.agentManager.terminateAgent(agent.id);
                } catch (error) {
                    console.error(`Failed to terminate agent ${agent.id}:`, error);
                }
            }
        }

        // End session in database
        await this.dbManager.endSession(session.id, summary);

        // Broadcast session end event
        await this.eventBus.emit('session_ended', {
            sessionId: session.id,
            summary,
            handoverCreated: !!handoverResult
        });

        return {
            content: [{
                type: 'text',
                text: `Session ended successfully!

📊 Session: ${session.id}
📝 Summary: ${summary || 'No summary provided'}
📄 Handover: ${handoverResult ? '✅ Created' : '❌ Not created'}
🧹 Agents: ${cleanupAgents ? '✅ Cleaned up' : '⚠️ Left running'}

${handoverResult ? `

Handover Document: ${handoverResult.context?.filePath || 'Created successfully'}` : ''}`
            }]
        };
    }

    setupEventHandlers() {
        this.eventBus.on('agent_error', async (data) => {
            await this.dbManager.logEvent({
                sessionId: data.sessionId,
                eventType: 'agent_error',
                agentId: data.agentId,
                eventData: { error: data.error, stack: data.stack }
            });
        });

        this.eventBus.on('agent_heartbeat', async (data) => {
            await this.dbManager.updateAgentStatus(data.agentId, data.status, true);
        });
    }

    async start() {
        await this.dbManager.initialize();
        
        const transport = new StdioServerTransport();
        await this.server.connect(transport);
        
        console.log('Central MCP Server started');
    }

    async stop() {
        await this.dbManager.cleanup();
        console.log('Central MCP Server stopped');
    }
}

// Helper functions
function getAgentEmoji(agentType) {
    const emojis = {
        'handover': '📄',
        'code-reviewer': '🔍',
        'doc-checker': '📚',
        'orchestrator': '🎭'
    };
    return emojis[agentType] || '🤖';
}

function getTimeAgo(timestamp) {
    if (!timestamp) return 'Never';
    
    const now = new Date();
    const then = new Date(timestamp);
    const diffMs = now - then;
    const diffSec = Math.floor(diffMs / 1000);
    const diffMin = Math.floor(diffSec / 60);
    
    if (diffSec < 60) return `${diffSec}s ago`;
    if (diffMin < 60) return `${diffMin}m ago`;
    return `${Math.floor(diffMin / 60)}h ago`;
}

// Start server if run directly
if (import.meta.url === `file://${process.argv[1]}`) {
    const projectPath = process.cwd();
    const server = new CentralMCPServer(projectPath);
    
    process.on('SIGINT', async () => {
        await server.stop();
        process.exit(0);
    });
    
    await server.start();
}
```

## Handover Agent MCP Server

### File: `.agents/session-handover/handover-mcp-server.js`

```javascript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { HandoverManager } from './lib/HandoverManager.js';
import { TemplateManager } from './lib/TemplateManager.js';
import { ValidationManager } from './lib/ValidationManager.js';
import { ContextAnalyzer } from './lib/ContextAnalyzer.js';

export class HandoverMCPServer {
    constructor(workspacePath) {
        this.server = new Server(
            { name: 'session-handover-agent', version: '1.0.0' },
            { capabilities: { tools: {} } }
        );
        
        this.workspacePath = workspacePath;
        this.handoverManager = new HandoverManager(workspacePath);
        this.templateManager = new TemplateManager(workspacePath);
        this.validationManager = new ValidationManager(workspacePath);
        this.contextAnalyzer = new ContextAnalyzer(workspacePath);
        
        this.setupTools();
    }

    setupTools() {
        this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
            tools: [
                {
                    name: 'analyze_session_context',
                    description: 'Analyze current session for handover generation',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            includeGitHistory: { type: 'boolean', default: true },
                            includeFileAnalysis: { type: 'boolean', default: true },
                            includeTodos: { type: 'boolean', default: true }
                        }
                    }
                },
                {
                    name: 'generate_handover',
                    description: 'Generate handover document from template',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            templateName: { type: 'string', default: 'handover.md' },
                            userInputs: { type: 'object', description: 'User-provided content for placeholders' },
                            autoFill: { type: 'boolean', default: true, description: 'Auto-fill what can be determined automatically' }
                        }
                    }
                },
                {
                    name: 'validate_handover',
                    description: 'Validate handover document against user rules',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            handoverPath: { type: 'string', description: 'Path to handover document' },
                            strict: { type: 'boolean', default: false, description: 'Strict validation mode' }
                        },
                        required: ['handoverPath']
                    }
                },
                {
                    name: 'suggest_next_files',
                    description: 'Suggest files for next session to read',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            maxSuggestions: { type: 'integer', default: 10 },
                            categories: { 
                                type: 'array',
                                items: { type: 'string' },
                                default: ['related', 'docs', 'tests', 'config']
                            }
                        }
                    }
                }
            ]
        }));

        this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
            const { name, arguments: args } = request.params;

            try {
                switch (name) {
                    case 'analyze_session_context':
                        return await this.analyzeSessionContext(args);
                    case 'generate_handover':
                        return await this.generateHandover(args);
                    case 'validate_handover':
                        return await this.validateHandover(args);
                    case 'suggest_next_files':
                        return await this.suggestNextFiles(args);
                    default:
                        throw new Error(`Unknown tool: ${name}`);
                }
            } catch (error) {
                return {
                    content: [{ 
                        type: 'text', 
                        text: `Error: ${error.message}` 
                    }],
                    isError: true
                };
            }
        });
    }

    async analyzeSessionContext(args) {
        const { includeGitHistory = true, includeFileAnalysis = true, includeTodos = true } = args;
        
        const analysis = await this.contextAnalyzer.analyzeSession({
            includeGitHistory,
            includeFileAnalysis,
            includeTodos
        });

        // Store analysis for later use
        await this.handoverManager.storeSessionAnalysis(analysis);

        return {
            content: [{
                type: 'text',
                text: `Session context analyzed successfully!

📊 **Analysis Summary:**
- Modified Files: ${analysis.modifiedFiles?.length || 0}
- New Functions: ${analysis.newFunctions?.length || 0}
- New Tests: ${analysis.newTests?.length || 0}
- Documentation Changes: ${analysis.docChanges?.length || 0}
- TODOs Found: ${analysis.todos?.length || 0}

🔍 **Key Findings:**
${analysis.keyFindings?.map(f => `• ${f}`).join('\n') || 'No specific findings'}

📝 **Ready for handover generation.** Use generate_handover tool next.`
            }]
        };
    }

    async generateHandover(args) {
        const { templateName = 'handover.md', userInputs = {}, autoFill = true } = args;
        
        // Load template
        const template = await this.templateManager.loadTemplate(templateName);
        if (!template) {
            throw new Error(`Template ${templateName} not found`);
        }

        // Get stored session analysis
        const analysis = await this.handoverManager.getLatestSessionAnalysis();
        if (!analysis) {
            throw new Error('No session analysis found. Run analyze_session_context first.');
        }

        // Generate handover
        const handover = await this.handoverManager.generateHandover({
            template,
            analysis,
            userInputs,
            autoFill
        });

        return {
            content: [{
                type: 'text',
                text: `Handover document generated successfully!

📄 **Document:** ${handover.filePath}
📋 **Status:** ${handover.placeholdersRemaining.length === 0 ? 'Complete' : 'Needs input'}

${handover.placeholdersRemaining.length > 0 ? `
⚠️ **Missing Information:**
${handover.placeholdersRemaining.map(p => `• ${p}`).join('\n')}

Please provide these details and regenerate the handover.
` : ''}

✅ **Next Step:** Run validate_handover to check compliance with your rules.`
            }]
        };
    }

    async validateHandover(args) {
        const { handoverPath, strict = false } = args;
        
        const validation = await this.validationManager.validateHandover(handoverPath, strict);
        
        return {
            content: [{
                type: 'text',
                text: `Handover validation ${validation.passed ? 'PASSED' : 'FAILED'}!

📋 **Validation Results:**
- Ready for finalization: ${validation.ready ? '✅ Yes' : '❌ No'}
- Issues found: ${validation.issues.length}
- Warnings: ${validation.warnings.length}

${validation.issues.length > 0 ? `
❌ **Issues to Fix:**
${validation.issues.map(issue => `• ${issue.message} (${issue.type})`).join('\n')}
` : ''}

${validation.warnings.length > 0 ? `
⚠️ **Warnings:**
${validation.warnings.map(warning => `• ${warning.message}`).join('\n')}
` : ''}

${validation.checklist.length > 0 ? `
📋 **Completion Checklist:**
${validation.checklist.map(item => 
    `${item.completed ? '✅' : '❌'} ${item.description}`
).join('\n')}
` : ''}

${validation.ready ? '🎉 Handover is ready for session finalization!' : '🔧 Please address the issues above.'}`
            }]
        };
    }

    async suggestNextFiles(args) {
        const { maxSuggestions = 10, categories = ['related', 'docs', 'tests', 'config'] } = args;
        
        const suggestions = await this.contextAnalyzer.suggestNextSessionFiles({
            maxSuggestions,
            categories
        });

        return {
            content: [{
                type: 'text',
                text: `Next session file suggestions generated!

📚 **Recommended Files (${suggestions.totalSuggestions}):**

${categories.map(category => {
    const categoryFiles = suggestions.byCategory[category] || [];
    return categoryFiles.length > 0 ? `
**${category.toUpperCase()} Files:**
${categoryFiles.map(file => `• ${file.path} - ${file.reason}`).join('\n')}` : '';
}).filter(Boolean).join('\n')}

🎯 **Top Priority Files:**
${suggestions.topPriority.map(file => `• ${file.path} (${file.score.toFixed(1)}/10)`).join('\n')}

💡 **Tip:** Include these in your session handover document for the next developer.`
            }]
        };
    }

    async start() {
        await this.handoverManager.initialize();
        
        const transport = new StdioServerTransport();
        await this.server.connect(transport);
        
        console.log('Handover MCP Server started');
    }
}

// Start server if run directly
if (import.meta.url === `file://${process.argv[1]}`) {
    const workspacePath = process.env.AGENT_WORKSPACE || process.cwd();
    const server = new HandoverMCPServer(workspacePath);
    
    process.on('SIGINT', () => {
        console.log('Handover MCP Server stopped');
        process.exit(0);
    });
    
    await server.start();
}
```

## Agent Manager Implementation

### File: `.agents-orchestrator/agents/AgentManager.js`

```javascript
import { spawn } from 'child_process';
import path from 'path';
import fs from 'fs/promises';

export class AgentManager {
    constructor(dbManager) {
        this.dbManager = dbManager;
        this.runningAgents = new Map(); // agentId -> process
        this.agentPorts = new Map(); // agentType -> port
        this.basePort = 3002;
    }

    async spawnAgent(agentType, sessionId) {
        // Check if agent type is supported
        const supportedTypes = ['handover', 'code-reviewer', 'doc-checker'];
        if (!supportedTypes.includes(agentType)) {
            throw new Error(`Unsupported agent type: ${agentType}`);
        }

        // Determine workspace path
        const workspacePath = path.join(process.cwd(), '.agents', `session-${agentType}`);
        await fs.mkdir(workspacePath, { recursive: true });

        // Register agent in database
        const agentId = await this.dbManager.registerAgent({
            name: `${agentType}-agent`,
            type: agentType,
            workspacePath,
            capabilities: this.getAgentCapabilities(agentType),
            config: {
                sessionId,
                mcpPort: this.getAgentPort(agentType)
            }
        });

        try {
            // Start Claude Code session for the agent
            const process = await this.startAgentProcess(agentType, workspacePath, agentId);
            
            this.runningAgents.set(agentId, process);
            
            // Update agent status
            await this.dbManager.updateAgentStatus(agentId, 'active');
            
            // Set up process monitoring
            this.setupProcessMonitoring(agentId, process);
            
            return agentId;
        } catch (error) {
            // Clean up on failure
            await this.dbManager.updateAgentStatus(agentId, 'error');
            throw error;
        }
    }

    async startAgentProcess(agentType, workspacePath, agentId) {
        const mcpConfigPath = path.join(workspacePath, '.claude', 'settings.json');
        
        // Ensure MCP config exists
        await this.createAgentMCPConfig(agentType, workspacePath, mcpConfigPath);
        
        // Start Claude Code with the agent's MCP configuration
        const claudeProcess = spawn('claude', [
            '--project', workspacePath,
            '--mcp-config', mcpConfigPath
        ], {
            stdio: ['pipe', 'pipe', 'pipe'],
            cwd: workspacePath
        });

        // Send initial agent prompt
        const systemPrompt = await this.getAgentSystemPrompt(agentType, workspacePath);
        claudeProcess.stdin.write(`${systemPrompt}\n\nI am ready to assist as a ${agentType} agent.\n`);

        return claudeProcess;
    }

    async createAgentMCPConfig(agentType, workspacePath, configPath) {
        await fs.mkdir(path.dirname(configPath), { recursive: true });
        
        const mcpServerPath = path.join(workspacePath, `${agentType}-mcp-server.js`);
        const mcpPort = this.getAgentPort(agentType);
        
        const config = {
            mcpServers: {
                [`${agentType}-tools`]: {
                    command: 'node',
                    args: [mcpServerPath],
                    env: {
                        AGENT_WORKSPACE: workspacePath,
                        MCP_PORT: mcpPort.toString()
                    }
                },
                'central-orchestrator': {
                    command: 'node',
                    args: [path.join(process.cwd(), '.agents-orchestrator', 'central-mcp-server.js')],
                    env: {
                        PROJECT_PATH: process.cwd()
                    }
                }
            }
        };

        await fs.writeFile(configPath, JSON.stringify(config, null, 2));
    }

    async getAgentSystemPrompt(agentType, workspacePath) {
        const promptPath = path.join(workspacePath, 'system-prompt.md');
        
        try {
            return await fs.readFile(promptPath, 'utf8');
        } catch (error) {
            // Return default prompt if custom one doesn't exist
            return this.getDefaultSystemPrompt(agentType);
        }
    }

    getDefaultSystemPrompt(agentType) {
        const prompts = {
            'handover': `You are a Session Handover Specialist. Your role is to help create comprehensive handover documents for development sessions.

Your capabilities include:
- Analyzing session context and changes
- Generating handover documents from user templates
- Validating handover completeness
- Suggesting files for next sessions

Always use your MCP tools to perform these tasks effectively.`,
            
            'code-reviewer': `You are a Code Quality Specialist. Your role is to review code changes and ensure adherence to project standards.

Your capabilities include:
- Analyzing code quality and style
- Checking for security issues
- Validating against project patterns
- Generating review reports

Focus on constructive feedback and actionable suggestions.`,
            
            'doc-checker': `You are a Documentation Specialist. Your role is to ensure documentation stays current and comprehensive.

Your capabilities include:
- Analyzing documentation completeness
- Checking for consistency
- Suggesting updates based on code changes
- Validating document structure

Help maintain high-quality, up-to-date documentation.`
        };

        return prompts[agentType] || 'You are a helpful AI assistant.';
    }

    getAgentCapabilities(agentType) {
        const capabilities = {
            'handover': [
                'analyze_session_context',
                'generate_handover',
                'validate_handover',
                'suggest_next_files'
            ],
            'code-reviewer': [
                'analyze_code_quality',
                'check_security',
                'validate_patterns',
                'generate_review'
            ],
            'doc-checker': [
                'analyze_documentation',
                'check_consistency',
                'suggest_updates',
                'validate_structure'
            ]
        };

        return capabilities[agentType] || [];
    }

    getAgentPort(agentType) {
        if (!this.agentPorts.has(agentType)) {
            this.agentPorts.set(agentType, this.basePort + this.agentPorts.size);
        }
        return this.agentPorts.get(agentType);
    }

    setupProcessMonitoring(agentId, process) {
        process.on('exit', async (code) => {
            console.log(`Agent ${agentId} exited with code ${code}`);
            this.runningAgents.delete(agentId);
            await this.dbManager.updateAgentStatus(agentId, 'inactive');
        });

        process.on('error', async (error) => {
            console.error(`Agent ${agentId} error:`, error);
            await this.dbManager.updateAgentStatus(agentId, 'error');
        });

        // Set up heartbeat monitoring
        const heartbeatInterval = setInterval(async () => {
            if (process.killed) {
                clearInterval(heartbeatInterval);
                return;
            }
            
            try {
                await this.dbManager.updateAgentStatus(agentId, 'active');
            } catch (error) {
                console.error(`Failed to update heartbeat for agent ${agentId}:`, error);
            }
        }, 30000); // 30 second heartbeat
    }

    async terminateAgent(agentId) {
        const process = this.runningAgents.get(agentId);
        
        if (process && !process.killed) {
            process.kill('SIGTERM');
            
            // Force kill after 5 seconds if still running
            setTimeout(() => {
                if (!process.killed) {
                    process.kill('SIGKILL');
                }
            }, 5000);
        }

        this.runningAgents.delete(agentId);
        await this.dbManager.updateAgentStatus(agentId, 'terminated');
    }

    async terminateAllAgents() {
        const agents = Array.from(this.runningAgents.keys());
        await Promise