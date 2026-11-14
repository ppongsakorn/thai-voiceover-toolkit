# Skills

skill สำหรับ AI agent หนึ่งโฟลเดอร์ต่อหนึ่ง skill แต่ละโฟลเดอร์มี `SKILL.md` และ `scripts/` ถ้ามีโค้ดประกอบ

## skill ที่มีแล้ว

| skill | ทำอะไร |
|---|---|
| [`voxcpm2-voiceover/`](voxcpm2-voiceover/) | พากย์เสียงด้วย VoxCPM2 ในเครื่อง: ตรวจเครื่องและติดตั้ง (`doctor.py`, `requirements.txt`), เลือกโหมด (Hi-Fi clone, clone + คำสั่งอารมณ์, voice design), สร้างหลาย take, ตรวจด้วย Whisper, ตัดเสียงเงียบ ปรับจังหวะ และต่อไฟล์ |

## ติดตั้ง skill ให้ Claude Code

symlink โฟลเดอร์ skill ไปไว้ที่ `~/.claude/skills/` เพื่อใช้ได้ทุกโปรเจกต์ และเมื่อ `git pull` แล้ว skill จะอัปเดตตามไปด้วย (รันจาก root ของ repo นี้)

```bash
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/voxcpm2-voiceover" ~/.claude/skills/voxcpm2-voiceover
```

ถ้าจะใช้เฉพาะบางโปรเจกต์ ให้ symlink ไปไว้ที่ `.claude/skills/` ของโปรเจกต์นั้นแทน ส่วนการติดตั้งโมเดลและ package ที่ skill ต้องใช้ อยู่ในหัวข้อ "ติดตั้ง" ของ `SKILL.md` แต่ละตัว

skill ที่ใช้คู่กันได้: [ffmpeg-skill](https://github.com/kajisho5/ffmpeg-skill) (MIT) สำหรับใส่เสียงลงวิดีโอ ใส่ซับไทย และใส่เพลง ซึ่งตั้งใจไม่ทำ TTS จึงใช้ต่อจาก `voxcpm2-voiceover` ได้พอดี

แนวทาง: ทำ skill ให้เล็กและทำงานเดียว เพื่อให้หยิบไปใช้แยกกันได้

## skill ที่วางแผนไว้

ตามขั้นตอนพากย์คลิปใน README หลัก:

- เตรียมสคริปต์ไทยก่อนสังเคราะห์เสียง (แปลงตัวเลข คำทับศัพท์ แบ่ง scene)
- สร้างเสียงราย scene และเลือก take
- ตรวจคุณภาพและปรับความยาวให้พอดีกับ scene
