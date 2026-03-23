## 📹 Video

[Watch this chapter](../../videos/Chapter_39_09-00 Basic Globbing/09-00 Basic Globbing.mp4)

---

# Basic Globbing

```
ls files/
bar.jpg  bar.txt  baz.jpg  baz.txt  foo.jpg  foo.txt

echo files/*
printf '%s\n' files/*

ls -1 files/*

ls -1 files/*.txt
ls -1 files/*.jpg

ls -1 files/foo.*
ls -1 files/bar.*

ls -1 files/ba?.txt

ls -1 files/ba[rz].txt
```
