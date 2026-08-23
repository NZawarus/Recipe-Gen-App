package edu.msoe.team8app.ui.dashboard

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import androidx.activity.addCallback
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import edu.msoe.team8app.R
import edu.msoe.team8app.databinding.FragmentChatBinding

class ChatFragment : Fragment() {

    private var _binding: FragmentChatBinding? = null
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        _binding = FragmentChatBinding.inflate(inflater, container, false)
        val root: View = binding.root

        val chatName = arguments?.getString("chatName") ?: "Chat"
        binding.chatTitle.text = chatName

        //Sample code below
        val content = "Vegan Pasta with Tomato Sauce\n" +
                "Ingredients:\n" +
                "\n" +
                "1/4 cup rice (not needed, use pasta instead)\n" +
                "1/4 cup pasta (spaghetti or linguine)\n" +
                "1 small white onion, diced\n" +
                "2 cloves garlic, minced\n" +
                "1 medium tomato, diced\n" +
                "1 tablespoon olive oil (not listed, use a neutral oil)\n" +
                "1 teaspoon dried basil\n" +
                "Salt and pepper to taste\n" +
                "\n" +
                "Instructions:\n" +
                "\n" +
                "Cook the pasta according to package instructions. Drain and set aside.\n" +
                "In a pan, heat the olive oil over medium heat. Add the diced onion and cook for 2-3 minutes until softened.\n" +
                "Add the minced garlic and cook for another minute.\n" +
                "Add the diced tomato and cook for 2-3 minutes until the sauce thickens.\n" +
                "Add the cooked pasta to the sauce and stir to combine. Season with basil, salt, and pepper to taste.\n" +
                "Serve hot."

        val chatList = listOf(
            ChatMessage("1", "Bob", "", R.drawable.sample_image, MessageType.IMAGE,true),
            ChatMessage("2", "Alice", content, null,MessageType.TEXT,false)
        )

        binding.recyclerView.layoutManager = LinearLayoutManager(context)
        binding.recyclerView.adapter = ChatAdapter(chatList)

        // Enable back button in toolbar
        val navController = findNavController()
        requireActivity().onBackPressedDispatcher.addCallback(viewLifecycleOwner) {
            navController.navigateUp()
        }

        return root
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}