package com.kabootar.client

import android.annotation.SuppressLint
import android.webkit.JavascriptInterface
import android.os.Bundle
import android.webkit.WebChromeClient
import android.webkit.WebResourceRequest
import android.webkit.WebResourceError
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {
    companion object {
        private const val PREFS_NAME = "kabootar"
        private const val PREF_ENDPOINT = "endpoint"
        private const val BOOTSTRAP_URL = "file:///android_asset/bootstrap.html"
    }

    private lateinit var webView: WebView

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        webView = findViewById(R.id.webView)

        with(webView.settings) {
            javaScriptEnabled = true
            domStorageEnabled = true
            databaseEnabled = true
            mixedContentMode = WebSettings.MIXED_CONTENT_COMPATIBILITY_MODE
            builtInZoomControls = false
            displayZoomControls = false
            allowFileAccess = true
            allowContentAccess = true
        }

        webView.addJavascriptInterface(AndroidBridge(), "KabootarAndroid")
        webView.webChromeClient = WebChromeClient()
        webView.webViewClient = object : WebViewClient() {
            private fun handleMainFrameError(failingUrl: String?) {
                if (!failingUrl.isNullOrBlank() && failingUrl.startsWith(BOOTSTRAP_URL)) {
                    return
                }
                Toast.makeText(
                    this@MainActivity,
                    "Unable to load endpoint",
                    Toast.LENGTH_LONG,
                ).show()
                loadBootstrap()
            }

            override fun onReceivedError(
                view: WebView?,
                request: WebResourceRequest?,
                error: WebResourceError?,
            ) {
                if (request?.isForMainFrame == true) {
                    handleMainFrameError(request.url?.toString())
                }
            }

            @Deprecated("Deprecated in Java")
            override fun onReceivedError(
                view: WebView?,
                errorCode: Int,
                description: String?,
                failingUrl: String?,
            ) {
                handleMainFrameError(failingUrl)
            }
        }

        loadBootstrap()
    }

    private fun loadBootstrap() {
        webView.loadUrl(BOOTSTRAP_URL)
    }

    private fun normalizedEndpoint(raw: String?): String {
        val value = (raw ?: "").trim()
        if (value.startsWith("https://") || value.startsWith("http://")) {
            return value
        }
        return ""
    }

    private fun getSavedEndpoint(): String {
        val prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
        return normalizedEndpoint(prefs.getString(PREF_ENDPOINT, ""))
    }

    private fun getDefaultEndpoint(): String {
        return normalizedEndpoint(BuildConfig.START_URL)
    }

    private fun saveEndpoint(value: String) {
        getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
            .edit()
            .putString(PREF_ENDPOINT, value)
            .apply()
    }

    private fun clearEndpoint() {
        getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
            .edit()
            .remove(PREF_ENDPOINT)
            .apply()
    }

    private fun openEndpoint(raw: String) {
        val url = normalizedEndpoint(raw)
        if (url.isBlank()) {
            Toast.makeText(this, "Enter a valid http or https address", Toast.LENGTH_LONG).show()
            return
        }
        saveEndpoint(url)
        webView.loadUrl(url)
    }

    inner class AndroidBridge {
        @JavascriptInterface
        fun getSavedEndpoint(): String = this@MainActivity.getSavedEndpoint()

        @JavascriptInterface
        fun getDefaultEndpoint(): String = this@MainActivity.getDefaultEndpoint()

        @JavascriptInterface
        fun openEndpoint(raw: String) {
            runOnUiThread {
                this@MainActivity.openEndpoint(raw)
            }
        }

        @JavascriptInterface
        fun clearSavedEndpoint() {
            runOnUiThread {
                this@MainActivity.clearEndpoint()
                this@MainActivity.loadBootstrap()
            }
        }
    }

    @Deprecated("Deprecated in Java")
    override fun onBackPressed() {
        if (::webView.isInitialized && webView.canGoBack()) {
            webView.goBack()
            return
        }
        super.onBackPressed()
    }
}
