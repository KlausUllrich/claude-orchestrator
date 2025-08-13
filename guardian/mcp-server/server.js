#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { DatabaseManager } from './lib/DatabaseManager.js';
import { MessageBroker } from './lib/MessageBroker.js';
import { FileMonitor } from './lib/FileMonitor.js';
import { AgentRegistry } from './lib/AgentRegistry.js';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

class GuardianMCPServer {
    constructor() {
        this.server = new Server(
            { 
                name: 'guardian-orchestrator',
                version: '1.0.0'
            },
            { 
                capabilities: { 
                    tools: {}
                }
            }
        );
        
        // Initialize components
        this.dbPath = path.join(__dirname, 'db', 'coordination.db');
        this.db = new DatabaseManager(this.dbPath);
        this.registry = new AgentRegistry(this.db);
        this.broker = new MessageBroker(this.db, this.registry);
        this.monitor = new FileMonitor(this.broker);
        
        this.setupTools();
    }

    setupTools() {
        // Register available tools
        this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
            tools: [
                {
                    name: 'register_agent',
                    description: 'Register this agent with the orchestrator',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            agent_id: { 
                                type: 'string',
                                description: 'Unique identifier for this agent (e.g., agent1, agent2)'
                            },
                            workspace_path: {
                                type: 'string',
                                description: 'Path to agent workspace directory'
                            },
                            capabilities: {
                                type: 'array',
                                items: { type: 'string' },
                                description: 'List of capabilities this agent has'
                            }
                        },
                        required: ['agent_id', 'workspace_path']
                    }
                },
                {
                    name: 'send_message',
                    description: 'Send a message to another agent',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            from_agent: {
                                type: 'string',
                                description: 'ID of sending agent'
                            },
                            to_agent: {
                                type: 'string',
                                description: 'ID of receiving agent'
                            },
                            message_type: {
                                type: 'string',
                                enum: ['request', 'response', 'notification'],
                                description: 'Type of message'
                            },
                            content: {
                                type: 'string',
                                description: 'Message content'
                            },
                            file_path: {
                                type: 'string',
                                description: 'Optional path to associated file'
                            }
                        },
                        required: ['from_agent', 'to_agent', 'message_type', 'content']
                    }
                },
                {
                    name: 'check_messages',
                    description: 'Check for messages addressed to this agent',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            agent_id: {
                                type: 'string',
                                description: 'ID of agent checking messages'
                            },
                            mark_as_read: {
                                type: 'boolean',
                                default: true,
                                description: 'Mark retrieved messages as read'
                            }
                        },
                        required: ['agent_id']
                    }
                },
                {
                    name: 'notify_output_ready',
                    description: 'Notify that an output file is ready',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            agent_id: {
                                type: 'string',
                                description: 'ID of agent that created output'
                            },
                            file_path: {
                                type: 'string',
                                description: 'Path to output file'
                            },
                            metadata: {
                                type: 'object',
                                description: 'Optional metadata about the output'
                            }
                        },
                        required: ['agent_id', 'file_path']
                    }
                },
                {
                    name: 'wait_for_output',
                    description: 'Wait for output from another agent',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            waiting_agent: {
                                type: 'string',
                                description: 'ID of agent waiting for output'
                            },
                            from_agent: {
                                type: 'string',
                                description: 'ID of agent expected to produce output'
                            },
                            timeout_ms: {
                                type: 'integer',
                                default: 30000,
                                description: 'Timeout in milliseconds'
                            }
                        },
                        required: ['waiting_agent', 'from_agent']
                    }
                },
                {
                    name: 'update_status',
                    description: 'Update agent status',
                    inputSchema: {
                        type: 'object',
                        properties: {
                            agent_id: {
                                type: 'string',
                                description: 'ID of agent'
                            },
                            status: {
                                type: 'string',
                                enum: ['active', 'busy', 'waiting', 'complete', 'error'],
                                description: 'Current status'
                            },
                            details: {
                                type: 'string',
                                description: 'Optional status details'
                            }
                        },
                        required: ['agent_id', 'status']
                    }
                },
                {
                    name: 'get_agent_list',
                    description: 'Get list of registered agents and their status',
                    inputSchema: {
                        type: 'object',
                        properties: {}
                    }
                }
            ]
        }));

        // Handle tool calls
        this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
            const { name, arguments: args } = request.params;
            
            try {
                switch (name) {
                    case 'register_agent':
                        return await this.registerAgent(args);
                    case 'send_message':
                        return await this.sendMessage(args);
                    case 'check_messages':
                        return await this.checkMessages(args);
                    case 'notify_output_ready':
                        return await this.notifyOutputReady(args);
                    case 'wait_for_output':
                        return await this.waitForOutput(args);
                    case 'update_status':
                        return await this.updateStatus(args);
                    case 'get_agent_list':
                        return await this.getAgentList();
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

    async registerAgent(args) {
        const { agent_id, workspace_path, capabilities = [] } = args;
        
        await this.registry.register(agent_id, workspace_path, capabilities);
        
        // Start monitoring agent's output directory
        const outputDir = path.join(workspace_path, 'outputs');
        this.monitor.watchDirectory(agent_id, outputDir);
        
        return {
            content: [{
                type: 'text',
                text: `Agent '${agent_id}' registered successfully\nWorkspace: ${workspace_path}\nMonitoring outputs at: ${outputDir}`
            }]
        };
    }

    async sendMessage(args) {
        const { from_agent, to_agent, message_type, content, file_path } = args;
        
        const messageId = await this.broker.sendMessage(
            from_agent,
            to_agent,
            message_type,
            content,
            file_path
        );
        
        return {
            content: [{
                type: 'text',
                text: `Message sent successfully\nID: ${messageId}\nFrom: ${from_agent} → To: ${to_agent}`
            }]
        };
    }

    async checkMessages(args) {
        const { agent_id, mark_as_read = true } = args;
        
        const messages = await this.broker.getMessagesForAgent(agent_id, mark_as_read);
        
        if (messages.length === 0) {
            return {
                content: [{
                    type: 'text',
                    text: 'No new messages'
                }]
            };
        }
        
        const messageText = messages.map(msg => 
            `[${msg.message_type}] From: ${msg.from_agent}\n` +
            `Content: ${msg.content}\n` +
            `${msg.file_path ? `File: ${msg.file_path}\n` : ''}` +
            `Time: ${msg.created_at}`
        ).join('\n---\n');
        
        return {
            content: [{
                type: 'text',
                text: `Found ${messages.length} message(s):\n\n${messageText}`
            }]
        };
    }

    async notifyOutputReady(args) {
        const { agent_id, file_path, metadata = {} } = args;
        
        await this.db.addOutput(agent_id, file_path, metadata);
        
        // Notify any waiting agents
        await this.broker.notifyOutputReady(agent_id, file_path);
        
        return {
            content: [{
                type: 'text',
                text: `Output notification sent\nAgent: ${agent_id}\nFile: ${file_path}`
            }]
        };
    }

    async waitForOutput(args) {
        const { waiting_agent, from_agent, timeout_ms = 30000 } = args;
        
        const startTime = Date.now();
        
        // Check if output already exists
        let output = await this.db.getLatestOutput(from_agent);
        
        // If not, wait for it
        while (!output && (Date.now() - startTime) < timeout_ms) {
            await new Promise(resolve => setTimeout(resolve, 500));
            output = await this.db.getLatestOutput(from_agent);
        }
        
        if (!output) {
            return {
                content: [{
                    type: 'text',
                    text: `Timeout waiting for output from ${from_agent}`
                }]
            };
        }
        
        return {
            content: [{
                type: 'text',
                text: `Output available from ${from_agent}\nFile: ${output.file_path}\nCreated: ${output.created_at}`
            }]
        };
    }

    async updateStatus(args) {
        const { agent_id, status, details } = args;
        
        await this.registry.updateStatus(agent_id, status, details);
        
        return {
            content: [{
                type: 'text',
                text: `Status updated for ${agent_id}: ${status}${details ? `\nDetails: ${details}` : ''}`
            }]
        };
    }

    async getAgentList() {
        const agents = await this.registry.getAllAgents();
        
        if (agents.length === 0) {
            return {
                content: [{
                    type: 'text',
                    text: 'No agents registered'
                }]
            };
        }
        
        const agentText = agents.map(agent =>
            `• ${agent.id}: ${agent.status} (${agent.workspace_path})`
        ).join('\n');
        
        return {
            content: [{
                type: 'text',
                text: `Registered agents:\n${agentText}`
            }]
        };
    }

    async start() {
        // Initialize database
        await this.db.initialize();
        
        // Start server
        const transport = new StdioServerTransport();
        await this.server.connect(transport);
        
        console.error('Guardian MCP Server started');
    }
}

// Start the server
const server = new GuardianMCPServer();
server.start().catch(error => {
    console.error('Failed to start server:', error);
    process.exit(1);
});