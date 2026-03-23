## 📹 Video

[Watch this chapter](../../videos/Chapter_22_04-03 IFS Variable/04-03 IFS Variable.mp4)

---

# IFS Variable

talk about a small section of IFS today

```
array=(foo bar baz)
echo "${array[*]}"

IFS=,
echo "${array[*]}"
echo ${array[*]}

IFS=_
echo "${array[*]}"

IFS=abcd
echo "${array[*]}"


unset array
declare -A array=([foo]=1 [bar]=2)
echo "${array[*]}"

IFS=,
echo "${array[*]}"
echo "${!array[*]}"
```
