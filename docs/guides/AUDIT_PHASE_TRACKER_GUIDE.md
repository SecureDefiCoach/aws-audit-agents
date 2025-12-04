# Audit Phase Tracker - Dashboard Feature

## Overview

The Audit Phase Tracker is a visual status indicator displayed at the top of the Agent Dashboard. It shows the current progress through the 6 major phases of audit execution with color-coded status indicators.

---

## Visual Design

### Phase Status Colors

- **White Background** (Not Started): Phase has not begun
- **Blue Background** (In Progress): Phase is currently active with pulsing animation
- **Green Background** (Complete): Phase has been completed with checkmark

### Phase Layout

The tracker displays all 6 phases in a horizontal grid:

```
┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│   Phase 1   │   Phase 2   │   Phase 3   │   Phase 4   │   Phase 5   │   Phase 6   │
│    Risk     │   Control   │  Workpaper  │Remediation  │   Audit     │  Follow-Up  │
│ Assessment  │   Testing   │   Review    │  Planning   │  Reporting  │             │
│             │             │             │             │             │             │
│ Not Started │ Not Started │ Not Started │ Not Started │ Not Started │ Not Started │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
```

---

## The 6 Audit Phases

### Phase 1: Risk Assessment & Planning
**Duration**: 2-3 weeks

**Activities**:
- Understanding the business
- Company inventory request
- Risk assessment and scoring
- Risk assessment review & approval
- Audit planning and control assignment

**Key Deliverable**: Approved risk assessment with 3-5 selected controls

---

### Phase 2: Control Testing (Fieldwork)
**Duration**: 3-4 weeks

**Activities**:
- Initial meeting with auditee
- Evidence collection
- Control testing
- Issue validation with auditee
- Workpaper completion

**Key Deliverable**: Complete control testing workpapers with evidence

---

### Phase 3: Workpaper Review & Quality Assurance
**Duration**: 1-2 weeks

**Activities**:
- Senior auditor review
- Workpaper revision (if needed)
- Audit manager review
- Official finding approval

**Key Deliverable**: Quality-assured workpapers with approved findings

---

### Phase 4: Remediation Planning
**Duration**: 1 week

**Activities**:
- Findings discussion with auditee
- Remediation plan development
- Timeline commitments

**Key Deliverable**: Remediation plans with timelines for each issue

---

### Phase 5: Audit Reporting
**Duration**: 1-2 weeks

**Activities**:
- Draft audit report
- Report review
- Report finalization & sign-off
- Closing meeting with management

**Key Deliverable**: Final signed audit report

---

### Phase 6: Follow-Up (Optional)
**Duration**: Varies

**Activities**:
- Remediation tracking
- Follow-up audit (if needed)
- Verification of issue resolution

**Key Deliverable**: Follow-up audit report or closure confirmation

---

## API Endpoints

### Get All Phase Status

```http
GET /api/audit/phases
```

**Response**:
```json
[
  {
    "number": 1,
    "name": "Risk Assessment & Planning",
    "status": "complete"
  },
  {
    "number": 2,
    "name": "Control Testing (Fieldwork)",
    "status": "in-progress"
  },
  {
    "number": 3,
    "name": "Workpaper Review & QA",
    "status": "not-started"
  },
  ...
]
```

---

### Update Phase Status

```http
POST /api/audit/phases
Content-Type: application/json

{
  "phase": 2,
  "status": "in-progress"
}
```

**Valid Status Values**:
- `"not-started"` - Phase has not begun
- `"in-progress"` - Phase is currently active
- `"complete"` - Phase has been completed

**Response**:
```json
{
  "success": true,
  "message": "Phase 2 status updated to 'in-progress'"
}
```

---

### Update Specific Phase

```http
PUT /api/audit/phases/2
Content-Type: application/json

{
  "status": "complete"
}
```

**Response**:
```json
{
  "success": true,
  "phase": 2,
  "status": "complete"
}
```

---

## Usage Examples

### Python - Update Phase Status

```python
import requests

def update_phase(phase_num, status):
    """Update audit phase status."""
    response = requests.post(
        'http://127.0.0.1:5000/api/audit/phases',
        json={'phase': phase_num, 'status': status}
    )
    return response.json()

# Start Phase 1
update_phase(1, 'in-progress')

# Complete Phase 1
update_phase(1, 'complete')

# Start Phase 2
update_phase(2, 'in-progress')
```

---

### JavaScript - Update Phase Status

