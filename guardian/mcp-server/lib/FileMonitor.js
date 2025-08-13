import chokidar from 'chokidar';
import path from 'path';

export class FileMonitor {
    constructor(messageBroker) {
        this.messageBroker = messageBroker;
        this.watchers = new Map(); // agent_id -> watcher instance
    }

    watchDirectory(agentId, directory) {
        // Stop existing watcher if any
        if (this.watchers.has(agentId)) {
            this.watchers.get(agentId).close();
        }

        console.error(`Starting file monitor for ${agentId} at ${directory}`);

        // Create new watcher
        const watcher = chokidar.watch(directory, {
            persistent: true,
            ignoreInitial: true, // Don't trigger for existing files
            awaitWriteFinish: {
                stabilityThreshold: 1000, // Wait for file to be stable for 1 second
                pollInterval: 100
            }
        });

        // Handle new files
        watcher.on('add', async (filePath) => {
            console.error(`New file detected from ${agentId}: ${filePath}`);
            
            // Notify through message broker
            await this.messageBroker.notifyOutputReady(agentId, filePath);
        });

        // Handle file changes
        watcher.on('change', async (filePath) => {
            console.error(`File updated from ${agentId}: ${filePath}`);
            
            // Could optionally notify about updates
            // await this.messageBroker.notifyOutputReady(agentId, filePath);
        });

        // Handle errors
        watcher.on('error', (error) => {
            console.error(`Watcher error for ${agentId}:`, error);
        });

        // Store watcher
        this.watchers.set(agentId, watcher);
    }

    stopWatching(agentId) {
        const watcher = this.watchers.get(agentId);
        if (watcher) {
            watcher.close();
            this.watchers.delete(agentId);
            console.error(`Stopped monitoring for ${agentId}`);
        }
    }

    stopAll() {
        for (const [agentId, watcher] of this.watchers) {
            watcher.close();
            console.error(`Stopped monitoring for ${agentId}`);
        }
        this.watchers.clear();
    }
}