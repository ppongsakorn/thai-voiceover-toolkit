# DIY Thai fine-tune of Chatterbox / IndexTTS-2(.5): feasibility, datasets, text frontend, precedents

Research date: 14 November 2026. All figures are as shown on the cited pages on that date. Items marked (inference) or (estimate) are my reasoning, not sourced facts. Several pages do not print a publication date; where that is so it is stated.

## 1. Thai speech datasets usable for TTS training (hours, speakers, quality, licence)

### Takeaway
Openly downloadable Thai speech that is commercially usable amounts to roughly 550-900 h of read, crowd-sourced, mostly 16 kHz audio (Common Voice CC0 + Porjai CC-BY-SA), plus ~500 h of CC-BY YouTube audio (YODAS). The only >10,000 h Thai corpus (GigaSpeech 2) is restricted to non-commercial research, Emilia / Emilia-YODAS contain no Thai, and no open Thai corpus is large, studio-grade and multi-speaker at once.

### Cited Findings

| Dataset | Hours / speakers | Type | Licence (commercial?) | Source |
|---|---|---|---|---|
| Common Voice Thai (v9.0 snapshot) | 158.88 h, 137,401 utterances, 4,656 speakers | Crowd-sourced read speech | CC0 (yes) | [MFA corpus page](https://mfa-models.readthedocs.io/en/latest/corpus/Thai/Common%20Voice%20Thai%20v9_0.html) |
| Common Voice Thai, newer releases | Scripted Speech 27.0 - Thai and Spontaneous Speech 5.0 - Thai are listed, both CC0-1.0; hours not shown on the listing | Crowd-sourced | CC0 (yes) | [Mozilla Data Collective](https://mozilladatacollective.com/datasets?q=Thai) |
| Porjai (CMKL) Thai voice dataset | ~700 h Central Thai + ~40 h each for Khummuang, Korat, Pattani dialects; 335,674 train examples in the central set; speaker count not stated; collected via Wang Data Market | Crowd-sourced read speech | CC-BY-SA 4.0 (yes, share-alike) | [HF dataset card](https://huggingface.co/datasets/CMKL/Porjai-Thai-voice-dataset-central/blob/main/README.md) |
| GigaSpeech 2 Thai | 12,901.8 h raw, 10,262.0 h refined; automatically crawled and transcribed | In-the-wild, ASR-labelled | Metadata tag says apache-2.0, but Terms of Access restrict use to "non-commercial research and educational purposes"; SpeechColab does not own audio copyright; gated | [HF dataset card](https://huggingface.co/datasets/speechcolab/gigaspeech2) |
| YODAS Thai | th000 (user-uploaded captions) 497.14 h; th100 (automatic captions) 1.87 h | YouTube, in-the-wild | cc-by-3.0 (only CC-licensed videos were downloaded) | [HF dataset card](https://huggingface.co/datasets/espnet/yodas) |
| Emilia / Emilia-YODAS | Six languages only (en, zh, de, fr, ja, ko), 215.6k h total; Thai is NOT included | In-the-wild | Emilia CC BY-NC 4.0; Emilia-YODAS CC BY 4.0 | [HF dataset card](https://huggingface.co/datasets/amphion/Emilia-Dataset) |
| Thai-SER (VISTEC / AIResearch) | 41 h 36 min, 27,854 utterances, 200 professional actors (112 F / 88 M); 5 emotions (neutral, angry, happy, sad, frustrated); studio ~31.7 h + Zoom ~9.9 h | Acted emotional speech | CC BY-SA 4.0 (yes, share-alike) | [arXiv 2507.09618](https://arxiv.org/html/2507.09618v1); data at [HF](https://huggingface.co/datasets/airesearch/thai-ser) |
| Thai Elderly Speech (Data Wow / VISAI) | 17 h 11 min, 19,200 files, 32 senior speakers | Read speech for ASR | CC BY-SA 4.0 | [SEACrowd card](https://huggingface.co/datasets/SEACrowd/thai_elderly_speech); [GitHub release](https://github.com/VISAI-DATAWOW/Thai-Elderly-Speech-dataset/releases/tag/v1.0.0) |
| TSync-2 (NECTEC) | 3.7 h usable after filtering in Vaja-Thai; one professional female speaker; studio | Studio single speaker | CC-BY-NC-SA 3.0 (no commercial use) | [Vaja-Thai card](https://huggingface.co/datasets/dubbing-ai/vaja-thai) |
| Vaja-Thai (dubbing-ai) — ready-made TTS aggregate | 554.6 h / 289,916 samples at 24 kHz: Porjai Central 412.5 h, Common Voice validated 130.3 h, GigaSpeech2 dev+test 8.1 h, TSync2 3.7 h; filtered at Whisper CER <= 0.15, 1-30 s; 16 kHz sources upsampled with AP-BWE; quality tiers 1-4 | Aggregate | Mixed; card says most restrictive (non-commercial) applies when combined; gated | [HF dataset card](https://huggingface.co/datasets/dubbing-ai/vaja-thai) |
| Content X Labs Thai Episodic Television | 100 h, 630.79 GB, "rights-cleared" | TV dialogue | CXL-DLA-1.0 (proprietary licence; terms not checked) | [Mozilla Data Collective](https://mozilladatacollective.com/datasets?q=Thai) |

Data actually used by Thai models in 2025-2026:
- F5-TTS-THAI: Common Voice Thai ~160 h (Porameht/processed-voice-th-169k) + Porjai ~300 h + Common Voice English ~40 h — [HF model card](https://huggingface.co/VIZINTZOR/F5-TTS-THAI)
- SiangTTS: ~205 h from Common Voice Thai, porjai_central and a LibriTTS-R English slice — [HF model card](https://huggingface.co/dubbing-ai/SiangTTS-VoxCPM2-Thai-LoRA)
- ThonburianTTS: card metadata lists `speechcolab/gigaspeech` as training dataset; hours not stated — [HF model card](https://huggingface.co/biodatlab/ThonburianTTS)
- JaiTTS-v1.0: ~10,000 h of proprietary Thai-centric speech (podcasts plus finance, healthcare, education, law; studio and crowd-sourced; ASR transcripts with post-processing); the data is not released — [arXiv 2604.27607](https://arxiv.org/html/2604.27607v2)
- OmniVoice: 581k h over 600+ languages from ~50 corpora including Emilia, Common Voice, FLEURS, GigaSpeech 2; the paper text gives no per-language Thai figure — [arXiv 2604.00688](https://arxiv.org/html/2604.00688v2)
- "Empowering Global Voices" Thai TTS: 500 h multi-domain (600+ speakers, 24 kHz) + 40 h vertical-domain YouTube data; not released — [arXiv 2504.07858](https://arxiv.org/html/2504.07858v1)

### Inferences
- OmniVoice's "~10,500 h Thai" figure quoted in the brief is consistent with GigaSpeech 2 refined Thai (10,262 h) plus Common Voice/FLEURS, but I could not confirm the number in the paper text (per-language data is only in figures). If that is the source, OmniVoice's Thai ability rests on non-commercial-terms data.
- The realistic "clean licence" DIY training set is what SiangTTS and F5-TTS-THAI used: Common Voice + Porjai, about 200-550 h after quality filtering (Vaja-Thai kept 412.5 h of Porjai's ~700 h and 130.3 h of Common Voice at CER <= 0.15).
- Both main open corpora are 16 kHz crowd recordings without reliable speaker labels (Porjai has none), which limits fidelity and speaker-similarity training for a 24 kHz/44.1 kHz cloning model; Vaja-Thai's bandwidth-extension step shows others had to work around this.

### Gaps
- Current validated hours and speaker count of Common Voice Scripted Speech 27.0 Thai: dataset pages did not render; only the v9.0 figure (158.88 h) and Vaja-Thai's filtered 130.3 h were verifiable.
- LOTUS (NECTEC), TSync-1, FLEURS Thai: no page with hours and licence was retrieved in this session; not verified. LOTUS family items found were LOTUSDIS (far-field meeting ASR corpus, [GitHub](https://github.com/CAI-NECTEC/LOTUSDIS)), which is not TTS-grade.
- TSync-2's original total hours (the 3.7 h figure is post-filter) and NECTEC's primary licence page were not retrieved.
- No public release of the JaiTTS 10k h set, the "Empowering Global Voices" 540 h set, or any 2026 large studio-grade open Thai TTS corpus was found.

## 2. Thai text frontend: normalisation, segmentation, G2P — and whether BPE/character models need them

### Takeaway
Recent Thai-capable models (JaiTTS, SiangTTS/VoxCPM2, OmniVoice, F5-TTS-THAI) feed raw Thai text through BPE or characters without G2P, so a G2P frontend is optional; but precedents show number/abbreviation/English normalisation remains the weak spot and is worth doing with PyThaiNLP-class tools before training and at inference.

### Cited Findings
- PyThaiNLP is Apache-2.0 (commercial use allowed); default word tokenizer is NewMM (dictionary maximum matching over Thai character clusters, 71.18% on BEST 2010, fastest tested), with a Rust port nlpo3; it includes "a couple of" G2P engines (one trained on Wiktionary data), RTGS romanisation, and CRF sentence segmentation. TLTK is a separate library offering G2P, IPA transcription and romanisation — [PyThaiNLP paper, arXiv 2312.04649](https://arxiv.org/html/2312.04649v1)
- PyThaiNLP API docs for transliteration/G2P and tokenisation engines — [transliterate docs](https://pythainlp.github.io/docs/5.0/api/transliterate.html); [tokenize docs](https://pythainlp.github.io/docs/2.2/api/tokenize.html)
- JaiTTS: text is BPE-tokenised and fed directly; authors say it handles numerals and Thai-English code-switching without explicit normalisation; no G2P — [arXiv 2604.27607](https://arxiv.org/html/2604.27607v2)
- SiangTTS: raw text, no phonetic-respelling dictionary; optional external text normalisation flag at inference — [HF model card](https://huggingface.co/dubbing-ai/SiangTTS-VoxCPM2-Thai-LoRA)
- OmniVoice: uses the Qwen3-0.6B subword tokenizer with no G2P or language-specific normalisation — [arXiv 2604.00688](https://arxiv.org/html/2604.00688v2)
- ThonburianTTS ships two checkpoints, Thai-script input and IPA input — [HF model card](https://huggingface.co/biodatlab/ThonburianTTS)
- F5-TTS-THAI takes Thai orthography; non-Thai words must be written as Thai readings (e.g. "Good Morning" as "กูดมอร์นิ่ง"); long texts and some words are misread — [HF model card](https://huggingface.co/VIZINTZOR/F5-TTS-THAI)
- A phoneme-tone pipeline (PyThaiNLP tokenizer extended from 60k to 100k words, IPA G2P with five tone markers, LLM pause prediction) reported that removing G2P optimisation raised WER to 22.5% and cut NMOS to 3.0 in that (non-LLM, predictor-based) architecture — [arXiv 2504.07858](https://arxiv.org/html/2504.07858v1)
- The Wayu/Paxa paper lists Thai frontend challenges as ambiguous word boundaries, lexical tone, names and loanwords, numeric verbalisation and Thai-English code-switching; its 82M fixed-voice model reaches 3.7% Thai CER — [HF papers 2609.03502](https://huggingface.co/papers/2609.03502)
- Chatterbox Multilingual uses a 2,454-token grapheme vocabulary (`grapheme_mtl_merged_expanded_v1.json`); scripts outside it are out-of-vocabulary — [chatterbox-mtl-uzbek card](https://huggingface.co/Tohirju/chatterbox-mtl-uzbek)
- IndexTTS-2.5 uses language-specific frontends (pinyin, CMU phonemes, Japanese kana; fugashi-based kanji-to-katakana for Japanese) — [IndexTTS repo](https://github.com/index-tts/index-tts); [IndexTTS 2.5 report](https://arxiv.org/pdf/2601.03888)
- Community German IndexTTS-2.5 fine-tune added its own normalisation frontend (`german_text.py`); numbers/dates were still the worst category at 15.62% WER — [HF model card](https://huggingface.co/sharrnah/index-tts-2.5-german)
- Slovak Chatterbox fine-tune: letter names, acronyms and units were misread, so text normalisation was required — [DEV post](https://dev.to/pekisko/fine-tuning-chatterbox-on-a-low-resource-language-7-things-that-mattered-13e1)

### Inferences
- For Chatterbox, Thai script is almost certainly out of the stock 2,454-token vocabulary (Thai is not among its languages), so the tokenizer and the T3 text embedding/head must be extended with Thai characters or an IPA/romanised form — the Vietnamese Viterbox precedent did exactly this (vocab grown to 2,549). (inference from the Uzbek/Tajik cards plus Viterbox card)
- Two workable Thai input designs: (a) raw Thai characters/BPE, relying on hundreds of hours to learn tone and segmentation implicitly (what every current open Thai zero-shot model does); (b) PyThaiNLP/TLTK G2P to IPA with tone marks, which lets small data go further but adds G2P errors and breaks code-switching. With only ~200-500 h, pre-normalising numerals, dates, abbreviations and ๆ (mai yamok) with PyThaiNLP is the low-risk middle path. (inference)

### Gaps
- attacut, deepcut and the standalone `thai-g2p` package: no primary page retrieved this session; their current maintenance status and licences are unverified.
- Exact PyThaiNLP function names for number/abbreviation expansion were not confirmed from the docs fetched.
- ThonburianTTS's measured IPA-vs-grapheme difference (iSAI-NLP 2025 paper) could not be read; the Mahidol repository page did not render.

## 3. Documented precedents of adding a language (Chatterbox, IndexTTS, comparable models) incl. Thai precedents

### Takeaway
Community fine-tunes show ~100-300 h is enough to add a new language to Chatterbox (T3 only) or IndexTTS-2.5 (LoRA on GPT + text embeddings) with intelligible output (roughly 5-19% WER), and ~200 h LoRA made VoxCPM2 Thai excellent — but no Thai Chatterbox or Thai IndexTTS fine-tune was found, the one tonal-language Chatterbox port (Vietnamese) used 3,000+ h, and Resemble's own v3 scores for Vietnamese and Korean are very poor.

### Cited Findings
Chatterbox:
- Chatterbox Multilingual v3 (10 June 2026) covers 25 entries (21 languages + 4 dialect variants); Thai is not among them; same 0.5B Llama backbone, MIT; training mix grew from 25.6k h to 36.7k h; Resemble reports Korean and Vietnamese at 70.90% and 75.21% CER and advises against commercial use in those; an August 2026 update says Chatterbox is retired commercially and stays open source with no support or updates — [Resemble AI](https://www.resemble.ai/resources/chatterbox-multilingual-v3-tts-with-embedded-watermarking-for-25-languages)
- Uzbek: 119.4 h (100k utterances, CC0 uzbekvoice), only T3 fine-tuned (S3Gen and voice encoder frozen), 12,500 steps at lr 1e-5, best checkpoint at step 6,000; round-trip WER on FLEURS-uz 19.1% mean / 14.8% median; no tokenizer extension — Uzbek Latin mapped to the Turkish language token; model MIT — [HF card](https://huggingface.co/Tohirju/chatterbox-mtl-uzbek)
- Tajik (Cyrillic): 205.5 h, same recipe, best checkpoint step 8,000, WER 10.7% mean / 8.3% median on FLEURS-tg (self-scored), run with `language_id="ru"`; MIT — [HF card](https://huggingface.co/Tohirju/chatterbox-mtl-tajik)
- Vietnamese (tonal) "Viterbox": 3,000+ h (ViVoice ~1,000 h, PhoAudiobook ~1,200 h, internal ~800 h), vocabulary extended to 2,549 tokens; no metrics published; released CC BY-NC 4.0 — [HF card](https://huggingface.co/dolly-vn/viterbox)
- Slovak: pitfalls were vocab-size mismatch on loading (pad `text_emb`/`text_head` with the row mean, not zeros), premature EOS, garbled first word, reference-clip noise carried into output, default sampling instability, and some loss of expressiveness with stabilised settings; no hours or metrics given — [DEV post, 26 Apr, year not shown](https://dev.to/pekisko/fine-tuning-chatterbox-on-a-low-resource-language-7-things-that-mattered-13e1)
- A LoRA fine-tuning toolkit for Chatterbox Multilingual states a 16 GB VRAM minimum (24 GB+ recommended), CPU training "much slower", and warns that a reference clip in another language carries its accent — [GitHub mirror](https://gh.hhj520.top/Ahmed-Ezzat20/chatterbox-finetuning-multilingual)

IndexTTS:
- Official IndexTTS-2.5 (weights released 10 Aug 2026) supports Chinese, English, Japanese, Spanish, Arabic — no Thai — [IndexTTS repo](https://github.com/index-tts/index-tts)
- bilibili added languages with tens of thousands of hours each (Japanese 42K h, Spanish 22.9K h, Arabic 20K h); only 135 h of emotional data, all Chinese/English, yet emotion similarity carried over to Japanese/Spanish (0.896 / 0.922) and to Arabic; Japanese WER 5.66%, Spanish 3.75%; training hardware not reported — [IndexTTS 2.5 technical report](https://arxiv.org/pdf/2601.03888)
- Community German fine-tune of IndexTTS-2.5: 310 h (MLS German 150 h, HUI 140 h, Emilia-YODAS German 20 h), LoRA rank 64 on all 24 GPT layers plus text embeddings and output heads, emotion path and speaker projection frozen, best checkpoint at step 16,000 (later ones were worse), 5.35% WER on 30 sentences; hardware/time and training code not stated — [HF card](https://huggingface.co/sharrnah/index-tts-2.5-german)

F5-TTS and others:
- Polish F5-TTS community reports: ~90 h trained from scratch converged around 350k steps, about 24 h on an A100 80GB; a guide (unverified) estimates 2-5 days on an RTX 4090 for 100k-150k fine-tune steps; vocab.txt must be extended; 24 GB cards hit VRAM crashes — [F5-TTS discussion #1168](https://github.com/SWivid/F5-TTS/discussions/1168)
- OmniVoice Thai community fine-tune: ~12.6 h, 2 speakers, 1,747 steps, ~1.5 h on one RTX 3090 (Vast.ai); only training loss reported, no CER — [HF card](https://huggingface.co/hotdogs/omnivoice-thai)

Thai models:
- F5-TTS-THAI: ~500 h (see section 1), fine-tuned from SWivid/F5-TTS to 1,000,000 steps, CC-BY-4.0; hardware not stated; still misreads long text and some words — [HF card](https://huggingface.co/VIZINTZOR/F5-TTS-THAI)
- ThonburianTTS: F5-TTS fine-tune, Thai-script and IPA variants, trained on the NSTDA ThaiSC supercomputer, CC BY-NC-SA 4.0 — [HF card](https://huggingface.co/biodatlab/ThonburianTTS); in the JaiTTS benchmark it scored 6.26% CER / 0.48 SIM on short clips and failed on long ones — [arXiv 2604.27607](https://arxiv.org/html/2604.27607v2)
- JaiTTS-v1.0: VoxCPM-based, ~10,000 h; 1.94% CER / 0.62 SIM short, 2.55% / 0.76 long (human reference 1.98% / 2.47%); beat ElevenLabs v3 and MiniMax speech-2.8-hd in 283 of 400 pairwise comparisons; training hardware not reported; emotion not discussed — [arXiv 2604.27607](https://arxiv.org/html/2604.27607v2)
- OpenJaiTTS-v1.0 (the released open model, F5-TTS-based, CC BY-NC 4.0): 4.78% short CER, 12.63% long CER — far behind the proprietary JaiTTS — [HF card](https://huggingface.co/JTS-AI/OpenJaiTTS-v1.0)
- SiangTTS: LoRA on VoxCPM2, ~205 h, 2 epochs on one RTX 3090 (24 GB); CER 3.26% (base) -> 0.84% vs 0.97% for real recordings, SIM 0.906 -> 0.909 on 80 cloning prompts; weak on rare Pali-Sanskrit vocabulary; adapter CC-BY-SA-4.0 — [HF card](https://huggingface.co/dubbing-ai/SiangTTS-VoxCPM2-Thai-LoRA)
- OmniVoice Thai (stock): WER 3.978, SIM 0.841 on MiniMax-Multilingual-24 (MiniMax 2.701, ElevenLabs 73.936) — [arXiv 2604.00688](https://arxiv.org/html/2604.00688v2)

### Inferences
- SiangTTS is not a like-for-like precedent: VoxCPM2 already spoke Thai (3.26% CER before tuning), so 205 h only polished it. Chatterbox and IndexTTS have zero Thai and no Thai script in their vocabularies, so a Thai fine-tune there is "new language", closer to the Uzbek/Tajik/German cases (10-19% WER class results at 120-310 h) than to SiangTTS's 0.84% CER.
- Tone is an extra risk the Latin/Cyrillic precedents do not test. The only tonal Chatterbox data points are negative or expensive: Resemble's own Vietnamese at 75% CER, and Viterbox needing 3,000+ h. A ~500 h Thai Chatterbox fine-tune is therefore unlikely to match JaiTTS/SiangTTS/OmniVoice on accuracy. (inference)
- Catastrophic forgetting was not measured in any precedent found; mitigation seen in practice is mixing in English (F5-TTS-THAI added ~40 h, SiangTTS a LibriTTS-R slice) and freezing non-text paths (German IndexTTS).
- Best checkpoints arrived early (6k-16k steps) and later ones degraded, so checkpoint sweeps with an ASR scorer (e.g. a Thai Whisper) are part of the required work.

### Gaps
- No Thai fine-tune of Chatterbox or IndexTTS-2/2.5 was found on Hugging Face or GitHub as of 14 Nov 2026.
- Whether bilibili has released official training/fine-tuning code for IndexTTS-2/2.5: the repo README does not say; the German fine-tune does not link its training code.
- XTTS-v2, CosyVoice and GPT-SoVITS new-language write-ups were not retrieved this session.
- The Towards AI article "What I Got Wrong Fine-Tuning F5-TTS for a New Writing System" could not be fetched.

## 4. Emotional Thai data: enough to keep emotion control working?

### Takeaway
Thai-SER (41.6 h, 200 actors, 5 emotions, CC BY-SA) is the only open emotional Thai corpus found; evidence from IndexTTS-2.5 suggests emotion control can transfer to a new language without any emotional data in that language if the emotion path is left untouched, so Thai-SER is a useful supplement rather than a prerequisite.

### Cited Findings
- Thai-SER: 41 h 36 min, 27,854 utterances, 200 professional actors, neutral/angry/happy/sad/frustrated, ~31.7 h studio and ~9.9 h Zoom, scripted and improvised, CC BY-SA 4.0 — [arXiv 2507.09618](https://arxiv.org/html/2507.09618v1)
- IndexTTS-2.5 trained emotion on only 135 h (Chinese and English); Japanese and Spanish had no emotional data yet scored emotion similarity 0.896 and 0.922, and emotion transferred to Arabic (MOS 4.18) — [IndexTTS 2.5 report](https://arxiv.org/pdf/2601.03888)
- German IndexTTS-2.5 fine-tune froze the emotion path and speaker projection; its example disables the Qwen emotion module and reports no German emotion evaluation — [HF card](https://huggingface.co/sharrnah/index-tts-2.5-german)
- Chatterbox precedents fine-tuned only T3 and left S3Gen/voice encoder frozen; the Slovak write-up kept `exaggeration` at 0.5 and noted reduced expressiveness with stabilised sampling settings; none evaluated emotion control — [Uzbek card](https://huggingface.co/Tohirju/chatterbox-mtl-uzbek); [DEV post](https://dev.to/pekisko/fine-tuning-chatterbox-on-a-low-resource-language-7-things-that-mattered-13e1)
- JaiTTS does not mention emotion control at all — [arXiv 2604.27607](https://arxiv.org/html/2604.27607v2)

### Inferences
- For IndexTTS, the least risky recipe is the German one: train only GPT LoRA + text embeddings, freeze the emotion path; emotion vectors/prompts should then still work in Thai, but this is unproven for Thai.
- For Chatterbox, the exaggeration control lives in T3 conditioning, which is the part being fine-tuned on neutral read speech (Common Voice/Porjai); some flattening is plausible. Mixing Thai-SER (~30 h studio) into training is the only open way to expose the model to expressive Thai. (inference; no source measured it)
- Thai-SER is 41.6 h of acted dialogue with five coarse labels — small next to IndexTTS's 135 h emotional set, and Zoom-recorded parts are low fidelity.

### Gaps
- No source measured emotion-control retention after a new-language fine-tune of Chatterbox.
- Thai-SER transcript availability/quality for TTS use (it is an SER corpus) was not checked.

## 5. Cost/time ranges reported, and MacBook Pro (Apple Silicon, 128 GB) vs cloud GPU

### Takeaway
Reported community fine-tunes of this kind ran on a single 24 GB RTX 3090/4090 or one A100 for hours to a few days; from-scratch or lab-scale training used 8 data-centre GPUs for 8-10 days. No source documents training Chatterbox or IndexTTS on Apple Silicon; the Mac is suited to data preparation, inference and evaluation, with training on a cloud GPU.

### Cited Findings
- SiangTTS: one RTX 3090 24 GB, 2 epochs over ~205 h; wall-clock not given — [HF card](https://huggingface.co/dubbing-ai/SiangTTS-VoxCPM2-Thai-LoRA)
- OmniVoice Thai fine-tune: ~1 h 30 min on one RTX 3090 (Vast.ai) for ~12.6 h of data — [HF card](https://huggingface.co/hotdogs/omnivoice-thai)
- F5-TTS Polish: ~90 h dataset, ~24 h on an A100 80GB; unverified guide figure of 2-5 days on an RTX 4090 for 100k-150k steps; out-of-memory crashes reported on 24 GB — [F5-TTS discussion #1168](https://github.com/SWivid/F5-TTS/discussions/1168)
- Chatterbox LoRA toolkit: minimum 16 GB NVIDIA VRAM, 24 GB+ recommended; CPU possible but much slower — [GitHub mirror](https://gh.hhj520.top/Ahmed-Ezzat20/chatterbox-finetuning-multilingual)
- Chatterbox Uzbek/Tajik: 12,500 steps total, best at 6,000-8,000; hardware not stated — [Uzbek card](https://huggingface.co/Tohirju/chatterbox-mtl-uzbek); [Tajik card](https://huggingface.co/Tohirju/chatterbox-mtl-tajik)
- IndexTTS-2.5 German: best at 16,000 steps; ~6 GB VRAM for inference; training hardware not stated — [HF card](https://huggingface.co/sharrnah/index-tts-2.5-german)
- Lab scale: OmniVoice 8x H800 for 9.66 days (2M updates, 581k h); "Empowering Global Voices" Thai system 8x A800 for 8 days (540 h) — [arXiv 2604.00688](https://arxiv.org/html/2604.00688v2); [arXiv 2504.07858](https://arxiv.org/html/2504.07858v1)
- F5-TTS-THAI was run to 1,000,000 steps — [HF card](https://huggingface.co/VIZINTZOR/F5-TTS-THAI)
- Apple Silicon: inference ports of Chatterbox exist (MLX package, MPS adaptation) — [chatterbox-mlx on PyPI](https://pypi.org/project/chatterbox-mlx/); [Apple Silicon adaptation notes](https://huggingface.co/spaces/Jimmi42/chatterbox-tts-apple-silicon/blob/main/APPLE_SILICON_ADAPTATION_SUMMARY.md)

### Inferences
- (estimate) A T3-only or LoRA fine-tune of Chatterbox or IndexTTS on ~200-500 h of Thai fits one 24-48 GB GPU and should take on the order of 1-4 days of GPU time including a few restarts and checkpoint sweeps; at typical single-A100/A10-class Azure on-demand rates that is tens to low hundreds of US dollars of compute per run, with several runs likely. I did not retrieve Azure prices; treat this as an order-of-magnitude estimate only.
- (estimate) The larger hidden cost is data work: downloading and filtering ~700 h of Porjai + Common Voice, ASR-based CER filtering, optional bandwidth extension to 24 kHz, normalisation, and building a Thai eval set — realistically 1-3 weeks of part-time engineering before the first useful run.
- MacBook Pro 128 GB: sensible for dataset filtering, Whisper-based CER scoring, PyThaiNLP normalisation and running inference/evaluation of checkpoints. Training on MPS is undocumented for these repos (toolkits state NVIDIA/CUDA requirements), so expect porting effort and much slower throughput; I found no report of a successful Chatterbox/IndexTTS training run on a Mac.

### Gaps
- No source gives a dollar cost for any of these fine-tunes.
- No source reports wall-clock time for a Chatterbox or IndexTTS new-language fine-tune.
- No benchmark of TTS fine-tuning on Apple Silicon (MPS/MLX) vs CUDA was found; Azure GPU SKU pricing was not looked up.

## 6. Licence implications (model weights and datasets)

### Takeaway
A Thai Chatterbox fine-tune can be MIT and commercially usable if trained only on CC0/CC-BY/CC-BY-SA data (share-alike data arguably pushes the weights to CC-BY-SA, as SiangTTS chose); a Thai IndexTTS fine-tune remains a "Derivative Work" under the bilibili licence with pass-through obligations; using GigaSpeech 2, TSync-2 or Emilia (non-YODAS) would taint a commercial model.

### Cited Findings
- Chatterbox (incl. Multilingual v3) is MIT; Resemble retired it commercially in August 2026 with no further support or updates; self-hosted outputs carry the PerTh watermark by default — [Resemble AI](https://www.resemble.ai/resources/chatterbox-multilingual-v3-tts-with-embedded-watermarking-for-25-languages)
- Community Chatterbox fine-tunes were released as MIT (Uzbek, Tajik) or CC BY-NC 4.0 (Vietnamese Viterbox, author's choice) — [Uzbek](https://huggingface.co/Tohirju/chatterbox-mtl-uzbek); [Viterbox](https://huggingface.co/dolly-vn/viterbox)
- bilibili Model Use License Agreement: royalty-free, non-exclusive licence; entities with >100 million MAU or >RMB 1 billion annual revenue need a separate written licence; "Derivative Work" explicitly covers fine-tuned, LoRA, quantised and merged models and outputs; redistribution must pass on the licence terms and notices and state that bilibili does not endorse the modifications; using the model or derivatives to improve other AI models is restricted (except the model itself, its derivatives, or non-commercial models); high-risk uses restricted; Chinese law, Shanghai arbitration — [LICENSE](https://raw.githubusercontent.com/index-tts/index-tts/main/LICENSE)
- The IndexTTS README directs commercial usage and cooperation enquiries to bilibili by email — [IndexTTS repo](https://github.com/index-tts/index-tts)
- The German IndexTTS-2.5 fine-tune is released under the bilibili licence as a derivative work — [HF card](https://huggingface.co/sharrnah/index-tts-2.5-german)
- SiangTTS released its adapter as CC-BY-SA-4.0, "inherited from the most restrictive training data" (Porjai) — [HF card](https://huggingface.co/dubbing-ai/SiangTTS-VoxCPM2-Thai-LoRA)
- Dataset terms: Common Voice CC0; Porjai CC-BY-SA 4.0; Thai-SER and Thai Elderly CC BY-SA 4.0; YODAS cc-by-3.0; TSync-2 CC-BY-NC-SA 3.0; GigaSpeech 2 non-commercial research/education only (though its card notes trained models "may be eligible for commercial license"); Emilia CC BY-NC 4.0, Emilia-YODAS CC BY 4.0 — sources as in section 1: [Porjai](https://huggingface.co/datasets/CMKL/Porjai-Thai-voice-dataset-central/blob/main/README.md), [GigaSpeech 2](https://huggingface.co/datasets/speechcolab/gigaspeech2), [Vaja-Thai](https://huggingface.co/datasets/dubbing-ai/vaja-thai), [Emilia](https://huggingface.co/datasets/amphion/Emilia-Dataset), [YODAS](https://huggingface.co/datasets/espnet/yodas)
- Existing Thai model licences for comparison: F5-TTS-THAI CC-BY-4.0; ThonburianTTS CC BY-NC-SA 4.0; OpenJaiTTS CC BY-NC 4.0; SiangTTS adapter CC-BY-SA-4.0 on Apache-2.0 VoxCPM2 — [F5-TTS-THAI](https://huggingface.co/VIZINTZOR/F5-TTS-THAI); [ThonburianTTS](https://huggingface.co/biodatlab/ThonburianTTS); [OpenJaiTTS](https://huggingface.co/JTS-AI/OpenJaiTTS-v1.0); [SiangTTS](https://huggingface.co/dubbing-ai/SiangTTS-VoxCPM2-Thai-LoRA)

### Inferences
- Whether share-alike dataset licences legally bind model weights is unsettled; SiangTTS took the conservative reading. A company deploying internally (not redistributing weights) is less exposed to share-alike than to non-commercial clauses. This is not legal advice.
- For a Thai commercial product, the clean stack is Chatterbox (MIT) + Common Voice + Porjai (+ Thai-SER, YODAS). IndexTTS is usable commercially below the size thresholds but with downstream licence pass-through and a restriction on using outputs/derivatives to train other commercial models (e.g. distilling into a small model as Wayu did from OmniVoice would be restricted).
- Chatterbox's retirement means a Thai fine-tune would sit on a base model that no longer receives fixes.

### Gaps
- The IndexTTS DISCLAIMER file was not read.
- Licences of VoxCPM2-era alternatives other than SiangTTS (OmniVoice model licence, Audio8-TTS-Realistic) were not verified here; the OmniVoice paper text does not name a model licence.

## 7. Overall judgement: is the DIY route realistic versus models that already speak Thai?

### Takeaway
Technically feasible for one person (single cloud GPU, ~200-550 h of open data, days of compute, weeks of data/eval work), but the evidence points to a result clearly below existing Thai-capable models: new-language fine-tunes at this data scale land around 5-19% WER, whereas SiangTTS reports 0.84% CER, JaiTTS 1.94% and stock OmniVoice about 4% WER on Thai.

### Cited Findings
- New-language fine-tune quality at 120-310 h: Uzbek 19.1% mean WER, Tajik 10.7%, German IndexTTS-2.5 5.35% — [Uzbek](https://huggingface.co/Tohirju/chatterbox-mtl-uzbek); [Tajik](https://huggingface.co/Tohirju/chatterbox-mtl-tajik); [German](https://huggingface.co/sharrnah/index-tts-2.5-german)
- Thai-capable baselines: SiangTTS 0.84% CER; JaiTTS 1.94% / 2.55% CER; OmniVoice 3.978 WER; OpenJaiTTS (F5-based) 4.78% / 12.63% CER; ThonburianTTS 6.26% CER and failure on long clips — [SiangTTS](https://huggingface.co/dubbing-ai/SiangTTS-VoxCPM2-Thai-LoRA); [JaiTTS](https://arxiv.org/html/2604.27607v2); [OmniVoice](https://arxiv.org/html/2604.00688v2); [OpenJaiTTS](https://huggingface.co/JTS-AI/OpenJaiTTS-v1.0)
- Resemble's own tonal-language result (Vietnamese 75.21% CER in v3) and the 3,000+ h used by Viterbox — [Resemble AI](https://www.resemble.ai/resources/chatterbox-multilingual-v3-tts-with-embedded-watermarking-for-25-languages); [Viterbox](https://huggingface.co/dolly-vn/viterbox)
- The same ~205 h of open data, applied as a LoRA to a model that already knows Thai, ran on one RTX 3090 — [SiangTTS](https://huggingface.co/dubbing-ai/SiangTTS-VoxCPM2-Thai-LoRA)

### Inferences
- Metrics above are from different test sets and ASR scorers and are not directly comparable; the direction, not the exact gap, is the finding.
- If the goal is a specific Chatterbox/IndexTTS feature in Thai (IndexTTS emotion/duration control), the IndexTTS-2.5 LoRA route with frozen emotion path is the better-evidenced experiment (German precedent, cross-lingual emotion transfer in the official report). If the goal is simply good Thai cloning, spending the same effort on a LoRA for a Thai-capable base is far better supported.

### Gaps
- No head-to-head evaluation of any Chatterbox or IndexTTS Thai output exists, so the expected Thai quality is extrapolated from other languages.
