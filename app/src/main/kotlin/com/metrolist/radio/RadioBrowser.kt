package com.metrolist.radio

import io.ktor.client.HttpClient
import io.ktor.client.call.body
import io.ktor.client.engine.okhttp.OkHttp
import io.ktor.client.plugins.contentnegotiation.ContentNegotiation
import io.ktor.client.request.*
import io.ktor.http.*
import io.ktor.serialization.kotlinx.json.json
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.Json

@Serializable
data class RadioStation(
    @SerialName("stationuuid") val stationUuid: String = "",
    @SerialName("name") val name: String = "",
    @SerialName("url_resolved") val urlResolved: String = "",
    @SerialName("url") val url: String = "",
    @SerialName("homepage") val homepage: String = "",
    @SerialName("favicon") val favicon: String = "",
    @SerialName("tags") val tags: String = "",
    @SerialName("country") val country: String = "",
    @SerialName("countrycode") val countryCode: String = "",
    @SerialName("state") val state: String = "",
    @SerialName("language") val language: String = "",
    @SerialName("codec") val codec: String = "",
    @SerialName("bitrate") val bitrate: Int = 0,
    @SerialName("votes") val votes: Int = 0,
    @SerialName("clickcount") val clickCount: Int = 0,
    @SerialName("lastcheckok") val lastCheckOk: Int = 0,
    @SerialName("lastchecktime") val lastCheckTime: String = "",
)

object RadioBrowser {
    private val json = Json {
        isLenient = true
        ignoreUnknownKeys = true
    }

    // radio-browser.info offers multiple mirrors; any one works. Clicked top stations are
    // limited on non-mirror hosts, so prefer the API mirror set.
    private val baseUrls =
        listOf(
            "https://de1.api.radio-browser.info",
            "https://nl1.api.radio-browser.info",
            "https://at1.api.radio-browser.info",
        )

    private val client by lazy {
        HttpClient(OkHttp) {
            install(ContentNegotiation) {
                json(json)
            }
            defaultRequest {
                header(HttpHeaders.UserAgent, "TheHive/1.0 (Android music app)")
            }
            expectSuccess = false
        }
    }

    suspend fun search(
        query: String = "",
        limit: Int = 100,
        by: String = "name",
        order: String = "clickcount",
        reverse: Boolean = true,
    ): List<RadioStation> {
        val escaped = query.replace(" ", "%20")
        val path =
            "/json/stations/search?name=$escaped&limit=$limit&order=$order&reverse=$reverse" +
                "&hidebroken=true"
        return fetch(path)
    }

    suspend fun top(limit: Int = 100): List<RadioStation> =
        fetch("/json/stations/topvote/$limit")

    suspend fun byCountry(countryCode: String, limit: Int = 100): List<RadioStation> =
        fetch("/json/stations/bycountrycodeexact/$countryCode?limit=$limit&hidebroken=true")

    suspend fun byTag(tag: String, limit: Int = 100): List<RadioStation> {
        val escaped = tag.replace(" ", "%20")
        return fetch("/json/stations/bytagexact/$escaped?limit=$limit&hidebroken=true")
    }

    private suspend fun fetch(path: String): List<RadioStation> {
        var lastError: Exception? = null
        for (base in baseUrls) {
            try {
                val resp = client.get("$base$path")
                if (resp.status.isSuccess()) {
                    return resp.body()
                }
            } catch (e: Exception) {
                lastError = e
            }
        }
        throw lastError ?: Exception("RadioBrowser: all mirrors failed")
    }
}