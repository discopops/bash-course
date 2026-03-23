## 📹 Video

[Watch this chapter](../../videos/Chapter_60_16-01 Aliases with Arguments/16-01 Aliases with Arguments.mp4)

---

# Aliases with Arguments

```
# mkdir and cd
alias mkdc='mkdir $1 && cd $1'

alias foo='echo $1 $2'

foo
foo hello world

set -- a b c
foo hello world

mkdc() {
    mkdir $1 && cd $1
}

then clean it up
```
