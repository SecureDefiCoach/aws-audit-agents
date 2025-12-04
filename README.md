# AWS Audit Agents

Autonomous AI agents that conduct professional AWS security audits using LLMs.

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up OpenAI API key
export OPENAI_API_KEY="your-key-here"

# 3. Start the dashboard
python examples/test_enhanced_dashboard.py

# 4. Open browser
open http://127.0.0.1:5000
```

**Full setup guide**: [docs/setup/QUICK_START.md](docs/setup/QUICK_START.md)

---

## 📖 Documentation

All documentation is organized in the [`docs/`](docs/) folder:

### Essential Guides
- **[Quick Start](docs/setup/QUICK_START.md)** - Get up and running in 5 minutes
- **[Dashboard Guide](docs/guides/WEB_DASHBOARD_GUIDE.md)** - Using the web dashboard
- **[Audit Phases](docs/audit-methodology/AUDIT_EXECUTION_PHASES.md)** - The 6 phases of audit execution
- **[Team Capabilities](docs/team/TEAM_SYSTEM_PROMPTS_AND_CAPABILITIES.md)** - All 7 agents' capabilities

### Documentation Categories
- 📁 **[docs/setup/](docs/setup/)** - Setup and installation guides
- 📁 **[docs/guides/](docs/guides/)** - User guides and how-tos
- 📁 **[docs/audit-methodology/](docs/audit-methodology/)** - Audit process documentation
- 📁 **[docs/team/](docs/team/)** - Team and agent information

**Browse all documentation**: [docs/README.md](docs/README.md)

---

## 🎯 What This Does

This system uses autonomous AI agents to conduct professional AWS security audits:

### The Audit Team (7 Agents)

**Management**
- **Maurice** - Audit Manager

**Senior Auditors**
- **Esther** - IAM & Logical Access (GPT-5)
- **Victor** - Logging & Monitoring (GPT-5)

**Staff Auditors**
- **Hillel** - IAM Support
- **Neil** - Encryption & Network Support
- **Juman** - Logging Support

**Company Representative**
- **Chuck** - CloudRetail IT Manager (provides evidence)

### The 6 Audit Phases

1. **Risk Assessment & Planning** - Identify high-risk areas
2. **Control Testing** - Test selected controls
3. **Workpaper Review** - Quality assurance
4. **Remediation Planning** - Plan fixes
5. **Audit Reporting** - Final report
6. **Follow-Up** - Verify remediation

---

## 🖥️ Web Dashboard

Monitor agents in real-time with the web dashboard:

![Dashboard Features](docs/dashboard-preview.png)

**Features**:
- Real-time agent monitoring
- Phase progression tracking
- System prompt editing
- Cost tracking
- Action history
- Memory inspection

**Guide**: [docs/guides/WEB_DASHBOARD_GUIDE.md](docs/guides/WEB_DASHBOARD_GUIDE.md)

---

## 🏗️ Project Structure

```
aws-audit-agents/
├── docs/                      # 📚 All documentation
│   ├── setup/                 # Setup guides
│   ├── guides/                # User guides
│   ├── audit-methodology/     # Audit process docs
│   └── team/                  # Team information
├── src/                       # Source code
│   ├── agents/                # Agent implementations
│   ├── aws/                   # AWS client wrappers
│   ├── web/                   # Web dashboard
│   └── utils/                 # Utilities
├── knowledge/                 # Agent knowledge bases
│   ├── shared/                # Shared procedures
│   ├── maurice/               # Manager knowledge
│   ├── esther/                # Senior auditor knowledge
│   ├── victor/                # Senior auditor knowledge
│   ├── chuck/                 # Company knowledge
│   └── [hillel|neil|juman]/   # Staff auditor knowledge
├── reference/                 # Reference materials
│   ├── audit-methodology/     # Audit standards
│   ├── isaca-audit-programs/  # ISACA programs
│   └── iam-policies/          # AWS policies
├── examples/                  # Example scripts
├── tests/                     # Unit tests
├── config/                    # Configuration files
└── templates/                 # CloudFormation templates
```

---

## 🔧 Key Features

### Autonomous Operation
- Agents reason independently using LLMs
- No step-by-step instructions needed
- Adapt to what they discover

### Professional Standards
- Follow ISACA audit methodology
- Generate professional workpapers
- Evidence-based findings
- Hierarchical review process

### Cost Optimization
- Strategic model selection (GPT-5 for seniors, GPT-4 for staff)
- 30-40% cost savings vs all GPT-5
- Transparent cost tracking

### Continuous Improvement
- Iterative refinement workflow
- System prompt editing
- Knowledge base updates
- Environment testing

---

## 🎓 Learning Path

### For New Users
1. [Quick Start](docs/setup/QUICK_START.md)
2. [Dashboard Guide](docs/guides/WEB_DASHBOARD_GUIDE.md)
3. [Audit Phases](docs/audit-methodology/AUDIT_EXECUTION_PHASES.md)

### For Developers
1. [LLM Agents Quickstart](docs/setup/LLM_AGENTS_QUICKSTART.md)
2. [Multi-Model Setup](docs/setup/MULTI_MODEL_SETUP.md)
3. [Agent Monitoring](docs/guides/AGENT_MONITORING_GUIDE.md)

### For Auditors
1. [Audit Execution Phases](docs/audit-methodology/AUDIT_EXECUTION_PHASES.md)
2. [Complete Workflow](docs/audit-methodology/COMPLETE_AUDIT_WORKFLOW_VISION.md)
3. [Team Capabilities](docs/team/TEAM_SYSTEM_PROMPTS_AND_CAPABILITIES.md)

---

## 🚦 System Requirements

- Python 3.8+
- OpenAI API key (GPT-4 Turbo and GPT-5 access)
- AWS account (optional, for real audits)
- 4GB RAM minimum
- Modern web browser

---

## 📊 Example Usage

### Run a Complete Audit

```python
from src.agents.agent_factory import AgentFactory

