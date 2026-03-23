## 📹 Video

[Watch this chapter](../../videos/Chapter_30_06-00 Bash Arguments/06-00 Bash Arguments.mp4)

---

# Bash Arguments

./00-simple-script

bash ./00-simple-script
bash -x ./00-simple-script

... edit script, add set -x ...

set +x add as well

PS4='>>>>' bash -x 00-simple-script

---

./01-syntax-error
bash -n ./01-syntax-error

explain why no output

bash -n 00-simple-script

---

./02-undef

bash -u ...

---

show shellcheck
