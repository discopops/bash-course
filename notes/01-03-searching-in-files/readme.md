## 📹 Video

[Watch this chapter](../../videos/Chapter_05_01-03 Searching in Files/01-03 Searching in Files.mp4)

---

# Searching in Files

- show `/usr/share/dict/words`
- grep it for dave
- let's make our own files
- `touch file.txt`
- `echo hello`
- `echo hello > file.txt`
- `echo a >> file.txt`, b, c
- `grep b file.txt`
- `grep -A1 b file.txt`, -B, -C
- open it with a text editor and add random words
- `grep -i ...`
- `grep -o ...`, `grep -v ...`
- `cat file.txt | grep -v ... | grep -o ...` #  subtle intro of pipelines
