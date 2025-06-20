# Shared storage for registered tags (max 3)
registered_tags = {}  # {tag_id: {"id": tag_id, "description": desc, "last_cnt": cnt, "last_seen": timestamp}}

# Global variables for simulation
global_cnt = 0
cycle_count = 0
last_tag_state = {'tag_id': None, 'cnt': None, 'timestamp': None}