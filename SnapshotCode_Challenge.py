"""
A regular map has the following interface methods:
get(k) -> v or KeyError
put(k, v)
delete(k)

We wish to augment this with two more methods:
take_snapshot() -> snap_id
get(k, snap_id) -> v or KeyError

take_snapshot captures the logical state of the map as of that point which can later be accessed via snap_id

get(.., snap_id) allows us to refer to the value of a key as of a historical snap_id.

Implement this data structure with following hard constraints:
values that have not changed across snapshots should not be duplicated 
All operations should be sub-linear in the size of the map (number of keys)

As a reference point for performance, imagine the map will have ~1 million keys, with ~100 snapshots, and 1% of the keys change in every snapshot.

Implement the methods besides delete first for simplicity, then return to implement delete if there’s time.
"""

import copy

class SnapshotMap:
	def __init__(self, history, data):
		self.history = history
		self.data = data

	def get(self, key):
		return self.data[key]

	def put(self, key, value):
		self.data[key] = value

	def remove(self, key):
		del self.data[key]

	def get_snapshot_value(self, key, snapshot_id):
		this_snapshot = {} # We begin adding data!
		data_stored_for_snapshot = self.history[snapshot_id]
		keys_to_ignore = [] # We already have found a later version, or found it was deleted later!
		Search_SID = snapshot_id
		while Search_SID > 0:
			for key in data_stored_for_snapshot.keys():
				if key in keys_to_ignore:
					continue
				if data_stored_for_snapshot[key] != None:
					this_snapshot[key] = data_stored_for_snapshot[key]
				keys_to_ignore.append(key)
			Search_SID -= 1
			data_stored_for_snapshot = self.history[Search_SID]
		return this_snapshot[key]

	def get_all_data_from_snapshot(self, snapshot_id):
		this_snapshot = {} # We begin adding data!
		data_stored_for_snapshot = self.history[snapshot_id]
		keys_to_ignore = [] # We already have found a later version, or found it was deleted later!
		Search_SID = snapshot_id
		while Search_SID > 0:
			data_stored_for_snapshot = self.history[Search_SID]
			for key in data_stored_for_snapshot.keys():
				if key in keys_to_ignore:
					continue
				if data_stored_for_snapshot[key] != None:
					this_snapshot[key] = data_stored_for_snapshot[key]
				keys_to_ignore.append(key)
			Search_SID -= 1
		return this_snapshot	

	def take_snapshot(self):
		snapshot_id = 1
		while snapshot_id in self.history:
			snapshot_id += 1
		if snapshot_id == 1:
			self.history[1] = copy.deepcopy(self.data)
			return # Done! We just copy all for the root instance, 1st snapshot.
		snapshot_data = {}
		previous_version = self.get_all_data_from_snapshot(snapshot_id-1)
		for key in self.data.keys():
			if key in previous_version: # Key exists in previous version! Has it been changed?
				if self.data[key] != previous_version[key]:
					snapshot_data[key] = self.data[key] # It changed so we better include that.
				# If not changed, no need to include.
			else: # New key, so we must include it in snapshot
				snapshot_data[key] = self.data[key]
		for key in previous_version.keys(): # We must check if keys were deleted!
			if key not in self.data:
				snapshot_data[key] = None # Mark as deleted!
		self.history[snapshot_id] = snapshot_data

"""
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
"""

# Do not edit any code above this comment.
# Add code to use this fake "API" below this comment.

## Sample code executions
s = SnapshotMap({}, {})
s.put("a", 'a1')
s.put("b", "b1")
s.put("c", "c1")

s.take_snapshot()
print(s.data)

s.put("b", "b2")
s.take_snapshot()
print(s.data)

#print last snapshop
print(s.history)

print(s.get_all_data_from_snapshot(2))

##Delete
s.remove("c")
s.take_snapshot()
print(s.data)
print(s.history[3])