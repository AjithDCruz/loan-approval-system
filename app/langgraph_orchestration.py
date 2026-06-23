"""
LangGraph-based orchestration for loan approval workflow
Provides state-based graph orchestration for multi-agent coordination
"""

from typing import TypedDict, Any, Annotated
from langgraph.graph import StateGraph, END
import json
from datetime import datetime
from app.agents import (
    ApplicantProfileAgent,
    FinancialRiskAgent,
    LoanDecisionAgent,
    ComplianceOrchestratorAgent
)


class LoanApplicationState(TypedDict):
    """State object for loan application workflow"""
    application_id: str
    user_input: dict
    profile_analysis: dict
    financial_analysis: dict
    decision: dict
    compliance_result: dict
    workflow_status: str
    error: str | None


class LangGraphLoanOrchestrator:
    """LangGraph-based orchestration engine for loan approval"""

    def __init__(self):
        self.workflow = self._build_workflow()
        self.profile_agent = ApplicantProfileAgent()
        self.financial_agent = FinancialRiskAgent()
        self.decision_agent = LoanDecisionAgent()
        self.compliance_agent = ComplianceOrchestratorAgent()

    def _build_workflow(self):
        """Build the LangGraph workflow"""
        graph = StateGraph(LoanApplicationState)

        # Add agent nodes
        graph.add_node("profile_analysis", self._profile_node)
        graph.add_node("financial_analysis", self._financial_node)
        graph.add_node("decision_making", self._decision_node)
        graph.add_node("compliance_check", self._compliance_node)

        # Define edges
        graph.add_edge("START", "profile_analysis")
        graph.add_edge("profile_analysis", "financial_analysis")
        graph.add_edge("financial_analysis", "decision_making")
        graph.add_edge("decision_making", "compliance_check")
        graph.add_edge("compliance_check", END)

        return graph.compile()

    def _profile_node(self, state: LoanApplicationState) -> LoanApplicationState:
        """Node: Analyze applicant profile"""
        try:
            profile_result = self.profile_agent.analyze(state["user_input"])
            state["profile_analysis"] = profile_result
            state["workflow_status"] = "profile_analysis_complete"
            return state
        except Exception as e:
            state["error"] = f"Profile analysis failed: {str(e)}"
            return state

    def _financial_node(self, state: LoanApplicationState) -> LoanApplicationState:
        """Node: Analyze financial risk"""
        try:
            financial_result = self.financial_agent.analyze(state["user_input"])
            state["financial_analysis"] = financial_result
            state["workflow_status"] = "financial_analysis_complete"
            return state
        except Exception as e:
            state["error"] = f"Financial analysis failed: {str(e)}"
            return state

    def _decision_node(self, state: LoanApplicationState) -> LoanApplicationState:
        """Node: Make loan decision"""
        try:
            decision_result = self.decision_agent.decide(
                state["profile_analysis"],
                state["financial_analysis"],
                state["user_input"]
            )
            state["decision"] = decision_result
            state["workflow_status"] = "decision_complete"
            return state
        except Exception as e:
            state["error"] = f"Decision making failed: {str(e)}"
            return state

    def _compliance_node(self, state: LoanApplicationState) -> LoanApplicationState:
        """Node: Compliance orchestration"""
        try:
            compliance_result = self.compliance_agent.orchestrate(
                state["decision"],
                state["user_input"],
                state["application_id"]
            )
            state["compliance_result"] = compliance_result
            state["workflow_status"] = "compliance_complete"
            return state
        except Exception as e:
            state["error"] = f"Compliance orchestration failed: {str(e)}"
            return state

    def process(self, application_id: str, user_input: dict) -> dict:
        """Execute the workflow"""
        initial_state = LoanApplicationState(
            application_id=application_id,
            user_input=user_input,
            profile_analysis={},
            financial_analysis={},
            decision={},
            compliance_result={},
            workflow_status="initialized",
            error=None
        )

        # Execute workflow
        result = self.workflow.invoke(initial_state)

        if result.get("error"):
            return {"error": result["error"], "status": "failed"}

        return {
            "application_id": result["application_id"],
            "profile_analysis": result["profile_analysis"],
            "financial_analysis": result["financial_analysis"],
            "decision": result["decision"],
            "compliance_result": result["compliance_result"],
            "workflow_status": result["workflow_status"],
            "status": "success"
        }
