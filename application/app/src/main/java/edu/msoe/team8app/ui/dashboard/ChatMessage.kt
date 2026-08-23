package edu.msoe.team8app.ui.dashboard

data class ChatMessage(
    val id: String,
    val sender: String,
    val content: String,  // Text message or Image URL
    val imageResId: Int? = null,  // Nullable, used for local images,
    val type: MessageType,
    val isUser: Boolean // True if the message is from the user

)

enum class MessageType {
    TEXT, IMAGE
}
