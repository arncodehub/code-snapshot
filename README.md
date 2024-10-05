# code-snapshot
To take version or snapshot of code or list of files -

get(key) >> Takes in a key, return's it value in `data`
put(key, value) >> Takes a key and value, adds it to `data`
remove(key) >> Deletes that key from `data` along with its value
get_snapshot_value(key, snapshot_id) >> Gets the historical value of a key in a stored snapshot NOT necessarily current `data`
take_snapshot() >> Takes an immutable snapshot of the current `data`
get_all_data_from_snapshot(snapshot_id) >> Gets ALL the data from a snapshot, not just changes

IMPORTANT: The first snapshot must be ID 1, next is ID 2, etc.
OR everything will fall apart and break down!!!

Also, there is NO error handling, so do not delete nonexistent keys, 
or add keys will value `None` this will break everything

YOU MUST initialize the class 'SnapshotMap' with {}, {} as arguments FIRST
or else it will not work