```javascript
async function updatePhase(phaseNumber, status) {
    const response = await fetch('/api/audit/phases', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            phase: phaseNumber,
            status: status
        })
    });
    
    return await response.json();
}

// Start Phase 1
await updatePhase(1, 'in-progress');

// Complete Phase 1
await updatePhase(1, 'complete');
```

---

### cURL - Update Phase Status

```bash
# Start Phase 1
curl -X POST http://127.0.0.1:5000/api/audit/phases \
  -H "Content-Type: application/json" \
  -d '{"phase": 1, "status": "in-progress"}'

# Complete Phase 1
curl -X POST http://127.0.0.1:5000/api/audit/phases \
  -H "Content-Type: application/json" \
  -d '{"phase": 1, "status": "complete"}'
```

---

## Demo Script

Run the included demo to see the phase tracker in action:

```bash
python examples/test_phase_tracker.py
```

This will:
1. Start the dashboard web server
2. Create a sample audit team
3. Simulate progression through all 6 phases
4. Update the dashboard in real-time

Open your browser to `http://127.0.0.1:5000` to watch the phases update!

---

## Persistence

Phase status is automatically saved to `output/audit_phase_status.json` and persists across dashboard restarts.

**Example Status File**:
```json
{
  "1": "complete",
  "2": "in-progress",
  "3": "not-started",
  "4": "not-started",
  "5": "not-started",
  "6": "not-started"
}
```

---

## Integration with Agents

Agents can automatically update phase status as they complete work:

```python
from src.agents.agent_factory import AgentFactory
import requests

# Create agents
factory = AgentFactory()
team = factory.create_audit_team()

# Esther completes risk assessment
esther = team['esther']
esther.set_goal("Perform risk assessment for CloudRetail Inc")
result = esther.run_autonomously()

# Update phase status when complete
if result['status'] == 'complete':
    requests.post(
        'http://127.0.0.1:5000/api/audit/phases',
        json={'phase': 1, 'status': 'complete'}
    )
```

---

## Responsive Design

The phase tracker automatically adapts to different screen sizes:

- **Desktop (>1200px)**: 6 columns (all phases visible)
- **Tablet (768-1200px)**: 3 columns (2 rows)
- **Mobile (480-768px)**: 2 columns (3 rows)
- **Small Mobile (<480px)**: 1 column (6 rows)

---

## Future Enhancements

Potential additions to the phase tracker:

1. **Phase Details Modal**: Click a phase to see detailed progress
2. **Sub-Phase Tracking**: Track individual steps within each phase
3. **Time Tracking**: Show elapsed time and estimated completion
4. **Agent Assignment**: Show which agents are working on each phase
5. **Milestone Markers**: Highlight critical checkpoints within phases
6. **Progress Percentage**: Show completion percentage for in-progress phases
7. **Phase Dependencies**: Visual indicators of phase dependencies
8. **Historical Timeline**: View past audit phase progressions

---

## Troubleshooting

### Phase Status Not Updating

1. Check that the dashboard is running: `http://127.0.0.1:5000`
2. Verify API endpoint is accessible: `curl http://127.0.0.1:5000/api/audit/phases`
3. Check browser console for JavaScript errors
4. Ensure phase number is 1-6 and status is valid

### Phase Status Not Persisting

1. Check that `output/` directory exists and is writable
2. Verify `output/audit_phase_status.json` is being created
3. Check file permissions

### Visual Issues

1. Clear browser cache and reload
2. Check browser console for CSS errors
3. Verify all CSS classes are properly defined

---

## Technical Details

### CSS Classes

- `.phase-tracker` - Container for the entire phase tracker
- `.phases-container` - Grid container for phase boxes
- `.phase-box` - Individual phase container
- `.phase-box.not-started` - White background (default)
- `.phase-box.in-progress` - Blue background with pulse animation
- `.phase-box.complete` - Green background with checkmark
- `.phase-number` - Circular phase number indicator
- `.phase-title` - Phase name text
- `.phase-subtitle` - Status text

### JavaScript Functions

- `updatePhaseStatus(phaseNumber, status)` - Update a phase's visual status
- `loadPhaseStatus()` - Load phase status from backend
- `setPhase(phaseNumber, status)` - Update phase and save to backend

---

**Created**: December 4, 2025  
**Purpose**: Document the Audit Phase Tracker dashboard feature  
**Location**: Top of Agent Dashboard at http://127.0.0.1:5000
