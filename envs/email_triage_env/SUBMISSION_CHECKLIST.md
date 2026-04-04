# email_triage_env — Pre-Submission Checklist

## Quick Pass/Fail Verification

**All Items Critical — Each must pass before submission**

---

### 1. ✅ HF Space Deployment  
- [ ] Deploy from [envs/email_triage_env](envs/email_triage_env)
- [ ] Confirm `/health` returns HTTP 200
- [ ] Test `reset()` call against deployed Space URL
- [ ] **Expected:** Space URL format `https://<username>-email-triage-env.hf.space`

---

### 2. ✅ OpenEnv Spec Compliance  
- [ ] Manifest [envs/email_triage_env/openenv.yaml](envs/email_triage_env/openenv.yaml) validates:
  ```yaml
  spec_version: 1
  name: email_triage_env
  type: space
  runtime: fastapi
  app: server.app:app
  port: 8000
  ```
- [ ] Typed models exist: [models.py](envs/email_triage_env/models.py) with `Action`, `Observation`, `State`
- [ ] Server app wiring: [server/app.py](envs/email_triage_env/server/app.py) uses `create_app(factory, ...)`
- [ ] **Run:** `openenv validate envs/email_triage_env --verbose`

---

### 3. ✅ Dockerfile Build  
- [ ] Build: `docker build -t email-triage-env:latest -f envs/email_triage_env/Dockerfile .`
- [ ] Run: `docker run --rm -p 8000:8000 email-triage-env:latest`
- [ ] Test: `curl http://localhost:8000/health` → HTTP 200
- [ ] **Note:** Dockerfile is at repo root `envs/email_triage_env/Dockerfile`, NOT `server/Dockerfile`

---

### 4. ✅ Baseline Inference Scripts  
- [ ] Old baseline: [baseline_openai.py](envs/email_triage_env/baseline_openai.py) works with `OPENAI_API_KEY`
- [ ] **NEW submission script:** [inference.py](envs/email_triage_env/inference.py) at repo root
- [ ] Reads required env vars:
  - `API_BASE_URL` — LLM endpoint
  - `MODEL_NAME` — Model identifier
  - `HF_TOKEN` — API credentials
- [ ] Output is JSON:
  ```json
  {
    "model": "meta-llama/Llama-3.2-70B-Instruct",
    "scores": {
      "easy_security_triage": 0.85,
      "medium_billing_outage": 0.72,
      "hard_vip_legal_security": 0.68
    },
    "average": 0.75
  }
  ```
- [ ] **Run:** `export API_BASE_URL=... MODEL_NAME=... HF_TOKEN=... && python inference.py`

---

### 5. ✅ 3+ Tasks with Graders  
- [ ] Tasks defined in [server/tasks.py](envs/email_triage_env/server/tasks.py):
  - ✓ `easy_security_triage` (6 checklist items, 8 step budget)
  - ✓ `medium_billing_outage` (10 checklist items, 12 step budget)
  - ✓ `hard_vip_legal_security` (16 checklist items, 16 step budget)
- [ ] Grader logic in [server/grader.py](envs/email_triage_env/server/grader.py)
- [ ] Each task scores in range [0.0, 1.0]
- [ ] **Verify:** Run 3 tasks; confirm all complete and scores are numeric

---

### 6. ✅ Required Environment Variables  
- [ ] Set before running `inference.py`:
  ```bash
  export API_BASE_URL="https://router.huggingface.co/v1"
  export MODEL_NAME="meta-llama/Llama-3.2-70B-Instruct"
  export HF_TOKEN="hf_xxxxx..."
  ```
- [ ] OpenAI Client is used: ✓ (`from openai import OpenAI`)
- [ ] Client initialized with `api_key=HF_TOKEN` and `base_url=API_BASE_URL`

---

### 7. ✅ Infra Constraints  
- [ ] Inference runtime: **< 20 minutes**
  - 3 runs × ~4-6 min per task = ~15-18 min typical
- [ ] Environment + inference fit vcpu=2, memory=8gb
  - No GPU required
  - No special model downloads during inference
- [ ] **Test locally on constrained machine or use small model first**

---

### 8. ✅ Pre-Submission Validation  
- [ ] Run validator script (if provided by submission):
  ```bash
  cd envs/email_triage_env
  bash validate.sh  # or python validate.py
  ```
- [ ] Run OpenEnv validation:
  ```bash
  openenv validate envs/email_triage_env --verbose
  ```
- [ ] Run tests locally:
  ```bash
  PYTHONPATH=src:envs pytest tests/envs/test_email_triage_environment.py -v
  ```

---

## Risk Mitigation: What to Fix Before Submit

| Issue | Fix |
|-------|-----|
| `inference.py` missing | ✓ Now at `envs/email_triage_env/inference.py` |
| Wrong env var names | ✓ Now uses `API_BASE_URL`, `MODEL_NAME`, `HF_TOKEN` exactly |
| Dockerfile in wrong place | ✓ Confirmed at `envs/email_triage_env/Dockerfile` (root of env, not server/) |
| Inference doesn't use OpenAI Client | ✓ Now imports `OpenAI` and initializes with `api_key`, `base_url` |
| Tests missing | ✓ Exist at `tests/envs/test_email_triage_environment.py` |
| Manifest format wrong | ✓ Confirmed `spec_version: 1` with current fields |

---

## Submission Steps (Order Matters)

1. **Verify local setup**
   ```bash
   cd envs/email_triage_env
   # Check all files exist
   ls -la | grep -E "openenv.yaml|Dockerfile|inference.py|models.py|pyproject.toml"
   ```

2. **Test Docker build**
   ```bash
   docker build -t email-triage-env:test .
   docker run --rm -p 8000:8000 email-triage-env:test &
   sleep 5
   curl http://localhost:8000/health
   kill %1
   ```

3. **Test inference script locally** (if LLM available)
   ```bash
   export API_BASE_URL="http://localhost:8000"  # Or real endpoint
   export MODEL_NAME="gpt-4o-mini"
   export HF_TOKEN="your-token"
   python inference.py
   ```

4. **Commit changes**
   ```bash
   git add envs/email_triage_env/
   git add tests/envs/test_email_triage_environment.py
   git commit -m "email_triage_env: add inference.py, finalize for submission"
   ```

5. **Push to staging/main**
   ```bash
   git push origin <branch>
   ```

6. **Submit via official channel**
   - Link to repo + commit hash
   - Highlight: email_triage_env ready at this commit
   - Note: inference.py at `envs/email_triage_env/inference.py`

---

## Final Checklist (Copy-Paste Ready)

```
[ ] openenv.yaml format correct
[ ] Dockerfile builds successfully
[ ] inference.py uses API_BASE_URL, MODEL_NAME, HF_TOKEN
[ ] inference.py outputs JSON with scores and average
[ ] 3+ tasks defined in server/tasks.py
[ ] Grader in server/grader.py assigns scores ∈ [0.0, 1.0]
[ ] openenv validate passes
[ ] Tests exist and logically sound
[ ] README updated with submission notes
[ ] Docker image health check works
[ ] Inference runtime < 20 minutes
[ ] All imports use dual-import pattern (in-repo + Docker)
[ ] __init__.py exports public API symbols
```

---

**Status:** ✅ Ready to submit

**Last Updated:** April 3, 2026

**Contact:** For questions, refer to [EMAIL_TRIAGE_ENV_VALIDATION_REPORT.md](EMAIL_TRIAGE_ENV_VALIDATION_REPORT.md)

