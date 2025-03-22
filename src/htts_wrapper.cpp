#include "htts.hpp"
#include <cstring>
#include <cstdlib>

extern "C" {

HTTS* create_tts(const char* data_path) {
    HTTS* tts = new HTTS;
    tts->set("PthModel", "Pth1");
    tts->set("Method", "HTS");
    tts->set("Lang", "eu");

    char dic_path[1024];
    sprintf(dic_path, "%s/dicts/eu_dicc", data_path);
    tts->set("HDicDBName", dic_path);

    if (!tts->create()) {
        delete tts;
        return nullptr;
    }

    char voice_path[1024];
    sprintf(voice_path, "%s/voices/aholab_eu_female/", data_path);
    tts->set("voice_path", voice_path);
    tts->set("vp", "yes");

    return tts;
}

int synthesize_text(HTTS* tts, const char* text, const char* data_path, short** out_samples, int* out_len) {
    if (!tts) return 0;

    const char* lang = "eu";
    if (tts->input_multilingual(text, lang, data_path, false)) {
        int len = tts->output_multilingual(lang, out_samples);
        if (out_len) *out_len = len;
        return len > 0;
    }
    return 0;
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
