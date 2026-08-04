# Plan 001: Improve agent architecture and code quality

Status: **implemented (Mode B)**  
Created from: code review of `main.py` (organization, memory wiring, tools, structure)  
Related code: [`main.py`](../../main.py), [`transcript_io.py`](../../transcript_io.py), [`tools.py`](../../tools.py), [`README.md`](../../README.md)

> Naming: plans in this folder use a numeric prefix (`001-`, `002-`, …) so later plans can be added without collisions.

---

## Goals

1. Align product mode (batch pipeline vs conversational memory) with code and prompts.
2. Make memory work correctly **only if** conversational mode is chosen; otherwise remove dead wiring.
3. Tighten tools, error handling, env validation, and module layout without over-engineering.
4. Keep the drop-and-run transcript discovery flow (`input/transcripts` → pending → `output/`).

---

## Decision first (do before coding)

Choose **one** product mode. Do not keep both half-implemented.

| Mode | Behavior | Memory |
|------|----------|--------|
| **A. Batch pipeline (recommended default for current `main()`)** | Drop transcripts → process pending → save notes → exit | No checkpointer / no follow-up chat |
| **B. Conversational session** | Process transcript, then allow follow-up questions in the same run | `InMemorySaver` + `thread_id` on every `invoke` |

If choosing **B**, also decide: **one thread per transcript date** (preferred) vs one global thread (risks mixing meetings).

Record the choice at the top of this file before implementation begins:

- [ ] Mode A — batch only  
- [x] Mode B — conversational (+ per-transcript thread ids)

**Mode B extra requirement (from implementation request):** draft notes are shown in the terminal first; the output file is written only after the user types `exit`, using the final consolidated notes from the session.

---

## Step-by-step implementation

### Phase 1 — Align prompt, memory, and `main()` flow

**Step 1.1 — Remove or finish memory wiring**

- If Mode A:
  - Remove unused `InMemorySaver`, `checkpointer=memory`, and `THREAD_ID`.
  - Rewrite `SYSTEM_PROMPT` to describe a one-shot meeting-notes pipeline (no “remind me” / multi-message session language).
- If Mode B:
  - Pass `config={"configurable": {"thread_id": ...}}` on every `agent.invoke(...)`.
  - Use a thread id derived from transcript date, e.g. `meeting-{transcript_date}`.
  - After each transcript is processed (or after all pending), add an interactive follow-up loop (`input()` until `exit`/`quit`) that reuses the same thread.
  - Save final notes only after `exit` (not immediately after the first draft).

**Step 1.2 — Update README**

- Document the chosen mode and how to run it.
- Document the chat loop (Mode B) and delayed file save on `exit`.

**Done when:** Prompt, imports, `invoke` call, and README all describe the same behavior; no unused `THREAD_ID`.

---

### Phase 2 — Improve tools so names match behavior

**Step 2.1 — Fix or replace weak tools**

Implemented improved tools in `tools.py`:

- `extract_key_points` — broader discussion/decision keywords  
- `extract_action_items` — broader ownership/timing keywords  
- `preview_transcript` — renamed from fake “summary”; clearly a preview helper  

**Step 2.2 — Tool registration**

- Tool list matches prompt guidance to use tools when helpful.

**Done when:** Tool names, docstrings, and prompt responsibilities are consistent; no misleading “summary” helper.

---

### Phase 3 — Harden runtime in `main()`

**Step 3.1 — Env validation**

- Validate both `GEMINI_MODEL` and `GEMINI_API_KEY` at startup with clear errors.

**Step 3.2 — Per-transcript error handling**

- Wrap each pending file’s process/save in `try/except`.
- On failure: print error, continue to next transcript.
- Print a failure summary at the end.

**Step 3.3 — Lazy agent construction**

- Move model/agent creation into `build_agent()` called from `main()`.

**Done when:** Missing env fails clearly; one bad file doesn’t stop the batch; import side effects are reduced.

---

### Phase 4 — Clarify module layout and naming

**Step 4.1 — Rename or split I/O module**

- Renamed `encoding.py` → `transcript_io.py`.

**Step 4.2 — Optional split of agent code**

- Extracted tools to `tools.py`; agent/orchestration remain in `main.py`.

**Step 4.3 — Clean tutorial leftover comments**

- Removed tutorial-style memory comments.

**Done when:** Filenames match responsibilities; `main.py` is orchestration-focused.

---

### Phase 5 — Polish and verification

**Step 5.1 — Manual verification checklist**

- [ ] Drop a new `transcript_YYYY-MM-DD.txt` → draft notes print; file appears only after `exit`
- [ ] Re-run skips already-processed dates
- [ ] README link added for new output
- [ ] Missing `.env` values produce clear errors
- [ ] Forced failure on one transcript still processes others
- [x] Mode B: follow-up questions use `thread_id` (`meeting-{date}`)

**Step 5.2 — Commit**

- Commit message provided in chat after implementation.
- Do not commit `.env`.

---

## Suggested order of work

1. Phase 1 (mode decision + memory/prompt alignment) — highest impact  
2. Phase 3 (env + per-file errors) — reliability  
3. Phase 2 (tools) — quality of notes  
4. Phase 4 (naming/layout) — maintainability  
5. Phase 5 (verify + commit)

---

## Out of scope for this plan

- CLI flags to force re-process a single date (can be plan `002-…`)
- Persistent memory across process restarts (SQLite/Postgres checkpointer)
- Moving processed transcripts to `input/processed/`
- Migrating off deprecated `google-generativeai` if unused after LangChain path

---

## Progress tracker

- [x] Mode chosen (A or B) — **B**
- [x] Phase 1 complete
- [x] Phase 2 complete
- [x] Phase 3 complete
- [x] Phase 4 complete
- [ ] Phase 5 verified and committed
