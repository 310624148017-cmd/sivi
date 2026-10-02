import os
import json
import logging
from typing import Dict, Any, Optional
from utils import get_data_dir, get_timestamp, logger

DESTRUCTIVE_ACTIONS = {
    "submit",
    "submit_form",
    "submit_application",
    "payment",
    "checkout",
    "delete",
    "clear",
    "send_email",
    "transfer"
}

class SafetyGuard:
    """
    Human-in-the-Loop (HITL) Safety Enforcement Engine.
    Ensures that no high-consequence, irreversible, or destructive actions
    can be taken autonomously without human confirmation.
    """
    def __init__(self, audit_log_filename: str = "audit_log.jsonl"):
        self.audit_log_path = os.path.join(get_data_dir(), audit_log_filename)
        self.pending_approvals: Dict[str, Dict[str, Any]] = {}
        logger.info(f"✓ SafetyGuard initialized. Audit trail: {self.audit_log_path}")

    def evaluate_action(self, action_type: str, parameters: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Determines whether the given action requires human approval.
        Returns safety assessment dictionary.
        """
        action_normalized = (action_type or "").lower().strip()
        is_destructive = action_normalized in DESTRUCTIVE_ACTIONS or any(d in action_normalized for d in ["submit", "delete", "pay", "buy"])

        reason = ""
        risk_level = "LOW"
        
        if is_destructive:
            risk_level = "HIGH"
            reason = f"Destructive/Irreversible action '{action_type}' requires Human-in-the-Loop approval before dispatching."
        elif action_normalized in ["fill", "upload", "click"]:
            risk_level = "LOW"
            reason = f"Standard safe interaction '{action_type}' allowed autonomously."

        return {
            "action": action_type,
            "requires_approval": is_destructive,
            "risk_level": risk_level,
            "reason": reason,
            "parameters": parameters
        }

    def register_approval_request(self, request_id: str, action_data: Dict[str, Any]) -> Dict[str, Any]:
        """Stores a pending approval awaiting judge/user decision"""
        self.pending_approvals[request_id] = {
            "id": request_id,
            "timestamp": get_timestamp(),
            "status": "PENDING",
            "action_data": action_data
        }
        logger.warning(f"[HITL GATE] Approval required for request [{request_id}]: {action_data.get('action')}")
        return self.pending_approvals[request_id]

    def resolve_approval(self, request_id: str, approved: bool, reviewer_comment: Optional[str] = None) -> Dict[str, Any]:
        """Processes human approval or rejection"""
        record = self.pending_approvals.get(request_id, {
            "id": request_id,
            "action_data": {"action": "submit"}
        })
        
        status = "APPROVED" if approved else "DENIED"
        record["status"] = status
        record["resolved_at"] = get_timestamp()
        record["reviewer_comment"] = reviewer_comment or ("Approved by Judge" if approved else "Denied by Judge")

        # Write to audit trail
        self.log_audit_event(
            event_type="APPROVAL_DECISION",
            action=record.get("action_data", {}).get("action", "unknown"),
            details={
                "request_id": request_id,
                "approved": approved,
                "status": status,
                "comment": record["reviewer_comment"],
                "parameters": record.get("action_data", {}).get("parameters", {})
            }
        )

        if request_id in self.pending_approvals:
            del self.pending_approvals[request_id]

        logger.info(f"[HITL GATE] Resolved request [{request_id}]: {status}")
        return record

    def log_audit_event(self, event_type: str, action: str, details: Dict[str, Any]):
        """Persists audit record to jsonl log file"""
        try:
            os.makedirs(os.path.dirname(self.audit_log_path), exist_ok=True)
            entry = {
                "timestamp": get_timestamp(),
                "event_type": event_type,
                "action": action,
                "details": details
            }
            with open(self.audit_log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            logger.error(f"[SAFETY] Error writing to audit trail: {e}")

# Global singleton
safety_guard = SafetyGuard()
