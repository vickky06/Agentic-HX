class AgentPolicyService:
    def can_execute(self, agent_name: str, user_role: str) -> bool:
        # Placeholder: RBAC, rate limits, etc.
        if user_role == "admin":
            return True
        return agent_name != "super_agent"
