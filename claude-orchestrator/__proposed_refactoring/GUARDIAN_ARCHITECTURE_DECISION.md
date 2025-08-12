# Guardian Architecture Decision

## Decision Summary

**APPROVED WITH MODIFICATIONS**

The Guardian architecture is viable and recommended, but must be implemented using:
- **run_in_background** for agent launching (NOT Task tool)
- **File-based signaling** for coordination
- **Status files** for monitoring
- **Sequential launching** with parallel execution

## Original Vision vs Reality

### Original Guardian Concept
```
Guardian (Task tool) → Multiple Agents (parallel) → Coordinated work
         ↓
   [Autonomous]
```

### Actual Implementation Required
```
Guardian (Python) → run_in_background → Agents (parallel) → File signals
         ↓              ↓                    ↓                  ↓
   [Coordinates]   [No blocking]      [Independent]      [Observable]
```

## Key Architectural Changes

### 1. Cannot Use Task Tool
**Finding**: Task tool blocks Claude for 14+ seconds
**Impact**: Guardian cannot use Task tool for orchestration
**Solution**: Use run_in_background directly

### 2. Sequential Launch, Parallel Execution
**Finding**: Must launch agents one at a time
**Impact**: Small overhead (0.5s per agent)
**Solution**: Acceptable trade-off for autonomy

### 3. File-Based Coordination Required
**Finding**: No built-in agent communication
**Impact**: Need coordination mechanism
**Solution**: Signal files + status files

## Recommended Guardian Implementation

### Core Components

```python
class Guardian:
    """
    Orchestrates parallel agent execution while maintaining Claude's autonomy
    """
    
    def __init__(self):
        self.signal_dir = Path(".orchestrate/guardian/signals")
        self.status_dir = Path(".orchestrate/guardian/status")
        self.running_agents = {}
        
    def orchestrate(self, workflow_config):
        """
        Main orchestration loop
        """
        # 1. Parse workflow and dependencies
        agents = self.parse_workflow(workflow_config)
        dep_graph = self.build_dependency_graph(agents)
        
        # 2. Launch initial agents (no dependencies)
        for agent in dep_graph.get_ready():
            self.launch_agent(agent)
            
        # 3. Monitor and coordinate
        while not self.all_complete():
            # Check for completed agents
            completed = self.check_completions()
            
            # Update signals for completed
            for agent in completed:
                self.write_signal(agent)
                
            # Launch newly ready agents
            ready = dep_graph.get_ready()
            for agent in ready:
                self.launch_agent(agent)
                
            # Brief pause to prevent CPU spinning
            time.sleep(0.5)
            
    def launch_agent(self, agent_config):
        """
        Launch agent using run_in_background
        """
        cmd = f"python {agent_config.script} {agent_config.args}"
        
        # This returns immediately!
        bash_id = Bash(cmd, run_in_background=True)
        
        self.running_agents[agent_config.name] = {
            "bash_id": bash_id,
            "status": "running",
            "started": datetime.now()
        }
```

### Workflow Configuration

```yaml
# guardian_workflow.yaml
name: "Code Review Workflow"
agents:
  - name: analyzer
    script: agents/code_analyzer.py
    timeout: 30
    
  - name: linter
    script: agents/linter.py
    timeout: 20
    
  - name: security_checker
    script: agents/security.py
    timeout: 25
    
  - name: report_generator
    script: agents/reporter.py
    depends_on: [analyzer, linter, security_checker]
    timeout: 15
    
coordination:
  method: file_signals
  status_update_interval: 2
  signal_dir: .orchestrate/guardian/signals
  status_dir: .orchestrate/guardian/status
```

### Agent Template

```python
# agents/base_agent.py
class GuardianAgent:
    """
    Base class for Guardian-orchestrated agents
    """
    
    def __init__(self, name):
        self.name = name
        self.signal_dir = Path(".orchestrate/guardian/signals")
        self.status_dir = Path(".orchestrate/guardian/status")
        
    def wait_for_dependencies(self, dependencies):
        """Wait for required signals"""
        while True:
            if all(self.check_signal(dep) for dep in dependencies):
                return True
            time.sleep(0.5)
            
    def update_status(self, state, progress=0, message=""):
        """Write status file for monitoring"""
        status = {
            "agent": self.name,
            "state": state,
            "progress": progress,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        status_file = self.status_dir / f"{self.name}.json"
        status_file.write_text(json.dumps(status))
        
    def signal_completion(self):
        """Signal that this agent is complete"""
        signal_file = self.signal_dir / f"{self.name}.complete"
        signal_file.write_text(datetime.now().isoformat())
```

