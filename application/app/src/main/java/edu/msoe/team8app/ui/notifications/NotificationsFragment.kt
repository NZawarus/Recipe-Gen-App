package edu.msoe.team8app.ui.notifications

import android.app.AlertDialog
import android.os.Bundle
import android.text.InputType
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.EditText
import androidx.fragment.app.Fragment
import androidx.lifecycle.ViewModelProvider
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import edu.msoe.team8app.databinding.FragmentNotificationsBinding

class NotificationsFragment : Fragment() {
    private lateinit var recyclerView: RecyclerView
    private lateinit var adapter: BlacklistAdapter
    private val itemList = mutableListOf<String>()
    private var _binding: FragmentNotificationsBinding? = null

    // This property is only valid between onCreateView and
    // onDestroyView.
    private val binding get() = _binding!!

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        val notificationsViewModel =
            ViewModelProvider(this).get(NotificationsViewModel::class.java)

        _binding = FragmentNotificationsBinding.inflate(inflater, container, false)
        val root: View = binding.root
        val addButton = binding.addButton
        recyclerView = binding.recyclerView

        adapter = BlacklistAdapter(itemList) { item -> removeItem(item) }
        recyclerView.layoutManager = LinearLayoutManager(requireContext())
        recyclerView.adapter = adapter

        addButton.setOnClickListener { showAddItemDialog()}
        return root
    }

    override fun onDestroyView() {
        super.onDestroyView()
        _binding = null
    }

    private fun showAddItemDialog() {
        val builder = AlertDialog.Builder(requireContext())
        builder.setTitle("Add Item")
        val input = EditText(requireContext())
        input.inputType = InputType.TYPE_CLASS_TEXT
        builder.setView(input)

        builder.setPositiveButton("Add") { _, _ ->
            val itemText = input.text.toString().trim()
            if (itemText.isNotEmpty()) {
                addItem(itemText)
            }
        }
        builder.setNegativeButton("Cancel") { dialog, _ -> dialog.cancel() }
        builder.show()
    }

    private fun addItem(item: String) {
        itemList.add(item)
        adapter.notifyItemInserted(itemList.size - 1)
    }

    private fun removeItem(item: String) {
        val position = itemList.indexOf(item)
        if (position != -1) {
            itemList.removeAt(position)
            adapter.notifyItemRemoved(position)
        }
    }
}