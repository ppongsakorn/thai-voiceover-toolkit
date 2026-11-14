# Thai-language support for IndexTTS-2 / IndexTTS-2.5 (state as of 14 Nov 2026)

Status legend used throughout: **OFFICIAL** = shipped by bilibili Index team; **COMMUNITY** = third-party fine-tune/fork exists; **NOT FOUND** = searched, nothing located.

Headline: Thai is **not officially supported** in any IndexTTS release (1.0, 1.5, 2, 2.5). **Community Thai fine-tunes exist, but only for IndexTTS-2** (three artefacts from two authors plus one opaque Replicate endpoint). **No Thai fine-tune of IndexTTS-2.5 was found.**

## 1. Official status: languages in IndexTTS-2 and IndexTTS-2.5, and what changed in 2.5

### Takeaway
Officially, IndexTTS-2 is Chinese + English and IndexTTS-2.5 is Chinese, English, Japanese, Spanish and Arabic; Thai appears nowhere in the README, the Hugging Face card, or the 2.5 technical report, and no language roadmap is published. IndexTTS-2.5 weights were released 10 Aug 2026 (technical report Jan 2026) with a 25 Hz semantic codec, Zipformer S2M and ~2.28x faster inference.

### Cited Findings
- (Read 14 Nov 2026) Official README states IndexTTS-2.5 "supports Chinese, English, Japanese, Spanish and Arabic"; Thai is not mentioned; no roadmap of future languages is given. — [GitHub README](https://github.com/index-tts/index-tts)
- README release log: 2025/02/12 paper on arXiv; 2025/03/25 IndexTTS-1.0 (weights + inference code); 2025/05/14 IndexTTS-1.5 ("significantly improving the model's stability and its performance in English"); 2025/09/08 IndexTTS-2; 2026/08/10 IndexTTS-2.5 ("faster inference than IndexTTS-2"). — [GitHub README](https://github.com/index-tts/index-tts)
- Hugging Face card IndexTeam/IndexTTS-2.5 (read 14 Nov 2026): 5 languages "Chinese, English, Japanese, Spanish and Arabic"; licence tag "bilibili-model-license"; 8-float emotion vector; optional text-based emotion (needs QwenEmotion model); `duration_factor` parameter valid 0.5–2.0; requires "an NVIDIA GPU", ~6 GB VRAM; 26,945 downloads last month, 269 likes; model tree shows 7 finetunes, 3 quantizations; Thai not mentioned; no training code mentioned. — [HF IndexTeam/IndexTTS-2.5](https://huggingface.co/IndexTeam/IndexTTS-2.5)
- IndexTTS 2.5 Technical Report (arXiv 2601.03888, v3 dated 9 Jan 2026): semantic codec frame rate 50 Hz -> 25 Hz; S2M backbone U-DiT -> Zipformer; T2S keeps IndexTTS-2 architecture; GRPO post-training on T2S; "2.28x improvement in real-time factor"; T2S RTF 0.232 -> 0.119, S2M RTF 0.078 -> 0.017. — [arXiv 2601.03888v3](https://arxiv.org/html/2601.03888v3)
- The technical report covers only four languages: Mandarin, English, Japanese, Spanish; training data ~100K hours (Mandarin 30K h, English 25K h, Japanese 42K h, Spanish 2.9K h) plus 135 h emotional speech. Thai is not mentioned. — [arXiv 2601.03888v3](https://arxiv.org/html/2601.03888v3)
- Report proposes three cross-lingual strategies (boundary-aware alignment, token-level concatenation, instruction-guided generation) and judges token-level concatenation most stable; claims "robust emotion transfer even without target-language emotional training data"; emotional similarity 0.846 (Japanese) and 0.924 (Spanish) vs CosyVoice 3 at 0.806 / 0.883. — [arXiv 2601.03888v3](https://arxiv.org/html/2601.03888v3)
- Third-party news page (updated 10 Aug 2026) summarises 2.5 vs 2: adds Japanese, Spanish, Arabic; faster inference; speaking-speed control; inline pronunciation control (Pinyin, CMU phonemes, Kana); 22.05 kHz output; ~0.8B GPT backbone; ~6 GB VRAM in bf16; no mention of training code or future languages. — [comfyui-wiki news](https://comfyui-wiki.com/en/news/2026-08-10-indextts-2-5)
- README notes for IndexTTS-2 (Sept 2025 release) that precise duration control "is not yet enabled in this release". — [GitHub README](https://github.com/index-tts/index-tts)

### Inferences
- Source discrepancy: the technical report (Jan 2026) lists 4 languages; README and HF card (Aug 2026 weights) list 5 including Arabic. Arabic was evidently added between report and open release; no document explains how much Arabic data was used.
- The Aug 2026 date for the open 2.5 weights is corroborated by independent artefacts dated right after it (issue #760 "Index TTS 2.5 LoRa Finetuning?" opened 2026-08-12; community repo hxyinan/index-tts25-lora-finetune pushed 2026-08-11), so the gap vs the Jan 2026 arXiv ID is a paper-then-weights sequence, not a typo.
- Spanish was added officially with only 2.9K hours, which suggests the Index team's own bar for a new Latin-script language is in the low thousands of hours when trained jointly with large zh/en/ja data.

### Gaps
- ModelScope card for IndexTTS-2.5 was not opened (HF and GitHub were used as primary); not verified whether it differs.
- No official statement of any kind about Thai (for or against) was found.

## 2. GitHub issues / discussions about Thai or new-language support; maintainer answers; official training code

### Takeaway
No issue in index-tts/index-tts specifically requests Thai, and in the new-language threads inspected no Index-team maintainer reply was found. Official training / fine-tuning code has not been released (README and HF cards cover inference only); all training tooling is community-made.

### Cited Findings
- GitHub REST search (14 Nov 2026) in index-tts/index-tts: "thai" -> 1 hit (#418, a general other-languages thread); "ไทย" -> 0 hits; "泰语" -> 1 unrelated hit (#361 pinyin tokenizer error). — [Issue #418](https://github.com/index-tts/index-tts/issues/418)
- #418 "IndexTTS2 is SOTA do you plan other languages? Only English and Chinese?" (opened 2025-09-21, open, 20 comments): users request Czech, Turkish, Vietnamese, Latin American Spanish, Danish, Hindi, Russian, Italian, French; no maintainer answer visible; community Vietnamese model `dinhthuan/index-tts-2-vietnamese` is shared there. — [Issue #418](https://github.com/index-tts/index-tts/issues/418)
- Open, unanswered-by-maintainer new-language / training-code issues include #60 "A new language" (2025-04-08), #141 "Release of training code" (2025-05-07), #185 and #177 "跪求开源微调代码" (May 2025), #215 "Are you planning on releasing fine-tuning scripts..." (2025-06-17), #400 "train new languages" (2025-09-18), #448 "Add Support for Finetuning IndexTTS2 on Other Languages" (2025-09-29), #687 Russian tokenizer adaptation (2026-05-06). In #60 the only replies are community members; one warns that if the tokenizer lacks your alphabet "you're basically doomed". — [Issue #60](https://github.com/index-tts/index-tts/issues/60)
- #105 "License and acceptance for finetuning with different language?" (2025-04-19): a user who extended the vocabulary with ~30k Vietnamese tokens asked whether he may release a fine-tune; no maintainer reply. — [Issue #105](https://github.com/index-tts/index-tts/issues/105)
- In #394 a community contributor (Arcitec, not labelled as maintainer) states that training a new language is closed-source and would need "A dataset of around 30 000 hours of speech per new language, tagged with correct emotions", and invites dataset owners to contact the IndexTTS team. — [Issue #394](https://github.com/index-tts/index-tts/issues/394)
- README (14 Nov 2026) documents inference, WebUI and model download only; training/fine-tuning code is not mentioned. — [GitHub README](https://github.com/index-tts/index-tts)

### Inferences
- The 30,000 h/language figure is a second-hand community statement, and it conflicts with the technical report's own Spanish figure (2.9K h) and with working community fine-tunes at 300–1,100 h; treat it as unreliable for feasibility planning.
- Absence of maintainer replies across more than a year of new-language requests implies no public commitment to Thai.

### Gaps
- Issue comment dates were mostly not exposed by the fetch; only issue-open dates are reliable.
- Issues #400, #448, #760 were found by search but not opened; a maintainer reply could exist there (#760 "Index TTS 2.5 LoRa Finetuning?" was closed 2026-08-12 with 2 comments — content unverified).
- GitHub Discussions tab and PR list were not searched separately.

## 3. Community Thai fine-tunes and forks

### Takeaway
COMMUNITY: three Thai IndexTTS-2 weight releases exist on Hugging Face (dubbing-ai LoRA, Apr 2026; williampike v1, Jan 2026; williampike thai_indextts2, Jun 2026) plus one undocumented Replicate endpoint (Feb 2026). All are small-audience, none publishes WER/CER/MOS, none is based on IndexTTS-2.5, and the best-documented one is explicitly non-commercial.

### Cited Findings

**A. dubbing-ai/indextts2-thai (GitHub) + dubbing-ai/indextts2-thai-lora (HF)**
- Described as "FastAPI server for zero-shot voice cloning TTS powered by IndexTTS2, with Thai language support via LoRA fine-tuning"; repo last pushed 2026-04-12, 0 stars, 0 forks, 11 commits, not a fork. — [GitHub dubbing-ai/indextts2-thai](https://github.com/dubbing-ai/indextts2-thai)
- Base: IndexTeam/IndexTTS-2 (GPT 871M params, 24 layers). Method: LoRA rank 32 on GPT attention + FFN, plus full fine-tune of text_embedding and text_head; 15.7M trainable params (1.76%). — [GitHub dubbing-ai/indextts2-thai](https://github.com/dubbing-ai/indextts2-thai)
- Tokenizer: "BPE tokenizer retrained from 12k -> 32k vocab, seeded with PyThaiNLP's 62k Thai word dictionary"; shipped as `bpe_thai.model` (Thai, Chinese, English). — [HF dubbing-ai/indextts2-thai-lora](https://huggingface.co/dubbing-ai/indextts2-thai-lora)
- Data: "vaja-thai", "a unified, quality-filtered Thai speech dataset (289k samples, 554h, 24kHz)"; trained on a 200k-sample subset (239k train / 12k val after oversampling), 4,669 speakers; sources porjai_central ~178k, CommonVoice ~105k, GigaSpeech2 ~6k, TSync2 ~2k. Hours of the trained subset not stated. — [GitHub dubbing-ai/indextts2-thai](https://github.com/dubbing-ai/indextts2-thai)
- Hardware/time: single RTX 3090 (24 GB VRAM, 32 GB RAM), "~22h per epoch, ~9 days for 10 epochs"; final validation loss 3.6813 at step 299,380. — [GitHub dubbing-ai/indextts2-thai](https://github.com/dubbing-ai/indextts2-thai)
- Speed table (FP16, seed 42): Thai with LoRA RTF 1.97 vs English 1.17 and Chinese 1.15 without LoRA (hardware for the table not defined). English/Chinese are served by the base model with LoRA disabled. — [GitHub dubbing-ai/indextts2-thai](https://github.com/dubbing-ai/indextts2-thai)
- Licence: tag "mixed-non-commercial"; card says "**Non-commercial use only.** This model is subject to multiple licenses"; TSync2 is CC-BY-NC-SA-3.0 and GigaSpeech2 is research-only; "The combined effect is: non-commercial use only, attribution required, share-alike for derivatives." Access is gated. — [HF dubbing-ai/indextts2-thai-lora](https://huggingface.co/dubbing-ai/indextts2-thai-lora)
- Popularity: 32 downloads last month, 4 likes (read 14 Nov 2026); HF listing shows last update "Apr 11". — [HF dubbing-ai/indextts2-thai-lora](https://huggingface.co/dubbing-ai/indextts2-thai-lora); [HF search](https://huggingface.co/models?search=indextts%20thai)
- Quality evidence: no WER/CER/MOS; no limitations section. Demo page defines 24 speakers (12 Thai-only, 12 bilingual with cross-lingual English) but the fetched page exposed no audio rows, metrics or emotion examples. — [Demo page](https://dubbing-ai.github.io/indextts2-thai/)
- Emotion controls: API accepts `emotion_audio` and `emotion_alpha` (0.0–1.0); emotion conditioning is listed as frozen and "Language-agnostic (prosody)"; no evaluation of emotion in Thai is reported; duration control is not mentioned. — [GitHub dubbing-ai/indextts2-thai](https://github.com/dubbing-ai/indextts2-thai)
- Training scripts are included in the repo (`prepare_vaja_thai.py`, `retrain_bpe.py`, `dataset.py`, `train_lora.py`, `publish_to_hf.py`). — [GitHub dubbing-ai/indextts2-thai](https://github.com/dubbing-ai/indextts2-thai)

**B. williampike/indextts2-thai_finetune_v1 (HF, listing date "Jan 16")**
- Thai-language card; fine-tuned from IndexTeam/IndexTTS-2 on the Porjai dataset trimmed from 700 h to 500 h, 1–15 s segments, >500,000 jsonl lines after GPT pairing; method follows Jarod Mica's training fork with added Pyannote speaker separation. — [HF williampike/indextts2-thai_finetune_v1](https://huggingface.co/williampike/indextts2-thai_finetune_v1)
- Licence header "unknown"; author writes (Thai) that it follows the main repo and, as far as he read, is usable unless you are a billion-scale company. — [HF williampike/indextts2-thai_finetune_v1](https://huggingface.co/williampike/indextts2-thai_finetune_v1)
- Author-reported limitations: text repetition (sometimes 10–30 repeats or speaker changes); spaces and non-Thai characters cause repetition/confusion (recommends stripping spaces, punctuation, digits, non-Thai text); degradation on long outputs (keep chunks under ~40 tokens); slower than F5-TTS Thai, much faster than VibeVoice 7B. — [HF williampike/indextts2-thai_finetune_v1](https://huggingface.co/williampike/indextts2-thai_finetune_v1)
- Emotion: author says emotion-vector modes work and expression is much better than F5-TTS Thai, but the training data is flat-read so emotional output can sound odd; demo is cherry-picked. No metrics. 4 likes; downloads not tracked. — [HF williampike/indextts2-thai_finetune_v1](https://huggingface.co/williampike/indextts2-thai_finetune_v1)

**C. williampike/thai_indextts2 (HF, listing date "Jun 11")**
- Second-generation Thai fine-tune of original bilibili IndexTTS2; about 800 hours of training data "including pairing"; data sources unnamed (author says an AI assistant sourced it and it was later deleted); checkpoint `thaiseperate2.pth` with a Thai BPE tokenizer, run through a modified `webui_parallel_thai.py`. — [HF williampike/thai_indextts2](https://huggingface.co/williampike/thai_indextts2)
- No licence metadata (empty YAML). No numeric metrics (TensorBoard tab only). 1 like; downloads not tracked. — [HF williampike/thai_indextts2](https://huggingface.co/williampike/thai_indextts2)
- Author-reported limitations: high error rates on long streams; duration control imprecise; slow; Thai mixed with English terms is a weak point; a "Thai 5-Emo Vectors" mode exists but is described as "not very good" with a high error rate. — [HF williampike/thai_indextts2](https://huggingface.co/williampike/thai_indextts2)

**D. aodianyun/indextts2-thai (Replicate)**
- Public hosted endpoint, 5 runs, latest version 2026-02-10, no description, no licence, no weights link, no training details; inputs: Thai text ("mainly Thai, a little English allowed"), Thai speaker reference audio, `use_emo_text`, `emo_text`, `emo_alpha` (default 0.8), `max_mel_tokens`, `interval_silence`; no emotion-vector, emotion-audio or duration inputs exposed. — [Replicate aodianyun/indextts2-thai](https://replicate.com/aodianyun/indextts2-thai/api)

**Search coverage**
- Hugging Face search "indextts thai" (14 Nov 2026) returns exactly three models: the two williampike repos and dubbing-ai/indextts2-thai-lora. — [HF search](https://huggingface.co/models?search=indextts%20thai)
- Fine-tunes registered under IndexTeam/IndexTTS-2.5 on HF: MLX conversions (vanch007, mlx-community), Turkish LoRA (berrkkaayy), German (sharrnah) — no Thai. — [HF finetune tree of IndexTTS-2.5](https://huggingface.co/models?other=base_model:finetune:IndexTeam/IndexTTS-2.5)

### Inferences
- "Jan 16", "Apr 11", "Jun 11" listing dates carry no year on the page; they must be 2026 because the IndexTTS-2 base was only released 8 Sep 2025.
- All Thai work targets IndexTTS-2 (50 Hz codec, U-DiT S2M). Because 2.5 changed the semantic codec to 25 Hz and the S2M backbone, IndexTTS-2 Thai LoRAs/checkpoints and their tokenizers should not be assumed loadable into 2.5; a Thai 2.5 model would need retraining.
- Emotion-reference audio and emotion vectors remain mechanically available in Thai fine-tunes because the emotion path is frozen, but the only first-hand reports (williampike) describe emotional Thai output as unreliable; emotion-from-text depends on the Qwen emotion model, which is not Thai-specific. Duration control in Thai is either absent (dubbing-ai, Replicate) or reported imprecise (williampike).
- Evidence of quality is entirely anecdotal; popularity signals (32 downloads/month, 1–4 likes, 0 GitHub stars, 5 Replicate runs) indicate very little independent validation.

### Gaps
- No objective Thai metrics (WER/CER/SIM/MOS) for any Thai IndexTTS model were found.
- ModelScope, bilibili, Zhihu, CSDN and Thai-language blogs/YouTube/Facebook were not individually searched; a Thai web search for "IndexTTS ภาษาไทย" returned no Thai-specific community posts. — [search evidence: only generic pages such as HF IndexTeam/Index-TTS](https://huggingface.co/IndexTeam/Index-TTS)
- dubbing-ai's LICENSE.md and demo audio could not be inspected; actual listening quality unverified.
- Relationship between aodianyun's Replicate model and any published weights is unknown.
- tts.ai shows an IndexTTS2 page with a `?lang=th` URL (surfaced in search, not opened) — unverified whether this is real Thai synthesis or only a Thai UI locale. — [tts.ai](https://tts.ai/voices/indextts2/?lang=th)

## 4. Community fine-tunes for other languages and community training repos (feasibility evidence)

### Takeaway
Community training code for IndexTTS-2 and LoRA tooling for 2.5 exist and have produced Japanese, Vietnamese, German, Turkish, Malay and multilingual models from roughly 300–1,100 hours on a single high-end GPU, by extending/retraining the BPE tokenizer and training only the GPT (T2S) stage. Results are intelligible but imperfect, and reports on emotion retention are mixed.

### Cited Findings
- Issue #501 (opened 2025-10-20, 50 comments): JarodMica published unofficial IndexTTS-2 GPT trainer in branch `training_v2` of his fork; workflow = train BPE tokenizer -> preprocess dataset -> train; only the GPT component is trained (timbre/pitch handled by s2mel). — [Issue #501](https://github.com/index-tts/index-tts/issues/501); [JarodMica fork](https://github.com/JarodMica/index-tts/tree/training_v2)
- Japanese (JarodMica): ~500 h Emilia-Yodas for ~3 epochs first, later ~1,100 h for ~5.5 epochs total, about a week on an RTX 6000 Pro at batch 16–32; tokenizer built by training a Japanese tokenizer and appending unique tokens up to 24k; released as Jmica/IndexTTS-2-Japanese. Early runs showed reference-audio "bleed", attributed to using the same clip as prompt and target, later addressed by pairing same-speaker different-utterance samples. — [Issue #501](https://github.com/index-tts/index-tts/issues/501)
- Multilingual run (JarodMica): tokenizer extended to 50k; ~1k h each of German, French, English, Korean, Japanese plus 300 h Chinese; after ~30k steps it could form sentences in each language, English and Chinese best. — [Issue #501](https://github.com/index-tts/index-tts/issues/501)
- Malay: one user reports success reusing the original tokenizer (Latin script); another reports poor results after 96,000 steps on 1.2M samples with a byte-fallback BPE tokenizer. — [Issue #501](https://github.com/index-tts/index-tts/issues/501)
- Emotion after fine-tuning (issue #501): JarodMica says training from the stage-1 base "seems to retain" emotional ability; another user reports emotion lost when speaker and emotion both come from one reference clip but kept with a separate emotion reference. — [Issue #501](https://github.com/index-tts/index-tts/issues/501)
- Advice in the thread: check that the dataset does not tokenize to `unk`; mix in English to preserve English; overfit ~1k samples first as a sanity check. Thai is not mentioned in the thread; no upstream maintainer responds. — [Issue #501](https://github.com/index-tts/index-tts/issues/501)
- Vietnamese: iamdinhthuan/index-tts-finetune-vietnamese (46 stars, pushed 2025-11-19) adapts IndexTTS2; BPE tokenizer trained with vocab 12,000 and byte fallback; example config 10 epochs, batch 16, lr 1e-5, AMP; weights dinhthuan/index-tts-2-vietnamese; no data hours or metrics; licence deferred to upstream, commercial questions to indexspeech@bilibili.com. — [GitHub iamdinhthuan](https://github.com/iamdinhthuan/index-tts-finetune-vietnamese)
- German on IndexTTS-2.5: sharrnah/IndexTTS-2.5-German, ~310 h (MLS German 150 h, HUI clean 140 h, Emilia-YODAS German 20 h; 105,616 utterances); LoRA rank 64 / alpha 128 on all 24 GPT layers with text embeddings and output heads trained; adds a German language-conditioning row plus a German text frontend; step-16,000 checkpoint 5.35% WER on 30 sentences x 2 held-out voices (Whisper Small), 15.62% WER on numeric/date forms; "substantially more intelligible in German, but pronunciation is not perfect"; emotion path "preserved/frozen", no emotion evaluation; distributed under the bilibili licence as a Derivative Work. — [HF sharrnah/index-tts-2.5-german](https://huggingface.co/sharrnah/index-tts-2.5-german)
- Turkish LoRA for 2.5 exists (berrkkaayy/IndexTTS-2.5-Turkish-LoRA). — [HF finetune tree](https://huggingface.co/models?other=base_model:finetune:IndexTeam/IndexTTS-2.5)
- Other community training repos (GitHub search 14 Nov 2026): yrom/finetune-index-tts (140 stars, IndexTTS 1.x notebooks, pushed 2025-06-17); CreateIntelligens/Indextts2-training (10 stars, 2025-12-01); hxyinan/index-tts25-lora-finetune (6 stars, 2026-08-11, voice LoRA for 2.5); wangzeyin2/indextts2-finetune-karenina (2.5 voice fine-tune pipeline, 2026-09-26). — [yrom/finetune-index-tts](https://github.com/yrom/finetune-index-tts); [hxyinan/index-tts25-lora-finetune](https://github.com/hxyinan/index-tts25-lora-finetune)

### Inferences
- A Thai fine-tune on IndexTTS-2.5 looks feasible with public tooling: the German 2.5 recipe (LoRA + trained text embeddings/heads, ~310 h) and the dubbing-ai Thai recipe (retrained 32k BPE seeded with PyThaiNLP, 554 h corpus, single RTX 3090 for ~9 days) together cover the two unknowns (2.5 codebase, Thai script). No one has published this combination yet.
- Thai specifics not solved by any of these recipes: no spaces between words (tokenizer/segmentation), digit and abbreviation normalisation (German fine-tune shows numerals stay the weakest category even in an easier language), and Thai-English code-switching (flagged as weak by williampike).

### Gaps
- Korean, Indonesian and Spanish community fine-tunes were not specifically located (Spanish is official in 2.5; Korean only appears inside JarodMica's multilingual run).
- No fine-tune reports objective emotion-control metrics in the new language.

## 5. What happens if Thai text is fed to the stock model?

### Takeaway
No first-hand report of Thai text in stock IndexTTS-2/2.5 was found; the closest evidence is that unsupported languages are read with wrong (English- or Chinese-like) phonetics, and that every Thai fine-tune had to retrain/extend the BPE tokenizer, implying the stock 12k vocabulary does not cover Thai script usefully.

### Cited Findings
- Issue #394 (opened 2025-09-18): Polish text in stock IndexTTS-2 comes out with heavy English-like phonetics and Russian with Chinese-influenced phonetics; reproduced locally by another user; a community reply states output text must be English or Chinese while reference voices can be any language. — [Issue #394](https://github.com/index-tts/index-tts/issues/394)
- Community warning in #60: if the tokenizer lacks your language's alphabet "you're basically doomed". — [Issue #60](https://github.com/index-tts/index-tts/issues/60)
- Stock IndexTTS-2 BPE vocabulary is 12k; the Thai LoRA project retrained it to 32k with a Thai dictionary, and JarodMica advises checking datasets for `unk` tokens. — [GitHub dubbing-ai/indextts2-thai](https://github.com/dubbing-ai/indextts2-thai); [Issue #501](https://github.com/index-tts/index-tts/issues/501)

### Inferences
- Thai characters most likely map to unknown tokens in the stock tokenizer and are skipped or garbled; this is an inference from tokenizer size and the fine-tuners' practice, not an observed test.
- A Thai *reference voice* can be used with the stock model for cross-lingual cloning into supported languages (2.5 advertises cross-lingual voice transfer), but that yields English/Chinese/Japanese/Spanish/Arabic speech, not Thai.

### Gaps
- Not tested directly (no GPU run); no documented user test with Thai script on stock 2 or 2.5 found. Whether 2.5's tokenizer contains any Thai codepoints is unverified.

## 6. Licence: bilibili Model Use License Agreement and commercial use of a Thai fine-tune

### Takeaway
The bilibili licence itself permits royalty-free use including commercial use below very high thresholds (>100M MAU or >RMB 1bn annual revenue) and allows distributing fine-tunes/LoRAs with pass-through terms, notices and a non-endorsement disclaimer; but the best-documented existing Thai fine-tune is non-commercial because of its training-data licences, so commercial Thai use realistically requires a fresh fine-tune on commercially-licensed Thai data.

### Cited Findings
- README: "This project is released under the bilibili Model Use License Agreement"; "For commercial usage and cooperation, please contact indexspeech@bilibili.com." — [GitHub README](https://github.com/index-tts/index-tts)
- Licence s.2.1 grants "a worldwide, non-exclusive, non-transferable, royalty-free limited license to Use the Model". — [LICENSE](https://raw.githubusercontent.com/index-tts/index-tts/main/LICENSE)
- s.2.2: products/services with more than 100 million monthly active users, or annual revenue above RMB 1 billion in the prior calendar year, "must request a separated license from us"; until granted in writing no rights under the agreement may be exercised. — [LICENSE](https://raw.githubusercontent.com/index-tts/index-tts/main/LICENSE)
- s.1.5: Derivative Works include any model "created by re-training, fine-tuning, quantizing, LoRA". s.3.4(a): must impose appropriate contractual terms on downstream recipients; s.3.4(b): retain copyright notices and a copy of the agreement; s.4.1(a): distributed derivatives must carry a disclaimer that modifications are not endorsed by the right-holder; s.5.2: no trademark rights. — [LICENSE](https://raw.githubusercontent.com/index-tts/index-tts/main/LICENSE)
- s.3.4(c): prohibits using the Model or derivatives to improve any AI model other than the Model itself, its derivatives, or non-commercial AI models. s.4.2 restricts high-risk deployment (medical diagnosis, autonomous driving, military, automated credit/employment decisions). Governing law PRC; arbitration at Shanghai Arbitration Commission. — [LICENSE](https://raw.githubusercontent.com/index-tts/index-tts/main/LICENSE)
- The licence text names the "bilibili indextts2" model (s.1.4); the IndexTTS-2.5 HF card carries the tag "bilibili-model-license". — [LICENSE](https://raw.githubusercontent.com/index-tts/index-tts/main/LICENSE); [HF IndexTeam/IndexTTS-2.5](https://huggingface.co/IndexTeam/IndexTTS-2.5)
- Conflicting community reading: the dubbing-ai Thai LoRA card summarises the base licence as "Derivatives limited to improving IndexTTS or non-commercial AI" and labels the whole release non-commercial (also because TSync2 is CC-BY-NC-SA-3.0 and GigaSpeech2 research-only). — [HF dubbing-ai/indextts2-thai-lora](https://huggingface.co/dubbing-ai/indextts2-thai-lora)
- williampike reads the licence as usable unless you are a billion-scale company; his repos carry no formal licence metadata and the 800 h dataset's provenance is undisclosed. — [HF williampike/indextts2-thai_finetune_v1](https://huggingface.co/williampike/indextts2-thai_finetune_v1); [HF williampike/thai_indextts2](https://huggingface.co/williampike/thai_indextts2)
- Maintainers did not answer a direct question on releasing a new-language fine-tune (#105, April 2025). — [Issue #105](https://github.com/index-tts/index-tts/issues/105)

### Inferences
- dubbing-ai's summary of the base licence appears stricter than the licence text: s.3.4(c) restricts using the model to *improve other AI models* (e.g. distillation / synthetic training data for a different commercial model), not commercial use of a fine-tune of IndexTTS itself. The non-commercial status of that Thai LoRA is nonetheless real, because the NC data licences independently bind it.
- For a company well under 100M MAU and RMB 1bn revenue, a self-trained Thai fine-tune on commercially usable data (e.g. CommonVoice CC-0, Porjai CC-BY-SA-4.0 as characterised on the dubbing-ai card) appears permissible under the licence text without contacting bilibili, subject to pass-through terms; CC-BY-SA share-alike implications for model weights and PRC-law arbitration are open legal points. This is a reading of the text, not legal advice; written confirmation from indexspeech@bilibili.com would remove ambiguity.
- Synthetic Thai speech from an IndexTTS model should not be used to train a different commercial TTS/ASR model (s.3.4(c)).

### Gaps
- The licence text has no version/date; not verified whether the 2.5 repo on HF ships an identical licence file (only the tag was seen).
- Licence of IndexTTS-1.0/1.5 weights was not re-verified (issue #105 from April 2025 refers to Apache 2.0 for the original model and code — second-hand).
- DISCLAIMER file content not read.

## 7. Apple Silicon (MPS / MLX)

### Takeaway
Officially IndexTTS targets NVIDIA CUDA and the 2.5 card says an NVIDIA GPU is required; upstream MPS use has open bug reports. Community MLX ports exist for IndexTTS-2 and 2.5 (including an mlx-community conversion) and run on 16 GB Macs, but none documents loading Thai LoRAs/custom BPE models, and only Mandarin and English are validated.

### Cited Findings
- README documents NVIDIA CUDA install (CUDA Toolkit 12.8+), BF16 for 2.5 / FP16 for 2; MPS / Apple Silicon not mentioned. HF 2.5 card: requires "an NVIDIA GPU", ~6 GB VRAM. — [GitHub README](https://github.com/index-tts/index-tts); [HF IndexTeam/IndexTTS-2.5](https://huggingface.co/IndexTeam/IndexTTS-2.5)
- Open upstream Mac issues: #193 "Fail on MacOS M3, 65536 not supported at the MPS device" (2025-06-01); #271 request to add MPS support (2025-09-03); #360 M4 Max 128 GB MPS long-text memory overflow, CPU inference very slow (2025-09-14); #414 M3 Ultra 256 GB "serious memory leak" (2025-09-20). — [Issue #193](https://github.com/index-tts/index-tts/issues/193); [Issue #360](https://github.com/index-tts/index-tts/issues/360); [Issue #414](https://github.com/index-tts/index-tts/issues/414)
- Community MLX ports (GitHub search 14 Nov 2026): solar2ain/mlx-indextts (v1.5 & v2.0, 20 stars); groxaxo/mlx-indextts2-inference (10); vanch007/mlx-indextts2 (6); samni728/mlx-indextts2.5 (2.5 MLX 8-bit, 4); chenlu-hung/indextts2-mlx (MLX-Swift, torch-free, 2026-10-22); blossomstack/mlx-indextts (native 2.5, 2026-10-31); realAllenSong/ThunderTalk macOS app bundling IndexTTS-2.5 (pushed 2026-11-13). — [solar2ain/mlx-indextts](https://github.com/solar2ain/mlx-indextts); [blossomstack/mlx-indextts](https://github.com/blossomstack/mlx-indextts)
- MLX weight conversions of 2.5 on HF: vanch007/mlx-indextts2-2.5-fp16 / -8bit / -fp32 and mlx-community/IndexTTS-2.5-fp16. — [HF finetune tree](https://huggingface.co/models?other=base_model:finetune:IndexTeam/IndexTTS-2.5)
- blossomstack/mlx-indextts benchmark on M2 Pro 16 GB (MLX 0.31.1): 30.2 s Mandarin audio generated in 16.07 s with Metal vocoder (26.40 s reference backend), peak MLX memory 4.67 GB; 24.4 s English in 12.95 s, peak 5.60 GB; only Mandarin and English validated end-to-end; emotion via `emotion` + `emo_alpha`; no duration control documented; port MIT-licensed, model weights remain under bilibili terms; LoRA / custom BPE / fine-tuned checkpoint loading not mentioned. — [blossomstack/mlx-indextts](https://github.com/blossomstack/mlx-indextts)

### Inferences
- Stock IndexTTS-2.5 runs faster than real time on Apple Silicon through MLX ports (roughly 0.53 RTF on an M2 Pro, calculated from the figures above), so Mac inference is practical for supported languages.
- Running Thai on a Mac would require either the PyTorch path (upstream code + Thai LoRA on MPS/CPU, with the known MPS memory problems) or converting a Thai checkpoint and tokenizer to MLX oneself; no turnkey Thai-on-MLX path was found.

### Gaps
- Whether the MPS issues persist in the 2.5 codebase is unverified (reports date from 2025, IndexTTS-1.5/2 era).
- No report found of anyone running a Thai IndexTTS fine-tune on Apple Silicon.
