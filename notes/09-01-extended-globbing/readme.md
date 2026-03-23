## 📹 Video

[Watch this chapter](../../videos/Chapter_40_09-01 Extended Globbing/09-01 Extended Globbing.mp4)

---

# Extended Globbing

```
set -H
shopt -s extglob

ls -1 files/*.txt
ls -1 files/!(*.txt)

ls -1 files/+(foo|bar).txt

+(thing) => /(thing)+/
?(thing) => /(thing)?/
*(thing) => /(thing)*/

---

@(thing)

ls files/+(foo).*
ls files/@(foo).*

touch files/foofoo.txt

ls files/@(foo).*

ls files/foo.*

touch files/barbar.txt
ls files/@(foo|bar).*
ls files/@(foo|ba?).*

```
