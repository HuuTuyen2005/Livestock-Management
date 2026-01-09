from auth.session import Session

def has_permission(code: str) -> bool:
    return code in Session.permissions

# def is_admin():
#     # Giả sử admin là user có tất cả quyền hệ thống
#     required_permissions = {
#         "USER_MANAGE",
#         "GROUP_MANAGE",
#         "PERMISSION_MANAGE",
#         "ADMIN_UNIT_MANAGE",
#         "SPECIES_MANAGE",
#         "GEN_MANAGE",
#         "FACILITY_MANAGE",
#         "FOOD_MANAGE",
#         "SUBSTANCE_MANAGE",
#         "HISTORY_VIEW",
#         "MANUAL_MANAGE",  # quyền admin cho manual
#     }
#     return required_permissions.issubset(Session.permissions)
