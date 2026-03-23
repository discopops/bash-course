## 📹 Video

[Watch this chapter](../../videos/Chapter_55_14-02 Is a TTY/14-02 Is a TTY.mp4)

---

# Is a TTY

```
ls
ls | wc -l
```

```
#!/usr/bin/env bash
if [[ -t 1 ]]; then
  echo stdout is a terminal
else
  echo stdout is NOT a terminal
fi
```

./check-terminal
./check-terminal | cat
```
