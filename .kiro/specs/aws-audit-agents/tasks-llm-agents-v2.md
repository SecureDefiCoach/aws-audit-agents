# Implementation Tasks - LLM-Based Audit Agents (REVISED)

**Key Changes from V1:**
- Risk assessment moved to Phase 2 (was Phase 4)
- ISACA integration happens early
- Agents are generalists, not specialists
- Dynamic task assignment based on risk assessment
- Interview simulation added
- Follows real audit workflow: Risk → Plan → Test → Report

---

## Phase 1: Foundation & Agent Creation ✅

- [x] 1. Set up LLM integration infrastructure
  - Install Ollama for local development
  - Create LLM client wrapper supporting multiple providers (Ollama, Claude, GPT-4)
  - Implement rate limiting for API calls
  - Add cost tracking for LLM usage
  - _Requirements: 9.1, 9.7_

- [x] 2. Implement base AuditAgent class with LLM reasoning
  - Create AuditAgent base class with LLM integration
  - Implement goal setting and tracking
  - Implement reasoning loop (reason → act → document)
  - Add memory/context management
  - Add tool registration and execution
  - _Requirements: 9.1, 9.2, 9.3_

- [x] 3. Create Tool interface and base tools
  - Define Tool base class with name, description, parameters
  - Implement WorkpaperTool for creating audit documentation
  - Implement EvidenceTool for storing and referencing evidence
  - Add tool execution error handling
  - _Requirements: 9.1, 9.8_

- [x] 4. Implement Esther (first LLM-based agent)
  - Create EstherAgent class extending AuditAgent
  - Define Esther's role and capabilities
  - Integrate IAMClient as a tool
  - Implement goal: "Assess IAM risks and document findings"
  - Add workpaper generation with reasoning documentation
  - _Requirements: 9.1, 9.2, 9.4, 9.8_

- [ ] 5. Test Esther against CloudRetail AWS account
  - Run Esther with goal to assess IAM risks
  - Verify Esther collects IAM evidence from AWS
  - Verify Esther creates workpaper with findings
  - Review workpaper for quality of reasoning
  - Verify evidence references are correct
  - _Requirements: 3.2, 4.2, 9.5, 9.8_

- [x] 5.5. Implement Agent Knowledge System ✅
  - Create knowledge folder structure (`knowledge/{agent_name}/`)
  - Add knowledge loading to AuditAgent base class
  - Each agent loads procedures from their knowledge folder
  - Knowledge is added to agent's LLM context
  - Create sample procedures for Maurice (risk assessment, audit planning)
  - Create sample procedures for senior auditors (control testing, interviews)
  - Document which procedures were used in workpapers
  - _Requirements: 9.1, 9.2_
  - **Status**: Core implementation complete. 5 procedures created. Tested and working.
  - **Remaining**: Add more knowledge files for Chuck, Victor, Neil, Juman

- [x] 5.6. Implement Agent Task Management System ✅
  - Create task folder structure (`tasks/{agent_name}-tasks.md`)
  - Create TaskManagementTool for agents
  - Agents can read their own task list
  - Agents can create tasks for themselves
  - Agents can assign tasks to other agents
  - Agents can mark tasks complete
  - Add task visibility to dashboard
  - Track who assigned what to whom
  - _Requirements: 9.2, 9.6_
  - **Status**: Core implementation complete. All task operations working. Tested.
  - **Remaining**: Dashboard integration for task visibility

---

## Phase 2: ISACA Integration & Risk Assessment

**CRITICAL: This phase must complete before control testing begins**

- [ ] 6. Load and parse ISACA Audit Program
  - Create ISACA CSV parser
  - Load all control domains (Logical Access, Encryption, Network, Logging, etc.)
  - Parse control objectives, testing steps, and evidence requirements
  - Create control library data structure (~45 controls)
  - Map controls to AWS services and APIs
  - Create ISACAControlTool for agents to query controls
  - _Requirements: 7.1, 7.2_

- [ ] 7. Implement Risk Assessment workflow
  - Agents assess CloudRetail AWS environment
  - Identify high-risk areas across all domains
  - Document inherent risks (what could go wrong)
  - Document residual risks (after considering existing controls)
  - Prioritize controls for testing based on risk scores
  - Create risk assessment workpaper
  - Maurice reviews and approves risk assessment
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7_

- [ ] 8. Generate Audit Plan from Risk Assessment
  - Select controls to test based on approved risk assessment
  - For each selected control, extract ISACA testing steps
  - Convert ISACA testing steps into Kiro tasks
  - Allocate simulated audit hours to high-risk areas
  - Create audit plan document with scope and procedures
  - Maurice reviews and approves audit plan
  - _Requirements: 2.8, 2.9, 2.10_

---

## Phase 3: Agent Capabilities for Control Testing

- [ ] 9. Create Interview Simulation Tool
  - Create InterviewTool for simulating auditee responses
  - Generate realistic responses based on control context
  - Document interview questions and responses in workpapers
  - Keep simple (no separate auditee agents for MVP)
  - Include interview metadata (date, interviewee role, topic)
  - _Requirements: 4.1, 9.8_

- [ ] 10. Make Agents Generalist (Remove Hardcoded Specialization)
  - Remove IAM-only restriction from EstherAgent
  - Create GenericAuditAgent that can handle any control domain
  - All agents can execute any ISACA testing step
  - Agents dynamically load required AWS client tools based on control
  - Update agent factory to create generalist agents
  - _Requirements: 9.1, 9.2_

