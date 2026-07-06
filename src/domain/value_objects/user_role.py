"""Value object for user roles."""

from enum import Enum


class UserRole(Enum):
    """User role enumeration with permission levels."""
    USER = "user"
    OPERATOR = "operator"
    ANALYST = "analyst"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"
    
    @property
    def permission_level(self) -> int:
        """Get the permission level for the role."""
        levels = {
            UserRole.USER: 1,
            UserRole.OPERATOR: 2,
            UserRole.ANALYST: 3,
            UserRole.ADMIN: 4,
            UserRole.SUPER_ADMIN: 5,
        }
        return levels[self]
    
    def can_manage_role(self, other_role: "UserRole") -> bool:
        """Check if this role can manage the other role."""
        return self.permission_level > other_role.permission_level
    
    def has_admin_privileges(self) -> bool:
        """Check if role has admin privileges."""
        return self.permission_level >= 4
