"""
MCP (Model Context Protocol) based agent communication
Provides standardized agent-to-service interaction with MCP compliance
"""

from typing import Any
import json
from datetime import datetime
from app.agents import (
    ApplicantProfileAgent,
    FinancialRiskAgent,
    LoanDecisionAgent,
    ComplianceOrchestratorAgent
)


class MCPAgentServer:
    """MCP-compliant agent server for loan approval system"""

    def __init__(self):
        self.profile_agent = ApplicantProfileAgent()
        self.financial_agent = FinancialRiskAgent()
        self.decision_agent = LoanDecisionAgent()
        self.compliance_agent = ComplianceOrchestratorAgent()
        self.agent_registry = self._build_registry()

    def _build_registry(self) -> dict:
        """Build MCP agent registry with capabilities"""
        return {
            "applicant_profile": {
                "agent": self.profile_agent,
                "tool": "analyze_applicant_profile",
                "description": "Analyze applicant profile for income stability and employment risk",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "age": {"type": "integer", "description": "Applicant age"},
                        "income": {"type": "number", "description": "Annual income"},
                        "employment": {"type": "string", "enum": ["Salaried", "Self-Employed", "Contract"]}
                    },
                    "required": ["age", "income", "employment"]
                }
            },
            "financial_risk": {
                "agent": self.financial_agent,
                "tool": "analyze_financial_risk",
                "description": "Analyze financial risk including DTI and credit assessment",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "credit_score": {"type": "integer"},
                        "loan_amount": {"type": "number"},
                        "liabilities": {"type": "number"},
                        "income": {"type": "number"}
                    },
                    "required": ["credit_score", "loan_amount", "liabilities", "income"]
                }
            },
            "loan_decision": {
                "agent": self.decision_agent,
                "tool": "make_loan_decision",
                "description": "Make final loan approval decision based on analysis",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "profile_analysis": {"type": "object"},
                        "financial_analysis": {"type": "object"},
                        "application_data": {"type": "object"}
                    },
                    "required": ["profile_analysis", "financial_analysis", "application_data"]
                }
            },
            "compliance": {
                "agent": self.compliance_agent,
                "tool": "orchestrate_compliance",
                "description": "Generate compliance records and audit trails",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "decision": {"type": "object"},
                        "application_data": {"type": "object"},
                        "application_id": {"type": "string"}
                    },
                    "required": ["decision", "application_data", "application_id"]
                }
            }
        }

    def call_tool(self, tool_name: str, parameters: dict) -> dict:
        """
        MCP-compliant tool calling interface
        Handles all agent tool invocations through standardized protocol
        """
        if tool_name == "analyze_applicant_profile":
            return self._call_profile_agent(parameters)
        elif tool_name == "analyze_financial_risk":
            return self._call_financial_agent(parameters)
        elif tool_name == "make_loan_decision":
            return self._call_decision_agent(parameters)
        elif tool_name == "orchestrate_compliance":
            return self._call_compliance_agent(parameters)
        else:
            return {"error": f"Unknown tool: {tool_name}"}

    def _call_profile_agent(self, params: dict) -> dict:
        """MCP call to profile agent"""
        try:
            result = self.profile_agent.analyze(params)
            return {
                "status": "success",
                "tool": "analyze_applicant_profile",
                "timestamp": datetime.now().isoformat(),
                "result": result
            }
        except Exception as e:
            return {
                "status": "error",
                "tool": "analyze_applicant_profile",
                "error": str(e)
            }

    def _call_financial_agent(self, params: dict) -> dict:
        """MCP call to financial agent"""
        try:
            result = self.financial_agent.analyze(params)
            return {
                "status": "success",
                "tool": "analyze_financial_risk",
                "timestamp": datetime.now().isoformat(),
                "result": result
            }
        except Exception as e:
            return {
                "status": "error",
                "tool": "analyze_financial_risk",
                "error": str(e)
            }

    def _call_decision_agent(self, params: dict) -> dict:
        """MCP call to decision agent"""
        try:
            result = self.decision_agent.decide(
                params["profile_analysis"],
                params["financial_analysis"],
                params["application_data"]
            )
            return {
                "status": "success",
                "tool": "make_loan_decision",
                "timestamp": datetime.now().isoformat(),
                "result": result
            }
        except Exception as e:
            return {
                "status": "error",
                "tool": "make_loan_decision",
                "error": str(e)
            }

    def _call_compliance_agent(self, params: dict) -> dict:
        """MCP call to compliance agent"""
        try:
            result = self.compliance_agent.orchestrate(
                params["decision"],
                params["application_data"],
                params["application_id"]
            )
            return {
                "status": "success",
                "tool": "orchestrate_compliance",
                "timestamp": datetime.now().isoformat(),
                "result": result
            }
        except Exception as e:
            return {
                "status": "error",
                "tool": "orchestrate_compliance",
                "error": str(e)
            }

    def get_tools_list(self) -> list:
        """Get list of available MCP tools"""
        return [
            {
                "name": agent_info["tool"],
                "description": agent_info["description"],
                "input_schema": agent_info["input_schema"]
            }
            for agent_info in self.agent_registry.values()
        ]

    def get_tool_schema(self, tool_name: str) -> dict:
        """Get MCP schema for specific tool"""
        for agent_key, agent_info in self.agent_registry.items():
            if agent_info["tool"] == tool_name:
                return {
                    "tool_name": tool_name,
                    "description": agent_info["description"],
                    "input_schema": agent_info["input_schema"]
                }
        return {"error": f"Tool not found: {tool_name}"}
