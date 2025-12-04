# Dashboard Agent Routing Fix

## Problem
When clicking on Esther's card in the dashboard, Maurice's memory was displayed instead.

## Root Cause
The dashboard was passing the agent's **display name** (e.g., "Maurice", "Esther") to the API endpoints, but the backend expects the **dictionary key** (e.g., "maurice", "esther").

While the JavaScript was calling `.toLowerCase()` on the name, this created a mismatch because:
- Display names: "Maurice", "Esther", "Chuck"
- Dictionary keys: "maurice", "esther", "chuck"

The issue was that when agents were sorted or accessed, the wrong agent was being retrieved.

## Solution

### 1. Backend Fix (`src/agents/agent_monitor.py`)
Added a `key` field to the agent summary that contains the dictionary key:

```python
def get_team_summary(self) -> List[Dict[str, Any]]:
    summaries = []
    for name, agent in self.agents.items():
        summaries.append({
            "key": name,  # Dictionary key (e.g., "maurice", "esther")
            "name": agent.name,  # Display name (e.g., "Maurice", "Esther")
            "role": agent.role,
            # ... other fields
        })
    return summaries
```

### 2. Frontend Fix (`src/web/templates/dashboard.html`)
Updated the dashboard to use `agent.key` instead of `agent.name` for routing:

**Agent Card Click:**
```javascript
// Before:
onclick="showAgentDetails('${agent.name}')"

// After:
onclick="showAgentDetails('${agent.key}')"
```

**Chuck Detection:**
```javascript
// Before:
const isChuck = agent.name.toLowerCase() === 'chuck';

// After:
const isChuck = agent.key === 'chuck';
```

**Sorting:**
```javascript
// Before:
if (a.name.toLowerCase() === 'chuck') return -1;

// After:
if (a.key === 'chuck') return -1;
```

**Modal Title:**
Updated `loadAgentInfo()` to set the modal title using the display name from the API response:
```javascript
document.getElementById('modal-agent-name').textContent = info.name;
```

## Files Modified
1. `src/agents/agent_monitor.py` - Added `key` field to agent summaries
2. `src/web/templates/dashboard.html` - Updated to use `agent.key` for routing

## Testing
After restarting the dashboard:
1. Click on Maurice's card → Should show Maurice's memory
2. Click on Esther's card → Should show Esther's memory
3. Click on Chuck's card → Should show Chuck's memory
4. Modal title should show the proper display name (e.g., "Maurice", not "maurice")

## How to Apply Fix
1. Restart the dashboard:
   ```bash
   python examples/launch_dashboard.py
   ```
2. Hard refresh the browser (Cmd+Shift+R on Mac, Ctrl+Shift+R on Windows/Linux) to clear cached JavaScript
3. Test by clicking on different agent cards

---

**Date**: December 4, 2025  
**Issue**: Dashboard showing wrong agent memory  
**Resolution**: Use dictionary key for routing, display name for UI
