package com.example.app_serv

import android.os.Bundle
import android.util.Log
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import kotlinx.coroutines.DelicateCoroutinesApi
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import kotlinx.coroutines.runBlocking

class MainActivity : AppCompatActivity() {
    val apiInterface = apiinterface.create().getBlog()
//    private lateinit var Reberth: String
////    val apiInterface = apiinterface.create().getBlog()
//    val quotesApi = RetrofitHelper.getInstance().create(QuotesApi::class.java)

    //    @SuppressLint("SetTextI18n")
//    @DelicateCoroutinesApi
    @DelicateCoroutinesApi
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

//        assertThat(authors).isNotEmpty
//        val call = apiinterface.create().getBlog()
        val textView_1: TextView = findViewById(R.id.tv_content) as TextView
//        fun capi_get_api() {
        val quotesApi = RetrofitHelper.getInstance().create(QuotesApi::class.java)
        // launching a new coroutine
        GlobalScope.launch {
            val result = quotesApi.getQuotes()
            val result_2 = quotesApi.getAuthor()
            val result_3 = result.body()
//            val result_3 = quotesApi.postQuotes(json)
            if (result != null)
            // Checking the results
                Log.d("ayush: ", result.body().toString())
                Log.d("ayush: ", result_2.body().toString())
                Log.d("ayush: ", result.headers().toString())
            textView_1.text = result.body().toString()

        }
    }
}
