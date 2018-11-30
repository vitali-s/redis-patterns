# Redis patterns

## Reduce memory usage

* Short structures - ziplist, configuration
```
# everything below configured limits will use ziplist structures, otherwise will be converted to non-zip
list-max-ziplist-entries 512
list-max-ziplist-value 64

hash-max-ziplist-entries 512
hash-max-ziplist-value 64

zset-max-ziplist-entries 128
zset-max-ziplist-value 64
```

To analize which encoding is used:
```
object encoding <key>
```

* for SET:
```
set-max-intset-entries 512
```

* Use short names for keys and values (will bring benefits for millions of records):
```
user-id:12345 -> uid:12345
```

* Sharding

