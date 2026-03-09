"""Generate synthetic enterprise risk management data for demo and GitHub use."""
from __future__ import annotations

from pathlib import Path
import random
import numpy as np
import pandas as pd


SEED = 42
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data"


RISKS = [
    ("Technology Risk", "Dependence on cloud platforms and endpoint security creates exposure to cyber incidents and system outages.", 5, 4, "IT Security"),
    ("Financial Stability", "Shifts in tuition revenue, grants, and partner funding can pressure operating margins.", 5, 3, "Finance"),
    ("Service Disruption", "Severe weather, vendor outages, or facility incidents could disrupt core services.", 4, 3, "Operations"),
    ("Market Demand", "Changes in learner preferences and employer demand may reduce program relevance.", 4, 3, "Strategy"),
    ("Facilities & Equipment", "Aging equipment and deferred maintenance can affect safety and delivery quality.", 4, 2, "Facilities"),
    ("Staffing Challenges", "Turnover and hiring delays can reduce service continuity and institutional knowledge.", 4, 3, "HR"),
    ("Health & Safety", "Safety incidents, emergency response gaps, or training failures can harm people and operations.", 5, 2, "Safety"),
    ("Regulatory Compliance", "Policy, privacy, and reporting obligations may be missed without strong controls.", 5, 2, "Compliance"),
    ("Reputation Management", "Public perception can deteriorate from misinformation, service failures, or negative coverage.", 4, 2, "Communications"),
    ("Third-Party Risk", "Key vendors may fail to meet security, uptime, or contractual expectations.", 4, 3, "Procurement"),
]

PLANS = {
    "Technology Risk": ["Identity & Access Management", "Security Monitoring", "Staff Awareness"],
    "Financial Stability": ["Revenue Diversification", "Scenario Planning", "Reserve Management"],
    "Service Disruption": ["Business Continuity Planning", "Remote Work Readiness", "Insurance Review"],
    "Market Demand": ["Program Review", "Advisory Council", "Curriculum Refresh"],
    "Facilities & Equipment": ["Preventive Maintenance", "Capital Planning", "Safety Inspections"],
    "Staffing Challenges": ["Compensation Review", "Professional Development", "Workload Balancing"],
    "Health & Safety": ["Safety Protocols", "Emergency Drills", "Training Program"],
    "Regulatory Compliance": ["Policy Review", "Internal Audit", "Control Monitoring"],
    "Reputation Management": ["Proactive Communications", "Sentiment Monitoring", "Issue Escalation"],
    "Third-Party Risk": ["Vendor Due Diligence", "Contract Controls", "Continuity Testing"],
}

