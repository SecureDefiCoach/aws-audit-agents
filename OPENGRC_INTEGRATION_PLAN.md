# OpenGRC Integration Plan

## Why This Makes Sense

Integrating OpenGRC will transform your audit agents from file-based to enterprise-grade:

### Current Limitations
- ❌ Workpapers stored as markdown files
- ❌ No structured control framework
- ❌ Evidence scattered in folders
- ❌ No risk register
- ❌ Manual reporting
- ❌ No audit trail
- ❌ Difficult to track testing status

### With OpenGRC
- ✅ Structured GRC database
- ✅ API-driven control management
- ✅ Centralized evidence repository
- ✅ Risk register with scoring
- ✅ Automated reporting
- ✅ Complete audit trail
- ✅ Real-time testing status

## OpenGRC Capabilities

### Core Features
1. **Risk Management**
   - Risk register
   - Risk assessments
   - Risk scoring (likelihood × impact)
   - Risk treatment plans

2. **Control Framework**
   - Control library (SOC 2, ISO 27001, NIST, etc.)
   - Control mapping
   - Control ownership
   - Control testing schedules

3. **Compliance Management**
   - Compliance requirements
   - Gap analysis
   - Remediation tracking
   - Compliance reporting

4. **Evidence Management**
   - Evidence repository
   - Evidence linking to controls
   - Evidence versioning
   - Evidence review workflow

5. **Audit Management**
   - Audit planning
   - Test procedures
   - Findings management
   - Workpaper generation

## Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Audit Agents                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │  Esther  │  │  Maurice │  │   Neil   │  │  Chuck   │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
│       │             │              │             │         │
│       └─────────────┴──────────────┴─────────────┘         │
│                          │                                  │
│                          ▼                                  │
│              ┌───────────────────────┐                     │
│              │  OpenGRC Client Tool  │                     │
│              └───────────┬───────────┘                     │
└──────────────────────────┼─────────────────────────────────┘
                           │
                           │ REST API
                           ▼
                ┌──────────────────────┐
                │     OpenGRC Server   │
                │                      │
                │  • Risk Register     │
                │  • Control Framework │
                │  • Evidence Repo     │
                │  • Audit Management  │
                │  • Reporting         │
                └──────────────────────┘
```

## Implementation Plan

### Phase 1: OpenGRC Client Tool (Day 1)
Create a new tool that agents can use to interact with OpenGRC:

```python
class OpenGRCTool(Tool):
    """Tool for interacting with OpenGRC API"""
    
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key
        
    # Risk Management
    def create_risk(self, title, description, likelihood, impact)
    def get_risk(self, risk_id)
    def update_risk(self, risk_id, **kwargs)
    def list_risks(self, filters=None)
    
    # Control Management
    def get_control(self, control_id)
    def list_controls(self, framework=None)
    def update_control_status(self, control_id, status)
    def link_evidence_to_control(self, control_id, evidence_id)
    
    # Evidence Management
    def upload_evidence(self, file_path, description, control_ids)
    def get_evidence(self, evidence_id)
    def list_evidence(self, control_id=None)
    
    # Testing
    def create_test_result(self, control_id, result, findings)
    def get_test_results(self, control_id)
    
    # Reporting
    def generate_audit_report(self, audit_id)
    def get_compliance_status(self, framework)
