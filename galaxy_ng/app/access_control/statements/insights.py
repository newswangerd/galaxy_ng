INSIGHTS_STATEMENTS = {
    'NamespaceViewSet': [
        {
            "action": ["list", "retrieve"],
            "principal": "authenticated",
            "effect": "allow",
            "condition": "has_rh_entitlements",
        },
        {
            "action": "create",
            "principal": "authenticated",
            "effect": "allow",
            "condition": ["has_model_perms:galaxy.add_namespace", "has_rh_entitlements"]
        },
        {
            "action": "update",
            "principal": "authenticated",
            "effect": "allow",
            "condition": [
                "has_model_or_obj_perms:galaxy.change_namespace",
                "has_rh_entitlements"]
        },
    ],
    'CollectionViewSet': [
        {
            "action": ["list", "retrieve"],
            "principal": "authenticated",
            "effect": "allow",
            "condition": "has_rh_entitlements",
        },
        {
            "action": "create",
            "principal": "authenticated",
            "effect": "allow",
            "condition": ["can_upload_to_namespace", "has_rh_entitlements"]
        },
        {
            "action": "update",
            "principal": "authenticated",
            "effect": "allow",
            "condition": "is_namespace_owner"
        },
        {
            "action": "move_content",
            "principal": "authenticated",
            "effect": "allow",
            # TODO: Add move collection permission to pulp_ansible
            "condition": [
                "has_model_perms:ansible.move_collection",
                "has_rh_entitlements"]
        }
    ],
    'UserViewSet': [
        {
            "action": ["retrieve"],
            "principal": "authenticated",
            "effect": "allow",
            "condition": "is_current_user"
        },
    ],
    'SyncListViewSet': [
        {
            "action": ["list"],
            "principal": "authenticated",
            "effect": "allow",
            "condition": ["has_model_perms:galaxy.view_synclist", "has_rh_entitlements"]
        },
        {
            "action": ["retrieve"],
            "principal": "authenticated",
            "effect": "allow",
            "condition": [
                "has_model_or_obj_perms:galaxy.view_synclist",
                "has_rh_entitlements"]
        },
        {
            "action": ["destroy"],
            "principal": "authenticated",
            "effect": "allow",
            "condition": [
                "has_model_perms:galaxy.delete_synclist",
                "has_rh_entitlements"]
        },
        {
            "action": ["create"],
            "principal": "authenticated",
            "effect": "allow",
            "condition": [
                "has_model_perms:galaxy.add_synclist",
                "has_rh_entitlements"]
        },
        {
            "action": ["update", "partial_update"],
            "principal": "authenticated",
            "effect": "allow",
            "condition": [
                "has_model_or_obj_perms:galaxy.change_synclist",
                "has_rh_entitlements"]
        },
    ],
    'MySyncListViewSet': [
        {
            "action": ["list"],
            "principal": "authenticated",
            "effect": "allow",
            "condition": ["has_rh_entitlements"]
        },
        {
            "action": ["retrieve"],
            "principal": "authenticated",
            "effect": "allow",
            "condition": [
                "has_model_or_obj_perms:galaxy.view_synclist",
                "has_rh_entitlements"]
        },
        {
            "action": ["update", "partial_update"],
            "principal": "authenticated",
            "effect": "allow",
            "condition": [
                "has_model_or_obj_perms:galaxy.change_synclist",
                "has_rh_entitlements"]
        },
    ],
    'TaskViewSet': [
        {
            "action": ["list", "retrieve"],
            "principal": "authenticated",
            "effect": "allow",
        },
    ],
    'TagViewSet': [
        {
            "action": ["list", "retrieve"],
            "principal": "authenticated",
            "effect": "allow",
        },
    ],
}