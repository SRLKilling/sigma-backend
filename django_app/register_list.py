from sigma_api.importer import register_entry, register_model

register_entry("Group", "group")
register_entry("GroupMember", "group-member")
register_entry("GroupField", "group-field")
register_entry("GroupFieldValue", "group-field-value")
register_entry("GroupInvitation","group-invitation")
register_entry("User","user")
register_entry("Chat","chat")
register_entry("ChatMessage","chat-message")
register_entry("ChatMember","chat-member")
register_entry("Event", "event")

# Ressources to be made visible to Django, but without entries
register_model("UserConnection")

register_model("Comment")
register_model("Like")
register_model("Participation")
register_model("Publication")
register_model("SharedPublication")
register_model("Tag")