ACTION_TEMPLATES = {
    "Identity & Access Management": ["Review privileged accounts", "Enforce MFA for all staff", "Rotate stale credentials", "Disable inactive accounts", "Test SSO failover"],
    "Security Monitoring": ["Tune SIEM alerts", "Patch critical systems", "Review endpoint detections", "Run phishing simulation", "Validate backup restore"],
    "Staff Awareness": ["Launch awareness campaign", "Update training content", "Track completion rates", "Target high-risk groups", "Publish monthly security tips"],
    "Revenue Diversification": ["Launch short certificate", "Create employer-sponsored cohort", "Expand alumni giving outreach", "Submit grant proposals", "Pilot executive workshop"],
    "Scenario Planning": ["Refresh revenue forecast", "Model downside scenarios", "Review expense triggers", "Update cost containment plan", "Review pricing assumptions"],
    "Reserve Management": ["Set reserve policy", "Track reserve ratio", "Review liquidity targets", "Rebalance reserve allocation", "Present reserve dashboard"],
    "Business Continuity Planning": ["Update continuity plan", "Identify critical processes", "Confirm recovery owners", "Map alternate workflows", "Review contact trees"],
    "Remote Work Readiness": ["Test VPN capacity", "Provision spare devices", "Document remote support steps", "Run remote access drill", "Review collaboration tooling"],
    "Insurance Review": ["Review policy coverage", "Confirm renewal dates", "Assess deductibles", "Validate insured assets", "Summarize coverage gaps"],
    "Program Review": ["Review enrollment trends", "Compare competitor offerings", "Analyze completion rates", "Survey graduates", "Draft improvement actions"],
    "Advisory Council": ["Recruit industry advisors", "Schedule quarterly meeting", "Capture recommendations", "Review skills demand", "Share follow-up plan"],
    "Curriculum Refresh": ["Pilot revised module", "Map curriculum to demand", "Review learning outcomes", "Test new delivery format", "Retire low-demand content"],
    "Preventive Maintenance": ["Inspect HVAC systems", "Service lab equipment", "Update maintenance log", "Replace worn components", "Test alarms and sensors"],
    "Capital Planning": ["Refresh asset inventory", "Prioritize major replacements", "Estimate capital needs", "Review lifecycle schedules", "Publish capital roadmap"],
    "Safety Inspections": ["Complete site walkthrough", "Log hazard findings", "Verify corrective actions", "Review signage placement", "Confirm PPE availability"],
    "Compensation Review": ["Benchmark salaries", "Review pay compression", "Update compensation bands", "Draft retention proposal", "Prepare leadership brief"],
    "Professional Development": ["Create training calendar", "Fund certifications", "Launch mentoring program", "Track skill development", "Evaluate training impact"],
    "Workload Balancing": ["Review capacity by team", "Reassign low-value work", "Document process bottlenecks", "Add temporary support", "Measure overtime trends"],
    "Safety Protocols": ["Review incident procedures", "Replenish first aid kits", "Audit access controls", "Inspect emergency exits", "Refresh safety signage"],
    "Emergency Drills": ["Run fire drill", "Run tabletop exercise", "Test notification system", "Capture lessons learned", "Retest corrective items"],
    "Training Program": ["Update onboarding content", "Deliver annual refresher", "Assess knowledge retention", "Track attendance", "Tailor role-based training"],
    "Policy Review": ["Review policy inventory", "Update privacy notice", "Clarify retention rules", "Publish policy changes", "Obtain annual attestations"],
    "Internal Audit": ["Test key controls", "Review exception logs", "Audit access reviews", "Validate evidence retention", "Report audit findings"],
    "Control Monitoring": ["Track overdue controls", "Review control failures", "Update risk indicators", "Escalate unresolved items", "Refresh compliance dashboard"],
    "Proactive Communications": ["Prepare holding statements", "Publish monthly updates", "Coordinate stakeholder messaging", "Review spokesperson list", "Monitor issue response times"],
    "Sentiment Monitoring": ["Track media mentions", "Monitor social channels", "Review support trends", "Flag misinformation", "Summarize weekly sentiment"],
    "Issue Escalation": ["Define escalation matrix", "Log reputational incidents", "Assign response owners", "Conduct post-incident review", "Update crisis playbook"],
    "Vendor Due Diligence": ["Assess vendor controls", "Review SOC reports", "Score critical suppliers", "Confirm data handling terms", "Track remediation items"],
    "Contract Controls": ["Standardize security clauses", "Review renewal risks", "Map critical dependencies", "Confirm SLA metrics", "Update exit provisions"],
    "Continuity Testing": ["Run vendor failover test", "Verify alternate suppliers", "Test manual workaround", "Review communication paths", "Document lessons learned"],
}