# Create the audit team
factory = AgentFactory()
team = factory.create_audit_team()

# Start with risk assessment
esther = team['esther']
esther.set_goal("Perform risk assessment for CloudRetail Inc")
result = esther.run_autonomously(max_iterations=15)

# View results in dashboard
# http://127.0.0.1:5000
```

### Monitor Agents

```python
from src.agents.agent_monitor import AgentMonitor

# Create monitor
monitor = AgentMonitor(team)

# Get team summary
summary = monitor.get_team_summary()

# Get cost breakdown
costs = monitor.get_cost_breakdown()
```

---

## 🔐 Security

- Read-only AWS access (no modifications)
- API keys stored in environment variables
- Audit logs for all actions
- Professional audit standards

**Guide**: [docs/setup/SECURITY_BEST_PRACTICES.md](docs/setup/SECURITY_BEST_PRACTICES.md)

---

## 💰 Cost Estimates

**Typical Audit** (3-5 controls):
- Risk Assessment: $0.50 - $1.00
- Control Testing: $2.00 - $4.00
- Workpaper Review: $0.50 - $1.00
- Reporting: $1.00 - $2.00
- **Total**: $4.00 - $8.00 per audit

**Cost Optimization**: 30-40% savings using mixed models (GPT-5 for seniors, GPT-4 for staff)

---

## 🤝 Contributing

Contributions welcome! Please:

1. Follow existing code style
2. Add tests for new features
3. Update documentation
4. Submit pull requests

---

## 📝 License

[Add your license here]

---

## 🆘 Support

- **Documentation**: [docs/README.md](docs/README.md)
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-repo/discussions)

---

## 🎯 Roadmap

- [ ] Additional AWS services (RDS, Lambda, ECS)
- [ ] Multi-cloud support (Azure, GCP)
- [ ] Compliance frameworks (SOC 2, ISO 27001)
- [ ] Advanced analytics dashboard
- [ ] Automated remediation suggestions
- [ ] Integration with ticketing systems

---

**Built with ❤️ using autonomous AI agents**

**Last Updated**: December 4, 2025
