## 📹 Video

[Watch this chapter](../../videos/Chapter_31_06-01 Pipe Status/06-01 Pipe Status.mp4)

---

# Pipe Status
echo hi
echo $?

echo hi | grep hi
echo $?

echo hi | grep bye
echo $?

$? the last command in a pipeline

echo "${PIPESTATUS[*]}"

true|false|true|false|true

(exit 4) | (exit 7) | (exit 100) | (exit 0)