```

### Phase 2: Update Agent Workflows (Day 2)
Modify agents to use OpenGRC instead of files:

**Esther (Senior Auditor)**
- Query controls from OpenGRC
- Document test results in OpenGRC
- Upload evidence to OpenGRC
- Link evidence to controls

**Maurice (Audit Manager)**
- Create audit in OpenGRC
- Assign controls to auditors
- Review test results
- Generate reports from OpenGRC

**Neil/Hillel/Juman (Staff Auditors)**
- Get assigned controls from OpenGRC
- Document testing in OpenGRC
- Upload evidence

**Chuck (IT Manager)**
- Provide evidence through OpenGRC
- View audit status
- Respond to findings

### Phase 3: Dashboard Integration (Day 3)
Update dashboard to show OpenGRC data:
- Control testing status
- Risk heatmap
- Compliance dashboard
- Evidence repository view

## API Endpoints Needed

### Risk Management
```
GET    /api/risks
POST   /api/risks
GET    /api/risks/{id}
PUT    /api/risks/{id}
DELETE /api/risks/{id}
```

### Control Management
```
GET    /api/controls
GET    /api/controls/{id}
PUT    /api/controls/{id}/status
POST   /api/controls/{id}/evidence
GET    /api/controls/{id}/test-results
```

### Evidence Management
```
GET    /api/evidence
POST   /api/evidence
GET    /api/evidence/{id}
PUT    /api/evidence/{id}
DELETE /api/evidence/{id}
```

### Testing
```
POST   /api/test-results
GET    /api/test-results/{id}
PUT    /api/test-results/{id}
GET    /api/controls/{id}/test-results
```

### Reporting
```
GET    /api/reports/audit/{audit_id}
GET    /api/reports/compliance/{framework}
GET    /api/reports/risk-register
```

## Benefits for Agents

### Before (File-Based)
```python
# Esther creates a workpaper
workpaper = """
# Workpaper WP-IAM-001
Control: User Access Reviews
Testing: Reviewed 50 users
Finding: 3 users with excessive permissions
"""
with open('output/workpapers/WP-IAM-001.md', 'w') as f:
    f.write(workpaper)
```

### After (OpenGRC)
```python
# Esther documents in OpenGRC
opengrc.create_test_result(
    control_id='IAM-001',
    result='FAIL',
    findings=[
        {
            'severity': 'MEDIUM',
            'description': '3 users with excessive permissions',
            'affected_items': ['user1@example.com', 'user2@example.com', 'user3@example.com']
        }
    ],
    evidence_ids=['evidence-123', 'evidence-124']
)
```

## Migration Strategy

### Option 1: Clean Start
- Set up OpenGRC fresh
- Import control framework
- Agents start using OpenGRC immediately

### Option 2: Gradual Migration
- Keep file-based system
- Add OpenGRC in parallel
- Agents write to both
- Migrate over time

### Option 3: Hybrid
- Use OpenGRC for structured data (controls, risks, test results)
- Keep files for unstructured data (notes, drafts)

## Recommended Approach

**Start with Option 1 (Clean Start)** because:
1. You're early in development
2. No legacy data to migrate
3. Cleaner architecture
4. Easier to maintain

## Next Steps

### Tomorrow's Tasks
1. **Research OpenGRC API**
   - Review API documentation
   - Test API endpoints
   - Understand data models

2. **Create OpenGRC Client**
   - Build Python client for OpenGRC API
   - Add authentication
   - Implement core methods

3. **Create OpenGRC Tool**
   - Wrap client in Tool class
   - Add to agent toolkit
   - Test with Esther

4. **Update One Workflow**
   - Pick simple workflow (e.g., control testing)
   - Modify Esther to use OpenGRC
   - Test end-to-end

5. **Document Integration**
   - API usage examples
   - Agent workflow changes
   - Benefits realized

## Questions to Answer

1. **OpenGRC Setup**
   - Self-hosted or cloud?
   - What's the base URL?
   - How do we get API keys?

2. **Control Framework**
   - Which framework to use? (SOC 2, ISO 27001, NIST CSF?)
   - Do we import pre-built framework?
   - Custom controls needed?

3. **Data Model**
   - How are controls structured?
   - How is evidence linked?
   - What's the testing workflow?

4. **Authentication**
   - API key authentication?
   - OAuth?
   - Service account?

## Resources Needed

- OpenGRC API documentation
- OpenGRC instance (dev/test)
- API credentials
- Sample control framework

## Success Metrics

After integration:
- ✅ Agents can query controls from OpenGRC
- ✅ Agents can document test results in OpenGRC
- ✅ Agents can upload evidence to OpenGRC
- ✅ Dashboard shows OpenGRC data
- ✅ Can generate audit report from OpenGRC
- ✅ Complete audit trail in OpenGRC

## Timeline

- **Day 1**: OpenGRC client + tool (4-6 hours)
- **Day 2**: Update agent workflows (4-6 hours)
- **Day 3**: Dashboard integration (2-4 hours)
- **Day 4**: Testing + refinement (2-4 hours)

**Total**: 2-3 days for full integration

This is a great move - OpenGRC will make your agents much more powerful and professional! 🚀
