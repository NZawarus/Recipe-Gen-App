package edu.msoe.team8app.ui.dashboard

import android.view.LayoutInflater
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.bumptech.glide.Glide

import edu.msoe.team8app.databinding.ItemImageMessageOtherBinding
import edu.msoe.team8app.databinding.ItemImageMessageUserBinding

import edu.msoe.team8app.databinding.ItemTextMessageOtherBinding
import edu.msoe.team8app.databinding.ItemTextMessageUserBinding

class ChatAdapter(private val messages: List<ChatMessage>) :
    RecyclerView.Adapter<RecyclerView.ViewHolder>() {

    private val TEXT_MESSAGE_USER = 1
    private val TEXT_MESSAGE_OTHER = 2
    private val IMAGE_MESSAGE_USER = 3
    private val IMAGE_MESSAGE_OTHER = 4

    override fun getItemViewType(position: Int): Int {
        val message = messages[position]
        return when {
            message.type == MessageType.TEXT && message.isUser -> TEXT_MESSAGE_USER
            message.type == MessageType.TEXT -> TEXT_MESSAGE_OTHER
            message.type == MessageType.IMAGE && message.isUser -> IMAGE_MESSAGE_USER
            else -> IMAGE_MESSAGE_OTHER
        }
    }

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): RecyclerView.ViewHolder {
        return when (viewType) {
            TEXT_MESSAGE_USER -> {
                val binding = ItemTextMessageUserBinding.inflate(LayoutInflater.from(parent.context), parent, false)
                TextMessageUserViewHolder(binding)
            }
            TEXT_MESSAGE_OTHER -> {
                val binding = ItemTextMessageOtherBinding.inflate(LayoutInflater.from(parent.context), parent, false)
                TextMessageOtherViewHolder(binding)
            }
            IMAGE_MESSAGE_USER -> {
                val binding = ItemImageMessageUserBinding.inflate(LayoutInflater.from(parent.context), parent, false)
                ImageMessageUserViewHolder(binding)
            }
            else -> {
                val binding = ItemImageMessageOtherBinding.inflate(LayoutInflater.from(parent.context), parent, false)
                ImageMessageOtherViewHolder(binding)
            }
        }
    }

    override fun onBindViewHolder(holder: RecyclerView.ViewHolder, position: Int) {
        val message = messages[position]
        when (holder) {
            is TextMessageUserViewHolder -> holder.bind(message)
            is TextMessageOtherViewHolder -> holder.bind(message)
            is ImageMessageOtherViewHolder -> holder.bind(message)
            is ImageMessageUserViewHolder -> holder.bind(message)
        }
    }

    override fun getItemCount(): Int = messages.size

    class TextMessageUserViewHolder(private val binding: ItemTextMessageUserBinding) :
        RecyclerView.ViewHolder(binding.root) {
        fun bind(message: ChatMessage) {
            binding.textMessage.text = message.content
        }
    }
    class TextMessageOtherViewHolder(private val binding: ItemTextMessageOtherBinding) :
        RecyclerView.ViewHolder(binding.root) {
        fun bind(message: ChatMessage) {
            binding.textMessage.text = message.content
        }
    }

    class ImageMessageOtherViewHolder(private val binding: ItemImageMessageOtherBinding) :
        RecyclerView.ViewHolder(binding.root) {
        fun bind(message: ChatMessage) {
            message.imageResId?.let {
                binding.imageMessage.setImageResource(it)  // Load local image
            }
        }
//        fun bind(message: ChatMessage) {
//            Glide.with(binding.imageMessage.context)
//                .load(message.content)
//                .into(binding.imageMessage)
//        }
    }
    class ImageMessageUserViewHolder(private val binding: ItemImageMessageUserBinding) :
        RecyclerView.ViewHolder(binding.root) {
        fun bind(message: ChatMessage) {
            message.imageResId?.let {
                binding.imageMessage.setImageResource(it)  // Load local image
            }
        }
//        fun bind(message: ChatMessage) {
//            Glide.with(binding.imageMessage.context)
//                .load(message.content)
//                .into(binding.imageMessage)
//        }
    }
}
