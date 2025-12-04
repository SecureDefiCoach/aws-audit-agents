# System Prompt Editor - Complete ✅

## What Was Added

The dashboard Memory tab now includes an **editable system prompt** feature that lets you view and modify an agent's system prompt in real-time.

## Features

### 1. View System Prompt
- System prompt is displayed at the top of the Memory tab
- Shows the complete system message that defines the agent's identity
- Includes role, capabilities, tools, and knowledge

### 2. Edit System Prompt
- Click the **"Edit"** button to enter edit mode
- Large textarea appears with the current system prompt
- Make any changes you need to fix problems or improve the prompt

### 3. Save Changes
- Click **"Save"** to update the agent's system prompt
- Changes are applied immediately to the agent's memory
- Agent will use the new prompt for all future reasoning

### 4. Cancel Editing
- Click **"Cancel"** to discard changes and return to view mode

## How to Use

1. **Open Dashboard**: Navigate to http://127.0.0.1:5000
2. **Click Agent Card**: Click on Maurice (or any agent)
3. **Go to Memory Tab**: Click the "Memory" tab
4. **View System Prompt**: See the current system prompt at the top
5. **Click Edit**: Click the "Edit" button
6. **Make Changes**: Edit the prompt text in the textarea
7. **Save**: Click "Save" to apply changes
8. **Verify**: The view updates to show your new prompt

## API Endpoints Added

### GET `/api/agents/<agent_name>/system_prompt`
Returns the agent's current system prompt.

**Response**:
```json
{
  "prompt": "You are Maurice, a Audit Manager..."
}
```

### POST `/api/agents/<agent_name>/system_prompt`
Updates the agent's system prompt.

**Request**:
```json
{
  "prompt": "You are Maurice, a Senior Audit Manager..."
}
```

**Response**:
```json
{
  "success": true,
  "message": "System prompt updated for maurice"
}
```

## What Problems This Solves

- **Fix Prompt Issues**: Quickly fix any problems you find in the system prompt
- **Improve Instructions**: Refine the agent's instructions based on behavior
- **Add Context**: Add specific context or constraints for the current task
- **Test Variations**: Try different prompt variations to improve performance
- **Real-time Updates**: No need to restart the agent or dashboard

## Example Use Cases

### Fix Role Description
**Before**: "You are Maurice, a Audit Manager."
**After**: "You are Maurice, an Audit Manager."

### Add Specific Instructions
Add to the prompt:
```
IMPORTANT: When creating workpapers, always include:
- Detailed risk analysis
- Specific evidence references
- Clear pass/fail criteria
```

### Adjust Tone
Change from:
```
You are an autonomous audit agent.
```
To:
```
You are a senior audit professional with 15 years of experience.
```

### Add Constraints
Add to the prompt:
```
CONSTRAINTS:
- Always consult your knowledge base before making decisions
- Escalate any findings with risk score > 15
- Document all reasoning in detail
```

## Technical Details

### Backend Changes
- Added `get_system_prompt()` endpoint in `src/web/agent_dashboard.py`
- Added `update_system_prompt()` endpoint in `src/web/agent_dashboard.py`
- System prompt is stored as the first message in `agent.memory`

### Frontend Changes
- Modified `loadAgentMemory()` function in `src/web/templates/dashboard.html`
- Added edit/save/cancel buttons and textarea
- Added `toggleEditPrompt()`, `cancelEditPrompt()`, and `saveSystemPrompt()` functions

### Files Modified
1. `src/web/agent_dashboard.py` - Added 2 new API endpoints
2. `src/web/templates/dashboard.html` - Enhanced Memory tab with editor

## Testing

Test the feature:
```bash
# Start dashboard
python3 examples/test_enhanced_dashboard.py

# Open browser to http://127.0.0.1:5000
# Click on Maurice
# Go to Memory tab
# Click Edit button
# Make changes
# Click Save
```

Test via API:
```bash
# Get current prompt
curl http://127.0.0.1:5000/api/agents/maurice/system_prompt

# Update prompt
curl -X POST http://127.0.0.1:5000/api/agents/maurice/system_prompt \
  -H "Content-Type: application/json" \
  -d '{"prompt": "You are Maurice, an experienced Audit Manager..."}'
```

## Benefits

✅ **Immediate Feedback**: See and fix prompt issues right away
✅ **No Restart Required**: Changes apply without restarting agents
✅ **Easy Iteration**: Quickly test different prompt variations
✅ **Full Control**: Complete access to the agent's system instructions
✅ **Professional UI**: Clean, intuitive editing interface

## Next Steps

You can now:
1. Review Maurice's system prompt for any issues
2. Make corrections or improvements
3. Test the agent with the updated prompt
4. Iterate on the prompt based on agent behavior

The system prompt is the foundation of agent behavior - having direct control over it gives you powerful debugging and optimization capabilities!

---
**Created**: December 4, 2025  
**Status**: ✅ Complete  
**Feature**: Editable System Prompt in Dashboard
