# WezTerm Setup for Claude Guardian

## Installation

### Manjaro/Arch
```bash
sudo pacman -S wezterm
sudo pacman -S ttf-jetbrains-mono
sudo pacman -S ttf-nerd-fonts-symbols-mono
```

## Configuration

### Basic WezTerm Config
Location: `~/.config/wezterm/wezterm.lua`

```lua
local wezterm = require 'wezterm'

return {
  -- Font
  font = wezterm.font('JetBrains Mono'),
  font_size = 11,
  
  -- Colors
  color_scheme = 'Dracula',
  
  -- Keybindings
  leader = { key = 'a', mods = 'CTRL' },
  keys = {
    -- Split panes
    { key = '%', mods = 'LEADER|SHIFT', action = wezterm.action.SplitHorizontal },
    { key = '"', mods = 'LEADER|SHIFT', action = wezterm.action.SplitVertical },
    -- Navigate panes
    { key = 'LeftArrow', mods = 'CTRL|SHIFT', action = wezterm.action.ActivatePaneDirection 'Left' },
    { key = 'RightArrow', mods = 'CTRL|SHIFT', action = wezterm.action.ActivatePaneDirection 'Right' },
    { key = 'UpArrow', mods = 'CTRL|SHIFT', action = wezterm.action.ActivatePaneDirection 'Up' },
    { key = 'DownArrow', mods = 'CTRL|SHIFT', action = wezterm.action.ActivatePaneDirection 'Down' },
  },
}
```

## Key Features for Claude Guardian

### 1. Dynamic Tab Titles
WezTerm supports ANSI escape sequences for setting tab titles:
```bash
echo -e "\033]0;Agent 1 - Orchestrator\007"
```

### 2. Multiplexing
- Native pane splitting without tmux
- Each pane can run independent Claude instance

### 3. Programmatic Control
- Full Lua scripting API
- Can automate pane creation and layout

## Keyboard Shortcuts

### Navigation
- **Ctrl+Shift+Arrow** - Move between panes
- **Ctrl+Shift+Z** - Toggle zoom current pane
- **Click** - Focus pane with mouse

#### Pane Management
- **Ctrl+Shift+%** - Split vertically
- **Ctrl+Shift+"** - Split horizontally
- **Ctrl+Shift+X** - Close current pane

### Tabs
- **Ctrl+Shift+T** - New tab
- **Ctrl+Tab** - Next tab
- **Ctrl+Shift+Tab** - Previous tab

#### Copy/Paste
- **Ctrl+Shift+C** - Copy
- **Ctrl+Shift+V** - Paste

## Multi-Agent Setup

### Manual Setup (3 panes)
1. Open WezTerm
2. Split right: `Ctrl+Shift+%`
3. Split bottom on right pane: `Ctrl+Shift+"`
4. Navigate to each pane and start Claude

### Automated Setup (Future)
```lua
-- In wezterm.lua, create startup function
wezterm.on('gui-startup', function(cmd)
  local tab, pane1, window = mux.spawn_window{}
  local pane2 = pane1:split{direction="Right", size=0.33}
  local pane3 = pane2:split{direction="Right", size=0.5}
  
  -- Start Claude in each
  pane1:send_text('cd agent1 && claude --dangerously-skip-permissions\n')
  pane2:send_text('cd agent2 && claude --dangerously-skip-permissions\n')
  pane3:send_text('cd agent3 && claude --dangerously-skip-permissions\n')
end)
```

## Requirements vs Features

### Why WezTerm over Warp
| Feature | WezTerm | Warp |
|---------|---------|------|
| Dynamic Tab Titles | ✅ Yes | ❌ No |
| Programmatic Control | ✅ Full Lua API | ❌ Limited |
| Cross-platform | ✅ Linux/Mac/Win | ⚠️ Mac-first |
| Open Source | ✅ Yes | ❌ No |
| Multiplexing | ✅ Native | ✅ Yes |

### Why Not Tmux
- WezTerm has native multiplexing
- Simpler for users unfamiliar with tmux
- Better mouse support
- Consistent cross-platform

## Testing Status
✅ **Confirmed Working**: 3-agent chain communication test
✅ **Permission Flag**: `--dangerously-skip-permissions` required
✅ **File Communication**: Cross-directory access works

---
*Consolidated from: wezterm-handover.md, wezterm-requirements.md, warp-features-analysis.md*

## Appendix: Quick Keyboard Reference

### Pane Navigation
- **Ctrl+Shift+←/→/↑/↓** - Move between panes
- **Click** - Focus pane with mouse

### Pane Management
- **Ctrl+Shift+%** - Split pane vertically (side by side)
- **Ctrl+Shift+"** - Split pane horizontally (top/bottom)
- **Ctrl+Shift+X** - Close current pane
- **Ctrl+Shift+Z** - Toggle pane zoom (fullscreen)

### Tab Management
- **Ctrl+Shift+T** - New tab
- **Ctrl+Shift+[1-9]** - Switch to tab number
- **Ctrl+Tab** - Next tab
- **Ctrl+Shift+Tab** - Previous tab
- **Ctrl+Shift+W** - Close tab

### Copy/Paste
- **Ctrl+Shift+C** - Copy
- **Ctrl+Shift+V** - Paste
- **Ctrl+Shift+Space** - Start selection mode
- **Ctrl+Shift+X** - Copy mode (vim-like selection)

### Window/Session
- **Ctrl+Shift+N** - New window
- **Ctrl+Shift+Q** - Quit WezTerm
- **F11** - Toggle fullscreen

### Scrolling
- **Ctrl+Shift+PageUp/PageDown** - Scroll up/down
- **Ctrl+Shift+Home/End** - Scroll to top/bottom

### Font Size
- **Ctrl+Plus** - Increase font size
- **Ctrl+Minus** - Decrease font size
- **Ctrl+0** - Reset font size

### For Our Test
1. **Move between agents**: Ctrl+Shift+Arrow Keys
2. **Watch all panes**: Ctrl+Shift+Z to zoom/unzoom
3. **Copy messages**: Ctrl+Shift+C/V between panes

### Tips
- Active pane has colored border
- Tab titles show at top
- Right-click for context menu