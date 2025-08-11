#!/usr/bin/env python3
"""
Game Dev Example: Unity Physics Optimization
Shows how to use parallel agents for a real game dev task
"""

from simple_parallel_coordinator import SimpleParallelCoordinator
from pathlib import Path
import json

def unity_physics_optimization_example():
    """
    Real example: Optimizing Unity physics performance
    Multiple agents work in parallel on different aspects
    """
    
    print("=" * 70)
    print("UNITY PHYSICS OPTIMIZATION - PARALLEL AGENT EXAMPLE")
    print("=" * 70)
    print()
    
    # Initialize coordinator
    coord = SimpleParallelCoordinator()
    
    # Define the optimization tasks
    optimization_tasks = [
        {
            "agent": "RESEARCHER",
            "task": "Research Unity physics optimization best practices, focusing on Rigidbody batching, collision layer optimization, and FixedUpdate timing"
        },
        {
            "agent": "ANALYZER", 
            "task": "Analyze the current physics setup in Assets/Scripts/Physics/, identify performance bottlenecks using the Profiler data"
        },
        {
            "agent": "CODER",
            "task": "Implement object pooling for physics objects in PhysicsObjectPool.cs, optimize Rigidbody settings for better performance"
        },
        {
            "agent": "TESTER",
            "task": "Create physics stress tests in Tests/PhysicsPerformanceTests.cs, measure frame rates with different object counts"
        },
        {
            "agent": "DOCUMENTER",
            "task": "Document physics optimization changes in Docs/PhysicsOptimization.md, create performance comparison charts"
        }
    ]
    
    # Queue all tasks
    print("Queueing optimization tasks...")
    for task_def in optimization_tasks:
        task_id = coord.queue_task(
            agent_type=task_def["agent"],
            objective=task_def["task"],
            priority=80  # High priority
        )
        print(f"  ✓ Queued: {task_def['agent']}")
    
    # Create batch for parallel execution
    batch_id = coord.create_batch()
    print(f"\nBatch created: {batch_id}")
    
    # Get the parallel execution commands
    commands = coord.get_batch_commands(batch_id)
    
    # Save to file for reference
    output_path = Path(".orchestrate/unity_physics_batch.txt")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(commands)
    
    # Create coordination file for agents to share findings
    coord_data = {
        "project": "Unity Physics Optimization",
        "batch_id": batch_id,
        "shared_findings": {
            "researcher": {},
            "analyzer": {},
            "coder": {},
            "tester": {},
            "documenter": {}
        },
        "optimization_targets": {
            "target_fps": 60,
            "max_physics_objects": 1000,
            "fixed_timestep": 0.02
        }
    }
    
    coord_path = Path(".orchestrate/physics_coordination.json")
    with open(coord_path, 'w') as f:
        json.dump(coord_data, f, indent=2)
    
    print("\n" + "=" * 70)
    print("PARALLEL EXECUTION COMMANDS:")
    print("=" * 70)
    print(commands)
    print("=" * 70)
    
    print("\n📋 INSTRUCTIONS:")
    print("1. Copy ALL Task commands above")
    print("2. Paste them into Claude Code in ONE message")
    print("3. All agents will work simultaneously on physics optimization")
    print()
    print(f"📁 Coordination file: {coord_path}")
    print(f"📄 Commands saved to: {output_path}")
    print()
    print("Expected parallel execution:")
    print("  • RESEARCHER: Gathering optimization techniques")
    print("  • ANALYZER: Profiling current performance")
    print("  • CODER: Implementing optimizations")
    print("  • TESTER: Creating benchmarks")
    print("  • DOCUMENTER: Recording changes")
    print("\nAll happening SIMULTANEOUSLY!")

def bug_fixing_marathon_example():
    """
    Example: Parallel bug fixing session
    Multiple agents tackle different bugs at once
    """
    
    print("\n" + "=" * 70)
    print("BUG FIXING MARATHON - PARALLEL AGENTS")
    print("=" * 70)
    print()
    
    coord = SimpleParallelCoordinator()
    
    # Different bugs for different agents
    bugs = [
        ("BUG_FIXER_1", "Fix null reference exception in PlayerController.cs line 127 when respawning"),
        ("BUG_FIXER_2", "Resolve memory leak in ParticleManager.cs caused by unreleased particle systems"),
        ("BUG_FIXER_3", "Fix animation glitch in CharacterAnimator.cs when transitioning from jump to idle"),
        ("BUG_TESTER", "Write regression tests for all fixed bugs in Tests/BugRegressionTests.cs"),
        ("BUG_TRACKER", "Update bug tracking documentation in Docs/Bugs/Fixed.md with all resolutions")
    ]
    
    for agent, bug in bugs:
        coord.queue_task(agent, bug, priority=90)  # Critical priority
    
    batch_id = coord.create_batch()
    commands = coord.get_batch_commands(batch_id)
    
    print(commands)
    print("\nAll bugs being fixed in PARALLEL! 🚀")

def level_design_parallel_example():
    """
    Example: Parallel level design tasks
    """
    
    print("\n" + "=" * 70)
    print("LEVEL DESIGN - PARALLEL CREATION")
    print("=" * 70)
    print()
    
    coord = SimpleParallelCoordinator()
    
    level_tasks = [
        ("LEVEL_DESIGNER", "Design layout for Level_3_Cave in LevelDesigns/Cave.txt with focus on exploration"),
        ("ASSET_CREATOR", "List required 3D models for cave level in Assets/Models/CaveAssets.txt"),
        ("LIGHTING_ARTIST", "Plan lighting setup for cave atmosphere in Lighting/CaveLighting.md"),
        ("SOUND_DESIGNER", "Define ambient sounds and music for cave in Audio/CaveAudio.md"),
        ("GAMEPLAY_CODER", "Implement cave-specific mechanics in Scripts/Levels/CaveMechanics.cs")
    ]
    
    for agent, task in level_tasks:
        coord.queue_task(agent, task)
    
    batch_id = coord.create_batch()
    commands = coord.get_batch_commands(batch_id)
    
    print(commands)
    print("\nEntire level being designed in PARALLEL! 🎮")

if __name__ == "__main__":
    # Run examples
    unity_physics_optimization_example()
    
    print("\n" + "=" * 70)
    print("OTHER GAME DEV EXAMPLES:")
    print("=" * 70)
    
    bug_fixing_marathon_example()
    level_design_parallel_example()
    
    print("\n" + "=" * 70)
    print("KEY TAKEAWAY:")
    print("=" * 70)
    print("ANY game dev task can be parallelized by:")
    print("1. Breaking it into agent-specific subtasks")
    print("2. Queueing them with the coordinator")
    print("3. Executing ALL Task commands in ONE message")
    print("\nNo complex frameworks needed! 🎯")