OWNERS = {
    "Technology Risk": ["Director of IT Security", "Infrastructure Manager", "HR Systems Lead"],
    "Financial Stability": ["Controller", "FP&A Manager", "Director of Partnerships"],
    "Service Disruption": ["Operations Director", "Business Continuity Manager", "Facilities Manager"],
    "Market Demand": ["Dean of Programs", "Director of Strategy", "Employer Partnerships Lead"],
    "Facilities & Equipment": ["Facilities Director", "Maintenance Supervisor", "Lab Operations Manager"],
    "Staffing Challenges": ["HR Director", "Talent Acquisition Lead", "Operations VP"],
    "Health & Safety": ["Safety Manager", "Campus Operations Lead", "Emergency Coordinator"],
    "Regulatory Compliance": ["Compliance Officer", "Privacy Lead", "Internal Audit Manager"],
    "Reputation Management": ["Communications Director", "Student Success Director", "Chief of Staff"],
    "Third-Party Risk": ["Procurement Manager", "Vendor Risk Analyst", "IT Compliance Lead"],
}


def build_data(seed: int = SEED) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Create synthetic risk register and action tracker datasets."""
    random.seed(seed)
    np.random.seed(seed)

    risk_rows: list[dict] = []
    action_rows: list[dict] = []

    for category, desc, impact, probability, risk_area in RISKS:
        priority = impact * probability
        for plan in PLANS[category]:
            owner = random.choice(OWNERS[category])
            n_actions = random.randint(4, 5)
            chosen_actions = ACTION_TEMPLATES[plan][:n_actions]
            planned_impact = round(n_actions * 0.10, 2)

            risk_rows.append(
                {
                    "risk_id": f"R{len(risk_rows)+1:03d}",
                    "risk_category": category,
                    "risk_description": desc,
                    "impact_level": impact,
                    "probability_level": probability,
                    "priority_level": priority,
                    "mitigation_plan": plan,
                    "planned_mitigation_impact": planned_impact,
                    "owner": owner,
                    "status_summary": random.choice(["On Track", "On Track", "On Track", "Needs Attention"]),
                    "risk_area": risk_area,
                }
            )

            for action in chosen_actions:
                status = random.choices(
                    ["Pending", "In Progress", "Complete", "Overdue"],
                    weights=[3, 4, 2, 1],
                    k=1,
                )[0]
                due_month = random.choice([3, 4, 5, 6, 7, 8, 9, 10, 11])
                due_day = random.choice([5, 12, 15, 20, 25, 28])

                action_rows.append(
                    {
                        "action_id": f"A{len(action_rows)+1:04d}",
                        "risk_category": category,
                        "mitigation_plan": plan,
                        "action": action,
                        "mitigation_impact": 0.10,
                        "deadline": f"2025-{due_month:02d}-{due_day:02d}",
                        "owner": owner,
                        "status": status,
                        "erm_bcm_management_type": random.choice(
                            [
                                "Risk Evaluation",
                                "Risk Treatment",
                                "Monitoring & Review",
                                "Recording & Reporting",
                            ]
                        ),
                        "management_detail": random.choice(
                            [
                                "Alignment",
                                "Focus",
                                "Reduction",
                                "Distribution",
                                "Tolerance",
                                "Execution",
                                "Validation",
                                "Adaptation",
                                "Foresight",
                                "Accountability",
                                "Learning",
                                "Communication",
                            ]
                        ),
                        "notes": random.choice(
                            [
                                "Synthetic sample record",
                                "Synthetic action for demo use",
                                "Generated for public repository",
                                "Use for testing and prototyping",
                            ]
                        ),
                    }
                )

    return pd.DataFrame(risk_rows), pd.DataFrame(action_rows)


def save_outputs(risk_df: pd.DataFrame, actions_df: pd.DataFrame) -> None:
    """Persist CSV files to the repo data directory."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    risk_df.to_csv(OUTPUT_DIR / "synthetic_risk_register.csv", index=False)
    actions_df.to_csv(OUTPUT_DIR / "synthetic_actions.csv", index=False)


if __name__ == "__main__":
    risks_df, actions_df = build_data()
    save_outputs(risks_df, actions_df)
    print(f"Saved {len(risks_df)} risk-plan rows and {len(actions_df)} action rows to {OUTPUT_DIR}")