## Implementation Benefits

### 1. Claude Autonomy ✅
- Never blocks during orchestration
- Can respond to user queries
- Can monitor progress
- Can handle errors gracefully

### 2. True Parallelization ✅
- Agents run simultaneously
- Dependencies properly managed
- Optimal execution time

### 3. Observable Progress ✅
- Status files show real-time progress
- Signal files show coordination
- Easy to debug issues

### 4. Flexible Architecture ✅
- Easy to add new agents
- Workflows defined in YAML
- Reusable agent templates

## Implementation Challenges

### 1. Launch Overhead
- **Issue**: 0.5s per agent launch
- **Impact**: 10 agents = 5s launch time
- **Mitigation**: Launch in priority order

### 2. File System Limits
- **Issue**: Many files for large workflows
- **Impact**: Performance at 100+ agents
- **Mitigation**: Batch status updates, cleanup old files

### 3. Error Recovery
- **Issue**: Agent failures need handling
- **Impact**: Workflow might stall
- **Mitigation**: Timeout + retry logic

### 4. No Real-Time Events
- **Issue**: Polling for changes
- **Impact**: 0.5s latency minimum
- **Mitigation**: Acceptable for most workflows

## Migration Path

### Phase 1: Basic Implementation (Week 1)
1. Create Guardian base class
2. Implement run_in_background launching
3. Add file-based signaling
4. Test with simple workflow

### Phase 2: Enhanced Features (Week 2)
1. Add dependency graph builder
2. Implement timeout handling
3. Add retry logic
4. Create status dashboard

### Phase 3: Production Ready (Week 3)
1. Add comprehensive logging
2. Implement cleanup routines
3. Create workflow templates
4. Performance optimization

### Phase 4: Advanced Features (Month 2)
1. Dynamic agent spawning
2. Conditional workflows
3. Resource management
4. Multi-project support

## Decision Rationale

### Why Proceed Despite Changes

1. **Core Value Intact**: Parallel execution with coordination
2. **Autonomy Achieved**: Claude never blocks
3. **Simple Solution**: Easier than expected
4. **Proven Technology**: File system + Bash reliable
5. **Debugging Friendly**: Everything observable

### Why Not Use Alternatives

**Task Tool**: Blocks Claude, defeats purpose
**MCP Server**: Over-complex for need
**Pure Python**: Claude still blocks
**No Orchestration**: Loses coordination benefits

## Success Criteria

### Must Have (Week 1)
- [ ] Guardian launches agents without blocking
- [ ] Agents run in parallel
- [ ] Basic dependency management
- [ ] Status monitoring

### Should Have (Week 2)
- [ ] Error handling
- [ ] Timeout management
- [ ] Progress reporting
- [ ] Workflow templates

### Nice to Have (Month 1)
- [ ] Dynamic workflows
- [ ] Resource limits
- [ ] Performance metrics
- [ ] Web dashboard

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| File system performance | Low | Medium | Caching, cleanup |
| Agent crashes | Medium | Low | Timeouts, retry |
| Complex dependencies | Low | High | Graph validation |
| User confusion | Medium | Medium | Clear documentation |

## Final Decision

### ✅ PROCEED WITH MODIFIED GUARDIAN ARCHITECTURE

**Rationale**: 
- Testing proves hybrid approach works
- Simpler than originally expected
- Maintains all core benefits
- Ready for implementation

**Next Steps**:
1. Clean up test artifacts
2. Create Guardian prototype
3. Implement basic workflow
4. Test with real use case
5. Iterate based on results

---

## Appendix: Key Learnings

### What We Learned
1. **Tool blocking is fundamental** - Cannot be worked around
2. **Simple solutions win** - run_in_background > complex servers
3. **Files are reliable** - Good enough for coordination
4. **Autonomy is critical** - Never sacrifice Claude's responsiveness

### What Surprised Us
1. Task tool blocks even with background agents
2. File signaling works better than expected
3. 0.5s launch overhead is acceptable
4. MCP setup more complex than documented

### What to Remember
1. Always test assumptions with real code
2. Simplicity beats complexity
3. User experience comes first
4. Autonomy enables everything else

---

*Decision Date: 2025-08-12*
*Decision Maker: Claude + User (via testing)*
*Status: APPROVED FOR IMPLEMENTATION*