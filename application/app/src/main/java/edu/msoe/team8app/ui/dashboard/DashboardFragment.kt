package edu.msoe.team8app.ui.dashboard

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.TextView
import android.widget.Toast
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import edu.msoe.team8app.R
import edu.msoe.team8app.databinding.FragmentDashboardBinding

class DashboardFragment : Fragment() {

    private var _binding: FragmentDashboardBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        val dashboardViewModel =
            ViewModelProvider(this).get(DashboardViewModel::class.java)

        _binding = FragmentDashboardBinding.inflate(inflater, container, false)
        val root: View = binding.root



        val chatList = listOf(
            ChatItem("1", "Recipe 1", "can you add rice to the recipe?"),
            ChatItem("2", "Recipe 2 ", "image.jpg"),
            ChatItem("3", "Recipe 3", ""),
            ChatItem("4", "Recipe 4", "")
        )

        val recyclerView: RecyclerView = binding.recyclerView
        recyclerView.layoutManager = LinearLayoutManager(context)
        recyclerView.adapter = ChatListAdapter(chatList) { chat ->
            val bundle = Bundle()
            bundle.putString("chatId", chat.chatId)
            bundle.putString("chatName", chat.name)
            findNavController().navigate(R.id.action_dashboard_to_chatFragment, bundle)
        }



        return root
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }
}