- [ ] 11. Implement additional AWS client tools
  - Create S3Tool (wraps S3Client for encryption testing)
  - Create VPCTool (wraps VPCClient for network testing)
  - Create CloudTrailTool (wraps CloudTrailClient for logging testing)
  - Create EC2Tool (wraps EC2Client for instance testing)
  - All tools follow same pattern as IAMTool
  - _Requirements: 3.3, 3.4, 3.5, 3.6, 3.7_

- [ ] 12. Implement AuditOrchestrator with Dynamic Assignment
  - Create Orchestrator class to coordinate agents
  - Load audit plan (selected controls and testing steps)
  - Dynamically assign controls to available agents
  - Load balancing based on agent capacity and workload
  - Track progress of control testing
  - Handle agent communication and message routing
  - Monitor for blocked agents and reassign work
  - _Requirements: 9.6, 9.7_

---

## Phase 4: Execute Full Audit Workflow

- [ ] 13. Run Complete End-to-End Audit
  - **Step 1: Risk Assessment**
    - Orchestrator assigns risk assessment to senior auditors
    - Agents assess CloudRetail environment
    - Create risk assessment workpaper
    - Maurice approves
  - **Step 2: Audit Planning**
    - Generate audit plan from approved risks
    - Select controls to test (subset of 45)
    - Maurice approves audit plan
  - **Step 3: Control Testing**
    - Orchestrator assigns controls to agents dynamically
    - Agents execute ISACA testing steps
    - Agents conduct simulated interviews
    - Agents collect AWS evidence
    - Agents create workpapers for each control
    - Maurice reviews workpapers
  - **Step 4: Findings & Reporting**
    - Aggregate findings from all workpapers
    - Generate final audit report
  - _Requirements: All_

---

## Phase 5: Reporting & Polish

- [ ] 14. Implement final audit report generation
  - Aggregate findings from all workpapers
  - Generate executive summary
  - Create detailed findings report with Pass/Fail for each control
  - Add evidence appendix
  - Include risk assessment and audit plan as appendices
  - Maurice signs off on final report
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ] 15. Add budget tracking and reporting
  - Track simulated audit hours by agent
  - Track actual LLM API costs
  - Generate budget variance report
  - Compare budgeted vs actual hours
  - Show cost per control tested
  - _Requirements: 2.11, 2.12_

- [ ] 16. Add ISACA modernization recommendations
  - Agents analyze ISACA 2022 audit program
  - Identify testing steps that can be fully automated
  - Identify steps that still require human judgment
  - Recommend 2025 tools and approaches
  - Document modernization recommendations in report
  - Compare traditional vs agentic audit efficiency
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ] 17. Polish and documentation
  - Create comprehensive README with setup instructions
  - Document LLM provider options (Ollama, Claude, GPT-4)
  - Add cost estimation guide
  - Create demo video script
  - Write article draft showcasing agent capabilities
  - Document the Risk → Plan → Test → Report workflow
  - _Requirements: All_

---

## Key Workflow Principles

**1. Risk-Driven Approach**
- Nothing happens until risk assessment is complete
- Controls are selected based on risk, not pre-assigned domains
- High-risk areas get more testing resources

**2. ISACA-Compliant**
- All testing follows ISACA audit program procedures
- Testing steps come directly from ISACA CSV files
- Workpapers reference ISACA control objectives

**3. Dynamic Assignment**
- Agents are generalists, not specialists
- Orchestrator assigns work based on availability
- Any agent can test any control

**4. Interview Documentation**
- Agents simulate interviews with auditees
- Interview notes documented in workpapers
- Keeps it simple (no separate auditee agents)

**5. Full Audit Cycle**
- Demonstrates complete workflow: Risk → Plan → Test → Report
- Maurice approves at each gate
- Realistic audit timeline and process

---

## Notes

- **Development**: Use Ollama (free) for all development and testing
- **Demo**: Use Claude Haiku ($1-5) or GPT-4 Turbo for final demonstration
- **Rate Limiting**: Limit to 10 LLM calls/minute to stay within free tiers
- **Pace**: Slow execution is OK - reflects realistic audit timeline
- **Focus**: Agent reasoning quality matters more than speed
- **Documentation**: All meaningful work goes in workpapers, not logs
- **ISACA First**: Risk assessment determines scope, not pre-defined agent roles

---

## What Changed from V1

**Removed:**
- ❌ Task 6: Implement Chuck (specialized encryption agent)
- ❌ Task 7: Implement Victor (specialized logging agent)
- ❌ Task 10: Implement adaptive agent behavior (now built-in)

**Added:**
- ✅ Task 6: Load ISACA Audit Program
- ✅ Task 9: Interview Simulation Tool
- ✅ Task 10: Make Agents Generalist
- ✅ Task 11: Additional AWS client tools

**Reordered:**
- ⬆️ Risk Assessment (Task 7, was Task 12)
- ⬆️ Audit Planning (Task 8, was Task 13)
- ⬆️ Orchestrator (Task 12, was Task 11)

**Why:**
- Follows real audit workflow
- Risk assessment drives everything
- Agents are flexible, not hardcoded
- ISACA integration is foundational
- More realistic and impressive demo
