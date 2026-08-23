package edu.msoe.team8app.ui.dashboard

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.recyclerview.widget.RecyclerView
import edu.msoe.team8app.R

class ChatListAdapter(
    private val chatList: List<ChatItem>,
    private val onChatClick: (ChatItem) -> Unit
) : RecyclerView.Adapter<ChatListAdapter.ChatViewHolder>() {

    class ChatViewHolder(view: View) : RecyclerView.ViewHolder(view) {
        val nameTextView: TextView = view.findViewById(R.id.chat_name)
        val lastMessageTextView: TextView = view.findViewById(R.id.chat_last_message)
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ChatViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_chat, parent, false)
        return ChatViewHolder(view)
    }

    override fun onBindViewHolder(holder: ChatViewHolder, position: Int) {
        val chat = chatList[position]
        holder.nameTextView.text = chat.name
        holder.lastMessageTextView.text = chat.lastMessage
        holder.itemView.setOnClickListener { onChatClick(chat) }
    }

    override fun getItemCount() = chatList.size
}