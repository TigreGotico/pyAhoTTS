#include "htts.hpp"
#include <cstring>
#include <cstdlib>
#include <string>

extern "C" {

HTTS* create_tts(const char* data_path, const char* lang) {
    HTTS* tts = new HTTS;
    tts->set("PthModel", "Pth1");
    tts->set("Method", "HTS");
    tts->set("Lang", lang);  // Use the passed language parameter

    char dic_path[1024];
    sprintf(dic_path, "%s/dicts/%s_dicc", data_path, lang);  // Dynamic dictionary path based on language
    tts->set("HDicDBName", dic_path);

    if (!tts->create()) {
        delete tts;
        return nullptr;
    }

    char voice_path[1024];
    sprintf(voice_path, "%s/voices/aholab_%s_female/", data_path, lang);  // Dynamic voice path
    tts->set("voice_path", voice_path);
    tts->set("vp", "yes");

    return tts;
}

int synthesize_text(HTTS* tts, const char* text, const char* data_path, const char* lang, short** out_samples, int* out_len) {
    if (!tts) return 0;

    if (tts->input_multilingual(text, lang, data_path, false)) {
        int len = tts->output_multilingual(lang, out_samples);
        if (out_len) *out_len = len;
        return len > 0;
    }
    return 0;
}

// Phonetic (SAMPA) transcription of `text`. Runs the full linguistic pipeline
// (normalization, G2P, syllabification, stress) but no acoustic synthesis, and
// returns a newly-allocated UTF-8/ISO string: one word per line, phones
// space-separated, lexical stress as a leading "'". Caller frees with free_string().
// Returns NULL on failure / empty result.
char* transcribe_text(HTTS* tts, const char* text, const char* data_path, const char* lang) {
    if (!tts) return nullptr;
    if (!tts->input_multilingual(text, lang, data_path, false)) return nullptr;

    std::string acc;
    char* seg;
    while ((seg = tts->transcribe_next(lang)) != nullptr) {
        if (seg[0]) {                       // skip flush/empty sentinels
            if (!acc.empty()) acc += "\n";
            acc += seg;
        }
        free(seg);
    }
    if (acc.empty()) return nullptr;
    return strdup(acc.c_str());
}

void free_string(char* s) {
    if (s) {
        free(s);
    }
}

void free_samples(short* samples) {
    if (samples) {
        free(samples);
    }
}

void destroy_tts(HTTS* tts) {
    delete tts;
}

}
