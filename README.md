# 1. Setup environment
- Init environment

```bash
python3 -m venv .venv 
```
```
source .venv/bin/activate
```
- Install libs 
```
pip3 install fastapi uvicorn aiofiles
```
# 2. Example 1
- Run program
```
python3 tag_simulator.py
```
> **_NOTE:_**: Please follow data in log directory include 2 files: **_simulator_tag_data_storage.json_**, **_simulator_tag_data.log_**

# 3. Example 2
- Tags Register
```
curl -X POST "http://localhost:8100/tags" -H "Content-Type: application/json" -d '{"id": "d7affa52-ddf", "description": "MinhPham description JAVA BE"}'
```
- Tags list
```
curl http://localhost:8100/tags
```
- Tag detail by tag id
```
curl http://localhost:8100/tag/28050dd9-b02
```
- Health API
```
curl http://localhost:8100/health
```

# 4. Example 3

```python
tag_log = []
def log(tag_id, cnt, timestamp):
    tag_log.append((tag_id, cnt, timestamp))
```

## Two issues in the code:

* Global tag_log variable: Using a global list is unsafe in multi-threaded/multi-process environments, risking data conflicts.
* Lack of input validation: The log function doesn't validate TAG_ID, CNT, or TIMESTAMP, potentially allowing invalid data.

## Improvements:

* Use TagLogger with Lock: Create a **_TagLogger_** class with a Lock for thread safety and log to a file instead of memory.
* Add input validation: Validate TAG_ID (non-empty string), CNT (non-negative integer), and TIMESTAMP (correct format)