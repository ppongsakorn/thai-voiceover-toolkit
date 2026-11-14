# ประกอบเสียงกับวิดีโอ

skill นี้ทำงานถึงขั้นได้ไฟล์เสียง ส่วนการใส่เสียงลงวิดีโอ ใส่ซับ หรือใส่เพลง ให้ใช้เครื่องมือตัดต่อ เช่น [ffmpeg-skill](https://github.com/kajisho5/ffmpeg-skill) (MIT) ซึ่งตั้งใจไม่ทำ TTS จึงใช้ต่อจาก skill นี้ได้พอดี

## วางเสียงตาม scene

วิธีนี้ใช้ทำคลิปแนะนำผลิตภัณฑ์ยาว 45 วินาทีที่มี 6 scene

1. สร้างเสียงหนึ่งบรรทัดต่อหนึ่ง scene แล้วใช้ `finish.py --out final` เพื่อให้ได้ไฟล์ที่ตัดเสียงเงียบแล้วต่อ scene
2. วางแต่ละประโยคที่ต้น scene บวก 0.25 วินาที (ประโยคแรกที่ 0.6 วินาที) และตั้งความยาว scene ให้เสียงจบก่อนเปลี่ยน scene อย่างน้อย 0.2 วินาที
3. ใช้ `check_takes.py --words final/s*.flac` เพื่อหาเวลาของคำ แล้วตั้งให้ภาพขึ้นก่อนคำราว 0.08 วินาที คำภาษาไทยจะออกมาเป็นชิ้นย่อยระดับตัวอักษร ส่วนคำอังกฤษออกมาเป็นคำเต็ม จึงยึดภาพกับชื่ออังกฤษได้ง่ายกว่า
4. รวมเสียงเป็นไฟล์เดียว ปรับความดังเป็น -16 LUFS แล้วรวมกับวิดีโอด้วย `ffmpeg -i video.mp4 -i voice.m4a -map 0:v -map 1:a -c copy -shortest out.mp4`

## งานที่ ffmpeg-skill ทำได้ต่อ

ยังไม่ได้ติดตั้งหรือทดสอบ ข้อมูลมาจากเอกสารของ ffmpeg-skill เมื่อ 14 พ.ย. 2026

| งาน | คำสั่ง |
|---|---|
| แทนเสียงในวิดีโอด้วยเสียงพากย์ | `audio.py in.mp4 --replace narration.wav` |
| ใส่เพลงและลดเพลงลงตอนมีเสียงพูด | `audio.py in.mp4 --music bed.mp3 --duck` |
| ทำให้เสียงยาวตรงตามจำนวน sample | `audio.py line.wav --tempo 1.1 --length-samples 96000 -o fit.wav` |
| ใส่ซับไทยลงวิดีโอ | `caption.py in.mp4 --srt subs.srt` จะตัดบรรทัดไทยเฉพาะที่ช่องว่าง และเลือกฟอนต์ที่มีอักษรไทยให้เอง |
| ปรับความดังและตรวจก่อนส่ง | `loudness.py in.mp4` และ `check.py out.mp4 --platform reels` |

ติดตั้งด้วย `npx ffmpeg-skill` ซึ่งรันโค้ดจาก npm จึงควรอ่านโค้ดก่อน การใส่ซับต้องใช้ ffmpeg ที่มี filter `subtitles` และ `drawtext` ซึ่ง ffmpeg ของ Homebrew แบบปกติไม่มี บน macOS ต้องติดตั้ง `brew install ffmpeg-full` แล้วตั้ง PATH ให้ใช้ตัวนั้น (`export PATH="$(brew --prefix ffmpeg-full)/bin:$PATH"`) ส่วน `finish.py` ของ skill นี้ใช้ได้กับ ffmpeg แบบปกติ
