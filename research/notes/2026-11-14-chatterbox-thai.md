# Thai-language support for Chatterbox TTS (Resemble AI) — state as of 14 Nov 2026

All pages below were retrieved on 14 Nov 2026. Classification used throughout: OFFICIALLY SUPPORTED / COMMUNITY FINE-TUNE EXISTS / NOT FOUND.

Bottom line: Thai = NOT officially supported; Thai community fine-tune = NOT FOUND; closest evidence = Vietnamese (Viterbox) and Indonesian community fine-tunes.

## 1. Official status: which languages do current Chatterbox releases support, and is Thai on any list or roadmap?

### Takeaway
Thai is NOT officially supported in any Chatterbox release (original, Multilingual V2/V3, Turbo, Nano, Single-Language Packs) and no roadmap names it. Resemble has also retired Chatterbox commercially (Aug 2026 notice: open source remains, "no support or updates"), so an official Thai release looks unlikely.

### Cited Findings
- Current model line-up in the README (retrieved 14 Nov 2026): Chatterbox-Turbo (350M, English), Chatterbox-Nano (110M, English, CPU/on-device), Chatterbox-Multilingual V3 (500M, 23 languages, recommended, `t3_model="v3"`), Multilingual V2 (legacy), original Chatterbox (500M, English, CFG + exaggeration), and a Single Language Pack of 6 finetunes (zh-cmn, es-mx-latam, pt-br, es-es, pt-pt, hi). — [GitHub README](https://github.com/resemble-ai/chatterbox)
- README language codes for Multilingual: ar, da, de, el, en, es, fi, fr, he, hi, it, ja, ko, ms, nl, no, pl, pt, ru, sv, sw, tr, zh. Thai (th) is absent; Malay (ms) is the only Southeast Asian language. — [GitHub README](https://github.com/resemble-ai/chatterbox)
- The same 23-code `SUPPORTED_LANGUAGES` dict appears in the model code `mtl_tts.py` (mirror in a HF Space). — [mtl_tts.py mirror](https://huggingface.co/spaces/jkorstad/TTS/blob/main/chatterbox/mtl_tts.py)
- Resemble's V3 blog post (10 June 2026) describes "21 languages and 4 dialects" = 25: Arabic, Chinese, Czech, Dutch, English, Finnish, French, German, Hebrew, Hindi, Italian, Japanese, Korean, Norwegian, Polish, Portuguese, Russian, Spanish, Swedish, Turkish, Vietnamese + pt-BR, pt-PT, es-MX/LATAM, es-ES. Thai not listed. — [Resemble blog, V3](https://www.resemble.ai/resources/chatterbox-multilingual-v3-tts-with-embedded-watermarking-for-25-languages)
- The V3 post rates Vietnamese as not production quality (75.21% CER reported) and advises against commercial use until improved; Korean and Vietnamese improvements were promised as upgraded checkpoints or dedicated packs. — [Resemble blog, V3](https://www.resemble.ai/resources/chatterbox-multilingual-v3-tts-with-embedded-watermarking-for-25-languages)
- Roadmap statement: Single-Language Pack to be broadened "to additional languages where the deployment volume and quality headroom justify dedicated models" — no language named. — [Resemble blog, V3](https://www.resemble.ai/resources/chatterbox-multilingual-v3-tts-with-embedded-watermarking-for-25-languages)
- An August 2026 update on that post says Chatterbox and Dramabox are retired commercially but remain open source, with no support or updates. — [Resemble blog, V3](https://www.resemble.ai/resources/chatterbox-multilingual-v3-tts-with-embedded-watermarking-for-25-languages)
- Resemble's /languages/ page now carries a notice that the company has "stopped offering voice generation as a commercial product"; it lists no languages and no Thai. — [resemble.ai/languages](https://www.resemble.ai/languages/)
- Licence: MIT for code and weights (README); V3 "continues the Chatterbox tradition of MIT licensing". Licence of Single-Language Pack models not stated on the blog. — [GitHub README](https://github.com/resemble-ai/chatterbox); [Resemble blog, V3](https://www.resemble.ai/resources/chatterbox-multilingual-v3-tts-with-embedded-watermarking-for-25-languages)
- A third-party catalogue (tts.ai, Thai UI) lists Chatterbox's language as English only; the Thai option on that page is a site-wide dropdown, not a Chatterbox capability. — [tts.ai](https://tts.ai/voices/chatterbox/?lang=th)

### Inferences
- CONFLICT to flag: README/code list 23 languages (incl. Danish, Greek, Malay, Swahili; no Czech/Vietnamese) while the V3 blog lists 21+4 (incl. Czech, Vietnamese; no Danish/Greek/Malay/Swahili). Probably the open-source V3 checkpoint keeps the 23-code set and the blog describes the NIM/enterprise set, but this was not confirmed. Thai is absent from both.
- With commercial retirement and "no support or updates", an official Thai release is improbable; Thai must come from community fine-tuning.

### Gaps
- Whether the hosted product ever supported Thai before retirement: not verifiable; the old knowledge-base page (knowledge.resemble.ai "what languages do you support") now redirects to docs.resemble.ai/welcome. GitHub issue #493 shows hosted "tts-v4" had more languages than OSS (Kazakh) but does not mention Thai.
- Hugging Face model cards for ResembleAI/chatterbox were not fetched directly; README + code used instead.
- Exact release dates/versions: README gives none; GitHub releases API was blocked in this session.

## 2. GitHub issues / discussions / PRs requesting or adding Thai

### Takeaway
NOT FOUND: no Thai issue or PR could be located, but the search was limited (GitHub search API and the issues page were blocked here), so this is "not found via web search", not proof of absence.

### Cited Findings
- Issue #493 "Clarify that hosted tts-v4 language support is broader than OSS ChatterboxMultilingualTTS" (author @Kaiyrly; date not visible): hosted product offered Kazakh (kk-kz) while OSS raises `ValueError` listing 23 languages. No maintainer reply visible. No Thai mention. — [Issue #493 (mirror)](https://github.blesdmm.dns-dynamic.net/resemble-ai/chatterbox/issues/493)
- README offers no fine-tuning instructions or new-language guidance; it points to the Single Language Pack and to Resemble's commercial tuning service. — [GitHub README](https://github.com/resemble-ai/chatterbox)

### Inferences
- Maintainers historically answered language gaps with hosted product / paid tuning, a path now closed by the commercial retirement.

### Gaps
- Direct search of resemble-ai/chatterbox issues for "Thai", "th", "ภาษาไทย" failed: github.com issues URL blocked by robots, gh REST/GraphQL denied for this repo. Worth a manual check at github.com/resemble-ai/chatterbox/issues?q=thai.
- HF Space discussions (ResembleAI/Chatterbox-Multilingual-TTS/discussions) not inspected.

## 3. Community Thai fine-tunes or adapters

### Takeaway
NOT FOUND: no Chatterbox Thai fine-tune, LoRA or fork was found on Hugging Face or via web search (English and Thai queries) as of 14 Nov 2026. Thai community TTS work uses other bases (F5-TTS, OmniVoice, VoxCPM2, Spark-TTS, Kokoro, MMS/VITS).

### Cited Findings
- Hugging Face model search "chatterbox thai" returns "No results found". — [HF search](https://huggingface.co/models?search=chatterbox%20thai)
- HF API listing of models matching "chatterbox" (up to 300, sorted by downloads) contains no id with thai/-th/_th; Southeast Asian hits were only Indonesian (grandhigh/Chatterbox-TTS-Indonesian, 446 downloads, 25 likes, created 2025-09-12; mazrba/...-gguf; adijaya1985 duplicate 2026-11-05; dhyield/chatterbox-luna-id 2026-10-08) and Vietnamese (tuankg1028/chatterbox_vi 2025-06-10; zenai-vietnam/TTS-Chatterbox-Urbie 2025-12-05; quangdung/chatterbox-turbo-vi 2026-03-17). — [HF API](https://huggingface.co/api/models?search=chatterbox&sort=downloads&limit=300)
- HF API listing of text-to-speech models matching "thai" (18 returned): none mention Chatterbox. Listed Thai models include VIZINTZOR/F5-TTS-THAI (55 likes, CC-BY-4.0), hotdogs/omnivoice-thai (870 downloads, 20 likes, Apache-2.0, created 2026-05-21), dubbing-ai/SiangTTS-VoxCPM2-Thai-LoRA (CC-BY-SA-4.0, 2026-06-22), Mametoyas/SparkTTS-Thai-Emotion-Control (CC-BY-NC-SA-4.0, 2026-10-19), kunato/wayu-kokoro-thai-v1 (Apache-2.0), hotdogs/vibevoice-1.5b-thai-tts-lora (Apache-2.0), tranhuyluyen/piper-voices-thai (CC-BY-NC-4.0), VIZINTZOR MMS-TTS-THAI models. — [HF API](https://huggingface.co/api/models?search=thai&filter=text-to-speech&sort=downloads&limit=100)

### Inferences
- If a Thai Chatterbox fine-tune exists it is unlabelled/obscure. Thai developers have chosen other open bases, which are the practical alternatives if Chatterbox is not mandatory.
- Voice cloning / `exaggeration` behaviour in Thai: no evidence, because no Thai model exists.

### Gaps
- The HF listing was capped at 300 models and read through a summariser; a low-download Thai repo beyond that could be missed. GitHub fork search was not possible.
- Thai-language web search surfaced no Thai blog/community post about training Chatterbox for Thai (only a generic apidog.com Thai-language intro article, not inspected).

## 4. What happens if Thai text is fed to the stock multilingual model?

### Takeaway
`language_id="th"` is rejected with a ValueError; the grapheme tokenizer was built for the 23 supported languages, so Thai script is very likely out of vocabulary. No first-hand report of Thai output was found.

### Cited Findings
- `ChatterboxMultilingualTTS.generate` raises `ValueError("Unsupported language_id '...'. Supported languages: ...")` for any code outside the 23; the check only runs when `language_id` is truthy. — [mtl_tts.py mirror](https://huggingface.co/spaces/jkorstad/TTS/blob/main/chatterbox/mtl_tts.py)
- Tokenizer file is `grapheme_mtl_merged_expanded_v1.json`, loaded through `MTLTokenizer`. — [mtl_tts.py mirror](https://huggingface.co/spaces/jkorstad/TTS/blob/main/chatterbox/mtl_tts.py)
- A fine-tuning toolkit describes the standard tokenizer as grapheme-based, ~2,454 tokens covering 23 languages, and says a custom `tokenizer.json` is needed when a language uses characters it lacks. — [gokhaneraslan/chatterbox-finetuning](https://github.com/gokhaneraslan/chatterbox-finetuning)
- Same failure pattern reported for Kazakh codes (kk-kz, kk, kz) in the OSS model. — [Issue #493 (mirror)](https://github.blesdmm.dns-dynamic.net/resemble-ai/chatterbox/issues/493)

### Inferences
- Omitting `language_id` or passing another code with Thai text would most likely map Thai characters to unknown tokens and give garbage/silence; this is inferred, not tested.

### Gaps
- Tokenizer vocab was not downloaded and inspected for the Thai Unicode block (U+0E00–U+0E7F); HF downloads were blocked by the proxy. A one-line check of the JSON would settle it.

## 5. Fine-tuning tooling and feasibility of adding Thai

### Takeaway
Adding a new language is feasible with community tooling and has been done for Vietnamese (tonal; vocab extended to 2,549 tokens; 3,000+ h claimed), Indonesian, Slovak, Finnish, Uzbek, Kazakh and Tajik; it needs tokenizer extension plus embedding resize. Good results appear to need far more than the toolkit minimums, and nobody has published a Thai result.

### Cited Findings
- gokhaneraslan/chatterbox-finetuning (Apache-2.0, 109 stars, 34 commits): supports Standard (Llama-based) and Turbo (GPT-2-based) with LoRA or full fine-tune; LoRA recommended for ≤10 h of data, full fine-tune for >10 h; at least 30+ minutes for basic training, 3–10 s segments; `new_vocab_size` in `src/config.py` must exactly match the token count of `tokenizer.json` (2454 Standard, 52260 Turbo); LoRA claimed ~60% less VRAM; examples are Latin-script only; Thai not mentioned. — [gokhaneraslan/chatterbox-finetuning](https://github.com/gokhaneraslan/chatterbox-finetuning)
- stlohrey/chatterbox-finetuning (137 stars, 24 commits, self-described WIP): scripts to fine-tune T3 and S3/flow; example command uses a German dataset named `DE_Emilia_Yodas_680h`; no tokenizer or new-language guidance. — [stlohrey/chatterbox-finetuning](https://github.com/stlohrey/chatterbox-finetuning)
- Viterbox (dolly-vn, Vietnamese; citation year 2025): fine-tuned from Chatterbox Multilingual, vocabulary extended with Vietnamese tokens to 2,549 total; claims 3,000+ h (ViVoice ~1,000 h, PhoAudiobook ~1,200 h, internal ~800 h); zero-shot cloning from 3–10 s and `exaggeration` 0.0–2.0 still exposed; limitations: no streaming, quality loss beyond ~500 words, English words in Vietnamese text may be mispronounced; no metrics; weights CC BY-NC 4.0; 19 likes, 45 downloads last month. — [dolly-vn/viterbox](https://huggingface.co/dolly-vn/viterbox)
- grandhigh/Chatterbox-TTS-Indonesian: fine-tune of ResembleAI/chatterbox T3 (`t3_cfg.safetensors`) on SuaraGabungan-ID (~8.03k items; hours not stated); Apache-2.0; voice cloning via audio prompt; no metrics or limitations stated; 446 downloads, 25 likes. — [grandhigh/Chatterbox-TTS-Indonesian](https://huggingface.co/grandhigh/Chatterbox-TTS-Indonesian)
- Slovak fine-tune write-up (dev.to, posted 26 Apr, year not shown; weights pekiskol/chatterbox-tts-slovak): fine-tune vocab differs from base, so `text_emb.weight` and `text_head.weight` are resized (padded with row mean or trimmed); noisy reference audio is cloned into output; stable settings temperature 0.6, top_p 0.92, repetition penalty 1.25 flatten prosody; first word can be garbled; acronyms need text normalisation; long inputs can end early (30 s narrative lost its last word), so chunk by sentence. Data hours and hardware not stated. — [dev.to](https://dev.to/pekisko/fine-tuning-chatterbox-on-a-low-resource-language-7-things-that-mattered-13e1)
- Other community new-language fine-tunes exist: RASMUS/Chatterbox-Finnish (with train.py), UAzimov/Uzbek-tts-chatterbox, Tohirju/chatterbox-mtl-kazakh / -uzbek / -tajik. Not inspected in detail. — [RASMUS/Chatterbox-Finnish](https://huggingface.co/RASMUS/Chatterbox-Finnish/blob/main/train.py); [UAzimov/Uzbek-tts-chatterbox](https://huggingface.co/UAzimov/Uzbek-tts-chatterbox); [Tohirju/chatterbox-mtl-kazakh](https://huggingface.co/Tohirju/chatterbox-mtl-kazakh)
- Official guidance: none in the README. — [GitHub README](https://github.com/resemble-ai/chatterbox)

### Inferences
- Thai-specific risks not covered by any precedent found: no word spaces (grapheme tokenizer gets no word-boundary signal), tone marks and stacked vowels as combining characters, number/abbreviation normalisation. Vietnamese is the nearest tonal precedent, but it is Latin-script and needed thousands of hours; Resemble's own Vietnamese scored 75.21% CER. Expect a serious Thai model to need hundreds to thousands of hours, not the 30-minute LoRA minimum.
- Thai corpora used by other Thai TTS fine-tunes (Porameht/processed-voice-th-169k, Thanarit/Thai-Voice-Test7, hotdogs/thai-speech-20k; see HF API link in section 3) could serve as training data; their licences were not checked.
- Fine-tuned weights carry their own licence regardless of MIT base (Viterbox is non-commercial), so a self-trained Thai model's usability depends on dataset licences.

### Gaps
- No Khmer, Burmese or Lao Chatterbox fine-tune found. No report of any non-Latin, non-space-delimited script being added by the community with published metrics.
- No hard numbers for GPU type, VRAM or training time for a full new-language fine-tune.

## 6. Apple Silicon (MPS / MLX) and watermarking

### Takeaway
Chatterbox runs on Apple Silicon (MPS in the official code, MLX ports of Multilingual v2/v3 in mlx-audio), still limited to the same 23 languages. Official output is always watermarked with PerTh.

### Cited Findings
- README Multilingual example notes device may be "cpu" / "mps"; repo ships `example_for_mac.py`; tested officially on Python 3.11 / Debian 11. — [GitHub README](https://github.com/resemble-ai/chatterbox)
- mlx-audio README lists "Chatterbox | Expressive multilingual TTS (v2/v3) | 23 languages". — [mlx-audio README](https://cdn.jsdelivr.net/gh/blaizzy/mlx-audio@main/README.md)
- aufklarer/Chatterbox-Multilingual-MLX-fp16: MLX fp16 conversion (~1.3 GB vs ~2.6 GB F32), zero-shot cloning, MIT, "23 languages"; no Thai; no benchmarks; watermark not mentioned. — [HF model card](https://huggingface.co/aufklarer/Chatterbox-Multilingual-MLX-fp16)
- Other MLX routes exist: `chatterbox-mlx` on PyPI and DePasqualeOrg/mlx-audio-plus (not inspected). — [PyPI chatterbox-mlx](https://pypi.org/project/chatterbox-mlx/); [mlx-audio-plus](https://github.com/DePasqualeOrg/mlx-audio-plus)
- Every generated file includes Resemble's Perth watermark, "imperceptible neural watermarks that survive MP3 compression"; detection via `perth.PerthImplicitWatermarker` returns 0.0/1.0. — [GitHub README](https://github.com/resemble-ai/chatterbox)
- In code: `self.watermarker = perth.PerthImplicitWatermarker()` in `__init__`, and `apply_watermark(wav, sample_rate=self.sr)` before returning audio. — [mtl_tts.py mirror](https://huggingface.co/spaces/jkorstad/TTS/blob/main/chatterbox/mtl_tts.py)
- mlx-audio lists other models with broad language counts (OmniVoice "646+ languages", Higgs Audio v3 "100 languages", Fish Audio Drama 3 "83 languages") without naming Thai. — [mlx-audio README](https://cdn.jsdelivr.net/gh/blaizzy/mlx-audio@main/README.md)

### Inferences
- The watermark is applied in the Python wrapper after synthesis, so it is a code-level step under MIT rather than baked into weights; MLX ports may or may not apply it.
- A Thai fine-tune of the T3 weights (plus extended tokenizer) should in principle load on MPS; MLX would need conversion and a tokenizer/vocab-size patch. Untested.

### Gaps
- No Apple Silicon speed benchmarks found. Whether mlx-audio applies PerTh was not confirmed.
